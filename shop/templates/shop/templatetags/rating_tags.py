from django import template
from django.utils.safestring import mark_safe

register = template.Library()

FULL_STAR = '''
<svg class="star-icon star-full" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
  <path fill="#f59e0b" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
</svg>'''

HALF_STAR = '''
<svg class="star-icon star-half" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
  <defs>
    <linearGradient id="half-grad">
      <stop offset="50%" stop-color="#f59e0b"/>
      <stop offset="50%" stop-color="#cbd5e1"/>
    </linearGradient>
  </defs>
  <path fill="url(#half-grad)" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
</svg>'''

EMPTY_STAR = """
<svg class="star-icon star-empty" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
  <path fill="#cbd5e1" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
</svg>"""

@register.filter(name='render_stars')
def render_stars(rating):
    """
    Converts a numeric rating (0.0 to 5.0) into 5 SVG star icons.
    """
    if rating is None:
        rating = 0.0
    else:
        rating = float(rating)

    full_stars = int(rating)
    has_half = (rating - full_stars) >= 0.4
    empty_stars = 5 - full_stars - (1 if has_half else 0)

    stars_html = (FULL_STAR * full_stars)
    if has_half:
        stars_html += HALF_STAR
    stars_html += (EMPTY_STAR * empty_stars)

    return mark_safe(f'<span class="svg-star-group">{stars_html}</span>')