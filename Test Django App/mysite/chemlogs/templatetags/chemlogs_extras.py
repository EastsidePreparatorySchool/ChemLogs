from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

# converts underscores to subscripts (only works with 1-digit subscript), and asterisks to dots
@register.filter(name='displayFormula')
@stringfilter
def displayFormula(raw):
    readable = ""
    closeTag = False
    for c in raw:
        if c == '_':
            readable += "<sub>"
            closeTag = True
            continue
        if c == '*':
            readable += ' &#8226; '
        else:
            readable += c
        if closeTag:
            readable += "</sub>"
            closeTag = False
    return mark_safe(readable)
