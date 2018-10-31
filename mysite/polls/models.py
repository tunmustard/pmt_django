import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings


class Pollset(models.Model):
    poll_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    user_performed = models.ManyToManyField(settings.AUTH_USER_MODEL)
    is_active = models.BooleanField(default=True)
    require_authorization = models.BooleanField(default=True)

    def __str__(self):
        return self.poll_text	
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Question(models.Model):
    question = models.ForeignKey(Pollset, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text	

	
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text	
		
