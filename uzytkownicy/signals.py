from django.contrib.auth.models import User
from .models import Profil
from django.db.models.signals import post_save, post_delete

from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        print('przed stworzeniem profilu')
        profile = Profil.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )
        print('po stworzeniu profilu')

        send_mail (
            "Witamy w oryginalnych przepisach!",
            "Dziękujemy że jesteś z nami! Zachęcamy do przeglądu naszej strony",
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=True,
        )
        print('po wysłaniu maila')
    


def updateUser(sender, instance, created, **kwargs):
    profil = instance
    user = profil.user
    if created == False:
        user.first_name = profil.name
        user.username = profil.username
        user.email = profil.email
        user.save()

def profileDeleted(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profil)
post_delete.connect(profileDeleted, sender=Profil)