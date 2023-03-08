from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

from forum.managers import LikeDislikeManager, TagManager, QuestionManager, AnswerManager
from users.models import User


class Tag(models.Model):
    title = models.CharField(unique=True, verbose_name="Tag", max_length=25)
    objects = TagManager()

    def __str__(self):
        return self.title


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    def __str__(self):
        return self.user.username + " liked"


@receiver(pre_delete, sender=LikeDislike)
def add_score(instance, **kwargs):
    instance.content_object.rate -= instance.vote
    instance.content_object.save()


class Question(models.Model):
    author = models.ForeignKey(User, null=False, verbose_name="Question Author", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, verbose_name='Question date')
    title = models.CharField(max_length=70, verbose_name='Question Title')
    text = models.TextField(verbose_name='Question full text')
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True, verbose_name='Tags')
    votes = GenericRelation(LikeDislike, related_query_name='question')
    rate = models.IntegerField(default=0, verbose_name='Rate')

    objects = QuestionManager()

    def __str__(self):
        return self.author.username


class Answer(models.Model):
    author = models.ForeignKey(User, null=False, verbose_name="Answer Author", on_delete=models.CASCADE)
    title = models.CharField(max_length=70, verbose_name='Answer Title')
    text = models.TextField(verbose_name='Answer full text')
    question = models.ForeignKey(Question, null=False, verbose_name="Question", on_delete=models.CASCADE)
    votes = GenericRelation(LikeDislike, related_query_name='answer')
    rate = models.IntegerField(default=0, verbose_name='Rate')

    objects = AnswerManager()

    def __str__(self):
        return self.author.username
