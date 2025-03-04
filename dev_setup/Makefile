# Variables
IMAGE_NAME := ai_ml_setup
IMAGE_TAG := 1.0
CONTAINER_NAME := ari-nlp-workspace
JUPYTER_PORT := 8888
LOCAL_WORKSPACE := $(shell pwd)/..
CONTAINER_WORKSPACE := /workspace

# Couleurs pour les messages
YELLOW := \033[1;33m
GREEN := \033[1;32m
RED := \033[1;31m
NC := \033[0m # No Color

.PHONY: help build run stop clean jupyter status logs shell rebuild save-image load-image

# Affiche l'aide
help:
	@echo "${YELLOW}ARI NLP Development Environment${NC}"
	@echo "${GREEN}Commandes disponibles:${NC}"
	@echo "  ${GREEN}make help${NC}        - Affiche cette aide"
	@echo "  ${GREEN}make build${NC}       - Construit l'image Docker"
	@echo "  ${GREEN}make run${NC}         - Lance un conteneur en mode détaché"
	@echo "  ${GREEN}make jupyter${NC}     - Lance un conteneur et affiche le lien Jupyter"
	@echo "  ${GREEN}make shell${NC}       - Ouvre un shell dans le conteneur"
	@echo "  ${GREEN}make stop${NC}        - Arrête le conteneur"
	@echo "  ${GREEN}make clean${NC}       - Supprime le conteneur"
	@echo "  ${GREEN}make status${NC}      - Affiche le statut du conteneur"
	@echo "  ${GREEN}make logs${NC}        - Affiche les logs du conteneur"
	@echo "  ${GREEN}make rebuild${NC}     - Reconstruit l'image Docker et relance le conteneur"
	@echo "  ${GREEN}make save-image${NC}  - Sauvegarde l'image dans un fichier tar"
	@echo "  ${GREEN}make load-image${NC}  - Charge l'image à partir d'un fichier tar"

# Construit l'image Docker
build:
	@echo "${YELLOW}Construction de l'image Docker ${IMAGE_NAME}:${IMAGE_TAG}...${NC}"
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile .
	@echo "${GREEN}Image Docker construite avec succès!${NC}"

# Lance un conteneur en mode détaché
run:
	@echo "${YELLOW}Lancement du conteneur ${CONTAINER_NAME}...${NC}"
	docker run --gpus all -d \
		--name $(CONTAINER_NAME) \
		-p $(JUPYTER_PORT):8888 \
		-v $(LOCAL_WORKSPACE):$(CONTAINER_WORKSPACE) \
		$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "${GREEN}Conteneur lancé avec succès!${NC}"
	@echo "${GREEN}Jupyter Lab est accessible à l'adresse: ${NC}http://localhost:$(JUPYTER_PORT)"

# Lance un conteneur et affiche le lien Jupyter
jupyter: run
	@echo "${YELLOW}Attendez quelques secondes pour que Jupyter démarre...${NC}"
	@sleep 3
	@echo "${GREEN}Jupyter Lab est accessible à l'adresse: ${NC}http://localhost:$(JUPYTER_PORT)"
	@echo "${YELLOW}Logs de Jupyter:${NC}"
	@docker logs $(CONTAINER_NAME)

# Ouvre un shell dans le conteneur
shell:
	@echo "${YELLOW}Ouverture d'un shell dans le conteneur ${CONTAINER_NAME}...${NC}"
	docker exec -it $(CONTAINER_NAME) /bin/bash

# Arrête le conteneur
stop:
	@echo "${YELLOW}Arrêt du conteneur ${CONTAINER_NAME}...${NC}"
	docker stop $(CONTAINER_NAME)
	@echo "${GREEN}Conteneur arrêté avec succès!${NC}"

# Supprime le conteneur
clean: stop
	@echo "${YELLOW}Suppression du conteneur ${CONTAINER_NAME}...${NC}"
	docker rm $(CONTAINER_NAME)
	@echo "${GREEN}Conteneur supprimé avec succès!${NC}"

# Affiche le statut du conteneur
status:
	@echo "${YELLOW}Statut du conteneur ${CONTAINER_NAME}:${NC}"
	@docker ps -a | grep $(CONTAINER_NAME) || echo "${RED}Le conteneur n'existe pas.${NC}"

# Affiche les logs du conteneur
logs:
	@echo "${YELLOW}Logs du conteneur ${CONTAINER_NAME}:${NC}"
	docker logs $(CONTAINER_NAME)

# Reconstruit l'image Docker et relance le conteneur
rebuild: clean build run
	@echo "${GREEN}Reconstruction et redémarrage effectués avec succès!${NC}"

# Sauvegarde l'image dans un fichier tar
save-image:
	@echo "${YELLOW}Sauvegarde de l'image ${IMAGE_NAME}:${IMAGE_TAG} dans ${IMAGE_NAME}-${IMAGE_TAG}.tar...${NC}"
	docker save -o $(IMAGE_NAME)-$(IMAGE_TAG).tar $(IMAGE_NAME):$(IMAGE_TAG)
	@echo "${GREEN}Image sauvegardée avec succès!${NC}"

# Charge l'image à partir d'un fichier tar
load-image:
	@echo "${YELLOW}Chargement de l'image à partir de ${IMAGE_NAME}-${IMAGE_TAG}.tar...${NC}"
	docker load -i $(IMAGE_NAME)-$(IMAGE_TAG).tar
	@echo "${GREEN}Image chargée avec succès!${NC}"
