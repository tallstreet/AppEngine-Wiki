from django import template
from markdown import markdown as markdown_func

register = template.Library()

def markdown(value):
    return markdown_func(value)
register.filter('markdown', markdown)
