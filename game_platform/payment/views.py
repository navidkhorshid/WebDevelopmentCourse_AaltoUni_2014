from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from game_platform.auth.forms import RegistrationForm, LoginForm
from hashlib import md5
from game_platform.models import Player, Game, Player_Game


def calculate_checksum_http_post(pid, sid, amount, secret_key):
    checksum_str = "pid=%s&sid=%s&amount=%s&token=%s" % (pid, sid, amount, secret_key)
    return md5(checksum_str.encode("ascii")).hexdigest()


def calculate_checksum_http_get(pid, ref, secret_key):
    checksum_str = "pid=%s&ref=%s&token=%s" % (pid, ref, secret_key)
    return md5(checksum_str.encode("ascii")).hexdigest()


@login_required(login_url='/auth/login')
def payment(request):
    if request.method == 'POST' and 'game_id' in request.REQUEST:
        if Player.objects.filter(user=request.user).first() is None:  # check if user is a player
            return render_to_response("403.html",
                                      {'error_message': 'You must be a player to buy a game.'},
                                      context_instance=RequestContext(request))  # permission denied
        try:
            game = Game.objects.get(id=request.REQUEST['game_id'])
            player = Player.objects.get(user=request.user)
        except Game.DoesNotExist or Player.DoesNotExist:
            # this game_id or user does not exist in database
            return render_to_response("404.html",
                                      {'error_message': 'Something went wrong with database, objects cannot be found.'},
                                      context_instance=RequestContext(request))
        if Player_Game.objects.filter(player=player).filter(game=game).first() is not None:  # game has been purchased
            return HttpResponseRedirect('/game/play/'+str(game.id))  # go to game's page
        pid = str(player.id)+'s'+str(game.id)  # pid is a combination of game_id and player_id
        sid = 'shamsin1'
        amount = game.price
        secret_key = '216d88a958e12c379cb0e30e22829da9'
        checksum = calculate_checksum_http_post(pid, sid, amount, secret_key)
        context = {"game": game}
        context["pid"] = pid
        context["sid"] = sid
        context["amount"] = amount
        context["checksum"] = checksum
        return render_to_response("payment/payment_details.html", context, context_instance=RequestContext(request))
    else:
        # it is not a post request with game_id and sth is wrong
        return render_to_response("404.html",
                                  {'error_message': 'The request cannot be handled.'},
                                  context_instance=RequestContext(request))


@login_required(login_url='/auth/login')
def success_pay(request):
    if request.method == 'GET' and 'pid' in request.REQUEST and 'ref' in request.REQUEST and \
                    'checksum' in request.REQUEST:
        pid = request.REQUEST['pid']
        ref = request.REQUEST['ref']
        checksum = request.REQUEST['checksum']
        secret_key = '216d88a958e12c379cb0e30e22829da9'
        try:
            player_id = pid.split('s')[0]  # first part of pid is player
            game_id = pid.split('s')[1]  # second part of pid is game
            game = Game.objects.get(id=game_id)
            player = Player.objects.get(id=player_id)
        except Game.DoesNotExist or Player.DoesNotExist:
            return render_to_response("404.html",
                                      {'error_message': 'Something went wrong with database, objects cannot be found.'},
                                      context_instance=RequestContext(request))  # exception
        if checksum == calculate_checksum_http_get(pid, ref, secret_key):
            # game has been purchased
            if Player_Game.objects.filter(player=player).filter(game=game).first() is not None:
                return HttpResponseRedirect('/game/play/'+str(game.id))  # go to game's page
            player_game = Player_Game(player=player, game=game, purchasePrice=game.price)
            player_game.save()
            context = {"game": game, "username": player.user.username}
            return render_to_response("payment/successful_payment.html", context,
                                      context_instance=RequestContext(request))
        else:
            return render_to_response("404.html",
                                      {'error_message': 'Payment checksum is not right.'},
                                      context_instance=RequestContext(request))  # checksum not match
    else:
        # it is not a post request with needed parameters and sth is wrong
        return render_to_response("404.html", {'error_message': 'The request cannot be handled.'},
                                  context_instance=RequestContext(request))


@login_required(login_url='/auth/login')
def failed_pay(request):
    if request.method == 'GET' and 'pid' in request.REQUEST and 'ref' in request.REQUEST and \
                    'checksum' in request.REQUEST:
        pid = request.REQUEST['pid']
        ref = request.REQUEST['ref']
        checksum = request.REQUEST['checksum']
        secret_key = '216d88a958e12c379cb0e30e22829da9'
        try:
            player_id = pid.split('s')[0]  # first part of pid is player
            game_id = pid.split('s')[1]  # second part of pid is game
            game = Game.objects.get(id=game_id)
            player = Player.objects.get(id=player_id)
        except Game.DoesNotExist or Player.DoesNotExist:
            return render_to_response("404.html",
                                      {'error_message': 'Something went wrong with database, objects cannot be found.'},
                                      context_instance=RequestContext(request))  # exception
        if checksum == calculate_checksum_http_get(pid, ref, secret_key):
            # game has been purchased
            if Player_Game.objects.filter(player=player).filter(game=game).first() is not None:
                return HttpResponseRedirect('/game/play/'+str(game.id))  # go to game's page
            context = {"game": game, "username": player.user.username}
            return render_to_response("payment/failed_payment.html", context, context_instance=RequestContext(request))
        else:
            return render_to_response("404.html", {'error_message': 'Payment checksum is not right.'},
                                      context_instance=RequestContext(request))  # checksum not match
    else:
        # it is not a post request with needed parameters and sth is wrong
        return render_to_response("404.html", {'error_message': 'The request cannot be handled.'},
                                  context_instance=RequestContext(request))