from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.core.mail import send_mail
from .models import Post, Author, Subscribers
from NewsPaper import settings
 

@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.title} {instance.creation_datetime.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment changed for {instance.title} {instance.creation_datetime.strftime("%d %m %Y")}'
 
    send_mail('New post addition', 'Тело письма', settings.EMAIL_HOST_USER, f'{instance.author.user.email}')


