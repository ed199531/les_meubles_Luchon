#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur statique — Les Meublés de Luchon
Source de vérité unique : header, footer, SEO, Schema.org et contenu.
Lancer :  python3 build.py   (génère tout le dossier /site)
"""
import os, json, html

BASE_URL = "https://lesmeublesdeluchon.com"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

# --- NAP (cohérent sur tout le site) ---
NAP = {
    "name": "Les Meublés de Luchon",
    "street": "5 rue Azémar",
    "postal": "31110",
    "city": "Bagnères-de-Luchon",
    "region": "Occitanie",
    "tel_display": "06 84 81 60 41",
    "tel_link": "+33684816041",
    "email": "contact@lesmeublesdeluchon.com",
    "facebook": "https://www.facebook.com/luchonlocations",
    "instagram": "https://www.instagram.com/lesmeublesdeluchon/",
}

NAV = [
    ("/", "Accueil"),
    ("/nos-logements/", "Appartements"),
    ("/cure-thermale/", "Cure thermale"),
    ("/services/", "Services"),
    ("/activites/", "Activités"),
    ("/guide/", "Infos pratiques"),
    ("/avis/", "Avis"),
    ("/contact/", "Contact"),
]

# ---- Données des logements ----
LOGEMENTS = {
    "la-perle-bleue": {
        "slug": "perle-bleue",
        "name": "La Perle Bleue",
        "type": "T2 — 2 pièces",
        "capacity": 4,
        "floor": "2ᵉ étage",
        "adresse": "5 bis rue Azémar, étage 2",
        "stars": 3,
        "booking": "superhote",
        "short": "Appartement deux pièces cosy et moderne, au cœur de Luchon.",
        "intro": "La Perle Bleue est un charmant appartement T2 à la décoration douce et contemporaine. Avec sa chambre séparée, son salon lumineux et son canapé convertible, il accueille confortablement jusqu'à 4 personnes — idéal pour une famille ou deux couples en séjour thermal ou au ski.",
        "images": [
            ("salon.jpg", "Salon lumineux de La Perle Bleue"),
            ("chambre.jpg", "Chambre avec literie confortable"),
            ("canape.jpg", "Canapé convertible du salon"),
            ("cuisine.jpg", "Cuisine entièrement équipée"),
            ("douche.jpg", "Salle de douche moderne"),
            ("lampe.jpg", "Détail décoration de La Perle Bleue"),
        ],
        "amenities": ["Chambre séparée + literie qualité", "Canapé convertible", "Cuisine équipée (four, lave-vaisselle)",
                      "Machine à café Nespresso", "Salle de douche", "Lave-linge / sèche-linge",
                      "Wi-Fi haut débit gratuit", "Télévision", "Linge de maison (option)", "Chauffage individuel"],
    },
    "l-echappee-verte": {
        "slug": "echappee-verte",
        "name": "L'Échappée Verte",
        "type": "T1 — Studio",
        "capacity": 2,
        "floor": "3ᵉ étage",
        "adresse": "5 bis rue Azémar, étage 3",
        "stars": 2,
        "booking": "superhote",
        "short": "Studio douillet et lumineux, à la décoration soignée.",
        "intro": "L'Échappée Verte est un studio cosy et lumineux, pensé pour deux voyageurs. Sa décoration soignée aux tons naturels, son coin cuisine-repas et son canapé convertible en font un nid parfait pour un séjour en amoureux, une cure thermale ou un week-end à la montagne.",
        "images": [
            ("cuisine.jpg", "Coin cuisine et repas de L'Échappée Verte"),
            ("cuisine-2.jpg", "Espace repas lumineux"),
            ("canape.jpg", "Canapé convertible"),
            ("entree.jpg", "Entrée du studio"),
            ("douche.jpg", "Salle d'eau"),
            ("salle-douche.jpg", "Salle de douche"),
        ],
        "amenities": ["Canapé convertible", "Coin cuisine équipé", "Machine à café Nespresso",
                      "Salle de douche", "Lave-linge / sèche-linge", "Wi-Fi haut débit gratuit",
                      "Télévision", "Linge de maison (option)", "Chauffage individuel"],
    },
    "le-refuge-thermal": {
        "slug": "refuge-thermal",
        "name": "Le Refuge Thermal",
        "type": "T2 — 2 pièces",
        "capacity": 4,
        "floor": "Rez-de-chaussée",
        "adresse": "5A rue Azémar, rez-de-chaussée",
        "stars": 2,
        "booking": "superhote",
        "short": "Appartement de plain-pied, idéal pour les curistes et l'accès facile.",
        "intro": "Le Refuge Thermal est un appartement T2 confortable et fonctionnel, situé en rez-de-chaussée pour un accès de plain-pied — un vrai atout pour les curistes et les personnes à mobilité réduite. Il se compose d'une chambre séparée avec un vrai lit double et d'une pièce de vie ouverte avec coin salon et cuisine équipée. À quelques minutes des thermes, il conjugue praticité et sérénité pour un séjour tout en douceur.",
        "images": [
            ("salon.jpg", "Séjour du Refuge Thermal avec canapé convertible"),
            ("piece-de-vie.jpg", "Vue d'ensemble de la pièce de vie du Refuge Thermal"),
            ("chambre.jpg", "Chambre avec lit double du Refuge Thermal"),
            ("cuisine.jpg", "Cuisine équipée avec crédence en carreaux de ciment"),
            ("cuisine-2.jpg", "Plan de travail et plaque induction"),
            ("douche.jpg", "Douche à l'italienne"),
            ("salle-de-bain.jpg", "Salle de bain avec vasque et sèche-serviettes"),
            ("sejour.jpg", "Coin salon lumineux du Refuge Thermal"),
        ],
        "amenities": ["Accès de plain-pied (RDC)", "Chambre séparée avec lit double", "Séjour avec canapé convertible",
                      "Cuisine équipée (induction)", "Douche à l'italienne", "Sèche-serviettes", "Lave-linge",
                      "Wi-Fi haut débit gratuit", "Télévision", "Idéal curistes / PMR", "Chauffage individuel"],
    },
}

# ---- Moteur de réservation Superhôte (clés publiques d'intégration) ----
SUPERHOTE = {
    "perle-bleue":    "propertyKeyhYHKfobjxVxjHhLTkzJPTehXA",
    "echappee-verte": "propertyKey3VpakNcQ3X2LlAXOTujQsws6e",
    "refuge-thermal": "propertyKey8WSw0zYWOvWLL0rAslYrAKaOu",
}

SUPERHOTE_SITE_KEY = "bcGpXSkB3NtJCWmMbGnVucHbT"
SUPERHOTE_GROUP = "Les Meublés de Luchon"   # filtre : n'affiche que les biens de la marque

def booking_search(height=1500):
    """Moteur multi-logements : recherche par dates, uniquement nos 3 appartements."""
    from urllib.parse import quote
    src = (f"https://app.superhote.com/#/get-available-rentals/{SUPERHOTE_SITE_KEY}"
           f"?groups={quote(SUPERHOTE_GROUP)}")
    return (f'<iframe class="booking-engine" id="bookingsearch" loading="lazy" allowfullscreen '
            f'title="Rechercher un appartement disponible" src="{src}" width="100%" height="{height}" '
            f'frameborder="0"></iframe>')

def booking_engine(slug=None, height=2400):
    """iframe officielle Superhôte : la réservation se fait sans quitter le site."""
    key = SUPERHOTE.get(slug, "")
    src = f"https://app.superhote.com/#/rental/{key}" if key else ""
    hidden = "" if key else " hidden"
    return (f'<iframe class="booking-engine" id="bookingengine" loading="lazy" allowfullscreen{hidden} '
            f'title="Moteur de réservation sécurisé" src="{src}" width="100%" height="{height}" '
            f'frameborder="0"></iframe>')

# ---- Empreinte de version des assets (anti-cache navigateur) ----
import hashlib

def asset_v(relpath):
    """Hash court du fichier -> /assets/....css?v=xxxx : le cache d'un an
    reste valable, mais toute modification change l'URL donc le navigateur
    recharge automatiquement la nouvelle version."""
    p = os.path.join(OUT, relpath.lstrip("/"))
    try:
        return hashlib.md5(open(p, "rb").read()).hexdigest()[:8]
    except OSError:
        return "1"

CSS_V = asset_v("/assets/css/style.css")
JS_V = asset_v("/assets/js/main.js")

# NB : le texte des <li class='amenities'> doit être encapsulé dans un <span>
# sinon chaque mot/<strong> devient un élément flex et l'alignement casse.
CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>')

# Éléments repris du hero d'accueil, réutilisés sur les bannières des autres pages
HERO_EYEBROW = ('<p class="eyebrow" style="color:#a9e0e4">'
                'Locations saisonnières · Bagnères-de-Luchon</p>')
HERO_BADGES = ('<div class="hero__badges">'
               '<span>⭐ Classés Meublé de Tourisme</span>'
               '<span>💬 Voyageurs conquis depuis 2018</span>'
               '<span>🔑 Arrivée autonome dès 16h</span>'
               '<span>🐾 Animaux bienvenus</span>'
               '</div>')


def stars_html(n):
    return '<span class="stars" aria-label="%d étoiles">%s</span>' % (n, "★" * n)

def jsonld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, ensure_ascii=False, indent=2)

# ----------------------------------------------------------------------------
def head(title, desc, path, og_image="/assets/img/logements/perle-bleue/salon.jpg",
         ld_blocks=None, robots="index, follow"):
    canonical = BASE_URL + path
    og_url = canonical
    ld = "\n".join(jsonld(b) for b in (ld_blocks or []))
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#026878">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Les Meublés de Luchon">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{og_url}">
<meta property="og:image" content="{BASE_URL}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{BASE_URL}{og_image}">
<link rel="icon" href="/assets/img/brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/brand/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unna:ital,wght@0,400;0,700;1,400&family=Open+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={CSS_V}">
<noscript><style>.reveal{{opacity:1!important;transform:none!important}}</style></noscript>
{ld}
</head>
<body>"""

