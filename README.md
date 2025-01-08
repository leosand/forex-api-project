# 📈 Forex & Market Data API

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Application de suivi en temps réel des taux de change Forex et des indices boursiers majeurs via l'API Yahoo Finance.

## 🌟 Fonctionnalités

- **Suivi Forex en temps réel**
  - EUR/USD, GBP/USD, JPY/USD, CHF/USD, AUD/USD, CAD/USD
  - Mise à jour automatique configurable
  - Alertes de prix personnalisables

- **Suivi des Indices**
  - CAC40 (^FCHI)
  - NASDAQ-100 (^NDX)
  - S&P500 (^GSPC)
  - DAX (^GDAXI)
  - Prix en temps réel
  - Variations en pourcentage
  - Alertes configurables

- **Sauvegarde des Données**
  - Format CSV structuré
  - Horodatage précis
  - Historique complet

## 🛠️ Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

## ⚙️ Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/forex-api-project.git
cd forex-api-project
```

2. Créez et activez l'environnement virtuel :
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Installez les pre-commit hooks :
```bash
pip install pre-commit
pre-commit install
```

## 🔧 Configuration

1. Copiez le fichier de configuration exemple :
```bash
cp config.example.json config.json
```

2. Modifiez `config.json` avec vos préférences :
```json
{
    "update_interval": 600,
    "output": {
        "csv_file": "market_data.csv"
    },
    "alerts": {
        "forex": {
            "EURUSD": {"min": 1.02, "max": 1.04}
        },
        "index": {
            "^FCHI": {"min": 7000, "max": 7500}
        }
    }
}
```

## 🚀 Utilisation

Lancez le script principal :
```bash
python forex_api.py
```

Le programme va :
1. Récupérer les données Forex et indices en temps réel via Yahoo Finance
2. Afficher les résultats dans la console
3. Sauvegarder les données dans `market_data.csv`
4. Alerter si les seuils configurés sont dépassés

## 🧪 Tests

Exécutez les tests unitaires :
```bash
pytest
```

Tests spécifiques :
```bash
pytest -m "not slow"  # Exclure les tests lents
pytest -m integration  # Tests d'intégration uniquement
pytest -m api  # Tests API uniquement
```

## 📊 Structure du Projet

```
forex-api-project/
├── forex_api.py        # Script principal
├── config.json         # Configuration
├── requirements.txt    # Dépendances
├── tests/             # Tests unitaires
│   └── test_forex_api.py
├── .github/           # Configuration GitHub
│   └── workflows/     # GitHub Actions
├── .gitignore        # Fichiers ignorés
├── .pre-commit-config.yaml  # Hooks pre-commit
└── README.md         # Documentation
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout de fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ⚠️ Limitations

- Certaines données peuvent avoir un délai de 15-20 minutes
- Les données sont limitées à celles disponibles via Yahoo Finance
- Certains symboles peuvent ne pas être disponibles

## 🔍 Dépannage

- **Données manquantes** : Vérifiez que les symboles sont corrects dans `config.json`
- **Erreurs réseau** : Vérifiez votre connexion Internet
- **Données retardées** : Normal pour certains indices, utilisez un flux en temps réel si nécessaire

## 📫 Support

Pour toute question ou problème :
1. Consultez les [Issues](https://github.com/votre-username/forex-api-project/issues)
2. Ouvrez une nouvelle issue si nécessaire
3. Contactez l'équipe de maintenance 