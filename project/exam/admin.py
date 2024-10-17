# exam/admin.py
from django.contrib import admin
from .models import  Question, Choice

admin.site.register(Question)
admin.site.register(Choice)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1  # Количество пустых форм для добавления новых опций

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