def header(active):
    links = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links += f'        <li><a href="{href}"{cur}>{label}</a></li>\n'
    return f"""
<a href="#main" class="skip-link">Aller au contenu</a>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="/" aria-label="Les Meublés de Luchon — accueil">
      <img src="/assets/img/brand/logo.png" alt="Logo Les Meublés de Luchon" width="46" height="46">
      <span class="brand__name">Les Meublés de Luchon<small>Bagnères-de-Luchon</small></span>
    </a>
    <nav aria-label="Navigation principale">
      <ul class="nav__links">
{links}      </ul>
    </nav>
    <div class="nav__cta">
      <a class="nav__phone" href="tel:{NAP['tel_link']}" title="Appeler le {NAP['tel_display']}" aria-label="Appeler le {NAP['tel_display']}">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.68 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.32 1.85.55 2.81.68A2 2 0 0 1 22 16.92z"/></svg>
        <span class="nav__phone-num">{NAP['tel_display']}</span>
      </a>
      <a class="btn btn--primary" href="/nos-logements/">Réserver</a>
      <button class="nav__toggle" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">"""

def breadcrumb(items):
    """items: liste de (label, href|None). Le dernier = page courante."""
    lis, ld_items = "", []
    for i, (label, href) in enumerate(items):
        if href:
            lis += f'<li><a href="{href}">{html.escape(label)}</a></li>'
            url = BASE_URL + href
        else:
            lis += f'<li aria-current="page">{html.escape(label)}</li>'
            url = BASE_URL + items[i][1] if items[i][1] else None
        ld_items.append({"@type": "ListItem", "position": i + 1, "name": label,
                         **({"item": BASE_URL + href} if href else {})})
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld_items}
    return (f'<nav class="breadcrumb" aria-label="Fil d\'ariane"><div class="container"><ol>{lis}</ol></div></nav>\n'
            + jsonld(ld))

