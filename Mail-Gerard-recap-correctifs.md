# E-mail récapitulatif à Gérard — correctifs apportés

**Objet :** Vos 95 retours ont été traités — le site est à jour, voici le détail

---

Bonjour Gérard,

J'ai repris l'intégralité de vos commentaires, page par page. La très grande majorité est appliquée et en ligne. Je vous fais un point détaillé ci-dessous — c'est un peu long, mais je préfère que vous sachiez exactement ce qui a été fait et surtout **pourquoi**, plutôt que de vous laisser redécouvrir les changements sans explication.

**Le site à jour :** https://les-meubles-luchon.vercel.app

Un conseil avant de regarder : faites **Ctrl+Maj+R** (ou Cmd+Maj+R sur Mac) pour forcer le rechargement. Sinon votre navigateur risque de vous réafficher l'ancienne version qu'il a gardée en mémoire.

---

## 1. Le vocabulaire

Vous aviez raison sur toute la ligne, et c'est le genre de détail qui change la perception d'un site.

- **« Appartements »** partout, à la place de « logements » et « hébergements ». C'est le mot que vos clients emploient, et c'est aussi celui qu'ils tapent sur Google.
- **« Rénové » retiré** de toutes les descriptions.
- **« Voyageurs »** au lieu de « personnes » dans les formulaires de réservation — c'est le terme du secteur, celui qu'on retrouve sur Airbnb ou Booking.
- Les libellés des formulaires ont été **explicités** : « Votre prénom et nom » plutôt que « Votre nom », « Votre numéro de téléphone » plutôt que « Téléphone », avec un exemple de saisie affiché en gris dans chaque champ. Pour quelqu'un qui n'est pas à l'aise avec l'informatique, ça évite les hésitations et les envois incomplets.

## 2. La cohérence visuelle

Plusieurs de vos remarques revenaient à la même chose : ça manquait d'unité.

- **Les boutons** ont été ramenés à trois styles seulement, avec un comportement identique au survol. Avant, on avait des tailles, des couleurs et des arrondis qui variaient d'une page à l'autre — c'est typiquement ce qui donne une impression d'amateurisme sans qu'on sache dire pourquoi.
- **Les titres** suivent une échelle unique sur les 21 pages.
- **Tous les boutons « Réserver »** mènent désormais au même endroit : la page Appartements, où se trouve le moteur de réservation. Avant, certains renvoyaient vers une page intermédiaire — un clic perdu, et un client qui décroche.
- **Les cartes d'avis** ont toutes la même hauteur, avec un « Lire la suite » pour les textes longs. Les blocs de tailles inégales, c'était effectivement pas terrible.

## 3. La réservation — le gros morceau

C'est là que le travail a été le plus technique.

**Le moteur Superhôte est maintenant intégré directement dans le site.** Concrètement : le visiteur choisit ses dates, voit les appartements disponibles, réserve et paie **sans jamais quitter votre site**. Avant, il basculait sur une page Superhôte extérieure — et à chaque changement de site, on perd du monde.

**Un filtre a été posé** pour que seuls vos trois appartements remontent. La Maison du Coué, qui ne fait pas partie des Meublés de Luchon, n'apparaît plus.

**J'ai ajouté nos propres champs de dates au-dessus du moteur.** Le calendrier de Superhôte s'ouvre en plein écran, ce qui est assez brutal — je ne peux pas le modifier, c'est un outil externe. En plaçant nos champs avant, le visiteur choisit ses dates chez nous, dans un calendrier au design du site, et le moteur se recharge déjà filtré. Il n'a jamais besoin d'ouvrir la fenêtre plein écran.

**Le sélecteur de voyageurs** distingue adultes, enfants et bébés, comme sur les plateformes de réservation.

