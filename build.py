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

# --- Widget de relecture client (n'apparaît que hors domaine de production) ---
FEEDBACK_EMAIL = "edwin@localisia.fr"      # destinataire des retours
FEEDBACK_WEB3KEY = ""                       # clé Web3Forms (gratuite) -> envoi in-page sans quitter la page ; vide = repli e-mail
PROD_DOMAIN = "lesmeublesdeluchon.com"      # le widget se masque sur ce domaine

NAV = [
    ("/", "Accueil"),
    ("/nos-logements/", "Logements"),
    ("/cure-thermale/", "Cure thermale"),
    ("/services/", "Services"),
    ("/activites/", "Activités"),
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
        "stars": 3,
        "booking": "superhote",
        "short": "Appartement deux pièces rénové, cosy et moderne, au cœur de Luchon.",
        "intro": "La Perle Bleue est un charmant appartement T2 entièrement rénové, à la décoration douce et contemporaine. Avec sa chambre séparée, son salon lumineux et son canapé convertible, il accueille confortablement jusqu'à 4 personnes — idéal pour une famille ou deux couples en séjour thermal ou au ski.",
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
        "stars": 2,
        "booking": "superhote",
        "short": "Studio douillet et lumineux, récemment rénové avec une décoration soignée.",
        "intro": "L'Échappée Verte est un studio cosy récemment rénové, pensé pour deux voyageurs. Sa décoration soignée aux tons naturels, son coin cuisine-repas et son canapé convertible en font un nid parfait pour un séjour en amoureux, une cure thermale ou un week-end à la montagne.",
        "images": [
            ("cuisine.jpg", "Coin cuisine et repas de L'Échappée Verte"),
            ("cuisine-2.jpg", "Espace repas lumineux"),
            ("canape.jpg", "Canapé convertible"),
            ("entree.jpg", "Entrée du studio"),
            ("douche.jpg", "Salle d'eau"),
            ("salle-douche.jpg", "Salle de douche rénovée"),
        ],
        "amenities": ["Canapé convertible", "Coin cuisine équipé", "Machine à café Nespresso",
                      "Salle de douche rénovée", "Lave-linge / sèche-linge", "Wi-Fi haut débit gratuit",
                      "Télévision", "Linge de maison (option)", "Chauffage individuel"],
    },
    "le-refuge-thermal": {
        "slug": "refuge-thermal",
        "name": "Le Refuge Thermal",
        "type": "T2 — 2 pièces",
        "capacity": 4,
        "floor": "Rez-de-chaussée",
        "stars": 2,
        "booking": "contact",
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

CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>')

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
<link rel="stylesheet" href="/assets/css/style.css">
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
      <a class="nav__phone" href="tel:{NAP['tel_link']}" aria-label="Appeler le {NAP['tel_display']}">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.68 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.32 1.85.55 2.81.68A2 2 0 0 1 22 16.92z"/></svg>
        {NAP['tel_display']}
      </a>
      <a class="btn btn--primary" href="/reservation/">Réserver</a>
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
          <li><a href="/nos-logements/">Nos logements</a></li>
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
        <h4>Nos logements</h4>
        <ul class="footer-links">
          <li><a href="/nos-logements/la-perle-bleue/">La Perle Bleue</a></li>
          <li><a href="/nos-logements/l-echappee-verte/">L'Échappée Verte</a></li>
          <li><a href="/nos-logements/le-refuge-thermal/">Le Refuge Thermal</a></li>
          <li><a href="/reservation/">Réserver</a></li>
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
  <a class="btn btn--primary" href="/reservation/">Réserver</a>
</div>
<div class="rvw" id="review" data-email="{FEEDBACK_EMAIL}" data-web3key="{FEEDBACK_WEB3KEY}" data-prod="{PROD_DOMAIN}">
  <button class="rvw__btn" id="rvw-toggle" type="button" aria-expanded="false">💬 Votre avis sur cette page</button>
  <div class="rvw__panel" role="dialog" aria-label="Donner un avis sur cette page">
    <button class="rvw__close" id="rvw-close" type="button" aria-label="Fermer">×</button>
    <h4>Votre avis sur cette page</h4>
    <p class="rvw__page" id="rvw-page"></p>
    <form id="rvw-form" class="rvw__form">
      <label>Votre nom <span>(facultatif)</span><input type="text" name="visitor_name" autocomplete="name"></label>
      <label>Votre remarque<textarea name="message" rows="4" required placeholder="Ce que vous aimez, ce qui manque, une correction…"></textarea></label>
      <button class="btn btn--primary btn--block" type="submit">Envoyer mon retour</button>
    </form>
    <div class="rvw__ok" id="rvw-ok" hidden>✅ Merci ! Votre retour a bien été envoyé.</div>
  </div>
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
<script src="/assets/js/main.js" defer></script>
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
# Widget de réservation réutilisable
def booking_widget(fixed_slug=None, cta="Vérifier les disponibilités", stacked=False):
    cls = "booking booking--stack" if stacked else "booking"
    if fixed_slug:
        lodging_field = f'<input type="hidden" name="lodging" value="{fixed_slug}">'
        data_lodging = f' data-lodging="{fixed_slug}"'
    else:
        data_lodging = ""
        lodging_field = """<div class="booking__field">
        <label for="bk-lodging">Logement</label>
        <select name="lodging" id="bk-lodging">
          <option value="perle-bleue">La Perle Bleue · T2 · 4 pers.</option>
          <option value="echappee-verte">L'Échappée Verte · T1 · 2 pers.</option>
          <option value="refuge-thermal">Le Refuge Thermal · T2 · 4 pers.</option>
        </select>
      </div>"""
    uid = fixed_slug or "w"
    return f"""<form class="{cls}" data-booking{data_lodging} aria-label="Rechercher un séjour">
      {lodging_field}
      <div class="booking__field">
        <label for="bk-in-{uid}">Arrivée</label>
        <input type="date" name="checkin" id="bk-in-{uid}" required>
      </div>
      <div class="booking__field">
        <label for="bk-out-{uid}">Départ</label>
        <input type="date" name="checkout" id="bk-out-{uid}" required>
      </div>
      <div class="booking__field">
        <label for="bk-ad-{uid}">Voyageurs</label>
        <select name="adults" id="bk-ad-{uid}">
          <option value="1">1 adulte</option>
          <option value="2" selected>2 adultes</option>
          <option value="3">3 adultes</option>
          <option value="4">4 adultes</option>
        </select>
      </div>
      <button class="btn btn--primary" type="submit">{cta}</button>
      <p class="booking__note">Réservation sécurisée · confirmation immédiate. Le Refuge Thermal se réserve sur simple demande.</p>
    </form>"""

# ============================================================================
build_pages = __import__("build_pages", fromlist=["*"]) if os.path.exists(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_pages.py")) else None

if __name__ == "__main__":
    import build_pages
    build_pages.run(globals())
    print("\n✅ Site généré dans /site")
