
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from simpleapp.models import PostCategory
from simpleapp.tasks import send_news_category


@receiver(m2m_changed, sender= PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_news_category.delay(instance.pk)