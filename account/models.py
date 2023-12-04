from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from pages.models import question, answer, Tags
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/user-default.png', null=True, blank=True)
    about = RichTextField(null=True, blank=True)
    user_questions = models.ManyToManyField(question, related_name='asked_by', blank=True)
    user_answers = models.ManyToManyField(answer, related_name='answered_by', blank=True)
    user_tags = models.ManyToManyField(Tags, related_name='used_by', blank=True)

    def __str__(self):
        return f'{self.user.username} profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.save()
    




@receiver(post_save, sender=question)
def add_question_t0_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.get(user=instance.user)
        user_profile.user_questions.add(instance)

@receiver(post_save, sender=answer)
def add_answer_to_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.get(user=instance.user)
        user_profile.user_answers.add(instance)
    
