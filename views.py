from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse, reverse, Http404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from player.models import *
from question.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialAccount
from django.utils import timezone
from ratelimit.decorators import ratelimit
from django.core import serializers
from question.views import *
import json

# Create your views here.
@ratelimit(key='ip', rate='10/m')
@login_required
def finalPlayerList(request):
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

@ratelimit(key='ip', rate='10/m')
@login_required
def getQuestion(request):
    player = get_object_or_404(Player, user=request.user)
    ques = get_object_or_404(Question, level=player.level)
    context = {
        'question': ques,
        'player': player,
        'rank': Player.rank(player),
        'social_account': SocialAccount.objects.get(user=player.user),
        'level_range': range(0, player.level+1),
        'showAnswerWindow': True
    }
    return render(request, "question/index.html", context)

@ratelimit(key='ip', rate='10/m')
@login_required
def getQuestionByLevel(request, level):
    player = get_object_or_404(Player, user=request.user)
    level = int(level)
    if level > player.level:
        raise Http404()
    ques = get_object_or_404(Question, level=level)
    context = {
        'question': ques,
        'player': player,
        'rank': Player.rank(player),
        'social_account': SocialAccount.objects.get(user=player.user),
        'level_range': range(0, player.level + 1),
        'showAnswerWindow': True if level == player.level else False
    }
    return render(request, "question/index.html", context)

@ratelimit(key='ip', rate='10/m')
@login_required
def submitAnswer(request):
    player = get_object_or_404(Player, user=request.user)
    ques = get_object_or_404(Question, level=player.level)
    answers = Answer.objects.filter(question=ques)
    status = False
    submission = Submission(player=player, question=ques, timestamp=timezone.now(), ans=request.POST.get('answer').lower())
    submission.save()
    for answer in answers:
        if answer.ans == request.POST.get('answer').lower():
            player.level += 1
            player.levelTime = timezone.now()
            player.save()
            status = True
            break

    return HttpResponse(str(status))
