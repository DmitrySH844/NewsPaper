from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver 
from django.core.mail import EmailMultiAlternatives
from .models import Post, Subscribers
from NewsPaper import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.html import strip_tags
 

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
                html_content = render_to_string('new_post.html', {'post': instance})
                text_content = strip_tags(html_content)
                msg=EmailMultiAlternatives(
                                subject,
                                text_content,
                                from_email=settings.EMAIL_HOST_USER,
                                to = [email]
                            )
                msg.attach_alternative(html_content, "text/html")
                msg.send()



