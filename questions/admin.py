from django.contrib import admin

# Register your models here.

from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'topic', 'difficulty', 'created_at')
    search_fields = ('question_text', 'topic', 'subtopic')
    list_filter = ('subject', 'difficulty')
