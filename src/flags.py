"""Simple country flags drawn as inline SVG (30x20). Placeholder: <!--FLAG gb-->"""
import re

RE = re.compile(r"<!--FLAG\s+([a-z]{2})-->")


def _s(inner):
    return f'<svg class="flag" viewBox="0 0 30 20" role="img" aria-hidden="true">{inner}</svg>'


def _h(*cols):
    h = 20 / len(cols)
    return "".join(f'<rect y="{i * h:.2f}" width="30" height="{h + .05:.2f}" fill="{c}"/>' for i, c in enumerate(cols))


def _v(*cols):
    w = 30 / len(cols)
    return "".join(f'<rect x="{i * w:.2f}" width="{w + .05:.2f}" height="20" fill="{c}"/>' for i, c in enumerate(cols))


FLAGS = {
    "de": lambda: _s(_h("#111", "#D00", "#FFCE00")),
    "fr": lambda: _s(_v("#0055A4", "#fff", "#EF4135")),
    "it": lambda: _s(_v("#009246", "#fff", "#CE2B37")),
    "nl": lambda: _s(_h("#AE1C28", "#fff", "#21468B")),
    "ua": lambda: _s(_h("#0057B7", "#FFD700")),
    "es": lambda: _s('<rect width="30" height="20" fill="#AA151B"/><rect y="5" width="30" height="10" fill="#F1BF00"/>'),
    "pt": lambda: _s('<rect width="12" height="20" fill="#006600"/><rect x="12" width="18" height="20" fill="#FF0000"/><circle cx="12" cy="10" r="4" fill="#FFCC00"/>'),
    "gr": lambda: _s('<rect width="30" height="20" fill="#0D5EAF"/>' + "".join(f'<rect y="{y}" width="30" height="2.2" fill="#fff"/>' for y in (2.2, 6.7, 11.1, 15.6))
                     + '<rect width="11" height="11" fill="#0D5EAF"/><rect x="4.4" width="2.2" height="11" fill="#fff"/><rect y="4.4" width="11" height="2.2" fill="#fff"/>'),
    "ch": lambda: _s('<rect width="30" height="20" fill="#D52B1E"/><rect x="13" y="4" width="4" height="12" fill="#fff"/><rect x="9" y="8" width="12" height="4" fill="#fff"/>'),
    "tr": lambda: _s('<rect width="30" height="20" fill="#E30A17"/><circle cx="11" cy="10" r="5" fill="#fff"/><circle cx="12.4" cy="10" r="4" fill="#E30A17"/><polygon points="17,10 20.5,8.8 18.3,11.8 18.3,8.2 20.5,11.2" fill="#fff"/>'),
    "no": lambda: _s('<rect width="30" height="20" fill="#BA0C2F"/><rect x="8" width="5" height="20" fill="#fff"/><rect y="7.5" width="30" height="5" fill="#fff"/><rect x="9.2" width="2.6" height="20" fill="#00205B"/><rect y="8.7" width="30" height="2.6" fill="#00205B"/>'),
    "is": lambda: _s('<rect width="30" height="20" fill="#02529C"/><rect x="8" width="5" height="20" fill="#fff"/><rect y="7.5" width="30" height="5" fill="#fff"/><rect x="9.2" width="2.6" height="20" fill="#DC1E35"/><rect y="8.7" width="30" height="2.6" fill="#DC1E35"/>'),
    "gb": lambda: _s('<rect width="30" height="20" fill="#012169"/><path d="M0 0 L30 20 M30 0 L0 20" stroke="#fff" stroke-width="4"/><path d="M0 0 L30 20 M30 0 L0 20" stroke="#C8102E" stroke-width="1.6"/><rect x="12" width="6" height="20" fill="#fff"/><rect y="7" width="30" height="6" fill="#fff"/><rect x="13" width="4" height="20" fill="#C8102E"/><rect y="8" width="30" height="4" fill="#C8102E"/>'),
}


def expand(html):
    return RE.sub(lambda m: FLAGS[m.group(1)](), html)
