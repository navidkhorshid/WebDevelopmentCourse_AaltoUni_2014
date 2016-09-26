import email
import hashlib
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from game_platform.auth.forms import RegistrationForm, LoginForm
from datetime import datetime, timedelta
from django.utils import timezone
import random
from game_platform.models import Developer, Player, UserProfile


def registration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')  # if user is authenticated it should go to homepage for e.g.
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Validation
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5]
            activation_key = hashlib.sha1((salt+form.cleaned_data['email']).encode('utf8')).hexdigest()
            key_expires = datetime.today() + timedelta(1)  # in 1 day from now
            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s,\n" \
                         "Thanks for signing up. To activate your account in Game Platform, click this link within 24 hours:\n" \
                         "http://peaceful-cliffs-8403.herokuapp.com/auth/confirm/%s" % (form.cleaned_data['username'], activation_key)
            send_mail(email_subject, email_body, 'game.platform.wsd@gmail.com',
                      [form.cleaned_data['email']], fail_silently=False)
            # after sending email we need to save user and its role
            # Create user and dev/player
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
            new_profile.save()
            if request.POST.get('btn_developer'):
                developer = Developer(user=user)
                developer.save()
            elif request.POST.get('btn_player'):
                player = Player(user=user)
                player.save()

            return HttpResponseRedirect('/auth/login')  # after successful registration go to validation page for e.g.
        else:
            return render_to_response('auth/signup.html', {'form': form}, context_instance=RequestContext(request))
    else:
        # show the registration form
        form = RegistrationForm()
        context = {'form': form}
        return render_to_response('auth/signup.html', context, context_instance=RequestContext(request))


# have to check for validation
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # Disable browser 'Back' button
def loginRequest(request):
        if request.user.is_authenticated():
            if Developer.objects.filter(user=request.user).first() is not None:
                return HttpResponseRedirect('/dev')  # load developers page
            elif Player.objects.filter(user=request.user).first() is not None:
                return HttpResponseRedirect('/game')  # load players page
            else:
                return HttpResponseRedirect('/admin')

        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        person = authenticate(username=username, password=password)
                        if person is not None:
                            if User.objects.get(id=person.id).is_active == False:
                                return render_to_response("404.html",
                                                          {'error_message'
                                                           : 'Validate your e-mail in order to login to your account.'},
                                                          context_instance=RequestContext(request))  # not activated
                            if Developer.objects.filter(user=person).first() is not None:
                                login(request, person)
                                return HttpResponseRedirect('/dev')  # load developers page
                            elif Player.objects.filter(user=person).first() is not None:
                                login(request, person)
                                return HttpResponseRedirect('/game')  # load players page
                            else:
                                return HttpResponseRedirect('/admin')  # load admin to login there
                        else:
                            return render_to_response('auth/signin.html', {'form': form},
                                                      context_instance=RequestContext(request))
                else:
                        return render_to_response('auth/signin.html', {'form': form},
                                                  context_instance=RequestContext(request))
        else:
                # show the login form
                form = LoginForm()
                context = {'form': form}
                return render_to_response('auth/signin.html', context, context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    # check if there is UserProfile which matches the activation key (if not then display 404)
    try:
        user_profile = UserProfile.objects.get(activation_key=activation_key)
    except UserProfile.DoesNotExist:
        return render_to_response("404.html", {'error_message': 'The activation code does not exist'},
                                  context_instance=RequestContext(request))
    # check if the activation key has expired, if it has then render 404
    if user_profile.key_expires < timezone.now():
        return render_to_response("404.html",
                                  {'error_message': 'Activation key has expired, try to make another account'},
                                  context_instance=RequestContext(request))
    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return HttpResponseRedirect('/auth/login')