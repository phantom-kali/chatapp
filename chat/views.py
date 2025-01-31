from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message


@login_required
def chatroom(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    messages = Message.objects.filter(sender=request.user, receiver=receiver)| Message.objects.filter(sender=receiver, receiver=request.user)
    
    
    if request.method == 'POST':
        message = request.POST.get('message')
        Message.objects.create(sender=request.user, receiver=receiver, message=message)
        return redirect('chatroom', receiver_id=receiver_id)
    
    return render(request, 'chat/chatroom.html', {'receiver': receiver, 'messages': messages})
    

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/user_list.html', {'users': users})


@login_required
def get_messages(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('created_at')  # Add created_at field to Message model if not exists
    
    message_list = [{
        'sender': msg.sender.username,
        'message': msg.message,
        'is_user': msg.sender == request.user
    } for msg in messages]
    
    return JsonResponse({'messages': message_list})