def footer():
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer__brand">
        <img src="/assets/img/brand/logo.png" alt="Les Meublés de Luchon" width="52" height="52">
        <p>Locations saisonnières d'appartements meublés au cœur de Bagnères-de-Luchon, dans les Pyrénées.</p>
        <div class="footer__social">
          <a href="{NAP['facebook']}" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
          <a href="{NAP['instagram']}" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/></svg></a>
        </div>
      </div>
      <div>
        <h4>Navigation</h4>
        <ul class="footer-links">
          <li><a href="/">Accueil</a></li>
          <li><a href="/nos-logements/">Nos appartements</a></li>
          <li><a href="/cure-thermale/">Cure thermale</a></li>
          <li><a href="/services/">Services</a></li>
          <li><a href="/activites/">Activités</a></li>
          <li><a href="/guide/">Guides pratiques</a></li>
          <li><a href="/faq/">FAQ</a></li>
          <li><a href="/avis/">Avis</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Nos appartements</h4>
        <ul class="footer-links">
          <li><a href="/nos-logements/la-perle-bleue/">La Perle Bleue</a></li>
          <li><a href="/nos-logements/l-echappee-verte/">L'Échappée Verte</a></li>
          <li><a href="/nos-logements/le-refuge-thermal/">Le Refuge Thermal</a></li>
          <li><a href="/nos-logements/">Réserver</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul class="footer-links footer-contact">
          <li><span class="fc-ico">📍</span><span>{NAP['street']}, {NAP['postal']} {NAP['city']}</span></li>
          <li><span class="fc-ico">📞</span><a href="tel:{NAP['tel_link']}">{NAP['tel_display']}</a></li>
          <li><span class="fc-ico">✉️</span><a href="mailto:{NAP['email']}">{NAP['email']}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Les Meublés de Luchon — Tous droits réservés.</span>
      <span>
        <a href="/mentions-legales/">Mentions légales</a> ·
        <a href="/politique-de-confidentialite/">Confidentialité</a> ·
        <a href="/plan-du-site/">Plan du site</a>
      </span>
    </div>
  </div>
