from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    author = models.ForeignKey(User)
    createdDate = models.DateTimeField('Created Date', default=datetime.now)
    modifiedDate = models.DateTimeField('Modified Date', default=datetime.now)
    
    def __unicode__(self):
        return self.title


class Comments(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User)
    comment = models.CharField(max_length = 300)
    conmmentTime = models.DateTimeField( default=datetime.now)

    def __unicode__(self):
        return str(self.id)