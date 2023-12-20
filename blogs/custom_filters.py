from django import template

register = template.Library()


@register.filter
def get_date_of_view(published_post, user):
    return published_post.get_date_of_view(user)

@register.filter
def get_date_of_like(published_post, user):
    return published_post.get_date_of_like(user)

@register.filter
def has_followed(blogger, user):
    return blogger.has_followed(user)

@register.filter(name = 'is_following')
def is_following(user, blogger):
    return user.ifollows.filter(followedPerson = blogger).exists()