from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import ChatMessage

@login_required
def community_chat(request):
    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        if msg:
            ChatMessage.objects.create(user=request.user, message=msg)
        return redirect('community:chat')

    messages_list = ChatMessage.objects.select_related('user__profile').all()[:50]
    return render(request, 'community/chat.html', {'messages': messages_list})

@login_required
def chat_messages_api(request):
    since = request.GET.get('since')
    qs = ChatMessage.objects.select_related('user__profile').all()
    if since:
        qs = qs.filter(id__gt=since)
    qs = qs[:20]
    data = [{
        'id': m.id,
        'username': m.user.username,
        'initial': m.user.username[0].upper(),
        'message': m.message,
        'time': m.created_at.strftime('%I:%M %p').lstrip('0'),
        'is_staff': m.user.is_staff,
        'win_rate': int(m.user.profile.win_rate) if hasattr(m.user, 'profile') else 0,
        'profile_image': m.user.profile.profile_image.url if hasattr(m.user, 'profile') and m.user.profile.profile_image else '',
    } for m in qs]
    return JsonResponse({'messages': data, 'latest_id': qs[0].id if qs else (int(since) if since else 0)})
