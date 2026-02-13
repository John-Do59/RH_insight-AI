#!/bin/bash

# Configuration du PYTHONPATH pour trouver les modules du projet
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Lancement de l'application via Streamlit en utilisant l'environnement virtuel
echo "Lancement de RH Insight AI..."
./venv/bin/python3 -m streamlit run app/streamlit_app.py
