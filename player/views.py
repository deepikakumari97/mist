from django.shortcuts import render, HttpResponseRedirect, HttpResponse, reverse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from player.models import *
from question.models import *
from django.utils import timezone
from allauth.socialaccount.models import SocialAccount
import json
from ratelimit.decorators import ratelimit
from django.core import serializers
from question.views import *

# Create your views here.
@ratelimit(key='ip', rate='10/m')
@csrf_exempt
def createPlayer(request):
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        player = Player(level=0, levelTime=timezone.now(), startTime=timezone.now(), user=request.user)
        player.save()
    return HttpResponseRedirect(reverse('question'))

def makePlayer(request):
    player = Player.objects.get(user=request.user)
    player.delete()
    player = Player(level=0, levelTime=timezone.now(), startTime=timezone.now(), user=request.user)
    player.save()
    return HttpResponseRedirect(reverse('question'))

@ratelimit(key='ip', rate='10/m')
@login_required
def playerList(request):
    player = get_object_or_404(Player, user=request.user)
    player_list = Player.objects.order_by('-level', 'levelTime', 'pk').filter(user__is_staff=False)
    paginator = Paginator(player_list, 50) # Show 25 player per page

    page = request.GET.get('page')
    try:
        player_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        player_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        player_list = paginator.page(paginator.num_pages)

    leaderboard = []
    for p in player_list:
        leaderboard.append({
            'player': p,
            'social_account': SocialAccount.objects.get(user=p.user),
            'rank': p.rank()
        })

    if player_list.paginator.num_pages <= 5:
        r = player_list.paginator.page_range
    else:
        if player_list.number <= 2:
            r = range(1,6)
        elif player_list.number <= player_list.paginator.num_pages - 2:
            r = range(player_list.number-2, player_list.number+3)
        else:
            r = range(player_list.paginator.num_pages-4, player_list.paginator.num_pages+1)

    context = {
        'player': player,
        'social_account': SocialAccount.objects.get(user=player.user),
        'leaderboard': leaderboard,
        'rank': player.rank(),
        'player_list': player_list,
        'range': r,
        'level_range': range(0, player.level+1),
    }

    return render(request, 'player/list.html', context)

@login_required
@ratelimit(key='ip', rate='10/m')
@csrf_exempt
def createSubmission(request):
    player = Player.objects.get(user=request.user)
    ques = Question.objects.get(level=player.level)
    submission = Submission(player=player, question=ques, ans=str(request.POST.get('answer')))
    submission.save()
    return HttpResponse("True")

def getPlayer(request):
    player = get_object_or_404(Player, user__pk = 2)
    fb = SocialAccount.objects.get(user=player.user)
    context = {
        "level": player.level,
        "name": player.user.first_name + " " + player.user.last_name,
        "fbid": fb.uid,
        "rank": player.rank()
    }
    jsonResponse = json.dumps(context)
    return HttpResponse(jsonResponse, content_type="application/json")
