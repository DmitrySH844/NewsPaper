from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import User, Post, Subscribers, Category 
from celery import shared_task
from django.urls import reverse_lazy
from NewsPaper import settings
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from datetime import datetime, timedelta


@shared_task
def weekly_send_mail():
    today = datetime.today()  
    week_ago = today - timedelta(days=7)  
    email_list = Subscribers.objects.values_list('user__email', flat=True).distinct()
    for email in email_list:
        user_subscribed_categories = Subscribers.objects.filter(user__email=email).values_list('category',
                                                                                                     flat=True)
        posts_list = Post.objects.filter(category__in=user_subscribed_categories, date__gte=week_ago)
        categories_names = Category.objects.filter(id__in=user_subscribed_categories).values_list('category_name',
                                                                                                  flat=True)
        if posts_list:
            subject = f'Еженедельная подборка новых публикаций.'
            html_content = render_to_string('weekly_post.html', {'posts': posts_list, 'categories_names': categories_names})
            text_content = strip_tags(html_content)
            msg=EmailMultiAlternatives(
                                subject,
                                text_content,
                                from_email=settings.EMAIL_HOST_USER,
                                to = [email]
                            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

#@shared_task
#def new_post_mail(post_id):
    #post = Post.objects.get(id=post_id)
    #post_categories = post.category.all()
    #email_list = Subscribers.objects.filter(category__in=post_categories).values_list('user__email',
                                                                                                #flat=True).distinct()
    #post_categories_name = ', '.join(post_categories.category.values_list('name_category', flat=True))
    #if email_list:
        #for email in email_list:
            #subject = f"Вышла новая публикация в категории {post_categories_name}."
            #html_content = render_to_string('new_post.html', {'post': post})
            #text_content = strip_tags(html_content)
            #msg=EmailMultiAlternatives(
                                #subject,
                                #text_content,
                                #from_email=settings.EMAIL_HOST_USER,
                                #to = [email]
                            #)
            #msg.attach_alternative(html_content, "text/html")
            #msg.send()