
# **Le jeu Démineur avec intégration de l’IA**


###  **Aperçu**
![image](https://github.com/user-attachments/assets/edfc8046-5b1e-49e7-b336-05897fd97d70)

Ce projet combine le jeu classique de **Démineur** avec une intelligence artificielle capable d'apprendre à y jouer de manière autonome. Développée dans le cadre d’un projet académique, elle utilise l’algorithme **Deep Q-Learning (DQN)** pour permettre à un agent de parcourir la grille, éviter les mines et maximiser ses récompenses par l’apprentissage par essai-erreur. La plateforme est construite de manière modulaire  moteur de jeu, modèle d’IA, pipeline d’entraînement et interface visuelle  ce qui garantit une bonne lisibilité du code et une extensibilité pour de futures améliorations.

Ce projet a été développé durant l’année universitaire **2024/2025**, dans le cadre du module de Modelisation Avancee et Theorie des Graphes


###  **Fonctionnalités**

* **Jeu de Démineur classique** : Profitez du jeu traditionnel avec une grille fonctionnelle, des drapeaux et une logique complète de gestion des mines.
* **Agent intelligent** : L’IA apprend à jouer au Démineur grâce à l’apprentissage par renforcement profond via un **Deep Q-Network (DQN)**.
* **Pipeline d'entraînement** : Entraînez l’agent avec `train.py`, incluant une mémoire de rejouabilité, une stratégie d’exploration et une adaptation des récompenses.
* **Suivi via TensorBoard** : Suivi en temps réel des performances et de la perte via **TensorBoard**.
* **Feedback sonore et visuel** : Inclut des effets sonores et des retours visuels pour les victoires, les défaites et la progression du jeu.
* **Mémoire de rejouabilité** : Sauvegarde les expériences de jeu pour améliorer l’apprentissage de l’IA.


🗂 Structure de Projet 
<pre> 
  .
├── DQN
│   ├── DQN.py
│   ├── DQN_agent.py
│   ├── minesweeper_env.py
│   ├── my_tensorboard2.py
│   ├── test.py
│   ├── train.py
│   ├── models
│   ├── replay
│   └── logs
│       └── conv64x4_dense512x2_y0.1_minlr0.001
├── DimineurGame
│   └── logs
│       └── conv64x4_dense512x2_y0.1_minlr0.001
│           ├── events.out.tfevents.1746742238.DESKTOP-2Q5NU70.12844.0.v2
│           └── train
├── creationAI
│   ├── creation.py
│   ├── documetation.md
│   └── pics
├── images
├── logs
├── mines
│   ├── ChampMines.py
│   └── mine.py
├── models
│   └── conv64x4_dense512x2_y0.1_minlr0.001.h5
├── replay
│   └── conv64x4_dense512x2_y0.1_minlr0.001.pkl
├── sounds
│   ├── ai_move.wav
│   ├── defeat.mp3
│   ├── put_flag.wav
│   ├── reveal_move.wav
│   └── victory.wav
├── .gitignore
├── LICENSE
├── README.md
├── ai.py
├── constants.py
├── grille.py
├── main.py
├── minesweeper.log
├── my_tensorboard.py

</pre>


**Comment fonctionne l’IA**

L’agent IA utilise un Deep Q-Network (DQN) avec une politique ε-greedy. Il interagit avec l’environnement (la grille), reçoit des récompenses pour les coups sûrs et des pénalités lorsqu’il touche une mine. Les valeurs Q sont apprises par rétropropagation en fonction de l’expérience de l’agent.

**Concepts clés :**

* États : Représentation de la grille actuelle.
* Actions : Choisir une cellule à cliquer.
* Récompenses :+10 pour une victoire, -10 pour une défaite (clic sur une mine), +1 pour un clic utile (progrès), -1 pour un clic au hasard ou sans progrès..
* Réseau de neurones : Couches entièrement connectées pour approximer les valeurs Q.
* Replay Buffer : Stocke les coups passés pour l’entraînement par batch.

**Pour commencer**
**Prérequis**

* Python 3.8+
* pip
* TensorFlow / Keras
* pygame
* NumPy
* TensorBoard


**Fichier requirements.txt**

C’est un fichier texte qui liste toutes les bibliothèques Python nécessaires au projet. En exécutant la commande `pip install -r requirements.txt`, toutes ces dépendances sont automatiquement installées, ce qui facilite la configuration de l’environnement de travail.

## Guide de démarrage

1. **Installer les dépendances**

Ouvre un terminal dans le dossier du projet et exécute :
```
pip install -r requirements.txt
```

2. **Lancer le projet**
    
pour lancer le jeu exécutez le fichier principal `main.py`

---
Nous tenons à remercier Monsieur Stephen Lee pour son dépôt https://github.com/sdlee94/Minesweeper-AI-Reinforcement-Learning, qui nous a vraiment aidés à comprendre comment intégrer le Deep Q-Network (DQN) dans notre projet de Démineur


