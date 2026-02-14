from django import template

register = template.Library()

@register.filter(name="money")
def money(value):
    try:
        n = int(float(value))
    except (TypeError, ValueError):
        return value
    return f"{n:,}".replace(",", " ")
