from django.contrib import admin

# Register your models here.
from swapfood.models import Mychats
# Register your models here.

@admin.register(Mychats)
class MychatAdmin(admin.ModelAdmin):
    list_display = ('id','me','frnd','chats')