**Les adresses exactes** des trois appartements sont désormais affichées (rue Azémar, avec l'étage). Pour le référencement local, c'est important : Google recoupe ces informations avec votre fiche d'établissement.

## 4. La page Cure thermale

Vous m'aviez signalé que les séjours de cure ne sont pas au tarif classique. C'était plus qu'un détail de présentation : **il y avait un vrai risque commercial.**

Un curiste qui cliquait sur « Réserver » pouvait réserver 18 jours au tarif normal. Impossible à rattraper ensuite sans annuler et froisser le client.

J'ai donc retiré de cette page **tout ce qui menait à la réservation en ligne** : les photos ne sont plus cliquables, et les boutons renvoient vers un formulaire **« Demander le tarif cure »**. J'ai évité « demande de devis », qui fait un peu froid — le visiteur cherche un tarif, autant le dire simplement.

Ce formulaire intègre un **calendrier** pour les dates de cure, à la place du champ texte libre. Nathalie recevra des dates exploitables plutôt qu'un « début septembre je crois » — et l'envoi est bloqué tant que les dates ne sont pas renseignées.

La page présente bien **les trois appartements**, pas seulement le Refuge Thermal, puisque les trois accueillent des curistes.

## 5. Le menu

Vous vouliez voir la FAQ dans le menu. Le problème : on arrivait à neuf entrées, et sur un écran de portable ça débordait.

J'ai donc regroupé la FAQ et les guides pratiques sous une entrée **« Infos pratiques »**. Vos deux demandes sont satisfaites — la FAQ est accessible depuis le menu, et le menu reste lisible sur mobile.

## 6. Les avis

Point important : **j'ai récupéré les 77 avis authentiques de votre ancien site.** Rien n'a été ressaisi, rien n'a été inventé. Ils défilent sur la page d'accueil pour montrer le volume, et sont tous consultables sur la page dédiée.

Je préfère être transparent sur un point : **je n'ai pas ajouté de note moyenne en étoiles.** Elle serait fabriquée, puisque les avis récupérés n'en comportent pas, et Google pénalise les notes non vérifiables. C'est un sujet à part entière qu'on peut traiter proprement — je vous en parle plus bas.

## 7. La page Activités

Elle a été entièrement repensée : **21 activités**, avec deux menus déroulants pour filtrer par **secteur** (Luchon, Superbagnères, Autour de Luchon, Peyragudes, Le Mourtis, vallées voisines) et par **type** (ski, thermes, randonnée, eaux vives, patrimoine…).

J'ai repris les secteurs de l'office de tourisme, pour que ça parle aux gens qui connaissent la région.

Deux choix volontaires :

- **Aucun tarif ni horaire.** Ça change chaque saison, et une information périmée sur votre site, c'est un client mécontent au téléphone. Un lien renvoie vers l'office de tourisme pour les informations à jour.
- **Cinq activités portent la mention « À pied depuis nos appartements »** (thermes, allées d'Étigny, télécabine…). C'est votre meilleur argument et personne d'autre ne peut l'écrire : vous êtes au centre. Ça transforme une page d'information en argument de réservation.

**Un point à valider avec vous :** j'ai rédigé ces descriptions à partir de mes recherches, mais vous connaissez le terrain bien mieux que moi. Un rapide coup d'œil de votre part sur les mentions « à pied » et sur les éventuels oublis serait précieux.

## 8. Ce qui ne se voit pas, mais qui compte

- **Redirections en place** depuis les anciennes adresses : les visiteurs et le référencement acquis ne sont pas perdus.
- **Titres et descriptions uniques** sur chaque page, plan du site, fil d'ariane, données structurées pour Google.
- **En-têtes de sécurité** et connexion sécurisée.
- **Bandeau cookies conforme CNIL** : aucun outil de mesure ne se déclenche avant votre accord.
- **Photos redimensionnées et chargées à la demande** pour la vitesse — c'est un critère de classement chez Google, et surtout de patience chez vos visiteurs.
- **Barre fixe en bas d'écran sur mobile** avec « Appeler » et « Réserver », toujours à portée de pouce. La majorité de vos visiteurs sont sur téléphone.
- La photo du chien était **coupée à la tête** dans deux cadres différents : recadrée.

---

## Ce dont j'aurais besoin de vous

Rien d'urgent, mais ça débloquerait les derniers points :

1. **Vos photos.** Superbagnères, le lac d'Oô, les allées d'Étigny, la Fête des Fleurs… Vos propres photos valent mieux que n'importe quelle banque d'images : elles sont authentiques, et Google les valorise davantage. J'en ai une un peu trop petite à remplacer (celle de la luge).
2. **Un test du parcours de réservation de votre côté**, sur une période que vous savez disponible. J'ai vu une recherche revenir vide sur des dates d'été et je préfère qu'on écarte tout doute sur le paramétrage Superhôte.
3. **Votre avis sur les avis clients** : souhaitez-vous que les locataires puissent en déposer directement ? Si oui, il faut prévoir une validation avant publication — sinon la porte est ouverte aux messages indésirables.

## Deux points que je souhaiterais discuter avec vous

Vous les aviez signalés et je ne les ai **volontairement pas appliqués**, parce que je pense qu'ils vous desserviraient. Je peux me tromper, et c'est votre site — j'en parle sans a priori :

**Le fil d'ariane** (le petit « Accueil › Activités » en haut des pages). Je comprends qu'il alourdisse visuellement. Mais il indique à Google la structure du site, et il s'affiche dans les résultats de recherche. Sur mobile, il aide aussi à revenir en arrière sans se perdre. Je propose qu'on le regarde ensemble : je peux l'alléger visuellement sans le supprimer.

**Les trois fiches détaillées par appartement.** Ce sont elles qui vous positionnent sur des recherches comme « La Perle Bleue Luchon » ou « appartement plain-pied Luchon ». Le moteur Superhôte, lui, est invisible pour Google — son contenu ne peut pas être indexé. Les supprimer reviendrait à perdre du référencement sans rien gagner.

---

Je reste évidemment ouvert à échanger sur tout ça. **Le mieux serait qu'on se voie** : on reprend le site ensemble, vous me montrez ce qui vous gêne encore, et on ajuste en direct. Certains points se règlent en deux minutes de vive voix alors qu'ils prennent dix e-mails.

Dites-moi vos disponibilités.

Bien à vous,

**Edwin**
Localisia
edwin@localisia.fr

---

*P.-S. — Si vous repérez d'autres choses en parcourant le site, n'hésitez pas à laisser vos commentaires directement sur les pages comme vous l'aviez fait : c'est le système le plus clair pour moi, je retrouve chaque remarque avec la page et l'endroit exact.*
