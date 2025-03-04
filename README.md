# PROJECT ARI (Assistant RH Intelligent)

# 1. Besoin Mis à Jour (Cabinet de recrutement Exeio Corp)

## I. Contexte

- **Type de documents** : Contrats de travail (CDI, CDD, avenants), bulletins de paie, notes internes liées aux avantages sociaux, politiques de congés, fiches de poste.
- **Volume** : Plusieurs centaines (voire milliers) de documents au format PDF, stockés historiquement dans un serveur ou une GED (Gestion Électronique de Documents).
- **Diversité** : Documents produits sur plusieurs années, avec différents formats, textes légaux variables selon les dates et les conventions collectives.

## II. Besoin métier

Le service Ressources Humaines souhaite :

1. **Réduire le temps passé** à répondre aux questions récurrentes des collaborateurs sur :
   - Les éléments de rémunération (primes, allocations, cotisations) dans les fiches de paie.
   - Les dispositions légales et clauses dans les contrats (période d’essai, préavis, avantages).
   - Les congés et absences (nombre de jours, conditions, procédures, etc.).
2. **Fournir un accès rapide** et automatisé (via une interface web ou un chatbot interne) pour faciliter la recherche de réponses précises, basées directement sur les documents officiels.
3. **Assurer la conformité** : toujours renvoyer la bonne clause ou la bonne version légale (selon la période contractuelle couverte par le document).
4. **Permettre aux collaborateurs** d’ajouter de **nouveaux documents** (contrats supplémentaires, mises à jour de fiches de paie, avenants, etc.) au volume existant, afin de toujours disposer d’un référentiel documentaire à jour et complet.

## III. Exemples de Questions/Réponses

- **Question** : “Quels sont les éléments qui composent mon salaire brut sur ma fiche de paie du mois d’octobre 2022 ?”
  - **Attente** : Le système doit retrouver la fiche de paie correspondante, extraire les lignes de rémunération et répondre avec les libellés et montants associés, tout en citant la source du document.
- **Question** : “Quel est mon délai de préavis si je démissionne, selon mon contrat à durée indéterminée signé en 2021 ?”
  - **Attente** : Le système doit localiser la section du contrat ayant valeur légale, en citer la clause exacte et éventuellement ajouter du contexte (articles de la convention collective, code du travail, etc.).

---

# 2. Cahier des Charges Personnel (Mise à Jour : Assistant RH Intelligent)

## 1. Introduction

Pour répondre aux besoins de **Exeio Corp** et à mon propre apprentissage, je développerai un **Assistant RH Intelligent (ARI)** basé sur une approche **RAG (Retrieval-Augmented Generation)**.  
Désormais, le modèle de base choisi pour la génération de texte est **[TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF](https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF)**. Ce modèle quantifié au format **GGUF** est compatible avec `llama.cpp` à partir d’un certain commit et avec plusieurs frontends (text-generation-webui, etc.), ce qui permet à la fois une exécution CPU+GPU et une réduction de la mémoire requise.

## 2. Objectifs

### 2.1 Objectifs Techniques

1. Mettre en place un pipeline **RAG** intégrant :
   - **LangChain** pour orchestrer la recherche et la génération.
   - Un **moteur de recherche vectorielle** (par ex. FAISS, Milvus) pour indexer les chunks de documents RH.
   - Le **modèle GGUF “CapybaraHermes-2.5-Mistral-7B”** pour la génération de réponses.
2. S’assurer de la **compatibilité** avec l’infrastructure existante et de la prise en compte des spécificités du modèle (fenêtre de contexte, quantification, paramètres “ngl”, etc.).
3. Permettre l’**upload** de nouveaux documents PDF et leur indexation automatique.
4. Exploiter **CUDA** si disponible, pour accélérer l’inférence (ajustement du nombre de couches à offloader via `-ngl` dans llama.cpp, par exemple).

### 2.2 Objectifs Fonctionnels

1. **Recherche intelligente** et **génération de réponses** textuelles basées sur les documents RH (contrats, bulletins de paie, etc.).
2. **Interface web** ergonomique (basée sur **NextJS + FastAPI**), intégrant :
   - Système de **chat** ou de **Q/R**.
   - **Upload** de documents et suivi de l’avancement de l’indexation.
   - Visualisation des extraits correspondant aux questions posées (trouver la bonne page, la bonne clause...).
3. **Traçabilité** : toutes les réponses doivent citer leurs sources, pour assurer la conformité légale.
4. **Sécurité** : gestion des accès et chiffrement des données, compte tenu de la sensibilité des documents RH.

## 3. Stack Technique

1. **Backend (Python + FastAPI)**

   - LangChain pour gérer :
     - Le “retriever” (base vecteur)
     - La construction de prompts pour le LLM
   - Inférence locale ou via conteneur du modèle **CapybaraHermes-2.5-Mistral-7B-GGUF** (ex. `llama.cpp` ou une alternative compatible, comme text-generation-webui).
   - Utilisation de **CUDA** lorsque possible (configurer `-ngl` pour offloader un certain nombre de couches sur GPU).

