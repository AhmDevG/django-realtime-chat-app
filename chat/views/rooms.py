from ..models import Room , Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView , ListView  , CreateView , UpdateView , DeleteView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.urls import reverse_lazy 
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect  , get_object_or_404


def broadcast_room_event(event_type, room_data, notify_chat=False):
    channel_layer = get_channel_layer()

    event = {
        "type": event_type,
        "room": room_data,
    }

    # Update the rooms list
    async_to_sync(channel_layer.group_send)("rooms", event)

    # Notify users currently inside this room
    if notify_chat:
        async_to_sync(channel_layer.group_send)(
            f"room_{room_data['id']}",
            event
        )

class RoomDetailView(LoginRequiredMixin , DetailView):
    model = Room
    template_name = "rooms/room.html"
    pk_url_kwarg = "room_id"


class RoomView(ListView):
    model = Room
    template_name = "index.html"
    context_object_name = "object_list"


class RoomCreateView(LoginRequiredMixin , CreateView):
    model = Room
    fields = ['room_name', 'room_description']
    template_name = 'rooms/add_room.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.room_author = self.request.user
        response = super().form_valid(form)

        channel_layer = get_channel_layer()
        room_data = {
            "id": self.object.id,
            "room_name": self.object.room_name,
            "room_description": self.object.room_description,
            "room_author": self.object.room_author.username,
            "created_at": self.object.created_at.strftime("%Y-%m-%d %H:%M"),
            "room_author_id": self.object.room_author.id,
        }
        transaction.on_commit(
            lambda: broadcast_room_event(
                "room.created",
                room_data
            )
        )
        return response

class RoomUpdateView(LoginRequiredMixin , UpdateView):
    model = Room
    fields = ['room_name', 'room_description']
    template_name = 'rooms/update_room.html'
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'room_id'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.room_author:
            messages.info(request , "You don't have permission to access this room")
            return redirect('index')

        response = super().dispatch(request, *args, **kwargs)
        
        return response


    def form_valid(self, form):
        form.instance.room_author = self.request.user
        response = super().form_valid(form)

        room_data = {
            "id": self.object.id,
            "room_name": self.object.room_name,
            "room_description": self.object.room_description,
            "room_author": self.object.room_author.username,
            "created_at": self.object.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        transaction.on_commit(
            lambda: broadcast_room_event(
                "room.updated",
                room_data,
                notify_chat=True
            )
        )
        return response


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = "rooms/room_confirm_delete.html"
    success_url = reverse_lazy("index")
    pk_url_kwarg = "room_id"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.room_author:
            messages.info(request, "You don't have permission to delete this room")
            return redirect("index")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        room_id = self.object.id 
        response = super().post(request, *args, **kwargs)

        room_data = {
            "id": room_id
        }

        transaction.on_commit(
            lambda: broadcast_room_event(
                "room.deleted",
                room_data,
                notify_chat=True
            )
        )

        return response


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'rooms/chat_room.html'
    pk_url_kwarg = 'room_id'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object
        chat_msgs = Message.objects.filter(room=room).select_related('message_author', 'reply_to').order_by('created_at')
        context['chat_msgs'] = chat_msgs
        context['current_user'] = self.request.user
        return context