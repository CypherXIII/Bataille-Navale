# Bataille Navale

Bienvenue dans le jeu de la Bataille Navale ! Ce projet est une version en ligne de commande du célèbre jeu de société où deux joueurs s'affrontent en plaçant stratégiquement leurs navires et en essayant de couler ceux de l'adversaire.

## Fonctionnalités

- Jouez à deux joueurs
- Jouez contre l'IA avec trois niveaux de difficulté (Facile, Moyen, Difficile)
- Mode de jeu où deux IA s'affrontent
- Sauvegarde et reprise de la partie en cours
- Affichage des 10 meilleurs scores
- Interface utilisateur en ligne de commande avec du texte centré et coloré

## Installation

1. Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/CypherXIII/Bataille-Navale.git
```

2. Accédez au répertoire du projet :

```bash
cd Bataille-Navale
```

3. Installez les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

## Utilisation

Pour lancer le jeu, exécutez le script principal :

```bash
python script.py
```

### Menu Principal

1. Jouer à 2 joueurs
2. Jouer contre l'IA
3. Deux IA l'une face à l'autre
4. Voir les règles du jeu
5. Voir les statistiques
6. Quitter le jeu

### Règles du Jeu

- Chaque joueur dispose d’une grille de 10 cases sur 10.
- Les colonnes de la grille sont indiquées par une lettre de A à J et les lignes sont numérotées de 1 à 10.
- Chaque joueur place 5 bateaux sur sa grille :
  - Un porte-avions (5 cases)
  - Un croiseur (4 cases)
  - Un contre-torpilleurs (3 cases)
  - Un sous-marin (3 cases)
  - Un torpilleur (2 cases)
- Le but est de couler tous les bateaux de l’adversaire en devinant leurs positions.

### Sauvegarder et Reprendre une Partie

Le jeu sauvegarde automatiquement votre progression dans un fichier de sauvegarde. Lors du prochain lancement, il vous sera demandé si vous souhaitez reprendre la partie en cours.

## Dépendances

- numpy
- colorama

## Licence

Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus de détails.

## Remerciements

Merci d'avoir joué ! Si vous avez des suggestions ou des commentaires, n'hésitez pas à les partager. Amusez-vous bien avec la Bataille Navale !

---

**Remarque :** Ce projet est une implémentation simple du jeu de la Bataille Navale pour l'apprentissage et le divertissement. Certaines fonctionnalités avancées peuvent ne pas être présentes.
