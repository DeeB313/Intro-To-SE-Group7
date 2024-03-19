from django import template
from inventory.models import Category
register = template.Library()

@register.inclusion_tag("core/menu.html")
def menu():
    categories = Category.objects.all()
    return {'categories': categories}
