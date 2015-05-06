from django.db import models
from django.contrib.auth.models import User

import const

#
class HashTag(models.Model):
    ctime       = models.DateTimeField(auto_now_add=True)
    content     = models.CharField(max_length=const.SHORT_TEXT_LENGTH)

    def __unicode__(self):
        return self.content

#
class Profile(models.Model):

    USER_TYPES = (
            (0, 'programmer'),
            (1, 'designer'),
            (2, 'individual hunter'),
            (3, 'company hunter'),
            )

    # username, last_name, first_name, email
    user        = models.ForeignKey(User)
    user_type   = models.IntegerField(default=0, choices=USER_TYPES)

    picture_url = models.CharField(blank=True, max_length=const.URL_LENGTH)
    ctime       = models.DateTimeField(auto_now_add=True)

    # properties help functions
    def _get_print_name(self):
        return self.user.first_name + " " + self.user.last_name
    def _get_username(self):
        return self.user.username
    def _get_email(self):
        return self.user.email

    def _get_credits(self):

        comments = Comment.objects.filter(user=self.user)
        total = 0

        if comments.count() <= 0:
            return 0

        for c in comments:
            total += c.score

        return total * 1.0 / comments.count()

    def _get_credits_d(self):
        return int(self._get_credits())

    def _get_inv_credits_d(self):
        return 5 - int(self._get_credits())


    # properties
    print_name  = property(_get_print_name)
    username    = property(_get_username)
    email       = property(_get_email)

    credits     = property(_get_credits)
    credits_d   = property(_get_credits_d)
    inv_credits_d   = property(_get_inv_credits_d)

    location    = models.CharField(blank=True, max_length=const.SHORT_TEXT_LENGTH)

    resume_url  = models.URLField(blank=True, max_length=const.URL_LENGTH)
    portfolio   = models.URLField(blank=True, max_length=const.URL_LENGTH)
    github_url  = models.URLField(blank=True, max_length=const.URL_LENGTH)
    website     = models.URLField(blank=True, max_length=const.URL_LENGTH)

    position    = models.CharField(blank=True, max_length=const.SHORT_TEXT_LENGTH)
    skills      = models.ManyToManyField(HashTag, related_name='hashtag', blank=True)

    overview    = models.TextField(blank=True)

    def get_picture_url(self):
        if not self.picture_url:
            return const.DEFAULT_PICTURE_URL
        return self.picture_url

    def __unicode__(self):
        return '[Profile: ' + self.username + ']'

#
class Comment(models.Model):

    CHOICES = [(i,i) for i in range(6)]

    def _get_inv_score(self):
        return 5 - self.score

    user        = models.ForeignKey(User, related_name="+")
    author      = models.ForeignKey(User, related_name="+")
    title       = models.CharField(max_length=const.SHORT_TEXT_LENGTH)
    content     = models.TextField()
    score       = models.IntegerField(choices=CHOICES, default=0)
    inv_score   = property(_get_inv_score)
    ctime       = models.DateTimeField(auto_now_add=True)

