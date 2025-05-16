from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
    fullname = models.CharField(max_length=400)
    phonenumber = models.CharField(max_length=10,unique=True)
    
    class  Meta:
        db_table = ''
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return f"{self.user} -=- {self.fullname}"
    