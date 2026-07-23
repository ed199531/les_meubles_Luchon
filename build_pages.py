# -*- coding: utf-8 -*-
import json, os, html as _h
_AVIS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avis-clients.json")
AVIS = json.load(open(_AVIS_PATH, encoding="utf-8"))

AVIS_THEMES = [
    ("proprete",    "Propreté",            ["propre", "proprete", "nickel", "impeccable"]),
    ("emplacement", "Emplacement",         ["emplacement", "centre", "proche", "a pied", "situe", "idealement", "commerce"]),
    ("equipement",  "Équipement", ["equipe", "cuisine", "literie", "lit ", "wifi", "linge", "fonctionnel", "confort"]),
    ("calme",       "Calme",               ["calme", "tranquill", "reposant", "silenc"]),
    ("montagne",    "Ski & montagne",      ["ski", "neige", "piste", "superbagnere", "montagne", "randonn"]),
    ("accueil",     "Accueil",             ["accueil", "nathalie", "hote", "disponib", "sympa", "chaleureu", "contact"]),
    ("cure",        "Cure thermale",       ["cure", "curiste", "therme", "thermal"]),
]


def _sans_accents(t):
    import unicodedata
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def avis_themes(a):
    t = _sans_accents(a["texte"])
    return [cid for cid, _lab, mots in AVIS_THEMES if any(m in t for m in mots)]


# Détection simple de la langue de l'avis (proxy de nationalité)
_MOTS_ES = [" que ", " muy ", " con ", " para ", " apartamento", "estancia", "gracias",
            "limpio", "perfecto", " los ", " las ", " una ", " nos ", "habitacion", " todo ", " bien "]
_MOTS_EN = [" the ", " and ", " very ", " was ", " we ", " apartment", " stay", " clean",
            " perfect", " great", " nice", " would ", " is ", " for ", " with ", " everything "]
_MOTS_FR = [" et ", " le ", " la ", " est ", " tres ", " nous ", " appartement", " avec ", " pour "]


def avis_langue(a):
    t = " " + _sans_accents(a["texte"]) + " "
    es = sum(t.count(w) for w in _MOTS_ES)
    en = sum(t.count(w) for w in _MOTS_EN)
    fr = sum(t.count(w) for w in _MOTS_FR)
    if es >= 2 and es > fr and es >= en:
        return "es"
    if en >= 3 and en > fr and en > es:
        return "en"
    return "fr"


AVIS_LANGUES = [("fr", "Français"), ("es", "Espagnol"), ("en", "Anglais")]


def avis_card(a, filtrable=False):
    d = f' <span class="review__date">— {a["date"]}</span>' if a.get("date") else ""
    attrs = ""
    if filtrable:
        rech = _h.escape(_sans_accents(a["texte"] + " " + a["auteur"]), quote=True)
        attrs = (f' data-themes="{" ".join(avis_themes(a))}" data-nat="{avis_langue(a)}"'
                 f' data-txt="{rech}"')
    return (f'<blockquote class="review reveal"{attrs}><p class="review__text">« '
            + _h.escape(a["texte"], quote=False) + ' »</p><div class="review__author">'
            + _h.escape(a["auteur"], quote=False) + d + '</div></blockquote>')

def pick_avis(keywords, n, used):
    out=[]
    for a in AVIS:
        if a["auteur"] in used: continue
        t=a["texte"].lower()
        if any(k in t for k in keywords) and 60 < len(a["texte"]) < 260:
            out.append(a); used.add(a["auteur"])
        if len(out)>=n: break
    return out

"""Contenus des pages — appelé par build.py"""

