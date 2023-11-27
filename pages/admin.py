from django.contrib import admin
from .models import Tags, answer, question, saved, comment, QuesComment, Vote


class questionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'published_date',)
    list_display_links = ('pk', 'title', 'published_date',)



admin.site.register(question, questionAdmin)
admin.site.register(Vote)
admin.site.register(answer)
admin.site.register(saved)
admin.site.register(comment)
admin.site.register(Tags)
admin.site.register(QuesComment)
