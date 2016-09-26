__author__ = 'Navid'
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from game_platform.models import Game, Category, Player_Game, Player, Developer
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


class GameListView(ListView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        return context


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        return context


def all_games(request):
    context = {"all_categories": Category.objects.all()}
    context["object_list"] = Game.objects.all()
    return render_to_response("game_platform/game_list.html", context, context_instance=RequestContext(request))


def popular_games(request):
    context = {"all_categories": Category.objects.all()}
    pg = Player_Game.objects.order_by('purchaseTime')[:30]  # 30 most recent downloaded
    tmp = []
    for i in range(pg.__len__()):
        tmp.append(pg[i].game)
    context["object_list"] = set(tmp)  # get games that are recently downloaded by district
    context["p_title"] = "Recent Downloaded"
    return render_to_response("game_platform/game_list.html", context, context_instance=RequestContext(request))


def show_category(request, category_id=None):
    context = {"all_categories": Category.objects.all()}  # for loading categories
    if 'query' in request.REQUEST:
        context["p_title"] = "Search Results"
        context["games"] = Game.objects.filter(title__icontains=request.REQUEST['query'])  # search option
    else:
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            context["category"] = category
            context["games"] = category.games.all()
        elif request.user.is_authenticated():  # if user is player then add his games to first page
            if Player.objects.filter(user=request.user).first() is not None:
                pg = Player_Game.objects.filter(player=Player.objects.get(user=request.user)).order_by('-purchaseTime')
                query = []
                for i in range(pg.__len__()):
                    query.append(pg[i].game)
                context["games"] = query
            elif Developer.objects.filter(user=request.user).first() is not None:  # if developer
                context["games"] = Developer.objects.get(user=request.user).games.all()
            else:  # if admin
                context["games"] = Game.objects.all()
            context["p_title"] = "My Games"
        elif not request.user.is_authenticated():  # guest user
            context["games"] = Game.objects.order_by('price')
            context["p_title"] = "Games by Price"
    if request.is_ajax():
        return render_to_response("game/game_list_by_category.html", context, context_instance=RequestContext(request))
    return render_to_response("game/game_category.html", context, context_instance=RequestContext(request))


__author__ = 'Ligia'
# The game currently played by the player will be passed as a variable Object Game from the previous page
@login_required(login_url='/auth/login')
def showScore(request, game_id=None):
    if Player.objects.filter(user=request.user).first() is None:  # check if user is a player
            return render_to_response("403.html", {'error_message': 'You must be a player to play a game.'},
                                      context_instance=RequestContext(request))  # permission denied
    try:
        if Player_Game.objects.filter(player=Player.objects.get(user=request.user))\
                .filter(game=game_id).first() is None:  # game has not been purchased
                return render_to_response("403.html", {'error_message': 'You must buy this game first.'},
                                          context_instance=RequestContext(request))  # permission denied
        # select from database the game corresponding to the one the player has chosen to play
        gamePlayed = Player_Game.objects.filter(game=Game.objects.get(pk=game_id))
    except Player_Game.DoesNotExist or Player.DoesNotExist:
        return render_to_response("404.html",
                                  {'error_message': 'Something went wrong with database, objects cannot be found.'},
                                  context_instance=RequestContext(request))
    context = {}
    if bool(gamePlayed):
        context['player_game'] = gamePlayed[:5]  # pass 5 highscores to play page

    context['game'] = Game.objects.get(pk=game_id)
    context['game_id'] = game_id

    return render_to_response("game/play_game.html", context, context_instance=RequestContext(request))

__author__ = 'Ligia'
@login_required(login_url='/auth/login')
def submitScore(request):
    if Player.objects.filter(user=request.user).first() is None:  # check if user is a player
            return render_to_response("403.html", {'error_message': 'You must be a player to play a game.'},
                                      context_instance=RequestContext(request))  # permission denied
    score = 0
    if request.is_ajax():
        score = request.GET.get('game_score')
        game_id = request.GET.get('game_id')
    if game_id:
        if Player_Game.objects.filter(player=Player.objects.get(user=request.user))\
                .filter(game=game_id).first() is None:  # game has not been purchased
                return render_to_response("403.html", {'error_message': 'You must buy this game first.'},
                                          context_instance=RequestContext(request))  # permission denied
        game_played = Game.objects.get(pk=game_id)
    player_logged = Player.objects.get(user=request.user)
    game_item = Player_Game.objects.filter(player=player_logged).get(game=game_played)
    score = float(score)
    if game_item.score < score:
        game_item.score = score
        game_item.save()  # updates the score in the database

    showScore(request, game_id)
    return HttpResponse(json.dumps(score), content_type='application/json')

__author__ = 'Ligia'
@login_required(login_url='/auth/login')
def saveGame(request):
    if Player.objects.filter(user=request.user).first() is None:  # check if user is a player
            return render_to_response("403.html", {'error_message': 'You must be a player to play a game.'},
                                      context_instance=RequestContext(request))  # permission denied
    if request.is_ajax():
        score = request.GET.get('game_score')
        game_id = request.GET.get('game_id')
        player_items = json.loads(request.GET.get('player_items'))  # <- It now comes as a list of string variables
        if game_id:
            if Player_Game.objects.filter(player=Player.objects.get(user=request.user))\
                    .filter(game=game_id).first() is None:  # game has not been purchased
                    return render_to_response("403.html", {'error_message': 'You must buy this game first.'},
                                              context_instance=RequestContext(request))  # permission denied

            # So player_items now is a list of string variables, each variable is an item
            print(player_items)
            print(player_items[0])
            print(player_items[1])
            print(score)

            # Parse items into string:
            player_items_to_save = ''.join(e+";" for e in player_items)
            print("Player Items to save: {}".format(player_items_to_save))

            game_played = Game.objects.get(pk=game_id)  # what game is being played
            player_logged = Player.objects.get(user=request.user)  # what is user is logged in

            game_item = Player_Game.objects.filter(player=player_logged).get(game=game_played)

            score = float(score)
            if game_item.score < score:
                game_item.score = score
            game_item.playerItems = player_items_to_save
            game_item.save()  # updates the score and items in the database

            showScore(request, game_id)
            return HttpResponse(json.dumps(""), content_type='application/json')
    return HttpResponse(json.dumps(""), content_type='application/json')

__author__ = 'Ligia'
@login_required(login_url='/auth/login')
def loadGame(request):
    if Player.objects.filter(user=request.user).first() is None:  # check if user is a player
            return render_to_response("403.html", {'error_message': 'You must be a player to play a game.'},
                                      context_instance=RequestContext(request))  # permission denied
    if request.is_ajax():
        game_id = request.GET.get('game_id')
        if game_id:
            if Player_Game.objects.filter(player=Player.objects.get(user=request.user))\
                    .filter(game=game_id).first() is None:  # game has not been purchased
                return render_to_response("403.html", {'error_message': 'You must buy this game first.'},
                                          context_instance=RequestContext(request))  # permission denied
        game_played = Game.objects.get(pk=game_id)  # what game is being played
        player_logged = Player.objects.get(user=request.user)  # what is user is logged in

        game_item = Player_Game.objects.filter(player=player_logged)
        response_data = {}   # <- That's what we will send to JavaScript back
        response_data['game_id'] = game_id
        if bool(game_item):
            game_item = Player_Game.objects.filter(player=player_logged).get(game=game_played)
            if bool(game_item):
                response_data['score'] = game_item.score
                player_items_string = game_item.playerItems
                # The last item on this list is empty, so we exclude it
                response_data["playerItems"] = player_items_string.split(";")[:-1]
            else:
                # In this case no played games were found
                response_data = "None"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse(json.dumps(""), content_type='application/json')