from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from user.models import UserProfile
from chat.utils import get_user_profile
from .models import Chat



# Create your views here.
@login_required
def home(request):
    ONLINE_THRESHOLD = timedelta(minutes=2)
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()
    is_online = profile and profile.last_seen >= now() - ONLINE_THRESHOLD

    messages = Chat.objects.filter(Q(sender=user) | Q(receiver=user))

    conversations = {}

    for msg in messages:
        other = msg.receiver if msg.sender == user else msg.sender

        if other not in conversations or msg.timestamp > conversations[other]["last"].timestamp:
            conversations[other] = {
                "last": msg,
                "unread": Chat.objects.filter(
                    sender=other,
                    receiver=user,
                    is_read=False
                ).count()
            }

    conversation_list = sorted(
        conversations.items(),
        key=lambda x: x[1]["last"].timestamp,
        reverse=True
    )

    return render(request, "chat/home.html", {
        "conversations": conversation_list,
        "is_online": is_online
    })

@login_required
def chat(request, username):
    other_user = get_object_or_404(User, username=username)
    Chat.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)
    return render(request, 'chat/ajax_chat.html', {'other_user':other_user})

@login_required
def ajax_chat(request, username):
    other_user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            message_instance = Chat.objects.create(
                sender=request.user,
                receiver=other_user,
                message=message
            )

            return JsonResponse({
                'id':message_instance.id,
                'sender':message_instance.sender.username,
                'receiver':message_instance.receiver.username,
                'message':message_instance.message,
                'timestamp':message_instance.timestamp.strftime('%H:%M'),
                'is_read':message_instance.is_read
                
            })
        

    messages = Chat.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    messages_data = []
    for msg in messages:
        messages_data.append({
            'id':msg.id,
                'sender':msg.sender.username,
                'receiver':msg.receiver.username,
                'message':msg.message,
                'timestamp':msg.timestamp.strftime('%H:%M'),
                'is_read':msg.is_read
        })

    return JsonResponse({'messages':messages_data})

@login_required
def inbox_ajax(request):
    user = request.user
    conversations = []

    other_users = User.objects.exclude(id=user.id)

    for other_user in other_users:
        last_msg = Chat.objects.filter(
            (Q(sender=user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=user))
        ).order_by('-timestamp').first()

        if last_msg:
            unread_count = Chat.objects.filter(
                sender=other_user,
                receiver=user,
                is_read=False
            ).count()

            profile = get_user_profile(request.user)
            online = timezone.now() - profile.last_seen < timezone.timedelta(seconds=30)

            conversations.append({
                "username": other_user.username,
                "last_message": last_msg.message,
                "last_sender":last_msg.sender.username if last_msg else "",
                "unread": unread_count,
                "online": profile.is_online(),
                "timestamp":last_msg.timestamp
            })

    # Sort by last message timestamp
    conversations.sort(key=lambda x: x['timestamp'], reverse=True)

    return JsonResponse({"conversations": conversations})

@login_required
def update_last_seen(request):
    print("HEARTBEAT:", request.user.username, request.method)
    if request.method =='POST':
        profile = get_user_profile(request.user)
        profile.last_seen = timezone.now()
        profile.save(update_fields=["last_seen"])
        return JsonResponse({
            'ok':True
        })
    return JsonResponse({
        "error":"Invalid Method"
    },status=400)

def mark_read(request, username):
    other_user = get_object_or_404(User, username=username)

    Chat.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({
        'status':'ok'
    })
