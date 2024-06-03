import datetime
import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView
from chatting.models import Message, MessagesLiked
from chatting.consumers import ChatConsumer
from projeto_chat.forms import MessageForm
from asgiref.sync import async_to_sync
from projeto_chat.settings import BASE_DIR, STATIC_URL


class ListAllMessages(ListView):
    model = Message
    queryset = Message.objects.filter(enabled=True).all()
    template_name = 'message_list.html'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            action = data.get('action')
            message_id = data.get('message_id')

            if message_id is None:
                return HttpResponseBadRequest('Missing message_id')

            message = Message.objects.get(id=message_id)
            user = request.user

            if action == 'like':
                if not MessagesLiked.objects.filter(message=message, user=user).exists():
                    MessagesLiked.objects.create(message=message, user=user)
                    message.likes += 1
                    message.save()
                    return JsonResponse({'success': True, 'likes': message.likes})
                else:
                    return JsonResponse({'success': False, 'error': 'Already liked'})
                
            elif action == 'unlike':
                try:
                    liked_entry = MessagesLiked.objects.get(message=message, user=user)
                    liked_entry.delete()
                    message.likes -= 1
                    message.save()
                    return JsonResponse({'success': True, 'likes': message.likes})
                except MessagesLiked.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Not liked yet'})
                
            else:
                return HttpResponseBadRequest('Invalid action')

        except Message.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found'})
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MessageForm()
        return context
        