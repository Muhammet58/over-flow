from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Tags(models.Model):
    name = models.CharField(max_length=250)
    content = models.TextField()

    def __str__(self):
        return f'{self.name}'


class question(models.Model):
    title = models.CharField(max_length=100)
    context = RichTextUploadingField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tags)

    def user_vote(self, user, value):
        try:
            vote = Vote.objects.get(user=user, question=self)
            if vote.value == value:
                self.votes -= value
                vote.delete()
            else:
                self.votes -= vote.value
                self.votes += value
                vote.value = value
                vote.save()
        except Vote.DoesNotExist:
            self.votes += value
            Vote.objects.create(user=user, question=self, value=value)
        
        self.save()

    def increment_view_count(self):
        self.view += 1
        self.save()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        unique_together = ('user', 'question')


class answer(models.Model):
    answer = RichTextField()
    answerToTheQuestion = models.ForeignKey(question, on_delete=models.CASCADE, related_name='answer')
    user = models.ForeignKey(User, models.CASCADE)
    votes = models.IntegerField(default=0)
    published_date = models.DateTimeField(auto_now_add=True)


    def user_answer_vote(self, user, value):
        try:
            vote = answerVote.objects.get(user=user, answer_votes=self)
            if vote.value == value:
                self.votes -= value
                vote.delete()
            else:
                self.votes -= vote.value
                self.votes += value
                vote.value = value
                vote.save()
        except answerVote.DoesNotExist:
            self.votes += value
            answerVote.objects.create(user=user, answer_votes=self, value=value)
        
        self.save()


    def __str__(self):
        return self.answer



class answerVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_votes = models.ForeignKey(answer, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        unique_together = ('user', 'answer_votes')



class saved(models.Model):
    que = models.ForeignKey(question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class comment(models.Model):
    comment = RichTextUploadingField()
    comment_answer = models.ForeignKey(answer, on_delete=models.CASCADE)
    comments_user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class QuesComment(models.Model):
    comment = models.TextField()
    commentQues = models.ForeignKey(question, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    PubDate = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.comment