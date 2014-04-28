from django.contrib import admin

from info import models

class Page(admin.ModelAdmin):
    list_display = ('name', 'title')
    search_fields = ['text']

class News(admin.ModelAdmin):
    #fields = ['created_at', 'text']
    list_display = ('frag_of_text', 'created_at')
    list_filter = ['created_at']
    search_fields = ['text']

class SpecOffer(admin.ModelAdmin):
    #fields = ['created_at', 'text']
    list_display = ('frag_of_text', 'created_at')
    list_filter = ['created_at']
    search_fields = ['text']

admin.site.register(models.Page, Page)
admin.site.register(models.News, News)
admin.site.register(models.SpecOffer, SpecOffer)
