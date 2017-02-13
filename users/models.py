from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
                                    User,
                                    BaseUserManager,
                                    AbstractBaseUser)
from django.db.models.signals import post_save

import random

# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField()
    random_num = models.IntegerField(default=random.randint(1, 100))

    def __unicode__(self):  # __str__
        return self.user.username