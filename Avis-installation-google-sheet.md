# Brancher la page « Laissez votre avis » sur un Google Sheet

La page existe déjà : **/deposer-un-avis/** (design maison, étoiles, non listée dans le menu — à envoyer par lien, e-mail, SMS ou QR code).

Il reste **une seule chose** à faire côté Google (compte de Nathalie/Gérard) pour recevoir les avis et les valider avant publication. ~10 minutes, une fois pour toutes.

---

## 1. Créer le Google Sheet
1. Aller sur **sheets.google.com** → nouveau tableur, le nommer par ex. **« Avis site Meublés de Luchon »**.
2. En ligne 1, créer ces colonnes (exactement) :
   `date` · `note` · `prenom` · `ville` · `message` · **`publier`**
3. La colonne **`publier`** est la case à cocher de modération : on met une **case à cocher** (Menu *Insertion → Case à cocher*). Décochée = brouillon ; cochée = publié.

## 2. Ajouter le petit script de réception
1. Dans le Sheet : menu **Extensions → Apps Script**.
2. Coller ce code (remplacer tout) :

```javascript
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var p = e.parameter;
  sheet.appendRow([
    new Date(),
    p.note || '',
    p.prenom || '',
    p.ville || '',
    p.message || '',
    false            // "publier" décoché par défaut = brouillon
  ]);
  return ContentService.createTextOutput('ok');
}
```

3. **Déployer** : bouton *Déployer → Nouveau déploiement → Type : Application Web*.
   - « Exécuter en tant que » : **moi**.
   - « Qui a accès » : **Tout le monde**.
   - Cliquer *Déployer*, autoriser l'accès quand Google le demande.
4. Google donne une **URL** qui finit par `…/exec`. **C'est elle qu'il me faut.**

## 3. Me transmettre l'URL
M'envoyer cette URL `…/exec` : je la mets dans la page à la place du texte `REMPLACER-PAR-VOTRE-URL-APPS-SCRIPT`, et les avis commenceront à tomber dans le Sheet.

---

## Comment ça marchera ensuite
- Un voyageur remplit la page → l'avis arrive **dans le Sheet**, colonne `publier` **décochée** (brouillon).
- Nathalie ouvre le Sheet, lit l'avis, **coche `publier`** si tout va bien.
- Sur le site, **seuls les avis cochés** apparaissent — les autres restent invisibles. Le spam ne s'affiche jamais tout seul.

## Points à retenir
- **Gratuit**, aucun compte pour le visiteur, un piège anti-robot est déjà intégré à la page.
- On affiche **tous** les avis validés (pas seulement les 5 étoiles) : masquer les avis mitigés est interdit en France, et un site 100 % parfait inspire moins confiance.
- La page n'est pas indexée par Google (normal, c'est un formulaire) : on la diffuse par lien / QR code après le séjour.
