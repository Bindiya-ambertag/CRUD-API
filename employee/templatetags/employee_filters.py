from django import template

register = template.Library()

@register.filter
def upper(value):
    return value.upper() if value else ""

@register.filter
def currency(value):
    try:
        return f"₹{int(value):,}"
    except:
        return "₹0"

@register.filter
def default_na(value):
    return value if value else "N/A"
