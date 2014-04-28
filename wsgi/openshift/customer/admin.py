from django.contrib import admin

from customer import models

class Profile(admin.ModelAdmin):
    pass

class QuestionKind(admin.ModelAdmin):
    pass

class QuestionStatus(admin.ModelAdmin):
    pass

class Question(admin.ModelAdmin):
    #fields = ['created_at', 'text']
    list_display = ('profile', 'number', 'created_at')
    list_filter = ['created_at']

class OrderKind(admin.ModelAdmin):
    pass

class OrderStatus(admin.ModelAdmin):
    pass

class Order(admin.ModelAdmin):
    #fields = ['created_at', 'text']
    list_display = ('profile', 'number', 'created_at')
    list_filter = ['created_at']

class DangerCategory(admin.ModelAdmin):
    pass

class Cargo(admin.ModelAdmin):
    #fields = ['created_at', 'text']
    list_display = ('order', 'number')

admin.site.register(models.Profile, Profile)
admin.site.register(models.QuestionKind, QuestionKind)
admin.site.register(models.QuestionStatus, QuestionStatus)
admin.site.register(models.Question, Question)
admin.site.register(models.OrderKind, OrderKind)
admin.site.register(models.OrderStatus, OrderStatus)
admin.site.register(models.Order, Order)
admin.site.register(models.DangerCategory, DangerCategory)
admin.site.register(models.Cargo, Cargo)
