__author__ = 'Navid'
from django.template import RequestContext
from game_platform.developer.forms import AddGameForm, EditGameForm
from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from game_platform.models import Category, Game, Developer, Player_Game
from django.contrib.auth.decorators import login_required
import random
import django
import datetime
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
#from matplotlib.dates import DateFormatter


@login_required(login_url='/auth/login')  # check if developer
def add_game(request):
    if Developer.objects.filter(user=request.user).first() is None:
        return render_to_response("403.html",
                                  {'error_message': 'You must be a developer to access this page.'},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = AddGameForm(request.POST)
        if form.is_valid():
            game = Game(title=form.cleaned_data['title'],picture_url=form.cleaned_data['picture_url'],
                        game_url=form.cleaned_data['game_url'],
                        price=form.cleaned_data['price'],
                        description=form.cleaned_data['description'],
                        category=form.cleaned_data['category'],
                        developer=Developer.objects.get(user=request.user))
            game.save()
            return HttpResponseRedirect('/dev')  # after successful adding game will go to validation page for e.g.
        else:
            return render_to_response('developer/add_game.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        # show the registration form
        form = AddGameForm()
        context = {'form': form}
        return render_to_response('developer/add_game.html', context, context_instance=RequestContext(request))


@login_required(login_url='/auth/login')
def edit_game(request, game_id=None):
    if Developer.objects.filter(user=request.user).first() is None:  # check if user is developer
        return render_to_response("403.html", {'error_message': 'You must be a developer to access this page.'},
                                  context_instance=RequestContext(request))
    try:
        if Game.objects.get(id=game_id).developer.user == request.user:  # check if developer owns this game
            game = Game.objects.get(id=game_id)
        else:
            # developer does not own the game
            return render_to_response("403.html", {'error_message': 'You do not own this game.'},
                                      context_instance=RequestContext(request))
    except Game.DoesNotExist:
        # this game_id does not exist in database
        return render_to_response("404.html",
                                  {'error_message': 'Something went wrong with database, objects cannot be found.'},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':  # if the player submit the edit page
        form = EditGameForm(request.POST)
        if form.is_valid():
            game.picture_url = form.cleaned_data['picture_url']
            game.game_url = form.cleaned_data['game_url']
            game.price = form.cleaned_data['price']
            game.description = form.cleaned_data['description']
            game.category = form.cleaned_data['category']
            game.save()
            return HttpResponseRedirect('/dev')
        else:
            return render_to_response('developer/edit_game.html', {'form': form, 'game_name': game.title,
                                                                   'game_id': game_id},
                                      context_instance=RequestContext(request))
    else:
        # show the registration form
        form = EditGameForm(instance=game)
        return render_to_response('developer/edit_game.html',
                                  {'form': form, 'game_name': game.title, 'game_id': game_id},
                                  context_instance=RequestContext(request))


@login_required(login_url='/auth/login')
def dev_page(request):
    if Developer.objects.filter(user=request.user).first() is None:
        if Developer.objects.filter(user=request.user).first() is None:
            return render_to_response("403.html", {'error_message': 'You must be a developer to access this page.'},
                                      context_instance=RequestContext(request))
    context = {"games": Game.objects.filter(developer=Developer.objects.get(user=request.user))}
    return render_to_response("developer/dev_page.html", context, context_instance=RequestContext(request))


@login_required(login_url='/auth/login')
def sales_list(request):
    if Developer.objects.filter(user=request.user).first() is None:
        if Developer.objects.filter(user=request.user).first() is None:
            return render_to_response("403.html", {'error_message': 'You must be a developer to access this page.'},
                                      context_instance=RequestContext(request))
    context = {"player_games": Player_Game.objects.filter(
        game__developer=Developer.objects.get(user=request.user)).order_by('-purchaseTime')[:100]}
    return render_to_response("developer/sales_list.html", context, context_instance=RequestContext(request))


@login_required(login_url='/auth/login')
def sales_game(request, game_id=None):
    if Developer.objects.filter(user=request.user).first() is None:
        return render_to_response("403.html", {'error_message': 'You must be a developer to access this page.'},
                                  context_instance=RequestContext(request))
    if game_id:  # stats for an specific game
        try:
            if Game.objects.get(id=game_id).developer.user == request.user:  # right user
                context = {"player_games": Player_Game.objects.filter
                (game__developer=Developer.objects.get(user=request.user)).
                    filter(game__id=game_id).order_by('-purchaseTime')[:100]}
                return render_to_response("developer/sales_list.html", context,
                                          context_instance=RequestContext(request))
            else:
                return render_to_response("403.html",
                                          {'error_message': 'You do not own this game.'},
                                          context_instance=RequestContext(request))
        except Game.DoesNotExist or Player_Game.DoesNotExist or Developer.DoesNotExist:
            return render_to_response("404.html",
                                      {'error_message': 'Something went wrong with database, objects cannot be found.'},
                                      context_instance=RequestContext(request))


#@login_required(login_url='/auth/login')
#def sales_chart(request, game_id=None):
#    if Developer.objects.filter(user=request.user).first() is None:
#        return render_to_response("403.html", {}, context_instance=RequestContext(request))
#    if game_id:  # chart for an specific game
#        try:
#            if Game.objects.get(id=game_id).developer.user == request.user:  # right user
#                fig = Figure()
#                ax = fig.add_subplot(111)
#                now_30 = datetime.datetime.now()-datetime.timedelta(days=30)
#                delta = datetime.timedelta(days=1)
#                x = []
#                y = []
#                for i in range(30):
#                    x.append(now_30)
#                    now_30 += delta
#                tmp_y = Game.objects.get(id=game_id).total_sell_in_month
#                y = tmp_y.split(",")
#                ax.plot_date(x, y, "-")
#                ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
#                fig.autofmt_xdate()
#                canvas = FigureCanvas(fig)
#                response = django.http.HttpResponse(content_type='image/png')
#                canvas.print_png(response)
#                return response
#            else:
#                return render_to_response("403.html", {}, context_instance=RequestContext(request))
#        except Game.DoesNotExist:
#            return render_to_response("404.html", {}, context_instance=RequestContext(request))