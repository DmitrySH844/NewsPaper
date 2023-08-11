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
    today = datetime.today()  # сегодня
    week_ago = today - timedelta(days=7)  # дата неделю назад
    # находим почту всех пользователей имеющих подписки
    email_list = Subscribers.objects.values_list('user__email', flat=True).distinct()
    for email in email_list:
        # находим для все категории на которые подписан данный user
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
