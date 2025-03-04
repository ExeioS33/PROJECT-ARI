# ARI NLP Development Environment

## 📋 Description

Image Docker personnalisée pour le développement et l'expérimentation NLP, basée sur l'image [huggingface/transformers-pytorch-gpu](https://hub.docker.com/r/huggingface/transformers-pytorch-gpu) avec des fonctionnalités supplémentaires.

Cette image a été optimisée pour les phases de développement et de POC (Proof of Concept) dans les projets d'IA et de NLP, en facilitant la création rapide de pipelines RAG (Retrieval Augmented Generation) et l'expérimentation avec les modèles Transformers.

## 🔍 Caractéristiques

- **Base**: Image huggingface/transformers-pytorch-gpu avec PyTorch et support CUDA
- **Environnement Jupyter**: JupyterLab préconfiguré et prêt à l'emploi
- **LangChain**: Intégration complète pour la création de pipelines RAG
- **Bind Volume**: Configuration optimisée pour lier des volumes locaux
- **Outils NLP supplémentaires**:
  - Sentence Transformers
  - SpaCy (modèles en/fr préinstallés)
  - FAISS-GPU pour la recherche de similarité vectorielle
  - ChromaDB pour le stockage de vecteurs
  - Autres bibliothèques utiles (pandas, matplotlib, scikit-learn, etc.)

## 🚀 Démarrage rapide

### Prérequis

- Docker installé
- Support NVIDIA avec nvidia-docker (pour GPU)
- Make (pour utiliser les commandes du Makefile)

### Construire l'image

```bash
cd dev_setup
make build
```

### Lancer Jupyter

```bash
make jupyter
```

Accédez ensuite à Jupyter Lab via votre navigateur: http://localhost:8888

## 📚 Commandes disponibles

Le Makefile fournit plusieurs commandes utiles pour gérer l'environnement:

- `make help` : Affiche l'aide du Makefile
- `make build` : Construit l'image Docker
- `make run` : Lance un conteneur en mode détaché
- `make jupyter` : Lance un conteneur et affiche le lien Jupyter
- `make shell` : Ouvre un shell dans le conteneur
- `make stop` : Arrête le conteneur
- `make clean` : Supprime le conteneur
- `make status` : Affiche le statut du conteneur
- `make logs` : Affiche les logs du conteneur
- `make rebuild` : Reconstruit l'image et relance le conteneur
- `make save-image` : Sauvegarde l'image dans un fichier tar
- `make load-image` : Charge l'image à partir d'un fichier tar

## 🧩 Structure des volumes

L'image est configurée pour monter le répertoire parent du dossier `dev_setup` en tant que dossier de travail dans le conteneur:

- **Local**: `$(pwd)/..` (répertoire parent de dev_setup)
- **Conteneur**: `/workspace`

## 💡 Cas d'utilisation

Cette image est particulièrement adaptée pour:

1. **Prototypage rapide** de solutions NLP avec des modèles Transformers
2. **Développement de RAG** avec LangChain et vos propres données
3. **Expérimentation interactive** via les notebooks Jupyter
4. **Développement collaboratif** grâce à des environnements cohérents

## ⚠️ Remarques importantes

- L'accès à Jupyter est configuré sans mot de passe pour simplifier le développement. Pour une utilisation en production, ajoutez des mesures de sécurité appropriées.
- Pour la persistance des données, veillez à sauvegarder vos notebooks et données importantes sur le volume monté.

## 🔄 Personnalisation

Pour personnaliser davantage l'image:

1. Modifiez le `Dockerfile` pour ajouter d'autres packages ou configurations
2. Ajustez les variables dans le `Makefile` selon vos besoins (ports, noms, etc.)
3. Reconstruisez l'image avec `make rebuild`

## 📄 Licence

Ce projet est distribué sous la licence interne ARI. 