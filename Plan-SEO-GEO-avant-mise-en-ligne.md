# Plan SEO / GEO — à faire avant et au moment de la mise en ligne
*Audit technique du site déployé + de l'ancien domaine. État au 21 juillet 2026.*

---

## A. Ce qui est DÉJÀ en place (rien à refaire)

Vérifié directement sur le site — la base technique est solide :

- **Titres et descriptions uniques** sur chaque page (pas de doublons, tous géolocalisés Luchon / Bagnères-de-Luchon).
- **Toutes les images ont un attribut alt** (bon pour l'accessibilité et Google Images).
- **Données structurées présentes** : LodgingBusiness + coordonnées GPS (accueil), Apartment (fiches), Service (cure), FAQPage (FAQ + pages), BreadcrumbList (fil d'ariane) partout.
- **Sitemap.xml** (19 pages) et **robots.txt** en place, pointant déjà vers le domaine final.
- **Canonicals** corrects sur le domaine final `lesmeublesdeluchon.com`.
- **En-têtes de sécurité**, HTTPS, et redirections des anciennes URL déjà prévues (/reservez-maintenant/, /reservation/, /nos-services/, /vos-avis/…).

Autrement dit : le référencement **technique** est prêt. Ce qui suit, c'est la mise en ligne propre + le travail qui fait vraiment remonter (local + contenu + IA).

---

## B. LE JOUR DE LA MISE EN LIGNE (critique — à ne pas rater)

C'est là que se gagne ou se perd le référencement acquis par l'ancien site.

1. **Brancher le domaine `lesmeublesdeluchon.com` sur le nouveau site (Vercel).**
   Aujourd'hui, le domaine sert encore l'ancien site WordPress (serveur Apache). Tant que ce n'est pas basculé, les canonicals du nouveau site pointent vers du contenu qui n'existe pas encore. → Action Vercel, à faire en une fois.

2. **Vérifier les redirections des anciennes URL (301).**
   L'ancien site a des adresses comme `/reservez-maintenant/` qui répondent encore. Chaque ancienne URL qui disparaît doit être **redirigée** vers la nouvelle équivalente, sinon on perd le classement Google de ces pages et on crée des erreurs 404. Une partie est déjà couverte ; il faut **lister toutes les URL indexées de l'ancien site** (via la Search Console de Gérard) et compléter les redirections manquantes.

3. **Forcer www → sans-www et http → https sur le nouveau domaine.**
   Ça fonctionne aujourd'hui sur l'ancien serveur ; il faut s'assurer que Vercel le refait (sinon Google voit deux sites = contenu dupliqué).

4. **Empêcher l'indexation de l'adresse de test `les-meubles-luchon.vercel.app`.**
   Elle est actuellement ouverte aux moteurs. Risque : Google indexe la version test en double du vrai site. À bloquer (noindex ou accès restreint) au moment du lancement.

---

## C. DANS LES JOURS QUI SUIVENT (indexation)

5. **Google Search Console** : ajouter le domaine, **soumettre le sitemap.xml**, demander l'indexation des pages principales. C'est ce qui accélère la prise en compte par Google et permet de suivre les positions.
6. **Bing Webmaster Tools** : même chose (Bing alimente aussi les réponses de ChatGPT et Copilot → utile pour le GEO).
7. **Google Analytics 4** : à connecter (le bandeau cookies conforme est déjà prêt, le tracking ne se déclenche qu'après consentement). Permet de mesurer d'où viennent les réservations.

---

## D. LE PLUS GROS LEVIER : la fiche Google Business Profile

Pour un meublé, **80 % de la visibilité locale se joue ici**, pas sur le site.

8. **Créer / revendiquer la fiche Google Business Profile** « Les Meublés de Luchon ».
   - C'est ELLE qui fait apparaître l'établissement dans Google Maps et le « pack local » (les 3 résultats avec carte).
   - C'est ELLE, et seulement elle, qui affiche les **étoiles jaunes** dans Google (pas les avis du site).
9. **Cohérence NAP (Nom – Adresse – Téléphone)** : l'adresse, le nom et le téléphone doivent être **identiques au caractère près** entre le site, la fiche Google et tous les annuaires. *À trancher avec Gérard :* le site indique « 5 rue Azémar » alors que les appartements sont au 5 bis et 5A — il faut fixer **une** adresse officielle d'établissement et l'utiliser partout.
10. **Inscription dans les annuaires locaux** : Office de Tourisme Pyrénées 31, Gîtes/Clévacances si applicable, annuaires de meublés. Chaque citation cohérente renforce le local.

---

## E. GEO / IA — se faire citer par ChatGPT, Perplexity, Google AI Overviews

Le site est déjà construit pour ça, il faut activer le reste :

11. **Le schema FAQPage et les réponses directes** (déjà en place) sont ce que les IA extraient. On l'a optimisé aujourd'hui.
12. **Être présent sur les sources que les IA lisent** : la fiche Google, l'Office de Tourisme, et idéalement quelques mentions externes (presse locale, blogs voyage). Les IA citent ce qui est confirmé par plusieurs sources.
13. **Avis** : le futur formulaire d'avis + les avis Google nourrissent la confiance que les IA reprennent (« bien noté, proche des thermes »).
14. **Contenu qui répond à des questions réelles** (guides + FAQ) : c'est le format que les IA adorent. On a la cure, le ski, l'accès, le chien — on pourra en ajouter.

---

## F. CONTENU & SUIVI (les semaines suivantes)

15. **Renforcer les pages sur les requêtes qui rapportent** : « location cure thermale Luchon », « appartement Luchon centre », « meublé Luchon proche thermes ». Le maillage interne est déjà là.
16. **Photos authentiques de Gérard/Nathalie** (Superbagnères, lac d'Oô, Fête des Fleurs) : Google valorise les photos originales, et elles servent aussi la fiche Google.
17. **Suivi mensuel** des positions et du trafic (Search Console) pour ajuster.

---

## G. Ce dont on a besoin de Gérard

- **Les accès à la Search Console** de l'ancien site (pour récupérer la liste des URL à rediriger et ne rien perdre).
- **La fiche Google Business Profile** : existe-t-elle déjà ? Qui la gère ? À revendiquer si besoin.
- **L'adresse d'établissement officielle** à figer (point NAP ci-dessus).
- **Le feu vert pour la bascule du domaine** vers le nouveau site, et le moment choisi.
- **Ses photos** pour finaliser.

---

**En résumé pour Gérard :** le site est techniquement prêt à être bien référencé. Le vrai travail de visibilité, maintenant, c'est **(1)** une bascule de domaine propre avec les redirections, **(2)** la fiche Google Business (le nerf de la guerre en local et pour les étoiles), et **(3)** les avis + les citations externes qui font remonter sur Google et dans les IA.
