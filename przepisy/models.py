from django.db import models
import uuid
from uzytkownicy.models import Profil
from django.conf import settings

class Przepis(models.Model):
    owner = models.ForeignKey(Profil, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_original = models.BooleanField(null=True, blank=True, default=False)
    was_asked = models.BooleanField(null=True, blank=True, default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-is_original', '-vote_ratio', '-vote_total', 'title']

    @property
    def reviewers(self):
        queryset = self.ocena_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def doesImageWork(self):
        try:
            return self.featured_image
        except:
            return False

    @property
    def getVoteCount(self):
        reviews = self.ocena_set.all()
        upVotes = reviews.filter(value="up").count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

class Ocena(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profil, on_delete=models.CASCADE, null=True)
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'przepis']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
