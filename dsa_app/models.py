from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from ckeditor.fields import RichTextField


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='user', related_name='profile', on_delete=models.CASCADE, )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures',
                                        default='uploads/profile_pictures/default.png',
                                        blank=True, null=True)
    location = models.CharField(max_length=500)
    about_yourself = models.TextField(max_length=1000, blank=True, null=True)
    profession = models.CharField(max_length=500, blank=True, null=True)
    instagram_link = models.CharField(max_length=500, blank=True, null=True)
    linkedin_link = models.CharField(max_length=500, blank=True, null=True)
    github_link = models.CharField(max_length=500, blank=True, null=True)
    portfolio_link = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


LEVEL = (
    ('BASIC', 'BASIC'),
    ('EASY', 'EASY'),
    ('MEDIUM', 'MEDIUM'),
    ('HARD', 'HARD'),
    ('EXPERT', 'EXPERT')
)


class Question(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, blank=True, null=True)
    ques_description = RichTextField()
    level = models.CharField(choices=LEVEL, max_length=100)
    gfg = models.CharField(max_length=500, blank=True, null=True)
    leetcode = models.CharField(max_length=500, blank=True, null=True)
    other = models.CharField(max_length=500, blank=True, null=True)
    cplusplus_video = models.CharField(max_length=500, blank=True, null=True)
    java_video = models.CharField(max_length=500, blank=True, null=True)
    python_video = models.CharField(max_length=500, blank=True, null=True)
    similar1 = models.CharField(max_length=1000)
    similar2 = models.CharField(max_length=1000)
    posted_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Sheet(models.Model):
    user = models.OneToOneField(UserProfile, verbose_name='user', related_name='sheet', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, blank=True, null=True)
    description = RichTextField()


@receiver(post_save, sender=UserProfile)
def create_sheet(sender, instance, created, **kwargs):
    if created:
        Sheet.objects.create(user=instance)


@receiver(post_save, sender=UserProfile)
def save_sheet(sender, instance, **kwargs):
    instance.sheet.save()


class UserQuestion(models.Model):
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    question_link = models.CharField(max_length=1000)
    solution_link = models.CharField(max_length=1000, blank=True, null=True)
    your_solution = RichTextField()
    posted_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Solution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    solution = RichTextField()
    posted = models.DateTimeField(auto_now_add=True)