def run(g):
    page = g["page"]; breadcrumb = g["breadcrumb"]; booking_widget = g["booking_widget"]
    booking_engine = g["booking_engine"]; booking_search = g["booking_search"]
    cal_fields = g["cal_fields"]; cal_panel = g["cal_panel"]
    EYEBROW = g["HERO_EYEBROW"]; BADGES = g["HERO_BADGES"]
    STEPS_INLINE = (
        '<ol class="steps-inline reveal">'
        '<li><span class="steps-inline__n">1</span><div><strong>Indiquez vos dates</strong>'
        "<span>Les appartements libres s'affichent</span></div></li>"
        '<li><span class="steps-inline__n">2</span><div><strong>Choisissez l\'appartement</strong>'
        '<span>Photos, équipements, tarif</span></div></li>'
        '<li><span class="steps-inline__n">3</span><div><strong>Payez en ligne</strong>'
        '<span>Sécurisé, sans frais cachés</span></div></li>'
        '<li><span class="steps-inline__n">4</span><div><strong>Recevez la confirmation</strong>'
        '<span>Accès autonome dès 16h</span></div></li>'
        '</ol>')
    LOGEMENTS = g["LOGEMENTS"]; NAP = g["NAP"]; stars_html = g["stars_html"]
    jsonld = g["jsonld"]; CHECK = g["CHECK"]; BASE = g["BASE_URL"]; write = g["write"]

    # =====================================================================
    # ACCUEIL
    # =====================================================================
    home_ld_business = {
        "@context": "https://schema.org", "@type": "LodgingBusiness",
        "@id": BASE + "/#business", "name": NAP["name"],
        "description": "Locations saisonnières d'appartements meublés au cœur de Bagnères-de-Luchon, proches des thermes et des pistes de ski.",
        "url": BASE + "/", "logo": BASE + "/assets/img/brand/logo.png",
        "image": BASE + "/assets/img/logements/perle-bleue/salon.jpg",
        "telephone": NAP["tel_link"], "email": NAP["email"], "priceRange": "€€",
        "address": {"@type": "PostalAddress", "streetAddress": NAP["street"],
                    "addressLocality": NAP["city"], "postalCode": NAP["postal"],
                    "addressRegion": NAP["region"], "addressCountry": "FR"},
        "geo": {"@type": "GeoCoordinates", "latitude": 42.7906, "longitude": 0.5936},
        "areaServed": NAP["city"],
        "sameAs": [NAP["facebook"], NAP["instagram"]],
    }
    home_ld_faq = {
        "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": "Où sont situés Les Meublés de Luchon ?",
             "acceptedAnswer": {"@type": "Answer", "text": "Nos appartements se trouvent 5 rue Azémar, au centre de Bagnères-de-Luchon (31110), en Occitanie, à quelques minutes à pied des thermes, des commerces et de la télécabine de Superbagnères."}},
            {"@type": "Question", "name": "Comment réserver un appartement ?",
             "acceptedAnswer": {"@type": "Answer", "text": "La réservation se fait en ligne : choisissez votre appartement, vos dates et le nombre de voyageurs, puis validez le paiement sécurisé. Vous recevez une confirmation immédiate par e-mail."}},
            {"@type": "Question", "name": "Les animaux sont-ils acceptés ?",
             "acceptedAnswer": {"@type": "Answer", "text": "Oui, les animaux sont les bienvenus moyennant un supplément de 50 € par séjour et par animal."}},
            {"@type": "Question", "name": "À quelle heure se fait l'arrivée ?",
             "acceptedAnswer": {"@type": "Answer", "text": "L'arrivée est flexible à partir de 16h grâce à une boîte à clés autonome. Le départ se fait avant 10h."}},
        ]}

    _used=set()
    _home_sel = pick_avis(["propre","équipé","situé","recommande","parfait"],12,_used)
    avis_home = "".join(avis_card(a) for a in _home_sel) * 2

    home = f"""
<section class="hero">
  <div class="hero__media">
    <img src="/assets/img/activites/randonnee.jpg" alt="Vue sur les montagnes des Pyrénées à Bagnères-de-Luchon" width="1400" height="930" fetchpriority="high">
  </div>
  <div class="container hero__inner">
    <p class="eyebrow" style="color:#a9e0e4">Locations saisonnières · Bagnères-de-Luchon</p>
    <h1>Vos appartements au cœur de Bagnères-de-Luchon, à deux pas des Thermes et de Superbagnères</h1>
    <p class="hero__sub">3 appartements confortables, parfaitement équipés, pour vos séjours à la montagne et escapades dans les Pyrénées ou vos cures thermales.</p>
    <div class="hero__badges">
      <span>⭐ Classés Meublé de Tourisme</span>
      <span>💬 Des voyageurs satisfaits depuis 2018</span>
      <span>📍 Centre-ville</span>
      <span>🐾 Animaux bienvenus</span>
    </div>
    <div style="margin-top:2rem">{booking_widget()}</div>
  </div>
</section>

<section class="section">
  <div class="container center reveal">
    <p class="eyebrow">Bienvenue</p>
    <h2>Le confort d'un appartement, l'esprit d'une station thermale</h2>
    <p class="lead">Les Meublés de Luchon, ce sont trois appartements meublés indépendants au centre de Bagnères-de-Luchon, tenus par Nathalie, votre hôte passionnée par sa région. Idéal pour un week-end au ski, des vacances nature en famille ou une <a href="/cure-thermale/">cure thermale</a> (tarif spécial sur demande).</p>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2.5rem">
      <p class="eyebrow">Nos appartements</p>
      <h2>Trois appartements chaleureux et confortables</h2>
    </div>
    <div class="grid grid--3">
      {logement_card(g, "la-perle-bleue")}
      {logement_card(g, "l-echappee-verte")}
      {logement_card(g, "le-refuge-thermal")}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2rem">
      <p class="eyebrow">Pourquoi nous choisir</p>
      <h2>Tout pensé pour un séjour sans souci</h2>
    </div>
    <div class="grid grid--3">
      <div class="feature reveal"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div><h3>Emplacement idéal</h3><p>À quelques pas des thermes, des commerces, du casino et de la télécabine de Superbagnères.</p></div>
      <div class="feature reveal"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></div><h3>Confort et équipement</h3><p>Appartements équipés avec soin, literie de qualité, cuisine équipée, lave-linge, Wi-Fi haut débit et Nespresso.</p></div>
      <div class="feature reveal"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></div><h3>Activités toute l'année</h3><p>Ski en hiver, thermalisme, randonnées, rafting, parapente… un accueil sur-mesure et nos bons plans.</p></div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container split">
    <div class="split__media reveal"><img src="/assets/img/brand/nathalie.jpg" alt="Nathalie, votre hôte aux Meublés de Luchon" loading="lazy" width="600" height="480"></div>
    <div class="split__body reveal">
      <p class="eyebrow">Votre hôte</p>
      <h2>Bienvenue à Luchon !</h2>
      <p>Je suis Nathalie et je serai heureuse de vous accueillir dans l'un de nos trois appartements. Je connais Luchon depuis de nombreuses années et je serai ravie de vous conseiller selon vos envies : cure thermale, randonnée, ski, vélo ou simplement quelques jours pour profiter de la montagne.</p>
      <a class="btn btn--primary" href="/services/">Découvrir nos services</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2.5rem">
      <p class="eyebrow">À faire à Luchon</p>
      <h2>Une destination quatre saisons</h2>
      <p class="lead">De la neige de Superbagnères aux eaux thermales, en passant par les sentiers du lac d'Oô, Luchon se vit toute l'année.</p>
    </div>
    <div class="grid grid--4">
      <a class="card reveal" href="/activites/#ski"><div class="card__media"><img src="/assets/img/activites/ski.jpg" alt="Ski à Luchon-Superbagnères" loading="lazy" width="400" height="300"></div><div class="card__body"><h3>Ski &amp; montagne</h3></div></a>
      <a class="card reveal" href="/activites/#thermalisme"><div class="card__media"><img src="/assets/img/activites/thermes.jpg" alt="Thermes de Luchon" loading="lazy" width="400" height="300"></div><div class="card__body"><h3>Thermes &amp; bien-être</h3></div></a>
      <a class="card reveal" href="/activites/#randonnee"><div class="card__media"><img src="/assets/img/activites/randonnee.jpg" alt="Randonnée dans les Pyrénées" loading="lazy" width="400" height="300"></div><div class="card__body"><h3>Randonnée &amp; nature</h3></div></a>
      <a class="card reveal" href="/activites/#eaux-vives"><div class="card__media"><img src="/assets/img/activites/rafting.jpg" alt="Rafting en eaux vives" loading="lazy" width="400" height="300"></div><div class="card__body"><h3>Sports en eaux vives</h3></div></a>
    </div>
    <div class="center" style="margin-top:2rem"><a class="btn btn--ghost" href="/activites/">Voir toutes les activités</a></div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2rem">
      <p class="eyebrow">Ils ont séjourné chez nous</p>
      <h2>Des voyageurs conquis</h2>
      <div class="rating-banner" style="margin-top:1rem">La confiance de nos voyageurs, saison après saison — depuis 2018</div>
    </div>
    <div class="avis-marquee"><div class="avis-marquee__track">{avis_home}</div></div>
    <div class="center" style="margin-top:2rem"><a class="btn btn--ghost" href="/avis/">Lire tous les avis</a></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split" style="align-items:start">
      <div class="split__body reveal">
        <p class="eyebrow">Simple et rapide</p>
        <h2>Réservez en 4 étapes</h2>
        <div class="steps" style="margin-top:1.5rem">
          <div class="step"><div class="step__num"></div><div><h3>Choisissez votre appartement</h3><p>Parcourez nos trois logements et trouvez celui qui vous ressemble.</p></div></div>
          <div class="step"><div class="step__num"></div><div><h3>Sélectionnez vos dates</h3><p>Vérifiez la disponibilité en temps réel selon votre période.</p></div></div>
          <div class="step"><div class="step__num"></div><div><h3>Confirmez et payez</h3><p>Paiement sécurisé en ligne, sans frais cachés.</p></div></div>
          <div class="step"><div class="step__num"></div><div><h3>Recevez votre confirmation</h3><p>Toutes les infos d'arrivée par e-mail, avec accès autonome dès 16h.</p></div></div>
        </div>
        <a class="btn btn--primary btn--lg" href="/appartements/" style="margin-top:1.5rem">Réserver</a>
      </div>
      <div class="split__media reveal">{diapo(g, [
        ("perle-bleue", "salon.jpg", "Salon de La Perle Bleue"),
        ("refuge-thermal", "piece-de-vie.jpg", "Pièce de vie du Refuge Thermal"),
        ("echappee-verte", "canape.jpg", "Coin salon de L'Échappée Verte"),
        ("perle-bleue", "chambre.jpg", "Chambre de La Perle Bleue"),
        ("refuge-thermal", "sejour.jpg", "Séjour du Refuge Thermal"),
        ("echappee-verte", "cuisine.jpg", "Cuisine équipée de L'Échappée Verte"),
        ("perle-bleue", "cuisine.jpg", "Cuisine de La Perle Bleue"),
        ("refuge-thermal", "chambre.jpg", "Chambre du Refuge Thermal"),
      ], interval=2200)}</div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container center">
    <p class="eyebrow">Ils nous font confiance</p>
    <h2 style="margin-bottom:2rem">Nos partenaires touristiques</h2>
    <div class="partners reveal">
      <img src="/assets/img/partners/pyrenees-31.png" alt="Pyrénées 31" loading="lazy" height="64">
      <img src="/assets/img/partners/haute-garonne.png" alt="Haute-Garonne Tourisme" loading="lazy" height="64">
      <img src="/assets/img/partners/occitanie.jpg" alt="Région Occitanie Pyrénées-Méditerranée" loading="lazy" height="64">
    </div>
  </div>
</section>

<section class="section">
  <div class="container"><div class="cta-band reveal">
    <h2>Prêt à poser vos valises à Luchon ?</h2>
    <p>Réservez dès maintenant votre appartement et vivez les Pyrénées comme à la maison.</p>
    <a class="btn btn--primary btn--lg" href="/appartements/">Réserver</a>
  </div>
  <p class="cta-band__more">Une question avant de réserver ? <a href="/faq/">Consultez notre foire aux questions</a></p>
</div>
</section>
"""
    page("index.html", "/", "Les Meublés de Luchon — Appartements meublés à Bagnères-de-Luchon",
         "Locations saisonnières au cœur de Bagnères-de-Luchon : appartements meublés, classés Meublé de Tourisme, proches des thermes et des pistes. Réservez en ligne.",
         home, ld_blocks=[home_ld_business, home_ld_faq])

    # =====================================================================
    # NOS LOGEMENTS (catégorie)
    # =====================================================================
    cards = "".join(logement_card(g, slug, reveal=True) for slug in LOGEMENTS)
    itemlist = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": BASE + "/appartements/" + slug + "/",
         "name": LOGEMENTS[slug]["name"]} for i, slug in enumerate(LOGEMENTS)]}
    nl = f"""
<section class="page-hero has-img"><div class="page-hero__img"><img src="/assets/img/logements/perle-bleue/salon.jpg" alt="Intérieur d'un appartement des Meublés de Luchon" width="1400" height="500"></div>
  <div class="container">{EYEBROW}<h1>Nos appartements à Bagnères-de-Luchon</h1><p>Trois appartements meublés, classés Meublé de Tourisme, au centre de la station thermale.</p>{BADGES}</div>
</section>
{breadcrumb([("Accueil", "/"), ("Nos appartements", None)])}
<section class="section" id="reserver">
  <div class="container">
    <div class="center reveal" style="margin-bottom:1.4rem">
      <p class="eyebrow">Disponibilités en direct</p>
      <h2>Rechercher un appartement disponible</h2>
    </div>
    {STEPS_INLINE}
    {booking_search()}
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2.5rem">
      <p class="eyebrow">En détail</p>
      <h2>Nos trois appartements</h2>
      <p class="lead">Photos, équipements et descriptif complet de chaque appartement.</p>
    </div>
    <div class="grid grid--3">{cards}</div>
  </div>
</section>
<section class="section section--tint"><div class="container center"><div class="cta-band reveal"><h2>Une question sur nos appartements ?</h2><p>Nathalie vous répond avec plaisir pour vous aider à choisir l'appartement idéal.</p><a class="btn btn--dark btn--lg" href="/contact/">Nous contacter</a></div>
  <p class="cta-band__more">Une question avant de réserver ? <a href="/faq/">Consultez notre foire aux questions</a></p>
</div></section>
"""
    page("appartements/index.html", "/appartements/", "Nos appartements meublés à Bagnères-de-Luchon | Les Meublés de Luchon",
         "Découvrez nos trois appartements meublés à Bagnères-de-Luchon : La Perle Bleue (T2), L'Échappée Verte (studio) et Le Refuge Thermal (T2, plain-pied). Classés Meublé de Tourisme.",
         nl, ld_blocks=[itemlist])

    # =====================================================================
    # PAGES LOGEMENT (détail)
    # =====================================================================
    for slug, d in LOGEMENTS.items():
        base_img = f"/assets/img/logements/{d['slug']}/"
        # galerie
        gitems = ""
        # galerie allégée : le moteur Superhôte réaffiche les photos plus bas
        for i, (fn, alt) in enumerate(d["images"][:4]):
            src = base_img + fn if not fn.startswith("..") else "/assets/img/logements/" + fn.replace("../", "")
            wide = " gallery__item--wide" if i == 0 else ""
            gitems += (f'<figure class="gallery__item{wide}"><img src="{src}" data-full="{src}" '
                       f'alt="{alt}" loading="lazy" width="600" height="600"></figure>')
        amen = "".join(f'<li>{CHECK}<span>{a}</span></li>' for a in d["amenities"])
        og = (base_img + d["images"][0][0]) if not d["images"][0][0].startswith("..") else "/assets/img/logements/perle-bleue/salon.jpg"

        ld_acc = {"@context": "https://schema.org", "@type": "Apartment",
                  "name": d["name"], "description": d["intro"],
                  "occupancy": {"@type": "QuantitativeValue", "maxValue": d["capacity"], "unitText": "personnes"},
                  "numberOfRooms": 2 if "T2" in d["type"] else 1,
                  "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": a, "value": True} for a in d["amenities"]],
                  "address": {"@type": "PostalAddress", "streetAddress": d["adresse"], "addressLocality": NAP["city"],
                              "postalCode": NAP["postal"], "addressCountry": "FR"},
                  "image": BASE + og}
        body = f"""
<section class="page-hero has-img"><div class="page-hero__img"><img src="{og}" alt="{d['name']} — {d['type']}" width="1400" height="500"></div>
  <div class="container"><p class="eyebrow" style="color:#a9e0e4">{d['tagline']}</p><h1>{d['name']}</h1><p>{d['type'].split('—')[0].strip()} · Jusqu'à {d['capacity']} personnes · {d['floor']}</p>{BADGES}</div>
</section>
{breadcrumb([("Accueil", "/"), ("Nos appartements", "/appartements/"), (d['name'], None)])}
<section class="section" id="reserver">
  <div class="container">
    <div class="center reveal" style="margin-bottom:1.4rem">
      <p class="eyebrow">Disponibilités en direct</p>
      <h2>Réserver {d['name']}</h2>
    </div>
    {STEPS_INLINE}
    {booking_engine(d["slug"])}
  </div>
</section>
<section class="section section--tint">
  <div class="container" style="max-width:900px">
    <div class="reveal">
      <h2>À propos de {d['name']}</h2>
      <p>{d['intro']}</p>
      <div class="card__meta" style="font-size:1rem;margin:1.2rem 0"><span>🛏️ {d['type']}</span><span>👥 {d['capacity']} personnes</span><span>🏢 {d['floor']}</span><span>📍 {d['adresse']}</span><span>{stars_html(d['stars'])} Meublé de Tourisme</span></div>
      <h3 style="margin-top:1.5rem">Équipements &amp; services</h3>
      <ul class="amenities">{amen}</ul>
      <p style="margin-top:1.6rem;font-size:.95rem">Une question avant de réserver ? <a href="tel:{NAP['tel_link']}">📞 {NAP['tel_display']}</a> · <a href="mailto:{NAP['email']}">✉️ Écrire</a></p>
    </div>
  </div>
</section>
<section class="section section--tint"><div class="container center"><div class="cta-band reveal"><h2>Envie de découvrir nos autres appartements ?</h2><p>Comparez nos trois logements et trouvez celui qui vous ressemble.</p><a class="btn btn--primary btn--lg" href="/appartements/">Voir tous les logements</a></div>
  <p class="cta-band__more">Une question avant de réserver ? <a href="/faq/">Consultez notre foire aux questions</a></p>
</div></section>
"""
        page(f"appartements/{slug}/index.html", "/appartements/",
             f"{d['name']} — {d['type']} à Bagnères-de-Luchon | Les Meublés de Luchon",
             f"{d['name']} : {d['short']} {d['type']}, jusqu'à {d['capacity']} personnes, {d['floor']}. Classé {d['stars']}★ Meublé de Tourisme. Réservez en ligne.",
             body, og_image=og, ld_blocks=[ld_acc])

    # =====================================================================
    # SERVICES
    # =====================================================================
    svc_ld = {"@context": "https://schema.org", "@type": "Service",
              "name": "Services aux voyageurs — Les Meublés de Luchon",
              "provider": {"@type": "LodgingBusiness", "name": NAP["name"]},
              "areaServed": NAP["city"],
              "description": "Livret d'accueil, arrivée autonome dès 16h, ménage, location de linge, Wi-Fi et conseils personnalisés."}
    services = f"""
<section class="page-hero"><div class="container">{EYEBROW}<h1>Nos services</h1><p>Tout est pensé pour que votre séjour à Luchon soit simple, confortable et sans surprise.</p>{BADGES}</div></section>
{breadcrumb([("Accueil", "/"), ("Services", None)])}

<section class="section">
  <div class="container split">
    <div class="split__media reveal"><img src="/assets/img/brand/nathalie.jpg" alt="Nathalie, votre hôte" loading="lazy" width="600" height="480"></div>
    <div class="split__body reveal">
      <p class="eyebrow">Votre hôte</p>
      <h2>Nathalie, à votre écoute</h2>
      <p>Je suis Nathalie, passionnée par notre région et soucieuse de vous offrir un séjour inoubliable à Bagnères-de-Luchon. Accueillir des voyageurs du monde entier est pour moi un véritable plaisir et je mets tout en œuvre pour que vous vous sentiez comme chez vous.</p>
      <p>Que ce soit pour vous conseiller sur les meilleures activités locales, pour découvrir les environs ou répondre à vos besoins, je suis toujours à votre écoute. Votre confort et votre satisfaction sont ma priorité : je m'engage à rendre votre séjour aussi agréable que possible.</p>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2.5rem"><p class="eyebrow">Compris dans votre séjour</p><h2>Appartements équipés avec soin</h2><p class="lead">Ces prestations sont incluses, sans supplément.</p></div>
    <div class="grid grid--2">
      <div class="card reveal"><div class="card__body"><h3>Le ménage</h3><p>Notre équipe de ménage assure un ménage rigoureux et soigné après chaque séjour. Nous mettons tout en œuvre pour vous accueillir dans un appartement d'une propreté irréprochable.</p></div></div>
      <div class="card reveal"><div class="card__body"><h3>Votre arrivée</h3><p>Vous êtes libre d'arriver <strong>à partir de 16h</strong>, à l'heure qui vous convient le mieux. Les clefs sont disponibles dans un coffre à clefs : vous recevez le code et toutes les instructions par e-mail avant votre venue.</p></div></div>
      <div class="card reveal"><div class="card__body"><h3>Le stationnement</h3><p>Des parkings gratuits proches du logement sont disponibles. Le temps de décharger vos bagages, vous pouvez vous garer dans l'impasse pour plus de simplicité.</p></div></div>
      <div class="card reveal"><div class="card__body"><h3>Le café</h3><p>Vous appréciez un bon café ? Nous mettons à votre disposition, au choix : une <strong>cafetière filtre</strong> ou une <strong>machine Nespresso</strong>.</p></div></div>
      <div class="card reveal"><div class="card__body"><h3>Le Wi-Fi</h3><p>Une connexion Wi-Fi haut débit gratuite dans chaque appartement, idéale pour rester connecté ou télétravailler.</p></div></div>
      <div class="card reveal"><div class="card__body"><h3>Nos conseils</h3><p>Un livret d'accueil avant votre séjour, et les bons plans de Nathalie sur les activités, les restaurants et les excursions.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2.5rem"><p class="eyebrow">Prestations en supplément</p><h2>À ajouter si vous le souhaitez</h2></div>
    <div class="grid grid--3">
      <div class="card reveal"><div class="card__media card__media--portrait"><img src="/assets/img/services/draps.jpg" alt="Draps de lit fournis" loading="lazy" width="400" height="300"></div><div class="card__body"><h3>Draps de lit</h3><p>Linge de lit propre, mis à disposition pour l'ensemble du séjour.</p><div class="card__foot"><span class="card__price">20 €<small>par lit</small></span></div></div></div>
      <div class="card reveal"><div class="card__media card__media--portrait"><img src="/assets/img/services/draps.jpg" alt="Serviettes de bain fournies" loading="lazy" width="400" height="300"></div><div class="card__body"><h3>Serviettes de bain</h3><p>Un jeu de deux serviettes par personne, pour l'ensemble du séjour.</p><div class="card__foot"><span class="card__price">10 €<small>par personne</small></span></div></div></div>
      <div class="card reveal"><div class="card__media card__media--portrait"><img src="/assets/img/services/animal.jpg" alt="Animal de compagnie accepté" loading="lazy" width="400" height="300"></div><div class="card__body"><h3>Animal de compagnie</h3><p>Votre animal est le bienvenu. Un lien de paiement vous sera envoyé.</p><div class="card__foot"><span class="card__price">50 €<small>par séjour</small></span></div></div></div>
    </div>
    <div class="reveal" style="max-width:760px;margin:2rem auto 0;text-align:center">
      <p><strong>Comment en profiter ?</strong> Si vous souhaitez ajouter l'une ou l'autre de ces options, merci de nous le faire savoir <a href="/contact/">au moment de la réservation</a> afin que tout soit prêt pour votre arrivée.</p>
    </div>
  </div>
</section>

{faq_section(g, [
    ("Le ménage est-il inclus ?", "Oui. Notre équipe assure un ménage rigoureux après chaque séjour : ce n'est pas une option, c'est compris dans votre réservation."),
    ("Fournissez-vous les draps et serviettes ?", "Vous pouvez apporter votre linge ou le louer : 20 € par lit pour les draps, 10 € par personne pour les serviettes, pour l'ensemble du séjour. Signalez-le nous à la réservation."),
    ("Puis-je venir avec mon animal ?", "Oui, votre animal est le bienvenu moyennant 50 € pour l'ensemble du séjour. Un lien de paiement vous sera envoyé."),
    ("Comment se passe l'arrivée ?", "L'arrivée est libre à partir de 16h grâce à un coffre à clefs. Vous recevez le code et toutes les instructions par e-mail avant votre venue."),
    ("Où puis-je me garer ?", "Des parkings gratuits sont disponibles à proximité. Le temps de décharger vos bagages, vous pouvez vous garer dans l'impasse."),
])}

<section class="section section--tint"><div class="container"><div class="cta-band reveal">
  <h2>Prêt à réserver votre séjour ?</h2>
  <p>Choisissez votre appartement et vos dates : réservation en ligne, confirmation immédiate.</p>
  <a class="btn btn--primary btn--lg" href="/appartements/">Réserver</a>
</div>
  <p class="cta-band__more">Une question avant de réserver ? <a href="/faq/">Consultez notre foire aux questions</a></p>
</div></section>
"""
    page("services/index.html", "/services/", "Nos services — accueil, ménage, linge, Wi-Fi | Les Meublés de Luchon",
         "Services des Meublés de Luchon : ménage inclus, arrivée libre dès 16h avec coffre à clefs, parking gratuit, Wi-Fi. En option : draps 20 €/lit, serviettes 10 €/pers., animal 50 €.",
         services, og_image="/assets/img/services/wifi.jpg", ld_blocks=[svc_ld])

    # =====================================================================
    # ACTIVITÉS
    # =====================================================================
    # Secteurs repris de la logique de l'office de tourisme (Pyrénées 31).
    SECTEURS = [
        ("luchon", "Luchon"),
        ("superbagneres", "Luchon-Superbagnères"),
        ("autour", "Autour de Luchon"),
        ("peyragudes", "Peyragudes"),
        ("mourtis", "Le Mourtis"),
        ("vallees", "Vallées voisines"),
    ]
    CATEGORIES = [
        ("hiver", "❄️", "Sports d'hiver"),
        ("thermes", "♨️", "Thermes & bien-être"),
        ("rando", "🥾", "Randonnée & nature"),
        ("eau", "🌊", "Sports en eaux vives"),
        ("air", "🪂", "Sports aériens"),
        ("velo", "🚴", "Vélo & cyclisme"),
        ("golf", "⛳", "Golf"),
        ("patrimoine", "🏛️", "Patrimoine & culture"),
        ("fetes", "🎉", "Fêtes & évènements"),
    ]
    # img = photo dédiée quand nous en avons une ; sinon bandeau catégorie.
    # "pied" = accessible à pied depuis nos appartements (centre de Luchon).
    ACTIVITES = [
        ("Les Thermes de Luchon", "luchon", "thermes", "thermes-luchon.jpg", True, "toutes",
         "L'établissement thermal et son <strong>vaporarium</strong>, une grotte de vapeur naturelle unique en Europe. Cures conventionnées, soins à la journée et espace détente, ouverts toute l'année."),
        ("Les allées d'Étigny", "luchon", "patrimoine", "allees-etigny.jpg", True, "toutes",
         "La grande promenade bordée de tilleuls qui mène du centre-ville aux thermes, avec ses façades Belle Époque, ses terrasses et ses boutiques. Le cœur battant de la station."),
        ("La télécabine de Superbagnères", "luchon", "hiver", "telecabine-superbagneres.jpg", True, "toutes",
         "Elle relie directement Luchon au plateau de Superbagnères. Skieurs l'hiver, promeneurs et vététistes l'été : en quelques minutes, vous passez de la ville au panorama sur la chaîne des Pyrénées."),
        ("Le golf de Luchon", "luchon", "golf", "golf.jpg", False, "ete",
         "Un parcours de montagne au charme ancien, dessiné entre forêts et sommets. L'un des plus anciens golfs des Pyrénées, à l'écart de l'agitation."),
        ("La Fête des Fleurs", "luchon", "fetes", "fete-des-fleurs.jpg", True, "ete",
         "Le grand rendez-vous de l'été luchonnais : corso fleuri, chars décorés et fanfares envahissent les allées d'Étigny. Une tradition qui remplit la ville — pensez à réserver tôt."),
        ("Le ski à Superbagnères", "superbagneres", "hiver", "ski.jpg", False, "hiver",
         "Le « balcon des Pyrénées » et son panorama à 360° sur la chaîne frontalière. Un domaine familial où l'on skie face aux sommets, accessible depuis Luchon sans reprendre la voiture."),
        ("Luge, raquettes et ski de fond", "superbagneres", "hiver", "luge-raquettes-fond.jpg", False, "hiver",
         "Au-delà des pistes : espaces débutants, sentiers raquettes et itinéraires de fond sur le plateau. De quoi occuper une journée de neige même sans chausser les skis alpins."),
        ("Le parapente au-dessus de la vallée", "superbagneres", "air", "parapente.jpg", False, "ete",
         "Le décollage depuis le plateau offre l'une des plus belles vues du massif : la vallée d'une part, les sommets frontaliers de l'autre. Baptêmes encadrés par des moniteurs locaux."),
        ("Les cols du Tour de France", "superbagneres", "velo", "cols-tour-de-france.jpg", False, "ete",
         "Superbagnères et le col de Peyresourde comptent parmi les ascensions mythiques de la Grande Boucle. Les cyclistes viennent de loin pour les gravir — et le départ se fait depuis Luchon."),
        ("Le lac d'Oô", "autour", "rando", "randonnee.jpg", False, "ete",
         "La randonnée emblématique du Luchonnais : un lac d'altitude alimenté par une cascade de plusieurs dizaines de mètres. Accessible en famille depuis les Granges d'Astau, spectaculaire à l'arrivée."),
        ("La vallée du Lys et la cascade d'Enfer", "autour", "rando", "vallee-du-lys.jpg", False, "ete",
         "Une vallée boisée toute proche, ses cascades et son gouffre. Balades courtes et ombragées, idéales pour une demi-journée ou une sortie avec des enfants."),
        ("L'Hospice de France", "autour", "rando", "hospice-de-france.jpg", False, "ete",
         "Ancien refuge sur la route des cols vers l'Espagne, dans un cirque de montagne au bout de la vallée de la Pique. Point de départ de nombreux sentiers, but de promenade en soi."),
        ("Le port de Vénasque", "autour", "rando", "port-de-venasque.jpg", False, "ete",
         "Une montée exigeante jusqu'à une brèche frontalière, récompensée par la vue sur le massif de la Maladeta et l'Aneto, plus haut sommet des Pyrénées. Pour marcheurs entraînés."),
        ("Rafting et canyoning", "autour", "eau", "rafting.jpg", False, "ete",
         "Les eaux vives de la Pique et de la Garonne se descendent en raft, en kayak ou en canyoning, encadrées par des professionnels. Le grand classique des journées d'été."),
        ("Le VTT de descente", "autour", "velo", "vtt-descente.jpg", False, "ete",
         "Les pentes du Luchonnais se prêtent à la descente comme au cross-country, avec des itinéraires balisés et des remontées ouvertes l'été pour éviter la montée."),
        ("Le ski à Peyragudes", "peyragudes", "hiver", "peyragudes.jpg", False, "hiver",
         "Un domaine plus vaste, à cheval sur deux versants, connu pour son altiport et ses pistes larges. À moins d'une heure de route pour varier les plaisirs."),
        ("Le lac de Loudenvielle et Balnéa", "peyragudes", "thermes", "loudenvielle-balnea.jpg", False, "toutes",
         "Un lac de montagne avec promenade aménagée, et le centre de bien-être Balnéa et ses bains inspirés de différentes cultures thermales. La sortie détente par temps incertain."),
        ("Le ski au Mourtis", "mourtis", "hiver", "le-mourtis.jpg", False, "hiver",
         "Une petite station familiale où l'on skie entre les sapins, réputée pour son ambiance tranquille et ses tarifs doux. Parfait pour débuter ou pour une première glisse avec des enfants."),
        ("La vallée d'Oueil", "vallees", "rando", "vallee-oueil.jpg", False, "toutes",
         "Une vallée pastorale préservée, ses hameaux de pierre et ses granges. On y vient pour le calme, les chemins de crête et les villages restés à l'écart du tourisme."),
        ("Saint-Bertrand-de-Comminges", "vallees", "patrimoine", "saint-bertrand-de-comminges.jpg", False, "toutes",
         "L'un des plus beaux villages de France, dominé par sa cathédrale et bâti sur un site romain. Une demi-journée de visite qui change complètement de la montagne."),
        ("Saint-Béat, cité du marbre", "vallees", "patrimoine", "saint-beat.jpg", False, "toutes",
         "Le marbre extrait ici a servi jusqu'à Versailles. Le village, ses carrières et ses ruelles étroites au bord de la Garonne se découvrent en une matinée."),
    ]
    CAT_MAP = {cid: (emo, lab) for cid, emo, lab in CATEGORIES}
    SEC_MAP = dict(SECTEURS)

    SAISON_LAB = {"ete": "Été", "hiver": "Hiver", "toutes": "Toutes saisons"}
    acards = ""
    for titre, sec, cat, img, pied, saison, desc in ACTIVITES:
        emo, clab = CAT_MAP[cat]
        if img:
            media = (f'<div class="card__media"><img src="/assets/img/activites/{img}" alt="{titre} — Bagnères-de-Luchon" '
                     f'loading="lazy" width="500" height="375"></div>')
        else:
            media = f'<div class="card__media card__media--cat"><span>{clab}</span></div>'
        MARCHE = {
            "Les Thermes de Luchon": "5 min à pied",
            "Les allées d'Étigny": "2 min à pied",
            "La télécabine de Superbagnères": "8 min à pied",
            "La Fête des Fleurs": "2 min à pied",
        }
        acces = (f'<p class="act__acces">À {MARCHE[titre]} depuis nos appartements</p>'
                 if pied and titre in MARCHE else
                 ('<p class="act__acces">À pied depuis nos appartements</p>' if pied else ''))
        pied_attr = ' data-pied="1"' if pied else ''
        acards += (f'<article class="card act reveal" data-sec="{sec}" data-cat="{cat}" data-saison="{saison}"{pied_attr}>{media}'
                   f'<div class="card__body"><p class="act__tags"><span class="act__tag">{clab}</span>'
                   f'<span class="act__tag act__tag--sec">{SEC_MAP[sec]}</span>'
                   f'<span class="act__tag act__tag--saison">{SAISON_LAB[saison]}</span></p>'
                   f'<h3>{titre}</h3><p>{desc}</p>{acces}</div></article>')

    def _select(name, label, tout, items, extra=None):
        opts = f'<option value="all">{tout}</option>'
        for val, lab in (extra or []):
            opts += f'<option value="{val}">{lab}</option>'
        for it in items:
            key, lab = (it[0], it[2]) if len(it) == 3 else it
            opts += f'<option value="{key}">{lab}</option>'
        return (f'<div class="filtres__champ">'
                f'<label class="filtres__label" for="f-{name}">{label}</label>'
                f'<select id="f-{name}" class="filtres__select" data-filtre="{name}">{opts}</select>'
                f'</div>')

    activites = f"""
<section class="page-hero has-img"><div class="page-hero__img"><img src="/assets/img/activites/randonnee.jpg" alt="Montagnes des Pyrénées à Luchon" width="1400" height="500"></div>
  <div class="container">{EYEBROW}<h1>Activités à Bagnères-de-Luchon</h1><p>Amateur de sensations, de culture ou de détente : Luchon et ses environs offrent une multitude d'activités en toutes saisons.</p>{BADGES}</div>
</section>
{breadcrumb([("Accueil", "/"), ("Activités", None)])}
<section class="section">
  <div class="container">
    <div class="filtres reveal" data-filtres>
      {_select("sec", "Secteur", "Tous les secteurs", SECTEURS, extra=[("pied", "À pied depuis nos appartements")])}
      {_select("cat", "Type d'activité", "Toutes les activités", CATEGORIES)}
      {_select("saison", "Saison", "Toutes saisons", [("ete", "Été"), ("hiver", "Hiver")])}
      <button type="button" class="filtres__reset" data-filtres-reset hidden>Réinitialiser</button>
    </div>
    <div class="grid grid--3" data-filtres-grid>{acards}</div>
    <p class="filtres__vide" data-filtres-vide hidden>Aucune activité ne correspond à ces filtres.</p>
    <div class="reveal" style="max-width:760px;margin:2.5rem auto 0;text-align:center">
      <p>Cette sélection rassemble les incontournables du Luchonnais. Pour l'agenda complet, les horaires et les tarifs à jour, consultez l'<a href="https://www.pyrenees31.com/preparer/activites" target="_blank" rel="noopener">Office de Tourisme Pyrénées 31</a>, qui recense toutes les activités du territoire.</p>
    </div>
  </div>
</section>
<section class="section section--tint"><div class="container center"><div class="cta-band reveal"><h2>Réservez votre séjour à Luchon</h2><p>Posez vos valises dans l'un de nos appartements et partez explorer les Pyrénées.</p><a class="btn btn--primary btn--lg" href="/appartements/">Réserver</a></div>
  <p class="cta-band__more">Une question avant de réserver ? <a href="/faq/">Consultez notre foire aux questions</a></p>
</div></section>
"""
    page("activites/index.html", "/activites/", "Activités à Bagnères-de-Luchon : ski, thermes, randonnée | Les Meublés de Luchon",
         "Que faire à Bagnères-de-Luchon ? Ski à Superbagnères, thermes et bien-être, randonnées au lac d'Oô, rafting, parapente, golf et Fête des Fleurs. Toutes les activités près de nos logements.",
         activites, og_image="/assets/img/activites/ski.jpg")

    # =====================================================================
    # AVIS
    # =====================================================================
    rcards = "".join(avis_card(a, filtrable=True) for a in AVIS)
    _star = ('<svg class="chip__star" viewBox="0 0 24 24" fill="currentColor" width="14" height="14" aria-hidden="true">'
             '<path d="M12 2l3 6.5 7 .8-5.2 4.8 1.4 7L12 17.8 5.4 21l1.4-7L1.6 9.3l7-.8z"/></svg>')
    _counts = {cid: sum(cid in avis_themes(a) for a in AVIS) for cid, _l, _m in AVIS_THEMES}
    chips = f'<button type="button" class="chip is-on" data-avis-cat="all">Tous</button>'
    chips += "".join(
        f'<button type="button" class="chip" data-avis-cat="{cid}">{_star}{lab} '
        f'<span class="chip__n">{_counts[cid]}</span></button>'
        for cid, lab, _m in AVIS_THEMES if _counts[cid] > 0)
    _nat_counts = {code: sum(avis_langue(a) == code for a in AVIS) for code, _l in AVIS_LANGUES}
    nat_opts = "".join(f'<option value="{code}">{lab}</option>'
                       for code, lab in AVIS_LANGUES if _nat_counts[code] > 0)
    avis = f"""
<section class="page-hero"><div class="container">{EYEBROW}<h1>Vos avis</h1><p>Ce que nos voyageurs retiennent de leur séjour : des témoignages sincères, récoltés au fil des saisons depuis 2018.</p>{BADGES}</div></section>
{breadcrumb([("Accueil", "/"), ("Avis", None)])}
<section class="section">
  <div class="container center" style="margin-bottom:2rem">
    <p class="avis-intro reveal">La confiance de nos voyageurs, saison après saison — depuis 2018.</p>
  </div>
  <div class="container">
    <div class="avis-filtres reveal" data-avis-filtres>
      <div class="avis-filtres__top">
        <div class="avis-search">
          <input type="search" id="avis-q" class="filtres__select" placeholder="Rechercher un avis (propre, calme, thermes…)" aria-label="Rechercher dans les avis" data-avis-search>
        </div>
        <div class="avis-nat">
          <label class="filtres__label" for="avis-nat">Langue</label>
          <select id="avis-nat" class="filtres__select" data-avis-nat>
            <option value="all">Toutes</option>{nat_opts}
          </select>
        </div>
      </div>
      <div class="chips" role="group" aria-label="Filtrer les avis par catégorie">{chips}</div>
    </div>
    <div class="grid grid--3" data-avis-grid>{rcards}</div>
    <p class="filtres__vide" data-avis-vide hidden>Aucun avis ne correspond à cette recherche.</p>
    <div class="center" style="margin-top:2rem"><button type="button" class="btn btn--dark" data-avis-more>Voir plus d'avis</button></div>
  </div>
</section>
<section class="section section--tint"><div class="container center"><div class="cta-band reveal"><h2>À votre tour de vivre l'expérience</h2><p>Réservez votre appartement et rejoignez nos voyageurs conquis.</p><a class="btn btn--primary btn--lg" href="/appartements/">Réserver</a></div>
  <p class="cta-band__more">Une question avant de réserver ? <a href="/faq/">Consultez notre foire aux questions</a></p>
</div></section>
"""
    page("avis/index.html", "/avis/", "Avis clients — ce que disent nos voyageurs | Les Meublés de Luchon",
         "Les avis de nos voyageurs à Bagnères-de-Luchon : propreté, équipement, emplacement central et accueil. Témoignages authentiques recueillis depuis 2018.",
         avis)


    # =====================================================================
    # CONTACT
    # =====================================================================
    contact_ld = {"@context": "https://schema.org", "@type": "LodgingBusiness", "name": NAP["name"],
                  "telephone": NAP["tel_link"], "email": NAP["email"],
                  "address": {"@type": "PostalAddress", "streetAddress": NAP["street"], "addressLocality": NAP["city"],
                              "postalCode": NAP["postal"], "addressRegion": NAP["region"], "addressCountry": "FR"},
                  "url": BASE + "/contact/"}
    contact = f"""
<section class="page-hero"><div class="container">{EYEBROW}<h1>Nous contacter</h1><p>Une question, une demande particulière ? Nathalie vous répond avec plaisir.</p>{BADGES}</div></section>
{breadcrumb([("Accueil", "/"), ("Contact", None)])}
<section class="section">
  <div class="container contact-grid">
    <div class="reveal">
      <h2>Coordonnées</h2>
      <ul class="info-list">
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><span>{NAP['street']}, {NAP['postal']} {NAP['city']}</span></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.68 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.32 1.85.55 2.81.68A2 2 0 0 1 22 16.92z"/></svg><span><a href="tel:{NAP['tel_link']}">{NAP['tel_display']}</a></span></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><polyline points="22,6 12,13 2,6"/></svg><span><a href="mailto:{NAP['email']}">{NAP['email']}</a></span></li>
      </ul>
      <div class="footer__social" style="margin-top:1rem">
        <a href="{NAP['facebook']}" target="_blank" rel="noopener" aria-label="Facebook" style="background:var(--brand)"><svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
        <a href="{NAP['instagram']}" target="_blank" rel="noopener" aria-label="Instagram" style="background:var(--brand)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/></svg></a>
      </div>
      <iframe class="map-embed" style="margin-top:1.5rem" loading="lazy" title="Carte — {NAP['city']}" src="https://www.openstreetmap.org/export/embed.html?bbox=0.5886161327362062%2C42.79012771935476%2C0.5921190977096558%2C42.79197989095705&amp;layer=mapnik&amp;marker=42.79105474600715%2C0.5903676152229309"></iframe>
    </div>
    <div class="reveal">
      <h2>Nous envoyer un message</h2>
      <p>Une question sur nos appartements, vos dates ou votre séjour à Luchon ? Écrivez-nous : Nathalie vous répond personnellement, en général sous 24 h.</p>
      <form class="form" action="mailto:{NAP['email']}" method="post" enctype="text/plain">
        <div><label for="c-name">Votre prénom et nom</label><input type="text" id="c-name" name="Nom" placeholder="ex. Marie Dupont" autocomplete="name" required></div>
        <div><label for="c-email">Votre adresse e-mail</label><input type="email" id="c-email" name="Email" placeholder="ex. marie.dupont@email.fr" autocomplete="email" required></div>
        <div><label for="c-tel">Votre numéro de téléphone</label><input type="tel" id="c-tel" name="Telephone" placeholder="ex. 06 12 34 56 78" autocomplete="tel"></div>
        <div><label for="c-subject">Objet de votre message</label><input type="text" id="c-subject" name="Sujet" value="Demande d'information"></div>
        <div><label for="c-msg">Votre message</label><textarea id="c-msg" name="Message" rows="5" placeholder="Vos dates, le nombre de personnes, vos questions…" required></textarea></div>
        <button class="btn btn--dark btn--lg" type="submit">Envoyer ma demande</button>
      </form>
    </div>
  </div>
</section>
"""
    page("contact/index.html", "/contact/", "Contact — Les Meublés de Luchon | Bagnères-de-Luchon",
         f"Contactez Les Meublés de Luchon : {NAP['street']}, {NAP['postal']} {NAP['city']}. Téléphone {NAP['tel_display']}, e-mail {NAP['email']}. Nathalie vous répond rapidement.",
         contact, ld_blocks=[contact_ld])

    # =====================================================================
    # DÉPOSER UN AVIS (page dédiée, non indexée — envoyée par lien / QR)
    # =====================================================================
    stars_input = "".join(
        f'<input type="radio" name="note" id="star{n}" value="{n}" required>'
        f'<label for="star{n}" title="{n} étoile{"s" if n>1 else ""}" aria-label="{n} étoile{"s" if n>1 else ""}">'
        '<svg viewBox="0 0 24 24" fill="currentColor" width="40" height="40" aria-hidden="true">'
        '<path d="M12 2l3 6.5 7 .8-5.2 4.8 1.4 7L12 17.8 5.4 21l1.4-7L1.6 9.3l7-.8z"/></svg></label>'
        for n in range(5, 0, -1))
    depot = f"""
<section class="page-hero"><div class="container"><h1>Laissez votre avis</h1><p>Votre séjour aux Meublés de Luchon vous a plu ? Partagez votre expérience en quelques secondes — merci beaucoup !</p></div></section>
<section class="section"><div class="container" style="max-width:620px">
  <form class="form review-form" data-review-form
        action="https://REMPLACER-PAR-VOTRE-URL-APPS-SCRIPT" method="post">
    <div>
      <label>Votre note</label>
      <div class="stars-input" role="radiogroup" aria-label="Note sur 5 étoiles">{stars_input}</div>
    </div>
    <div><label for="rv-name">Votre prénom</label><input type="text" id="rv-name" name="prenom" placeholder="ex. Marie" autocomplete="given-name" required></div>
    <div><label for="rv-city">Votre ville (facultatif)</label><input type="text" id="rv-city" name="ville" placeholder="ex. Toulouse" autocomplete="address-level2"></div>
    <div><label for="rv-msg">Votre avis</label><textarea id="rv-msg" name="message" rows="5" placeholder="Qu'avez-vous apprécié pendant votre séjour ?" required></textarea></div>
    <input type="text" name="site_web" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
    <button class="btn btn--dark btn--lg" type="submit" data-review-submit>Envoyer mon avis</button>
    <p class="review-form__note">Votre avis sera lu puis publié sur le site après validation. Merci de votre confiance.</p>
  </form>
  <div class="review-form__ok" data-review-ok hidden>
    <h2>Merci beaucoup ! 🙏</h2>
    <p>Votre avis a bien été envoyé. Nathalie le lira avant sa publication sur le site.</p>
    <a class="btn btn--primary" href="/">Retour à l'accueil</a>
  </div>
</div></section>
"""
    page("deposer-un-avis/index.html", "/deposer-un-avis/",
         "Laissez votre avis — Les Meublés de Luchon",
         "Partagez votre expérience de séjour aux Meublés de Luchon à Bagnères-de-Luchon.",
         depot, robots="noindex, nofollow")

    # =====================================================================
    # PLAN DU SITE
    # =====================================================================
    plan = f"""
<section class="page-hero"><div class="container"><h1>Plan du site</h1><p>Toutes les pages des Meublés de Luchon en un coup d'œil.</p></div></section>
{breadcrumb([("Accueil", "/"), ("Plan du site", None)])}
<section class="section"><div class="container prose">
  <ul>
    <li><a href="/">Accueil</a></li>
    <li><a href="/appartements/">Nos appartements</a>
      <ul>
        <li><a href="/appartements/la-perle-bleue/">La Perle Bleue</a></li>
        <li><a href="/appartements/l-echappee-verte/">L'Échappée Verte</a></li>
        <li><a href="/appartements/le-refuge-thermal/">Le Refuge Thermal</a></li>
      </ul>
    </li>
    <li><a href="/services/">Services</a></li>
    <li><a href="/activites/">Activités</a></li>
    <li><a href="/avis/">Avis</a></li>
    <li><a href="/appartements/">Réservation</a></li>
    <li><a href="/guide/">Guides pratiques</a></li>
    <li><a href="/faq/">FAQ</a></li>
    <li><a href="/contact/">Contact</a></li>
    <li><a href="/mentions-legales/">Mentions légales</a></li>
    <li><a href="/politique-de-confidentialite/">Politique de confidentialité</a></li>
  </ul>
</div></section>
"""
    page("plan-du-site/index.html", "/plan-du-site/", "Plan du site | Les Meublés de Luchon",
         "Plan du site des Meublés de Luchon : accédez rapidement à toutes nos pages — logements, services, activités, avis, réservation et contact.",
         plan, robots="index, follow")

    # =====================================================================
    # MENTIONS LÉGALES
    # =====================================================================
    ml = f"""
<section class="page-hero"><div class="container"><h1>Mentions légales</h1></div></section>
{breadcrumb([("Accueil", "/"), ("Mentions légales", None)])}
<section class="section"><div class="container prose">
  <h2>Éditeur du site</h2>
  <p><strong>{NAP['name']}</strong><br>{NAP['street']}, {NAP['postal']} {NAP['city']}<br>
  Téléphone : <a href="tel:{NAP['tel_link']}">{NAP['tel_display']}</a><br>
  E-mail : <a href="mailto:{NAP['email']}">{NAP['email']}</a></p>
  <p><em>À compléter : nom du responsable de publication, statut juridique (auto-entrepreneur / SCI…), numéro SIRET et, le cas échéant, numéro de TVA intracommunautaire.</em></p>
  <h2>Hébergement</h2>
  <p><em>À compléter : nom et adresse de l'hébergeur du site (ex. OVH SAS, 2 rue Kellermann, 59100 Roubaix).</em></p>
  <h2>Propriété intellectuelle</h2>
  <p>L'ensemble des contenus (textes, photographies, logos) présents sur ce site est la propriété des Meublés de Luchon, sauf mention contraire. Toute reproduction sans autorisation est interdite.</p>
  <h2>Crédits</h2>
  <p>Photographies : Les Meublés de Luchon. Conception et réalisation du site : refonte 2026.</p>
  <h2>Données personnelles</h2>
  <p>Les informations recueillies via les formulaires sont utilisées uniquement pour répondre à vos demandes. Consultez notre <a href="/politique-de-confidentialite/">politique de confidentialité</a> pour en savoir plus sur vos droits.</p>
</div></section>
"""
    page("mentions-legales/index.html", "/mentions-legales/", "Mentions légales | Les Meublés de Luchon",
         "Mentions légales du site Les Meublés de Luchon — éditeur, hébergement, propriété intellectuelle et données personnelles.",
         ml, robots="noindex, follow")

    # =====================================================================
    # CONFIDENTIALITÉ
    # =====================================================================
    conf = f"""
<section class="page-hero"><div class="container"><h1>Politique de confidentialité</h1></div></section>
{breadcrumb([("Accueil", "/"), ("Politique de confidentialité", None)])}
<section class="section"><div class="container prose">
  <p>La présente politique décrit la manière dont Les Meublés de Luchon traite vos données personnelles, conformément au Règlement Général sur la Protection des Données (RGPD) et aux recommandations de la CNIL.</p>
  <h2>Responsable du traitement</h2>
  <p>{NAP['name']} — {NAP['street']}, {NAP['postal']} {NAP['city']} — <a href="mailto:{NAP['email']}">{NAP['email']}</a>.</p>
  <h2>Données collectées</h2>
  <p>Nous collectons uniquement les données que vous nous transmettez volontairement (nom, e-mail, téléphone, message) via nos formulaires de contact et de réservation, afin de traiter votre demande.</p>
  <h2>Cookies &amp; mesure d'audience</h2>
  <p>Aucun cookie de mesure d'audience ou de suivi n'est déposé sans votre consentement préalable. Un bandeau vous permet d'accepter ou de refuser ces cookies. Vous pouvez modifier votre choix à tout moment en supprimant les cookies de votre navigateur.</p>
  <h2>Durée de conservation</h2>
  <p>Vos données sont conservées le temps nécessaire au traitement de votre demande, puis archivées ou supprimées conformément aux obligations légales.</p>
  <h2>Vos droits</h2>
  <p>Vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition sur vos données. Pour l'exercer, écrivez-nous à <a href="mailto:{NAP['email']}">{NAP['email']}</a>. Vous pouvez également introduire une réclamation auprès de la CNIL (www.cnil.fr).</p>
</div></section>
"""
    page("politique-de-confidentialite/index.html", "/politique-de-confidentialite/",
         "Politique de confidentialité | Les Meublés de Luchon",
         "Politique de confidentialité des Meublés de Luchon : données collectées, cookies, durée de conservation et vos droits (RGPD / CNIL).",
         conf, robots="noindex, follow")

    # =====================================================================
    # 404
    # =====================================================================
    nf = """
<section class="section" style="min-height:50vh;display:grid;place-items:center;text-align:center">
  <div class="container">
    <p class="eyebrow">Erreur 404</p>
    <h1>Cette page a pris le large</h1>
    <p class="lead" style="margin:0 auto 1.5rem">La page que vous cherchez n'existe pas ou a été déplacée. Retrouvez votre chemin vers nos appartements.</p>
    <a class="btn btn--primary btn--lg" href="/">Retour à l'accueil</a>
    <a class="btn btn--ghost btn--lg" href="/appartements/">Nos appartements</a>
  </div>
</section>
"""
    page("404.html", "/", "Page introuvable (404) | Les Meublés de Luchon",
         "La page demandée est introuvable. Retournez à l'accueil des Meublés de Luchon.",
         nf, robots="noindex, follow")

    # =====================================================================
    # CURE THERMALE — page pilier dédiée (orientée conversion curistes)
    # =====================================================================
    cure_service_ld = {
        "@context": "https://schema.org", "@type": "Service",
        "name": "Hébergement pour cure thermale à Bagnères-de-Luchon",
        "serviceType": "Location saisonnière pour curistes",
        "provider": {"@type": "LodgingBusiness", "name": NAP["name"],
                     "telephone": NAP["tel_link"], "email": NAP["email"],
                     "address": {"@type": "PostalAddress", "streetAddress": NAP["street"],
                                 "addressLocality": NAP["city"], "postalCode": NAP["postal"],
                                 "addressRegion": NAP["region"], "addressCountry": "FR"}},
        "areaServed": NAP["city"],
        "description": "Appartements meublés à quelques minutes à pied des Thermes de Luchon, adaptés aux séjours de cure de 18 jours : plain-pied, cuisine équipée, calme et confort.",
        "url": BASE + "/cure-thermale/",
    }
    cure_faq = [
        ("Vos logements sont-ils proches des Thermes de Luchon ?", "Oui, nos trois appartements sont au centre de Luchon, à quelques minutes à pied des thermes — vous rejoignez vos soins sans voiture."),
        ("Quel appartement choisir pour une cure ?", "Le Refuge Thermal, notre T2 de plain-pied au rez-de-chaussée, est spécialement adapté aux curistes et aux personnes à mobilité réduite. La Perle Bleue et L'Échappée Verte conviennent également très bien."),
        ("Proposez-vous des séjours de trois semaines ?", "Oui, nos logements sont pensés pour les séjours de cure de 18 jours et plus, avec cuisine équipée, lave-linge et Wi-Fi pour vivre confortablement sur la durée."),
        ("Combien de temps dure une cure et est-elle remboursée ?", "La cure conventionnée dure 18 jours de soins et se fait sur prescription de votre médecin. La prise en charge par l'Assurance Maladie dépend de votre situation : votre médecin et votre caisse vous renseigneront précisément."),
        ("Quels services proposez-vous aux curistes ?", "Ménage de fin de séjour, location de draps et de serviettes, Wi-Fi haut débit, parking gratuit à proximité, animaux acceptés, et les conseils personnalisés de Nathalie."),
    ]
    avis_cure = "".join(avis_card(a) for a in (pick_avis(["curiste","cure","therme"],3,_used) + pick_avis(["équipé","propre","calme"],3,_used))[:3])

    # Page Cure : pas de réservation en ligne (tarif spécial), on renvoie vers le formulaire.
    CURE_CTA = ("Demander le tarif cure", "#tarif-cure")

    cure = f"""
<section class="page-hero has-img"><div class="page-hero__img"><img src="/assets/img/activites/thermes-bassin.jpg" alt="Bassin extérieur des Thermes de Luchon face aux Pyrénées" width="1400" height="500"></div>
  <div class="container">
    <p class="eyebrow" style="color:#a9e0e4">Cure thermale · Bagnères-de-Luchon</p>
    <h1>Votre hébergement pour une cure thermale à Luchon</h1>
    <p>Des appartements meublés, à quelques minutes à pied des Thermes de Luchon, pensés pour le confort des curistes : cuisine équipée, calme et séjours de trois semaines en toute sérénité. <strong>Un tarif spécial s'applique aux séjours de cure : demandez-nous le tarif.</strong></p>
    {BADGES}
  </div>
</section>
{breadcrumb([("Accueil", "/"), ("Cure thermale", None)])}

<section class="section">
  <div class="container center reveal">
    <p class="eyebrow">Séjour thermal</p>
    <h2>Séjournez à deux pas des Thermes de Luchon</h2>
    <p class="lead">La cure conventionnée de Luchon dure 18 jours. Nos trois appartements, tous au centre-ville, vous placent à quelques minutes à pied des thermes — sans voiture, sans stress. Le Refuge Thermal, de plain-pied, est spécialement adapté aux curistes et aux personnes à mobilité réduite.</p>
    <div style="margin-top:1.8rem;display:flex;flex-wrap:wrap;gap:.8rem;justify-content:center">
      <a class="btn btn--primary btn--lg" href="#tarif-cure">Demander le tarif cure</a>
      <a class="btn btn--ghost btn--lg" href="#logements">Voir les appartements</a>
    </div>
  </div>
</section><section class="section">
  <div class="container split">
    <div class="split__media reveal">{diapo(g, [
        ("refuge-thermal", "piece-de-vie.jpg", "Pièce de vie du Refuge Thermal, de plain-pied"),
        ("perle-bleue", "salon.jpg", "Salon de La Perle Bleue"),
        ("echappee-verte", "canape.jpg", "Coin salon de L'Échappée Verte"),
        ("refuge-thermal", "chambre.jpg", "Chambre du Refuge Thermal"),
        ("perle-bleue", "chambre.jpg", "Chambre de La Perle Bleue"),
        ("echappee-verte", "cuisine.jpg", "Cuisine équipée de L'Échappée Verte"),
        ("refuge-thermal", "cuisine.jpg", "Cuisine du Refuge Thermal"),
        ("perle-bleue", "cuisine.jpg", "Cuisine de La Perle Bleue"),
      ], interval=2200)}</div>
    <div class="split__body reveal">
      <p class="eyebrow">Nos appartements pour votre cure</p>
      <h2>Nos trois appartements accueillent les curistes</h2>
      <p>La Perle Bleue, L'Échappée Verte et Le Refuge Thermal sont tous situés au centre de Luchon, à quelques minutes à pied des thermes. Chacun dispose d'une cuisine équipée et d'un lave-linge, indispensables pour un séjour de trois semaines. Le Refuge Thermal, en rez-de-chaussée, offre en plus un <strong>accès de plain-pied</strong> — particulièrement apprécié en cas de mobilité réduite.</p>
      <a class="btn btn--primary" href="#logements">Voir les trois appartements</a>
    </div>
  </div>
</section>

<section class="section section--tint" id="logements">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2.5rem"><p class="eyebrow">Nos hébergements</p><h2>Trois appartements pour votre cure</h2><p class="lead">Tous au centre de Luchon, à quelques minutes à pied des thermes. Les séjours de cure ne se réservent pas en ligne : ils bénéficient d'un tarif spécial, sur demande.</p></div>
    <div class="grid grid--3">
      {logement_card(g, "le-refuge-thermal", cta=CURE_CTA, link_photos=False)}
      {logement_card(g, "la-perle-bleue", cta=CURE_CTA, link_photos=False)}
      {logement_card(g, "l-echappee-verte", cta=CURE_CTA, link_photos=False)}
    </div>
  </div>
</section>



<section class="section section--tint">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2rem"><p class="eyebrow">Pensé pour les curistes</p><h2>Un séjour de cure sans souci</h2></div>
    <div class="grid grid--3">
      <div class="feature reveal"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div><h3>À pied des thermes</h3><p>À quelques minutes des Thermes de Luchon : rejoignez vos soins chaque jour sans prendre la voiture.</p></div>
      <div class="feature reveal"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h18M3 6h18M3 18h18"/></svg></div><h3>Un appartement de plain-pied</h3><p>Le Refuge Thermal est au rez-de-chaussée : un accès facile, sans escalier, idéal pour les curistes.</p></div>
      <div class="feature reveal"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 3h16v7a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4z"/><path d="M8 14v7M16 14v7"/></svg></div><h3>Cuisine équipée</h3><p>Four, plaques, réfrigérateur, cafetière : de quoi cuisiner sereinement pendant vos trois semaines.</p></div>
      <div class="feature reveal"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a9 9 0 1 0 9 9"/><path d="M12 7v5l3 2"/></svg></div><h3>Calme et récupération</h3><p>Des appartements confortables et une literie de qualité pour bien vous reposer entre deux soins.</p></div>
      <div class="feature reveal"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg></div><h3>Séjours longue durée</h3><p>Nos appartements sont adaptés aux cures de 18 jours et plus, avec lave-linge et Wi-Fi inclus.</p></div>
      <div class="feature reveal"><div class="feature__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div><h3>Un accueil attentionné</h3><p>Nathalie vous conseille avant votre arrivée et reste disponible tout au long de votre cure.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split split--reverse">
    <div class="split__media reveal"><img src="/assets/img/services/menage.jpg" alt="Services pour curistes : ménage, linge" loading="lazy" width="600" height="480"></div>
    <div class="split__body reveal">
      <p class="eyebrow">Services adaptés</p>
      <h2>Tout pour un séjour de trois semaines</h2>
      <p>Parce qu'une cure dure longtemps, nous facilitons votre quotidien : ménage de fin de séjour, location de draps et de serviettes, Wi-Fi haut débit, parking gratuit à proximité, et animaux acceptés. Nathalie vous transmet un livret d'accueil et ses meilleurs conseils.</p>
      <p style="margin-top:.4rem"><a class="link-more" href="/services/">Voir le détail de nos services et tarifs →</a></p>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="center reveal" style="margin-bottom:2rem"><p class="eyebrow">Ils ont fait leur cure chez nous</p><h2>La confiance des curistes</h2></div>
    <div class="grid grid--3">
      {avis_cure}
    </div>
    <p class="center" style="margin-top:1.5rem;font-size:.95rem;color:var(--muted)">Ils ont fait leur cure chez nous et le racontent — <a class="link-more" href="/avis/">lire tous les avis →</a></p>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split__body reveal">
      <p class="eyebrow">Bon à savoir</p>
      <h2>La cure thermale de Luchon en quelques mots</h2>
      <ul class="amenities" style="margin-top:1rem">
        <li>{CHECK}<span>Cure conventionnée de <strong>18 jours</strong></span></li>
        <li>{CHECK}<span>Prise en charge possible <strong>sur prescription médicale</strong></span></li>
        <li>{CHECK}<span>Orientations <strong>rhumatologie</strong> et <strong>voies respiratoires</strong></span></li>
        <li>{CHECK}<span>Le <strong>vaporarium</strong>, hammam naturel unique en Europe</span></li>
      </ul>
      <p style="margin-top:1.2rem"><a href="/guide/cure-thermale-a-luchon/"><strong>Lire notre guide complet de la cure thermale à Luchon →</strong></a></p>
    </div>
    <div class="split__media reveal"><img src="/assets/img/activites/thermes-bassin.jpg" alt="Bassin extérieur des Thermes de Luchon avec vue sur la montagne" loading="lazy" width="600" height="480"></div>
  </div>
</section>

{faq_section(g, cure_faq)}

<section class="section section--tint" id="tarif-cure">
  <div class="container" style="max-width:760px">
    <div class="center reveal" style="margin-bottom:1.8rem">
      <p class="eyebrow">Tarif cure</p>
      <h2>Demander le tarif cure</h2>
      <p class="lead">Les séjours de cure (18 jours et plus) bénéficient d'un <strong>tarif spécial</strong>, différent des réservations classiques. Indiquez-nous vos dates : Nathalie vous répond sous 24 h.</p>
    </div>
    <form class="form reveal" action="mailto:{NAP['email']}" method="post" enctype="text/plain">
      <div><label for="cu-name">Votre prénom et nom</label><input type="text" id="cu-name" name="Nom" placeholder="ex. Marie Dupont" autocomplete="name" required></div>
      <div><label for="cu-email">Votre adresse e-mail</label><input type="email" id="cu-email" name="Email" placeholder="ex. marie.dupont@email.fr" autocomplete="email" required></div>
      <div><label for="cu-tel">Votre numéro de téléphone</label><input type="tel" id="cu-tel" name="Telephone" placeholder="ex. 06 12 34 56 78" autocomplete="tel"></div>
      <div>
        <label id="cu-dates-l">Dates de votre cure</label>
        <div class="form__dates" data-cal-host aria-labelledby="cu-dates-l">
          {cal_fields("cure", "Arrivée", "Départ")}
          {cal_panel("Arrivee", "Depart", required=True)}
        </div>
      </div>
      <div><label for="cu-pers">Nombre de voyageurs</label><input type="text" id="cu-pers" name="Personnes" placeholder="ex. 2 personnes"></div>
      <div><label for="cu-msg">Votre message</label><textarea id="cu-msg" name="Message" rows="4" placeholder="Précisez si vous souhaitez un appartement de plain-pied, des draps, etc."></textarea></div>
      <input type="hidden" name="Objet" value="Demande de tarif - cure thermale">
      <button class="btn btn--dark btn--lg" type="submit">Envoyer ma demande</button>
    </form>
    <p class="center" style="margin-top:1.2rem;font-size:.95rem">Ou par téléphone : <a href="tel:{NAP['tel_link']}"><strong>{NAP['tel_display']}</strong></a></p>
  </div>
</section>
<section class="section"><div class="container"><div class="cta-band reveal">
  <h2>Réservez votre séjour de cure à Luchon</h2>
  <p>Les séjours de cure bénéficient d'un <strong>tarif spécial</strong> : contactez-nous avec vos dates, Nathalie vous répond sous 24 h.</p>
  <div style="display:flex;flex-wrap:wrap;gap:.8rem;justify-content:center">
    <a class="btn btn--primary btn--lg" href="#tarif-cure">Demander le tarif cure</a>
    <a class="btn btn--ghost btn--lg" href="tel:+33684816041" style="border-color:#fff;color:#fff">Appeler</a>
  </div>
</div>
  <p class="cta-band__more">Une question avant de réserver ? <a href="/faq/">Consultez notre foire aux questions</a></p>
</div></section>
"""
    page("cure-thermale/index.html", "/cure-thermale/",
         "Cure thermale à Luchon : hébergement pour curistes près des thermes | Les Meublés de Luchon",
         "Appartements meublés pour votre cure thermale à Bagnères-de-Luchon : à quelques minutes à pied des thermes, appartement de plain-pied, cuisine équipée, séjours de 18 jours. Réservez en direct.",
         cure, og_image="/assets/img/activites/thermes-bassin.jpg", ld_blocks=[cure_service_ld])

    # =====================================================================
    # GUIDES (contenu longue traîne) + index /guide/
    # =====================================================================
    GUIDES = [
        {
            "slug": "cure-thermale-a-luchon",
            "meta_title": "Cure thermale à Luchon : guide complet et où loger | Les Meublés de Luchon",
            "desc": "Tout sur la cure thermale de Bagnères-de-Luchon : durée (18 jours), prise en charge, indications (rhumatologie, voies respiratoires), le vaporarium, et où loger près des thermes.",
            "h1": "Cure thermale à Luchon : le guide complet (et où loger)",
            "hero": "/assets/img/activites/thermes-bassin.jpg",
            "hero_alt": "Thermes de Bagnères-de-Luchon",
            "eyebrow": "Guide pratique · Thermalisme",
            "lead": "La cure thermale conventionnée de Luchon dure 18 jours et se fait sur prescription médicale. Voici l'essentiel à savoir — et comment bien se loger à deux pas des thermes.",
            "short": "Cure thermale à Luchon",
            "body": """
<p><strong>En bref :</strong> Bagnères-de-Luchon est une station thermale reconnue pour ses eaux sulfurées, avec une double orientation <strong>rhumatologie</strong> et <strong>voies respiratoires</strong>. La cure conventionnée dure <strong>18 jours</strong> et se fait sur prescription médicale, et la ville abrite le <strong>seul hammam naturel d'Europe</strong>, le vaporarium.</p>

<h2>Qu'est-ce que la cure thermale de Luchon ?</h2>
<p>Les Thermes de Luchon exploitent des eaux hypothermales sulfurées aux bienfaits reconnus. L'établissement, récemment rénové, propose des cures conventionnées de 18 jours, des mini-cures et des séjours bien-être. Sa particularité : le <strong>vaporarium</strong>, un hammam naturel unique en Europe, où l'on profite de galeries creusées dans la roche alimentées par des vapeurs sulfureuses à <strong>38-42 °C</strong>.</p>

<h2>Quelles sont les indications ?</h2>
<ul>
  <li><strong>Rhumatologie</strong> : arthrose, douleurs articulaires, suites de traumatismes.</li>
  <li><strong>Voies respiratoires</strong> : sinusites, bronchites chroniques, asthme — le vaporarium est particulièrement indiqué pour décongestionner et apaiser les bronches.</li>
</ul>

<h2>Durée, prescription et remboursement</h2>
<p>La cure conventionnée s'étend sur <strong>18 jours de soins</strong>, prescrite par votre médecin et prise en charge par l'<strong>Assurance Maladie</strong> (le taux et les conditions dépendent de votre situation ; l'hébergement et le transport peuvent aussi faire l'objet d'une aide sous conditions de ressources). Il faut donc prévoir un hébergement pour <strong>environ trois semaines</strong> — d'où l'importance de bien le choisir.</p>

<h2>Où loger pour sa cure à Luchon ?</h2>
<p>Nos trois appartements meublés sont situés au centre de Luchon, à quelques minutes à pied des thermes — idéal pour rejoindre vos soins sans voiture. Découvrez notre <a href="/cure-thermale/"><strong>page dédiée à la cure thermale</strong></a> et nos hébergements pour curistes. Pour une cure, nous recommandons particulièrement <a href="/appartements/le-refuge-thermal/"><strong>Le Refuge Thermal</strong></a>, un T2 de plain-pied (rez-de-chaussée) pensé pour les curistes et l'accès facile. <a href="/appartements/la-perle-bleue/">La Perle Bleue</a> et <a href="/appartements/l-echappee-verte/">L'Échappée Verte</a> conviennent aussi parfaitement.</p>
<p>Pour un séjour de trois semaines, pensez à nos <a href="/services/">services</a> : ménage, location de draps et de serviettes, Wi-Fi haut débit pour rester connecté, et animaux acceptés.</p>

<h2>Nos conseils de curiste</h2>
<ul>
  <li><strong>Réservez tôt</strong> : les logements proches des thermes partent vite en saison de cure (mars à novembre).</li>
  <li>Privilégiez un <strong>appartement avec cuisine équipée</strong> pour cuisiner sur la durée — les nôtres le sont tous.</li>
  <li>Profitez des demi-journées libres pour découvrir <a href="/activites/">les activités de Luchon</a> : randonnées douces, allées d'Étigny, casino.</li>
</ul>
""",
            "faq": [
                ("Combien de temps dure une cure thermale à Luchon ?", "Une cure conventionnée dure 18 jours de soins, prescrite par votre médecin. Prévoyez donc un hébergement d'environ trois semaines."),
                ("La cure est-elle remboursée ?", "Oui, la cure conventionnée fait l'objet d'une prise en charge par l'Assurance Maladie sur prescription médicale. Le taux et les conditions dépendent de votre situation : renseignez-vous auprès de votre médecin ou de votre caisse. L'hébergement et le transport peuvent aussi faire l'objet d'une aide selon vos ressources."),
                ("Quel appartement choisir pour une cure ?", "Le Refuge Thermal, notre T2 de plain-pied au rez-de-chaussée, est idéal pour les curistes et les personnes à mobilité réduite. Nos trois appartements sont à quelques minutes à pied des thermes."),
                ("Quelles sont les indications des Thermes de Luchon ?", "Deux orientations : la rhumatologie (arthrose, douleurs articulaires) et les voies respiratoires (sinusites, bronchites, asthme), avec le vaporarium, hammam naturel unique en Europe."),
            ],
        },
        {
            "slug": "ski-a-superbagneres",
            "meta_title": "Ski à Luchon-Superbagnères : accès, domaine et où loger | Les Meublés de Luchon",
            "desc": "Guide du ski à Luchon-Superbagnères : 28 pistes jusqu'à 2125 m, accès en 8 minutes par la télécabine depuis le centre-ville, et où loger au pied des pistes.",
            "h1": "Ski à Luchon-Superbagnères : accès, domaine et où loger",
            "hero": "/assets/img/activites/ski.jpg",
            "hero_alt": "Domaine skiable de Luchon-Superbagnères",
            "eyebrow": "Guide pratique · Ski & montagne",
            "lead": "Superbagnères, le « balcon des Pyrénées », culmine à 2125 m et s'atteint en 8 minutes par télécabine depuis le centre de Luchon. Le bon plan : loger en ville et monter skier chaque matin.",
            "short": "Ski à Superbagnères",
            "body": """
<p><strong>En bref :</strong> le domaine de Luchon-Superbagnères s'étend de <strong>1465 à 2125 m</strong> d'altitude avec <strong>28 pistes</strong> réparties sur trois secteurs, accessible directement depuis le centre-ville par la télécabine <strong>Crémaillère Express</strong> en <strong>8 minutes</strong>.</p>

<h2>Le domaine skiable en un coup d'œil</h2>
<ul>
  <li><strong>Altitude :</strong> 1465 m à 2125 m (le « balcon des Pyrénées »).</li>
  <li><strong>28 pistes</strong> : 15 % vertes, 45 % bleues, 21 % rouges, 18 % noires — idéal pour tous les niveaux, des débutants aux confirmés.</li>
  <li><strong>Trois secteurs</strong> : Téchous, Lac et Céciré.</li>
  <li>Ski alpin, ski de fond, luge et raquettes, avec une vue imprenable sur la vallée.</li>
</ul>

<h2>Comment accéder aux pistes ?</h2>
<p>C'est l'un des grands atouts de Luchon : la nouvelle télécabine 10 places <strong>Crémaillère Express</strong> (ouverte en décembre 2023) relie le centre-ville aux pistes en seulement <strong>8 minutes</strong>. Pas besoin de prendre la voiture ni de faire la route de montagne chaque matin : vous partez skier à pied depuis votre appartement.</p>

<h2>Pourquoi loger à Luchon plutôt qu'en altitude ?</h2>
<p>Loger en ville, c'est profiter du meilleur des deux mondes : les pistes le jour, et l'ambiance d'une vraie station thermale le soir — commerces, restaurants, casino, et surtout les <a href="/activites/#thermalisme">thermes</a> pour un après-ski bien-être. Nos <a href="/appartements/">appartements meublés</a> sont à quelques minutes à pied de la télécabine.</p>

<h2>Nos conseils pour un séjour au ski</h2>
<ul>
  <li>Réservez votre <a href="/appartements/">appartement</a> tôt pour les vacances scolaires d'hiver.</li>
  <li>Un appartement avec <a href="/services/">Wi-Fi, lave-linge et cuisine équipée</a> facilite les séjours en famille.</li>
  <li>Vérifiez l'enneigement et les forfaits sur le site officiel de la station avant de partir.</li>
</ul>
""",
            "faq": [
                ("Comment accéder aux pistes de Superbagnères depuis Luchon ?", "La télécabine Crémaillère Express relie le centre-ville de Luchon aux pistes en 8 minutes. Vous pouvez partir skier à pied depuis nos appartements, sans voiture."),
                ("Quelle est l'altitude de Superbagnères ?", "Le domaine s'étend de 1465 m à 2125 m d'altitude, ce qui lui vaut le surnom de « balcon des Pyrénées »."),
                ("Combien y a-t-il de pistes ?", "28 pistes réparties en 15 % vertes, 45 % bleues, 21 % rouges et 18 % noires, sur trois secteurs (Téchous, Lac, Céciré)."),
                ("Vaut-il mieux loger à Luchon ou à la station ?", "Loger à Luchon permet de skier la journée et de profiter le soir des thermes, restaurants et commerces de la ville, tout en étant à quelques minutes de la télécabine."),
            ],
        },
        {
            "slug": "venir-a-bagneres-de-luchon",
            "meta_title": "Venir à Bagnères-de-Luchon : accès, train, voiture, parking | Les Meublés de Luchon",
            "desc": "Comment venir à Bagnères-de-Luchon : 1h45 de Toulouse en voiture (140 km), train direct depuis Toulouse Matabiau (2h10) avec gare en ville, et infos parking.",
            "h1": "Comment venir à Bagnères-de-Luchon : accès, train, voiture, parking",
            "hero": "/assets/img/activites/randonnee.jpg",
            "hero_alt": "Route vers Bagnères-de-Luchon dans les Pyrénées",
            "eyebrow": "Guide pratique · Accès",
            "lead": "Luchon est à environ 1h45 de Toulouse en voiture (140 km) et accessible en train direct depuis Toulouse Matabiau (≈ 2h10) — la gare est en centre-ville.",
            "short": "Venir à Luchon",
            "body": """
<p><strong>En bref :</strong> Bagnères-de-Luchon se rejoint facilement depuis Toulouse en <strong>voiture (≈ 1h45, 140 km)</strong> ou en <strong>train direct (≈ 2h10)</strong> depuis la gare de Toulouse Matabiau, avec une gare située en plein centre de Luchon.</p>

<h2>En voiture</h2>
<p>Depuis Toulouse, comptez environ <strong>1h45 pour 140 km</strong> : autoroute A64 jusqu'à la sortie Montréjeau, puis la D125 qui remonte la vallée jusqu'à Luchon. La route est belle et bien entretenue. En hiver, prévoyez des équipements adaptés pour rejoindre les pistes.</p>

<h2>En train</h2>
<p>La SNCF propose un <strong>train direct Toulouse Matabiau → Luchon en environ 2h10</strong>. Grand avantage : la <strong>gare est en centre-ville</strong>, à quelques minutes à pied de nos appartements — idéal pour venir sans voiture, notamment pour une cure.</p>

<h2>En avion</h2>
<p>L'aéroport le plus proche est <strong>Toulouse-Blagnac</strong>, puis liaison en voiture de location ou en train via Toulouse Matabiau.</p>

<h2>Se déplacer sur place et se garer</h2>
<p>À Luchon, <strong>tout est accessible à pied</strong> : thermes, commerces, restaurants, télécabine de Superbagnères. C'est l'un des atouts de nos <a href="/appartements/">logements</a>, tous situés au centre-ville. Un <strong>parking gratuit</strong> se trouve à proximité (voir <a href="/services/">nos services</a>). Pour préparer votre venue, contactez-nous : nous vous transmettons toutes les informations d'accès et de stationnement avec votre <a href="/appartements/">confirmation de réservation</a>.</p>
""",
            "faq": [
                ("Comment aller à Bagnères-de-Luchon depuis Toulouse ?", "En voiture, comptez environ 1h45 (140 km) via l'A64 puis la D125. En train, un service direct relie Toulouse Matabiau à Luchon en environ 2h10, avec une gare en centre-ville."),
                ("Y a-t-il un train pour Luchon ?", "Oui, la SNCF propose un train direct depuis Toulouse Matabiau jusqu'à Luchon (≈ 2h10). La gare est située en plein centre, à quelques minutes à pied de nos appartements."),
                ("Où se garer à Luchon ?", "Un parking gratuit se trouve à proximité de nos logements. Toutes les informations de stationnement vous sont transmises avec votre confirmation de réservation."),
                ("A-t-on besoin d'une voiture sur place ?", "Non : à Luchon, les thermes, commerces, restaurants et la télécabine de Superbagnères sont accessibles à pied depuis nos appartements du centre-ville."),
            ],
        },
        {
            "slug": "louer-avec-son-chien-a-luchon",
            "meta_title": "Louer avec son chien à Bagnères-de-Luchon | Les Meublés de Luchon",
            "desc": "Location d'appartement acceptant les animaux à Bagnères-de-Luchon : nos meublés accueillent votre chien (50 € par séjour). Idées de balades et conseils pour un séjour réussi.",
            "h1": "Louer un appartement avec son chien à Bagnères-de-Luchon",
            "hero": "/assets/img/services/animal.jpg",
            "hero_alt": "Chien accueilli dans un appartement des Meublés de Luchon",
            "eyebrow": "Guide pratique · Animaux",
            "lead": "Oui, nos appartements meublés acceptent les animaux (50 € par séjour et par animal). Luchon et les Pyrénées sont une destination idéale pour voyager avec son chien.",
            "short": "Louer avec son chien",
            "body": """
<p><strong>En bref :</strong> nos trois logements <strong>acceptent les animaux</strong> moyennant un supplément de <strong>50 € par séjour et par animal</strong>. Merci de nous le signaler à la réservation. Luchon, entre montagnes et sentiers, est parfaite pour un séjour avec votre compagnon à quatre pattes.</p>

<h2>Des appartements qui acceptent les animaux</h2>
<p>Que vous choisissiez <a href="/appartements/la-perle-bleue/">La Perle Bleue</a>, <a href="/appartements/l-echappee-verte/">L'Échappée Verte</a> ou <a href="/appartements/le-refuge-thermal/">Le Refuge Thermal</a>, votre chien est le bienvenu. Le supplément de 50 € couvre le nettoyage supplémentaire. Le Refuge Thermal, de plain-pied, est particulièrement pratique pour les sorties fréquentes.</p>

<h2>Où promener son chien à Luchon ?</h2>
<ul>
  <li>Les <a href="/activites/#randonnee">sentiers de randonnée</a> de la vallée, dont la montée vers le lac d'Oô.</li>
  <li>Les allées d'Étigny et le parc du casino, en plein centre, pour les balades quotidiennes.</li>
  <li>Les grands espaces de montagne autour de Superbagnères en été.</li>
</ul>

<h2>Nos conseils pour un séjour réussi avec votre animal</h2>
<ul>
  <li>Signalez la présence de votre animal <strong>dès la réservation</strong>.</li>
  <li>Prévoyez son couchage et sa gamelle ; nous vous indiquons les commerces et vétérinaires à proximité.</li>
  <li>Merci de ne pas laisser votre animal seul dans l'appartement et de veiller à la propreté des lieux.</li>
</ul>
<p>Prêt à partir avec votre chien ? <a href="/appartements/">Vérifiez nos disponibilités</a> ou <a href="/contact/">contactez-nous</a>.</p>
""",
            "faq": [
                ("Les animaux sont-ils acceptés dans vos logements ?", "Oui, nos trois appartements acceptent les animaux moyennant 50 € par séjour et par animal. Merci de nous le signaler à la réservation."),
                ("Quel logement choisir avec un chien ?", "Tous nos logements acceptent les animaux. Le Refuge Thermal, de plain-pied, est particulièrement pratique pour les sorties fréquentes."),
                ("Où promener son chien à Luchon ?", "Les sentiers de la vallée (lac d'Oô), les allées d'Étigny et le parc du casino en centre-ville, et les espaces de montagne autour de Superbagnères en été."),
            ],
        },
    ]

    def guides_nav(current_slug):
        links = "".join(
            f'<li><a href="/guide/{gg["slug"]}/">{gg["short"]}</a></li>'
            for gg in GUIDES if gg["slug"] != current_slug)
        return (f'<section class="section section--tint"><div class="container">'
                f'<h2 class="center">À lire aussi</h2><ul class="guides-nav">{links}'
                f'<li><a href="/faq/">Questions fréquentes</a></li></ul></div></section>')

    def article_ld(gg):
        return {"@context": "https://schema.org", "@type": "Article",
                "headline": gg["h1"], "description": gg["desc"],
                "image": BASE + gg["hero"],
                "inLanguage": "fr-FR",
                "author": {"@type": "Organization", "name": NAP["name"]},
                "publisher": {"@type": "Organization", "name": NAP["name"],
                              "logo": {"@type": "ImageObject", "url": BASE + "/assets/img/brand/logo.png"}},
                "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + "/guide/" + gg["slug"] + "/"}}

    for gg in GUIDES:
        m = f"""
<section class="page-hero has-img"><div class="page-hero__img"><img src="{gg['hero']}" alt="{gg['hero_alt']}" width="1400" height="500"></div>
  <div class="container"><p class="eyebrow" style="color:#a9e0e4">{gg['eyebrow']}</p><h1>{gg['h1']}</h1><p>{gg['lead']}</p></div>
</section>
{breadcrumb([("Accueil", "/"), ("Guides pratiques", "/guide/"), (gg['short'], None)])}
<section class="section"><div class="container prose">{gg['body']}</div></section>
<section class="section" style="padding-top:0"><div class="container"><div class="cta-band reveal"><h2>Envie de séjourner à Luchon ?</h2><p>Découvrez nos appartements meublés au centre-ville et réservez en quelques clics.</p><a class="btn btn--primary btn--lg" href="/appartements/">Réserver</a></div>
  <p class="cta-band__more">Une question avant de réserver ? <a href="/faq/">Consultez notre foire aux questions</a></p>
</div></section>
{faq_section(g, gg['faq'])}
{guides_nav(gg['slug'])}
"""
        page(f"guide/{gg['slug']}/index.html", "/guide/", gg["meta_title"], gg["desc"], m,
             og_image=gg["hero"], ld_blocks=[article_ld(gg)])

    # Index /guide/
    gcards = "".join(
        f'<article class="card reveal"><a class="card__media" href="/guide/{gg["slug"]}/">'
        f'<img src="{gg["hero"]}" alt="{gg["hero_alt"]}" loading="lazy" width="500" height="375"></a>'
        f'<div class="card__body"><h3>{gg["short"]}</h3><p>{gg["lead"]}</p>'
        f'<div class="card__foot"><a class="btn btn--ghost" href="/guide/{gg["slug"]}/">Lire le guide</a></div></div></article>'
        for gg in GUIDES)
    guide_index = f"""
<section class="page-hero"><div class="container">{EYEBROW}<h1>Guides pratiques pour votre séjour à Luchon</h1><p>Cure thermale, ski, accès, séjour avec animaux : tous nos conseils pour préparer votre venue à Bagnères-de-Luchon.</p>{BADGES}</div></section>
{breadcrumb([("Accueil", "/"), ("Guides pratiques", None)])}
<section class="section"><div class="container"><div class="grid grid--2">{gcards}</div>
  <p class="center" style="margin-top:2rem">Vous cherchez une réponse précise ? Consultez notre <a href="/faq/"><strong>foire aux questions</strong></a>.</p>
</div></section>
<section class="section section--tint"><div class="container"><div class="cta-band reveal">
  <h2>Votre séjour à Luchon commence ici</h2>
  <p>Maintenant que vous avez toutes les clés, choisissez vos dates et votre appartement au centre de Bagnères-de-Luchon.</p>
  <a class="btn btn--primary btn--lg" href="/appartements/">Réserver</a>
</div>
  <p class="cta-band__more">Une question avant de réserver ? <a href="/faq/">Consultez notre foire aux questions</a></p>
</div></section>
"""
    page("guide/index.html", "/guide/", "Guides pratiques — Luchon (cure, ski, accès) | Les Meublés de Luchon",
         "Guides pratiques pour préparer votre séjour à Bagnères-de-Luchon : cure thermale, ski à Superbagnères, accès et transport, location avec animaux.",
         guide_index, og_image="/assets/img/activites/randonnee.jpg")

    # =====================================================================
    # FAQ (page dédiée et étoffée, une seule FAQPage schema)
    # =====================================================================
    faq_cats = [
        ("Réserver un appartement à Luchon", [
            ("Comment réserver un appartement à Luchon ?", "Indiquez vos dates sur notre page Nos appartements : les logements disponibles à Bagnères-de-Luchon s'affichent automatiquement. Vous choisissez le vôtre, confirmez et payez en ligne, avec une confirmation immédiate par e-mail."),
            ("Est-ce moins cher de réserver en direct plutôt que sur Airbnb ou Booking ?", "Oui. En réservant en direct sur notre site, vous évitez les commissions des plateformes et bénéficiez du meilleur tarif, tout en échangeant directement avec Nathalie, votre hôte à Luchon."),
            ("Le paiement en ligne est-il sécurisé ?", "Oui, le paiement s'effectue sur une plateforme de réservation sécurisée, avec confirmation immédiate par e-mail."),
            ("Y a-t-il un nombre minimum de nuits à Luchon ?", "La durée minimale varie selon la saison et s'affiche automatiquement au moment de choisir vos dates. Les séjours d'une semaine ou plus sont fréquents, notamment pour les curistes."),
            ("Quelle est la politique d'annulation ?", "Les conditions d'annulation sont précisées lors de la réservation, avant tout paiement. Pour toute question, contactez directement Nathalie."),
            ("Peut-on réserver un long séjour ou une cure de trois semaines ?", "Oui. Pour les séjours de cure (18 jours et plus), un tarif spécial s'applique : il ne se réserve pas en ligne mais sur simple demande via notre page Cure thermale."),
        ]),
        ("Où se situent vos appartements à Luchon ?", [
            ("Où sont situés vos appartements à Luchon ?", "Nos trois appartements sont au centre de Bagnères-de-Luchon, rue Azémar, à quelques minutes à pied des Thermes de Luchon, des allées d'Étigny et des commerces."),
            ("Peut-on loger à pied des thermes de Luchon ?", "Oui. Nos appartements sont tous à quelques minutes à pied des Thermes de Luchon : idéal pour une cure, sans avoir à prendre la voiture chaque jour."),
            ("Vos logements sont-ils proches de la télécabine de Superbagnères ?", "Oui. Depuis le centre de Luchon, la télécabine Crémaillère Express rejoint les pistes de Superbagnères en environ 8 minutes, à courte distance de nos appartements."),
            ("Faut-il une voiture pour séjourner à Luchon ?", "Non pour la ville : les thermes, les commerces, les restaurants et la télécabine se rejoignent à pied depuis nos appartements. Une voiture reste utile pour les excursions autour de Luchon (lac d'Oô, Hospice de France, vallées voisines)."),
        ]),
        ("Arrivée, clés et départ", [
            ("À quelle heure puis-je arriver dans mon appartement à Luchon ?", "L'arrivée est autonome et flexible à partir de 16h, grâce à une boîte à clés sécurisée. Vous recevez le code et toutes les instructions par e-mail avant votre venue."),
            ("Comment récupérer les clés ?", "Via une boîte à clés autonome : aucun rendez-vous nécessaire. Vous êtes libre de vos horaires d'arrivée à partir de 16h."),
            ("Puis-je arriver tard le soir à Luchon ?", "Oui, grâce à l'arrivée autonome. Signalez-nous simplement votre horaire approximatif."),
            ("À quelle heure dois-je libérer le logement ?", "Le départ se fait avant 10h le jour du check-out."),
        ]),
        ("Équipements des logements", [
            ("Combien de personnes peut-on accueillir ?", "La Perle Bleue (T2) et Le Refuge Thermal (T2) accueillent jusqu'à 4 personnes ; L'Échappée Verte (studio) jusqu'à 2 personnes."),
            ("Avez-vous un logement adapté aux personnes à mobilité réduite à Luchon ?", "Oui. Le Refuge Thermal est un appartement de plain-pied au rez-de-chaussée, particulièrement adapté aux curistes et aux personnes à mobilité réduite."),
            ("Les cuisines sont-elles équipées ?", "Oui : plaques, four ou micro-ondes, réfrigérateur, vaisselle et machine à café Nespresso. La Perle Bleue dispose en plus d'un lave-vaisselle."),
            ("Les appartements ont-ils le Wi-Fi et un lave-linge ?", "Oui. Chaque appartement dispose d'une connexion Wi-Fi haut débit gratuite et d'un lave-linge — indispensable pour un séjour de plusieurs semaines."),
            ("Les draps et serviettes sont-ils fournis ?", "Vous pouvez apporter votre linge ou le louer : 20 € par lit pour les draps, 10 € par personne pour les serviettes, pour l'ensemble du séjour."),
        ]),
        ("Animaux, ménage et services", [
            ("Peut-on venir à Luchon avec son chien ?", "Oui, les animaux sont les bienvenus dans nos appartements, moyennant 50 € par séjour et par animal. Merci de nous le signaler à la réservation. Luchon et les Pyrénées se prêtent parfaitement aux séjours avec un chien."),
            ("Le ménage est-il inclus ?", "Oui, le ménage est assuré par notre équipe après chaque séjour : ce n'est pas une option payante, c'est compris dans votre réservation."),
            ("Y a-t-il un parking à proximité à Luchon ?", "Oui, un parking gratuit se trouve à proximité de nos appartements. Les informations de stationnement vous sont transmises avec votre confirmation."),
            ("Nathalie donne-t-elle des conseils sur place ?", "Oui. Nathalie vous transmet un livret d'accueil et ses meilleurs conseils sur les activités, les restaurants et les excursions autour de Luchon."),
        ]),
        ("Cure thermale à Luchon", [
            ("Où loger pour une cure thermale à Luchon ?", "Nos trois appartements, au centre de Bagnères-de-Luchon, sont à quelques minutes à pied des thermes et pensés pour les séjours de cure. Le Refuge Thermal, de plain-pied, est spécialement adapté aux curistes et aux personnes à mobilité réduite."),
            ("Vos appartements conviennent-ils pour une cure de 18 jours ?", "Tout à fait. Cuisine équipée, lave-linge, calme et proximité immédiate des thermes : nos appartements sont adaptés aux cures conventionnées de trois semaines à Luchon."),
            ("Comment obtenir le tarif cure ?", "Les séjours de cure bénéficient d'un tarif spécial, différent des réservations classiques. Indiquez vos dates via le formulaire de notre page Cure thermale : Nathalie vous répond sous 24 h."),
        ]),
        ("Venir et se déplacer à Luchon", [
            ("Comment venir à Luchon depuis Toulouse ?", "En voiture, comptez environ 1h45 (140 km) par l'A64. En train, une ligne directe relie Toulouse-Matabiau à Luchon en environ 2h10, et la gare est en centre-ville, à courte distance de nos appartements."),
            ("Peut-on venir à Luchon en train ?", "Oui. La gare de Luchon est en centre-ville, accessible à pied depuis nos appartements : un séjour à Luchon est tout à fait possible sans voiture."),
            ("Que faire à Luchon et dans les environs ?", "Thermes et vaporarium, ski à Superbagnères, randonnées vers le lac d'Oô, rafting, parapente, et villages autour de Luchon comme Saint-Bertrand-de-Comminges. Retrouvez notre sélection sur la page Activités."),
        ]),
    ]
    faq_all = []
    groups_html = ""
    for gi, (cat_title, qas) in enumerate(faq_cats):
        faq_all += qas
        items = "".join(
            f'<div class="faq__item"><button class="faq__q" aria-expanded="false">{q}</button>'
            f'<div class="faq__a"><p>{a}</p></div></div>' for q, a in qas)
        open0 = gi == 0                      # première catégorie ouverte par défaut
        groups_html += (
            f'<div class="faq-group" data-faq-group>'
            f'<button class="faq-group__head" aria-expanded="{"true" if open0 else "false"}">'
            f'<span class="faq-group__title">{cat_title}</span>'
            f'<span class="faq-group__count">{len(qas)}</span>'
            f'<span class="faq-group__icon" aria-hidden="true"></span></button>'
            f'<div class="faq-group__body"{"" if open0 else " hidden"}><div class="faq">{items}</div></div>'
            f'</div>')
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_all]}
    faq_page = f"""
<section class="page-hero"><div class="container">{EYEBROW}<h1>Questions fréquentes sur nos appartements à Luchon</h1><p>Réservation, arrivée, équipements, animaux, accès et cure thermale : tout ce qu'il faut savoir pour louer un appartement à Bagnères-de-Luchon.</p>{BADGES}</div></section>
{breadcrumb([("Accueil", "/"), ("FAQ", None)])}
<section class="section"><div class="container" style="max-width:860px">{groups_html}
  <div class="cta-band reveal" style="margin-top:2.5rem"><h2>Une autre question ?</h2><p>Nathalie vous répond avec plaisir, avant comme pendant votre séjour.</p><a class="btn btn--dark btn--lg" href="/contact/">Nous contacter</a>
</div>
</div></section>
"""
    page("faq/index.html", "/guide/", "FAQ — Louer un appartement à Luchon : réservation, séjour, accès | Les Meublés de Luchon",
         "Questions fréquentes sur la location d'un appartement à Luchon (Bagnères-de-Luchon) : réserver en direct, arrivée autonome, proximité des thermes, animaux, cure thermale et accès depuis Toulouse.",
         faq_page, ld_blocks=[faq_ld])

    # =====================================================================
    # Fichiers techniques
    # =====================================================================
    write_tech(g)


