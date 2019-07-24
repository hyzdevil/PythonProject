import json
from django import template

register = template.Library()

@register.filter(name="deserialization")
def Deserialization(value):
    return json.loads(value)