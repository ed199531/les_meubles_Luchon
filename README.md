# Les Meublés de Luchon — Refonte 2026

Refonte complète du site [lesmeublesdeluchon.com](https://lesmeublesdeluchon.com) : site statique moderne, rapide, responsive, optimisé SEO/GEO, à partir de l'existant (charte, photos, contenus, moteur de réservation Superhôte).

## 🚀 Lancer le site en local

```bash
cd "Les meublés de Luchon"
python3 serve.py
```
Puis ouvrir **http://localhost:8137**

Le serveur sert le dossier `site/` avec des URLs propres (dossiers `index.html`).

## 📁 Structure

```
Les meublés de Luchon/
├── serve.py              # Serveur local (port 8137)
├── build.py              # Générateur (source de vérité : header, footer, SEO, NAP)
├── build_pages.py        # Contenu de chaque page
├── site/                 # ← Site généré (à mettre en production)
│   ├── index.html
│   ├── nos-logements/    (+ la-perle-bleue, l-echappee-verte, le-refuge-thermal)
│   ├── services/  activites/  avis/  reservation/  contact/
│   ├── mentions-legales/  politique-de-confidentialite/  plan-du-site/
│   ├── 404.html  robots.txt  sitemap.xml  .htaccess
│   └── assets/  (css, js, img)
```

**Pour modifier le site :** éditer `build_pages.py` (contenu) ou `build.py` (structure/SEO), puis relancer `python3 build.py`. Le CSS/JS s'éditent directement dans `site/assets/`.

## 🎨 Charte (reprise et modernisée de l'existant)

- **Couleurs** : `#026878` (teal thermal), `#00444f` (teal foncé), `#3ab0b3` (teal clair), `#ff705c` (corail), `#212121` (texte).
- **Polices** : Unna (titres, serif) + Open Sans (corps) — identiques à l'ancien site.

## ✅ Standards appliqués

- **SEO** : title/meta uniques par page, canonical, sitemap.xml, robots.txt, fil d'ariane cliquable + `BreadcrumbList`, Open Graph + Twitter Cards, `alt` sur toutes les images, URLs propres.
- **GEO / IA** : Schema.org riche (`LodgingBusiness`, `Apartment`, `FAQPage`, `Service`, `Review`), FAQ en réponses directes, NAP cohérent partout.
- **Sécurité** (`.htaccess`) : HTTPS forcé, www → non-www, en-têtes (X-Frame-Options, X-Content-Type-Options, HSTS, Referrer-Policy), 301 des anciennes URLs WordPress.
- **Performance** : images redimensionnées, `loading="lazy"`, `width`/`height`, fonts en `preconnect`, JS en `defer`.
- **Accessibilité** : mobile-first, HTML sémantique, `aria-*`, lien d'évitement, contrastes AA, fallback `<noscript>`.
- **CNIL** : bandeau de consentement — **aucun traceur avant accord**.

## 🔑 Réservation (fonctionnelle)

Le widget reconstruit les liens du moteur **Superhôte** existant :
- **La Perle Bleue** → `propertyKeyhYHKfobjxVxjHhLTkzJPTehXA`
- **L'Échappée Verte** → `propertyKey3VpakNcQ3X2LlAXOTujQsws6e`
- **Le Refuge Thermal** → pas de clé Superhôte connue : bascule sur une **demande e-mail pré-remplie** (à remplacer par la clé quand elle sera disponible, dans `site/assets/js/main.js`).

## 🛠️ À compléter avant mise en production

1. **Mentions légales** : SIRET, statut juridique, responsable de publication, hébergeur (placeholders en place).
2. **Le Refuge Thermal** : ajouter la **clé Superhôte** dans `main.js` pour activer la réservation en ligne directe (les vraies photos sont déjà intégrées ; en attendant, réservation par demande e-mail).
3. **Analytics** : coller l'ID Google Analytics 4 dans la fonction `loadAnalytics()` de `main.js` (déjà conditionné au consentement).
4. **WebP** : `sips` (macOS) n'écrit pas le WebP. Sur le serveur de prod, convertir avec `cwebp` pour un gain de poids supplémentaire.
5. **Search Console + Bing Webmaster** : soumettre `https://lesmeublesdeluchon.com/sitemap.xml`.
6. **Avis** : synchroniser les vrais avis depuis la source (SuperHote / Google) — quelques avis d'illustration sont en place.
```