# ------- helpers de contenu -------
def diapo(g, photos, interval=2500):
    """Diaporama automatique : réutilise le carrousel des cartes logement."""
    slides = "".join(
        f'<div class="card__slide"><img src="/assets/img/logements/{dossier}/{fichier}" alt="{alt}" '
        f'loading="lazy" width="600" height="480"></div>'
        for dossier, fichier, alt in photos)
    dots = "".join(
        f'<button class="card__dot" type="button" aria-label="Voir la photo {n + 1}"'
        + (' aria-current="true"' if n == 0 else '') + '></button>'
        for n in range(len(photos)))
    return f"""<div class="card__slider diapo" data-slider data-interval="{interval}">
        <div class="card__slides">{slides}</div>
        <button class="card__arrow card__arrow--prev" type="button" aria-label="Photo précédente">‹</button>
        <button class="card__arrow card__arrow--next" type="button" aria-label="Photo suivante">›</button>
        <div class="card__dots">{dots}</div>
      </div>"""


def logement_card(g, key, reveal=True, cta=None, link_photos=True):
    """cta = (libellé, href) pour remplacer le bouton Réserver (page Cure : tarif différent)."""
    LOGEMENTS = g["LOGEMENTS"]; stars_html = g["stars_html"]
    d = LOGEMENTS[key]
    base = f"/assets/img/logements/{d['slug']}/"
    imgs = d["images"][:5]
    if link_photos:
        slides = "".join(
            f'<a class="card__slide" href="/appartements/{key}/" aria-label="{alt}">'
            f'<img src="{base}{fn}" alt="{alt}" loading="lazy" width="600" height="450"></a>'
            for fn, alt in imgs)
    else:
        slides = "".join(
            f'<div class="card__slide">'
            f'<img src="{base}{fn}" alt="{alt}" loading="lazy" width="600" height="450"></div>'
            for fn, alt in imgs)
    dots = "".join(
        f'<button class="card__dot" type="button" aria-label="Voir la photo {n + 1}"'
        + (' aria-current="true"' if n == 0 else '') + '></button>'
        for n in range(len(imgs)))
    rc = " reveal" if reveal else ""
    return f"""<article class="card{rc}">
        <div class="card__slider" data-slider>
          <span class="card__tag">{stars_html(d['stars'])} Meublé de Tourisme</span>
          <div class="card__slides">{slides}</div>
          <button class="card__arrow card__arrow--prev" type="button" aria-label="Photo précédente">‹</button>
          <button class="card__arrow card__arrow--next" type="button" aria-label="Photo suivante">›</button>
          <div class="card__dots">{dots}</div>
        </div>
        <div class="card__body">
          <h3>{d['name']}</h3>
          <p class="card__tagline">{d['tagline']}</p>
          <div class="card__meta"><span>🛏️ {d['type'].split(' ')[0]}</span><span>👥 Jusqu'à {d['capacity']} pers.</span><span>🏢 {d['floor']}</span><span>📍 Centre-ville</span></div>
          <p>{d['short']}</p>
          <div class="card__foot">
            <a class="btn btn--primary" href="{cta[1] if cta else f'/appartements/{key}/#reserver'}">{cta[0] if cta else 'Réserver'}</a>
          </div>
        </div>
      </article>"""


