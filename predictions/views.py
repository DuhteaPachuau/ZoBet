from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Prediction
from events.models import Event

@login_required
def my_predictions_view(request):
    predictions = Prediction.objects.filter(user=request.user).select_related('event', 'team')
    return render(request, 'predictions/my_predictions.html', {'predictions': predictions})

def event_predictions_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    predictions = Prediction.objects.filter(event=event).select_related('user', 'team')

    team_breakdown = {}
    for pred in predictions:
        team_name = pred.team.name
        if team_name not in team_breakdown:
            team_breakdown[team_name] = 0
        team_breakdown[team_name] += 1

    return render(request, 'predictions/event_predictions.html', {
        'event': event,
        'predictions': predictions,
        'team_breakdown': team_breakdown,
    })
