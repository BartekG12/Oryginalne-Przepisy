from django.contrib import admin

from .models import Przepis, Ocena, Tag

admin.site.register(Przepis)
admin.site.register(Ocena)
admin.site.register(Tag)
