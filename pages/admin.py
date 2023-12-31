from django.contrib import admin
from .models import Tags, Answers, Questions, Save, AnswerComments, QuestionComments, Vote, AnswerVote


class QuestionsModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'published_date')
    list_display_links = ('pk', 'title', 'published_date',)



admin.site.register(Questions, QuestionsModelAdmin)
admin.site.register(Vote)
admin.site.register(Answers)
admin.site.register(Save)
admin.site.register(AnswerComments)
admin.site.register(Tags)
admin.site.register(QuestionComments)
admin.site.register(AnswerVote)
