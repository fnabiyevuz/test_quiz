from django.contrib import admin
from .models import Subject, Direction, Student, Question, Answer, StudentAnswer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1 

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    inlines = [QuestionInline]  # Add this line to include the inline formset for questions


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject1', 'subject2', 'subject3', 'maximum_score']
    search_fields = ['name']
    readonly_fields = ['maximum_score']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'direction', 'birth_date', 'result']
    search_fields = ['first_name', 'last_name']
    list_filter = ['direction']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1 


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'subject']
    search_fields = ['text']
    list_filter = ['subject']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'question', 'is_correct']
    list_filter = ['question', 'is_correct']
    search_fields = ['text']


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'question', 'answer']
    list_filter = ['student', 'question']