2. **Frontend (NextJS)**

   - Interface de **chat** ou de Q/R
   - Formulaire d’upload de documents PDF
   - Tableau de bord pour visualiser la liste des documents et leur statut d’indexation

3. **Base Vectorielle**

   - FAISS, Milvus ou autre solution pour rechercher les chunks pertinents.
   - Stockage local ou conteneur séparé (MinIO/S3 si nécessaire).

4. **Conteneurisation & Déploiement**
   - **Docker** pour encapsuler l’application :
     - Un conteneur pour le backend (FastAPI + Python + dépendances LLM + GPU drivers compatibles)
     - Un conteneur pour le frontend (NextJS)
     - Un conteneur ou un service pour la base vectorielle
   - Versioning via Git, CI/CD si souhaité.

## 4. Fonctionnalités Principales

1. **Indexation des Documents**

   - Téléversement PDF → extraction texte
   - Découpage en chunks → génération embeddings → enregistrement en base vectorielle
   - Classification par type (fiche de paie, contrat, note, etc.)

2. **Recherche + RAG**

   - Interrogation sémantique, récupération des chunks via embeddings
   - Concaténation du contexte dans un prompt “ChatML” (ou format similaire)
   - Génération de la réponse par le modèle **CapybaraHermes-2.5-Mistral-7B-GGUF**
     - Utiliser `-c <valeur>` (ex. 2048, 4096, etc.) pour définir la fenêtre de contexte selon les besoins/capacités de la quantification
     - Ajuster la température, le repeat_penalty, etc., pour la qualité de la réponse

3. **Interface Utilisateur**

   - **Chat** (interaction question/réponse en direct) ou mode “assistant conversationnel”
   - **Visualisation** des références documentaires
   - **Gestion** des documents (upload, supprimer, etc.)

4. **Performances & Optimisations**
   - Réduction de la latence :
     - Exploitation de la quantification (GGUF) pour tourner sur des GPU modestes ou en CPU partiel
     - Ajustement du `-ngl` (nombre de layers GPU) pour tirer parti du hardware disponible
   - Possibilité de fixer un “max tokens” si la VRAM est limitée
   - Monitoring des ressources GPU/CPU pour maintenir une bonne réactivité

## 5. Planning

1. **Phase 1 : Setup Technique** (1-2 semaines)

   - Installation de l’environnement (Docker, CUDA, `llama.cpp`/text-generation-webui)
   - Téléchargement et test local du modèle **CapybaraHermes-2.5-Mistral-7B-GGUF**
   - Lecture/validation de la doc ([Hugging Face](https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF)) pour comprendre les paramètres `-c`, `-ngl`, etc.

2. **Phase 2 : RAG & Indexation** (2-3 semaines)

   - Mise en place de la base vectorielle (FAISS, Milvus, etc.)
   - Développement du pipeline LangChain (ingestion, chunking, retrieval)
   - Test d’inférence sur quelques documents (contrôler la qualité des réponses, latence)

3. **Phase 3 : Frontend & Upload** (2-3 semaines)

   - Création d’une interface NextJS (upload PDF, chat)
   - Intégration du backend FastAPI (API upload, API question/réponse)
   - Amélioration de l’ergonomie utilisateur

4. **Phase 4 : Sécurité, Validation & Optimisation** (2 semaines)
   - Mise en place d’authentification basique / gestion des rôles
   - Ajustements des paramètres du modèle (p. ex. `-c 2048`, `-ngl 32`) en fonction du GPU disponible
   - Optimisation pour la vitesse d’inférence (quantification, offloading)
   - Documentation finale

## 6. Critères de Réussite

1. **Précision des réponses** : le système doit renvoyer des informations exactes, issues des documents indexés.
2. **Simplicité d’ajout de documents** : un collaborateur doit pouvoir importer des PDF sans expertise technique particulière, avec un délai d’indexation raisonnable (< 1 minute pour un document standard).
3. **Performance** : un temps de réponse < 5 secondes pour des requêtes simples, sur un GPU grand public (6-8 Go VRAM).
4. **Robustesse** : gestion des cas d’erreur (fichiers non reconnus, questions hors périmètre, etc.).
5. **Exploitation correctes des spécificités du modèle** (réglages `llama.cpp`, quantification GGUF, etc.) pour tirer le meilleur parti du hardware cible.

---

_Ce cahier des charges mis à jour tient compte de l’utilisation du modèle quantifié [TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF](https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF). L’architecture RAG et l’interface utilisateur devront s’adapter aux limitations et possibilités de ce dernier, notamment en ce qui concerne la taille de la fenêtre de contexte, la configuration GPU/CPU et la quantification._