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
        if closeTag and not c.isnumeric():
            readable += "</sub>"
            closeTag = False
        if c == '*':
            readable += ' &#8226; '
        else:
            readable += c
    if closeTag:
        readable += "</sub>"
    return mark_safe(readable)
