import math
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator
from django.contrib.auth.models import User

from markdown import markdown


# Create your models here.
class Dashboard(models.Model):
    name = models.CharField('Nom', unique=True, max_length=30)
    description = models.CharField('Description', max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__dashboard=self).count()

    def get_lastest_post(self):
        return Post.objects.filter(topic__dashboard=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField('Sujet', max_length=225)
    last_updated = models.DateTimeField('Dernière mise à jour', auto_now_add=True)
    dashboard = models.ForeignKey(Dashboard, related_name='topics', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_lastest_posts(self):
        return self.posts.order_by(
            '-created_at')[:10]


class Post(models.Model):
    message = models.TextField('Message', max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Date de réponse', auto_now_add=True)
    updated_at = models.DateTimeField('Date de mise à jour', null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        truncated_m = Truncator(self.message)
        return truncated_m.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
