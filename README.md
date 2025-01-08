# 📈 Forex & Market Data API

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Application de suivi en temps réel des taux de change Forex et des indices boursiers majeurs via l'API Alpha Vantage.

## 🌟 Fonctionnalités

- **Suivi Forex en temps réel**
  - EUR/USD, GBP/USD, JPY/USD, CHF/USD, AUD/USD, CAD/USD
  - Mise à jour automatique toutes les 10 minutes
  - Alertes de prix configurables

- **Suivi des Indices**
  - CAC40, NASDAQ-100, S&P500, DAX
  - Prix en temps réel
  - Variations en pourcentage
  - Alertes personnalisables

- **Sauvegarde des Données**
  - Format CSV structuré
  - Horodatage précis
  - Historique complet

## 🛠️ Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Clé API Alpha Vantage (gratuite sur [alphavantage.co](https://www.alphavantage.co/))
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

2. Modifiez `config.json` avec votre clé API et vos préférences :
```json
{
    "api_key": "VOTRE_CLE_API",
    "update_interval": 600,
    "alerts": {
        "forex": {
            "EUR/USD": {"min": 1.02, "max": 1.04}
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
1. Récupérer les données Forex et indices en temps réel
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

## ⚠️ Limitations API

- API gratuite limitée à 25 requêtes par jour
- Mise à jour toutes les 10 minutes par défaut
- Certains indices peuvent avoir un délai de 15 minutes

## 🔍 Dépannage

- **Erreur "API rate limit exceeded"** : Attendez 24h ou utilisez une clé API premium
- **Données manquantes** : Vérifiez la validité des symboles dans `config.json`
- **Erreurs réseau** : Vérifiez votre connexion Internet

## 📫 Support

Pour toute question ou problème :
1. Consultez les [Issues](https://github.com/votre-username/forex-api-project/issues)
2. Ouvrez une nouvelle issue si nécessaire
3. Contactez l'équipe de maintenance 