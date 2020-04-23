from django import template
from Media_app.models import *

register = template.Library()


@register.filter
def notification_count(user):
    return Notification.objects.filter(user=user).count()


@register.filter
def friend_request(user):
    friend = User.objects.get(display_name=user)
    return friend.friend_requests.count()


@register.filter
def groups_count(user):
    return Group.objects.filter(user=user).count()
