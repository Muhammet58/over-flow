import datetime
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Tags(models.Model):
    name = models.CharField(max_length=250)
    content = models.TextField()

    def __str__(self):
        return f'{self.name}'


class Questions(models.Model):
    title = models.CharField(max_length=100)
    context = RichTextUploadingField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(default=0)
    vote = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tags, related_name='questions')

    def userVote(self, user, value):
        try:
            votes = Vote.objects.get(user=user, question_vote=self)
            if votes.value == value:
                self.vote -= value
                votes.delete()
            else:
                self.vote -= votes.value
                self.vote += value
                votes.value = value
                votes.save()
        except Vote.DoesNotExist:
            self.vote += value
            Vote.objects.create(user=user, question_vote=self, value=value)

        self.save()

    def incrementViewCount(self):
        self.view += 1
        self.save()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_vote = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='votes')
    published_date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField()

    class Meta:
        unique_together = ('user', 'question_vote')


class Answers(models.Model):
    answer = RichTextField()
    answer_to_the_question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, models.CASCADE)
    vote = models.IntegerField(default=0)
    published_date = models.DateTimeField(auto_now_add=True)

    def userAnswerVote(self, user, value):
        try:
            votes = AnswerVote.objects.get(user=user, answer_vote=self)
            if votes.value == value:
                self.vote -= value
                votes.delete()
            else:
                self.vote -= votes.value
                self.vote += value
                votes.value = value
                votes.save()
        except AnswerVote.DoesNotExist:
            self.vote += value
            AnswerVote.objects.create(user=user, answer_vote=self, value=value)

        self.save()

    def __str__(self):
        return self.answer


class AnswerVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_vote = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='answer_votes')
    published_date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField()

    class Meta:
        unique_together = ('user', 'answer_vote')


class Save(models.Model):
    questions = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='saves')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AnswerComments(models.Model):
    comment = RichTextUploadingField()
    comment_answer = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='answer_comments')
    comments_user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class QuestionComments(models.Model):
    comment = models.TextField()
    comment_question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='question_comments')
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
