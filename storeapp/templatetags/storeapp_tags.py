from django import template
from ..models import Post 

register = template.Library()

@register.inclusion_tag('storeapp/post/latest_posts.html')
def show_latest_post(count=5):
    latest_post = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_post}  