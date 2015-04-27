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

    # properties
    print_name  = property(_get_print_name)
    username    = property(_get_username)
    email       = property(_get_email)

    location    = models.CharField(blank=True, max_length=const.SHORT_TEXT_LENGTH)

    resume_url  = models.URLField(blank=True, max_length=const.URL_LENGTH)
    portfolio   = models.URLField(blank=True, max_length=const.URL_LENGTH)
    github_url  = models.URLField(blank=True, max_length=const.URL_LENGTH)

    position    = models.CharField(blank=True, max_length=const.SHORT_TEXT_LENGTH)
    skills      = models.ManyToManyField(HashTag, related_name='hashtag')

    def get_picture_url(self):
        if not self.picture_url:
            return const.DEFAULT_PICTURE_URL
        return self.picture_url

    def __unicode__(self):
        return '[Profile: ' + self.username + ']'