</footer>
<div class="mobile-bar">
  <a class="btn btn--ghost" href="tel:{NAP['tel_link']}" aria-label="Appeler">📞 Appeler</a>
  <a class="btn btn--primary" href="/nos-logements/">Réserver</a>
</div>
<div class="cookie" id="cookie" role="dialog" aria-live="polite" aria-label="Consentement aux cookies">
  <h4>🍪 Nous respectons votre vie privée</h4>
  <p>Ce site utilise des cookies de mesure d'audience pour améliorer votre expérience. Aucun traceur n'est activé sans votre accord, conformément au RGPD et aux recommandations de la CNIL.</p>
  <div class="cookie__actions">
    <button class="btn btn--primary" id="cookie-accept">Tout accepter</button>
    <button class="btn btn--ghost" id="cookie-refuse">Continuer sans accepter</button>
    <a class="btn btn--ghost" href="/politique-de-confidentialite/">En savoir plus</a>
  </div>
</div>
<script src="/assets/js/main.js?v={JS_V}" defer></script>
</body>
</html>"""

def write(path, contents):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(contents)
    print("écrit :", path)

def page(path, active, title, desc, main_html, og_image="/assets/img/logements/perle-bleue/salon.jpg",
         ld_blocks=None, robots="index, follow"):
    doc = head(title, desc, "/" + path.replace("index.html", ""), og_image, ld_blocks, robots) \
        + header(active) + main_html + footer()
    write(path, doc)

# ============================================================================
# Calendrier de dates réutilisable (widget de réservation + formulaire cure)
def cal_fields(uid, lab_in="Arrivée", lab_out="Départ"):
    """Les deux boutons Arrivée / Départ qui ouvrent le calendrier."""
    def one(key, titre):
        return f"""<div class="booking__field booking__field--date">
        <span class="booking__flabel" id="bk-{key}l-{uid}">{titre}</span>
        <button type="button" class="booking__pickbtn" id="bk-{key}b-{uid}"
                aria-labelledby="bk-{key}l-{uid} bk-{key}b-{uid}" aria-expanded="false"
                aria-haspopup="dialog" data-cal-open="{key}">
          <span data-cal-label="{key}">Ajouter une date</span>
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/></svg>
        </button>
      </div>"""
    return one("in", lab_in) + one("out", lab_out)


def cal_panel(name_in="checkin", name_out="checkout", required=False):
    """Le panneau calendrier + les champs cachés qui portent les valeurs ISO."""
    req = " data-cal-required" if required else ""
    return f"""<input type="hidden" name="{name_in}" data-cal-in><input type="hidden" name="{name_out}" data-cal-out>
      <div class="cal" data-cal{req} role="dialog" aria-label="Sélectionnez les dates" hidden>
        <p class="cal__heading">Sélectionnez les dates</p>
        <div class="cal__head">
          <button type="button" class="cal__nav" data-cal-prev aria-label="Mois précédent">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>
          </button>
          <p class="cal__title" data-cal-title aria-live="polite"></p>
          <button type="button" class="cal__nav" data-cal-next aria-label="Mois suivant">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>
          </button>
        </div>
        <div class="cal__months" data-cal-months></div>
        <div class="cal__foot">
          <button type="button" class="cal__clear" data-cal-clear>Effacer les dates</button>
          <button type="button" class="cal__done" data-cal-close>Fermer</button>
        </div>
      </div>"""


# ============================================================================
# Widget de réservation réutilisable
def booking_widget(fixed_slug=None, cta="Rechercher", stacked=False):
    """Barre de recherche : dates + voyageurs (adultes / enfants / bébés) -> moteur Superhôte."""
    cls = "booking booking--stack" if stacked else "booking"
    uid = fixed_slug or "w"

    def row(key, titre, sous, mini, maxi, val):
        return f"""<div class="guests__row">
            <div><strong>{titre}</strong><span>{sous}</span></div>
            <div class="guests__stepper">
              <button type="button" class="guests__btn" data-step="-1" data-for="{key}" aria-label="Retirer un {titre.lower().rstrip('s')}">−</button>
              <output data-out="{key}">{val}</output>
              <button type="button" class="guests__btn" data-step="1" data-for="{key}" aria-label="Ajouter un {titre.lower().rstrip('s')}">+</button>
            </div>
            <input type="hidden" name="{key}" value="{val}" data-min="{mini}" data-max="{maxi}">
          </div>"""

    rows = (row("adults", "Adultes", "18 ans et plus", 1, 4, 2)
            + row("children", "Enfants", "De 2 à 17 ans", 0, 4, 0))

    return f"""<form class="{cls}" data-booking data-cal-host aria-label="Rechercher un séjour">
      {cal_fields(uid)}
      {cal_panel()}
      <div class="booking__field booking__field--guests" data-guests>
        <span class="booking__flabel" id="bk-gl-{uid}">Voyageurs</span>
        <button type="button" class="booking__guests-btn" id="bk-gb-{uid}" aria-labelledby="bk-gl-{uid} bk-gb-{uid}"
                aria-expanded="false" aria-haspopup="dialog" data-guests-toggle>
          <span data-guests-label>2 voyageurs</span>
          <svg class="booking__chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div class="guests__panel" role="dialog" aria-labelledby="bk-gl-{uid}" hidden>
          {rows}
          <button type="button" class="guests__close" data-guests-close>Fermer</button>
        </div>
      </div>
      <button class="btn btn--primary booking__submit" type="submit">{cta}</button>
      <p class="booking__note">Réservation sécurisée · confirmation immédiate.</p>
    </form>"""

# ============================================================================
build_pages = __import__("build_pages", fromlist=["*"]) if os.path.exists(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_pages.py")) else None

if __name__ == "__main__":
    import build_pages
    build_pages.run(globals())
    print("\n✅ Site généré dans /site")
