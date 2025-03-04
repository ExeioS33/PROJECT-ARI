FROM huggingface/transformers-pytorch-gpu:latest

LABEL maintainer="ARI Team"
LABEL description="Image Docker pour le développement et l'expérimentation NLP avec Transformers, PyTorch, Jupyter et LangChain"

# Mise à jour du système et installation des dépendances nécessaires
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installation de Jupyter et des extensions
RUN pip install --no-cache-dir \
    jupyter \
    jupyterlab \
    nbconvert \
    ipywidgets \
    jupyterlab-git

# Installation de LangChain et ses dépendances pour les pipelines RAG
RUN pip install --no-cache-dir \
    langchain \
    langchain-community \
    langchain-core \
    chromadb \
    faiss-gpu \
    sentence-transformers \
    tiktoken \
    openai

# Ajout d'autres outils utiles
RUN pip install --no-cache-dir \
    pandas \
    matplotlib \
    seaborn \
    scikit-learn \
    tqdm \
    nltk \
    spacy \
    einops

# Téléchargement de modèles spaCy courants
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download fr_core_news_sm

# Configuration de Jupyter
RUN mkdir -p /root/.jupyter
RUN jupyter notebook --generate-config
RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py

# Création du répertoire de travail
WORKDIR /workspace

# Exposition du port Jupyter
EXPOSE 8888

# Commande par défaut pour démarrer Jupyter
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"] 