from django.contrib import admin
from .models import Registration, Question, Response, Relationship_Started_Year, Option, Question_Category
# Register your models here.


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name','description','negative_mark_to','question_category')
    inlines=[OptionInline]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('partner1','male_negative_mark','female_negative_mark','attended_question_count','no_of_questions')

    

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('partner1','partner2','qdescription','game')

   



admin.site.register(Relationship_Started_Year)
admin.site.register(Option)
admin.site.register(Question_Category)
