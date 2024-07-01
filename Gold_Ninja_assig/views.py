from . import views
import random
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

WINNING_GOLD = 350
MAX_MOVES = 15

def index(request):
    if 'gold' not in request.session:
        request.session['gold'] = 0
    if 'activities' not in request.session:
        request.session['activities'] = []
    if 'moves' not in request.session:
        request.session['moves'] = 0
    if 'game_over' not in request.session:
        request.session['game_over'] = False

    return render(request, 'index.html', {
        'gold': request.session['gold'],
        'activities': request.session['activities'],
        'moves': request.session['moves'],
        'game_over': request.session['game_over'],
        'winning_gold': WINNING_GOLD,
        'max_moves': MAX_MOVES
    })

def process_money(request):
    building = request.POST['building']
    gold_earned = 0
    
    buildings_gold = {
        'farm': random.randint(10, 20),
        'cave': random.randint(10, 20),
        'house': random.randint(10, 20),
        'casino': random.randint(-50, 50)
    }

    gold_earned = buildings_gold.get(building, 0)
    print(gold_earned)
    request.session['gold'] += gold_earned
    request.session['moves'] += 1

    # Create activity entry
    if gold_earned >= 0:
        activity = f"Earned {gold_earned} gold from the {building}! ({datetime.now().strftime('%B %dth %Y (%I:%M %p')})"
        color = "green"
    else:
        activity = f"Lost {abs(gold_earned)} gold at the {building}... Ouch! ({datetime.now().strftime('%B %dth %Y (%I:%M %p')})"
        color = "red"
    request.session['activities'].insert(0, {'activity': activity, 'color': color})
    # Check for win/lose conditions
    if request.session['gold'] >= WINNING_GOLD or request.session['moves'] >= MAX_MOVES:
        request.session['game_over'] = True
    return redirect('/')

def reset(request):
    request.session.clear()
    return redirect('/')
