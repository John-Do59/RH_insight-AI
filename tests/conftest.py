"""
Fichier de configuration pytest.
Ajoute le répertoire racine au PYTHONPATH.
"""

import sys
import os

# Add project root to path so app modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
