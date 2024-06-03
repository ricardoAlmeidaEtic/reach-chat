from django.contrib import admin

from chatting.models import Message, MessagesLiked

# Register your models here.

@admin.register(Message)
class ProductAdmin(admin.ModelAdmin):
    list_display=("id","message","date","user","image","likes","enabled")
    list_editable=("image","enabled","likes",)

@admin.register(MessagesLiked)
class ProductAdmin(admin.ModelAdmin):
    list_display=("id","message","user")
    list_editable=()