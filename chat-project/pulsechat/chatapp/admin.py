from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Chat)
admin.site.register(PulseChatUsers)
admin.site.register(Messages)
admin.site.register(Group)
admin.site.register(GroupMessages)