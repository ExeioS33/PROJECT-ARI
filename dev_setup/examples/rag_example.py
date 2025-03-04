#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemple de pipeline RAG avec LangChain et Transformers
=====================================================

Ce script démontre comment créer un pipeline RAG (Retrieval Augmented Generation) simple
en utilisant LangChain et les modèles Transformers de Hugging Face.
"""

import os
import pandas as pd
import torch
from tqdm import tqdm

# 1. Vérifier l'accès au GPU
print(f"GPU disponible: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Carte GPU: {torch.cuda.get_device_name(0)}")
    print(f"Mémoire disponible: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# 2. Préparation des données
documents = [
    "L'intelligence artificielle est un domaine de la science informatique qui se concentre sur la création de machines capables d'imiter l'intelligence humaine.",
    "Le deep learning est une sous-catégorie du machine learning qui utilise des réseaux de neurones artificiels avec plusieurs couches.",
    "Les transformers sont une architecture de réseau de neurones introduite par Google en 2017 qui a révolutionné le traitement du langage naturel.",
    "LangChain est un framework qui permet de développer des applications alimentées par des modèles de langage.",
    "Le RAG, ou Retrieval Augmented Generation, combine la récupération d'informations à partir d'une base de connaissances avec la génération de texte par un LLM."
]

# Création d'un DataFrame pour stocker nos documents
df = pd.DataFrame({"content": documents, "id": range(len(documents))})
print("\nExemple de documents:")
print(df.head())

# 3. Création de l'index vectoriel avec Sentence Transformers et FAISS
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

# Création du modèle d'embeddings
print("\nInitialisation du modèle d'embeddings...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"}
)

# Conversion des textes en documents LangChain
langchain_docs = [Document(page_content=text, metadata={"id": i}) for i, text in enumerate(documents)]

# Création de l'index FAISS
print("Création de l'index vectoriel FAISS...")
db = FAISS.from_documents(langchain_docs, embeddings)
print("Index vectoriel créé avec succès!")

# 4. Création d'un retrieveur
retrievers = db.as_retriever(search_kwargs={"k": 2})

# Test du retrieveur
query = "Qu'est-ce que le RAG?"
print(f"\nRecherche pour la requête: '{query}'")
docs = retrievers.get_relevant_documents(query)

print(f"Documents récupérés pour la requête: '{query}'")
for i, doc in enumerate(docs):
    print(f"Document {i+1}: {doc.page_content}")

# 5. Création d'un générateur avec un modèle Hugging Face Transformers
# Note: Cette partie peut être lourde et nécessiter beaucoup de RAM/VRAM
# Vous pouvez commenter cette section si vous n'avez pas assez de ressources
print("\nChargement du modèle de langage (peut prendre du temps)...")
try:
    from transformers import pipeline
    from langchain.llms import HuggingFacePipeline

    # Création d'un pipeline de génération de texte
    # Utilisez un modèle plus petit si nécessaire
    gen_pipeline = pipeline(
        "text-generation",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        max_length=512,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15
    )

    # Création d'un LLM LangChain à partir du pipeline
    llm = HuggingFacePipeline(pipeline=gen_pipeline)
    
    # 6. Construction du pipeline RAG complet
    from langchain.schema import StrOutputParser
    from langchain.schema.runnable import RunnablePassthrough
    from langchain.prompts import ChatPromptTemplate

    # Création du template de prompt
    template = """
    Tu es un assistant IA expert en intelligence artificielle et en traitement du langage naturel.
    Utilise le contexte suivant pour répondre à la question posée.

    Contexte:
    {context}

    Question: 
    {question}

    Réponse détaillée:
    """

    prompt = ChatPromptTemplate.from_template(template)

    # Fonction pour formater le contexte récupéré
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])

    # Construction du pipeline RAG
    rag_chain = (
        {"context": retrievers | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Test du pipeline RAG
    print("\nTest du pipeline RAG complet...")
    result = rag_chain.invoke("Explique-moi le concept de RAG et son utilité.")
    print("\nRéponse du modèle:")
    print(result)
except Exception as e:
    print(f"\nErreur lors du chargement du modèle: {e}")
    print("Cette section nécessite un GPU avec suffisamment de VRAM pour charger un grand modèle de langage.")
    print("Vous pouvez utiliser un modèle plus petit ou configurer l'environnement avec plus de ressources.")

# 7. Stockage persistant avec ChromaDB (Bonus)
print("\nCréation d'une base de données vectorielle persistante avec ChromaDB...")
try:
    from langchain.vectorstores import Chroma

    # Création d'un répertoire pour stocker les embeddings
    persist_directory = "chroma_db"
    os.makedirs(persist_directory, exist_ok=True)

    # Création de la base de données vectorielle persistante
    db_persistent = Chroma.from_documents(
        documents=langchain_docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    # Persistence de la base de données
    db_persistent.persist()
    print("Base de données vectorielle persistante créée avec succès!")
except Exception as e:
    print(f"Erreur lors de la création de la base persistante: {e}")

print("\nL'exemple de pipeline RAG est terminé!")
print("Consultez le code source pour comprendre chaque étape et l'adapter à vos besoins.") 