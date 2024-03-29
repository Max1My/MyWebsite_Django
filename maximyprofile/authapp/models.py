from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name = 'возраст', default=18)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True,blank=True,null=True)


    def is_activation_key_expires(self):
        if now() <= self.activation_key_expires + timedelta(hours=48):
            return False
        else:
            return True

class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE,'М'),
        (FEMALE,'Ж')
    )

    user = models.OneToOneField(ShopUser,unique=True,null=False,db_index=True,on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги',max_length=128,blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512,blank=True )
    gender = models.CharField(verbose_name='пол',max_length=1,choices=GENDER_CHOICES,blank=True)
    langs = models.CharField(verbose_name='язык',max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save,sender=ShopUser)
    def create_user_profile(sender,instance,created,**kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save,sender=ShopUser)
    def save_user_profile(sender,instance,**kwargs):
        instance.shopuserprofile.save()