def faq_section(g, qas):
    jsonld = g["jsonld"]
    items = ""
    for q, a in qas:
        items += (f'<div class="faq__item"><button class="faq__q" aria-expanded="false">{q}</button>'
                  f'<div class="faq__a"><p>{a}</p></div></div>')
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}
    return (f'<section class="section"><div class="container"><div class="center reveal" style="margin-bottom:2rem">'
            f'<p class="eyebrow">Questions fréquentes</p><h2>Bon à savoir</h2></div>'
            f'<div class="faq">{items}</div></div>{jsonld(ld)}</section>')


def write_tech(g):
    write = g["write"]; BASE = g["BASE_URL"]
    # robots.txt
    write("robots.txt", f"""User-agent: *
Allow: /
Disallow: /404.html

Sitemap: {BASE}/sitemap.xml
""")
    # sitemap.xml
    urls = [
        ("/", "1.0", "weekly"),
        ("/appartements/", "0.9", "weekly"),
        ("/appartements/la-perle-bleue/", "0.9", "weekly"),
        ("/appartements/l-echappee-verte/", "0.9", "weekly"),
        ("/appartements/le-refuge-thermal/", "0.9", "weekly"),
        ("/cure-thermale/", "0.9", "monthly"),
        ("/services/", "0.7", "monthly"),
        ("/activites/", "0.7", "monthly"),
        ("/guide/", "0.7", "monthly"),
        ("/guide/cure-thermale-a-luchon/", "0.8", "monthly"),
        ("/guide/ski-a-superbagneres/", "0.8", "monthly"),
        ("/guide/venir-a-bagneres-de-luchon/", "0.7", "monthly"),
        ("/guide/louer-avec-son-chien-a-luchon/", "0.7", "monthly"),
        ("/faq/", "0.7", "monthly"),
        ("/avis/", "0.7", "monthly"),
        ("/contact/", "0.6", "monthly"),
        ("/plan-du-site/", "0.3", "yearly"),
        ("/mentions-legales/", "0.2", "yearly"),
        ("/politique-de-confidentialite/", "0.2", "yearly"),
    ]
    body = "\n".join(
        f'  <url><loc>{BASE}{u}</loc><changefreq>{cf}</changefreq><priority>{p}</priority></url>'
        for u, p, cf in urls)
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
""")
    # .htaccess (production Apache/OVH)
    write(".htaccess", """# === Les Meublés de Luchon — configuration Apache ===
Options -Indexes
DirectoryIndex index.html

# --- Forcer HTTPS + non-www ---
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\\.(.*)$ [NC]
RewriteRule ^ https://lesmeublesdeluchon.com%{REQUEST_URI} [R=301,L]

# --- URLs propres : /page renvoie /page/ ---
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} !(/$|\\.)
RewriteRule ^(.*)$ /$1/ [R=301,L]

# --- Redirections 301 des anciennes URLs WordPress ---
Redirect 301 /nos-services/ /services/
Redirect 301 /reservez-maintenant/ /appartements/
Redirect 301 /vos-avis/ /avis/
Redirect 301 /politique-de-confidentialite-2/ /politique-de-confidentialite/
Redirect 301 /politique-des-cookies/ /politique-de-confidentialite/

# --- Page d'erreur personnalisée ---
ErrorDocument 404 /404.html

# --- En-têtes de sécurité ---
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
</IfModule>

# --- Cache navigateur ---
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
</IfModule>

# --- Compression ---
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml
</IfModule>
""")
