from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver 
from django.core.mail import send_mail
from .models import Post, Subscribers
from NewsPaper import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
 

@receiver(m2m_changed, sender=Post.category.through) 
def notify_for_subscriber(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        post_categories = instance.category.filter(pk__in=pk_set).distinct()
        email_list = Subscribers.objects.filter(category__in=post_categories).values_list('user__email',
                                                                                                flat=True).distinct()
        post_categories_name = ', '.join(instance.category.values_list('name_category', flat=True))
        if email_list:
            for email in email_list:
                subject = f"Вышла новая публикация в категории {post_categories_name}."
                message = render_to_string('new_post.html', {'post': instance})
                send_mail(
                                subject=subject,
                                message=message,
                                from_email=settings.EMAIL_HOST_USER,
                                recipient_list=[email]
                            )


