from celery import shared_task
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import News_All, Category


@shared_task
def send_news_category(pk):
    post = News_All.objects.get(pk=pk)
    categories = post.link_PostCategory.all()
    subscribers_emails = []

    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/news_or_art/News_all/{pk}'
            # или не pk, а id
        }
    )

    msg = EmailMultiAlternatives(
        subject=post.name,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def my_job():
    #  Your job processing logic here...
    today=timezone.now()
    last_week=today-timedelta(days=7)
    posts=News_All.objects.filter(time_in__gte=last_week)
    categories=set(posts.values_list('link_PostCategory__name', flat=True))
    subscribers=set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()