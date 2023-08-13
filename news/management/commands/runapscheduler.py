import logging
from news.models import Subscribers, Category, Post
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils.html import strip_tags


logger = logging.getLogger(__name__)

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

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            weekly_send_mail,
            # trigger=CronTrigger(second="*/30"),
            trigger=CronTrigger(day="*/7"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="weekly_send_mail",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_send_mail'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")