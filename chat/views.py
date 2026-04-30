from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Message
from users.models import CustomUser


@login_required
def counselors_list(request):
    """List all available counselors for students to start a chat."""
    counselors = CustomUser.objects.filter(role='counselor')
    return render(request, 'chat/counselors.html', {'counselors': counselors})


@login_required
def inbox(request):
    """Show all chat conversations for the current user."""
    user = request.user
    # Get all users who have had conversations with current user
    sent_to = Message.objects.filter(sender=user).values_list('receiver', flat=True).distinct()
    received_from = Message.objects.filter(receiver=user).values_list('sender', flat=True).distinct()
    contact_ids = set(list(sent_to) + list(received_from))
    contacts = CustomUser.objects.filter(id__in=contact_ids)

    # Unread count per contact
    contacts_data = []
    for contact in contacts:
        unread = Message.objects.filter(sender=contact, receiver=user, is_read=False).count()
        last_msg = Message.objects.filter(
            Q(sender=user, receiver=contact) | Q(sender=contact, receiver=user)
        ).last()
        contacts_data.append({'contact': contact, 'unread': unread, 'last_msg': last_msg})

    return render(request, 'chat/inbox.html', {'contacts_data': contacts_data})


@login_required
def conversation(request, user_pk):
    """Show conversation thread between current user and another user."""
    other_user = get_object_or_404(CustomUser, pk=user_pk)
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    # Get list of contacts for sidebar
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    contact_ids = set(list(sent_to) + list(received_from))
    contacts = CustomUser.objects.filter(id__in=contact_ids)

    return render(request, 'chat/conversation.html', {
        'other_user': other_user,
        'messages_list': messages_list,
        'contacts': contacts,
    })


@login_required
def send_message(request):
    """AJAX endpoint to send a message."""
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content', '').strip()
        if not content:
            return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
        receiver = get_object_or_404(CustomUser, pk=receiver_id)
        msg = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
        )
        return JsonResponse({
            'status': 'ok',
            'message': {
                'id': msg.id,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%H:%M'),
                'sender': msg.sender.username,
            }
        })
    return JsonResponse({'status': 'error'}, status=405)


@login_required
def get_new_messages(request, user_pk):
    """Poll endpoint to get new messages since a given message id."""
    last_id = request.GET.get('last_id', 0)
    other_user = get_object_or_404(CustomUser, pk=user_pk)
    new_msgs = Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        id__gt=last_id,
    )
    new_msgs.update(is_read=True)
    data = [{
        'id': m.id,
        'content': m.content,
        'timestamp': m.timestamp.strftime('%H:%M'),
        'sender': m.sender.username,
    } for m in new_msgs]
    return JsonResponse({'messages': data})
