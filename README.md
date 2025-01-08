# Forex & Market Data API

Ce projet permet de suivre en temps réel les taux de change Forex et les indices boursiers majeurs (CAC40, NASDAQ-100) via l'API Alpha Vantage.

## Fonctionnalités

- Suivi en temps réel des paires de devises (EUR/USD, GBP/USD, JPY/USD)
- Suivi des indices boursiers (CAC40, NASDAQ-100)
- Mise à jour automatique toutes les 10 minutes
- Sauvegarde des données dans un fichier CSV
- Affichage des variations en pourcentage pour les indices

## Prérequis

- Python 3.8+
- Une clé API Alpha Vantage (gratuite sur [alphavantage.co](https://www.alphavantage.co/))

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/forex-api-project.git
cd forex-api-project
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
```

3. Activez l'environnement virtuel :
- Windows :
```bash
.\venv\Scripts\activate
```
- Linux/Mac :
```bash
source venv/bin/activate
```

4. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

1. Remplacez la clé API dans le fichier `forex_api.py` :
```python
API_KEY = "VOTRE_CLE_API"
```

2. Assurez-vous d'avoir les droits d'écriture sur le disque où vous souhaitez sauvegarder les données.

## Utilisation

Pour lancer le script :
```bash
python forex_api.py
```

Le script va :
1. Récupérer les données Forex et des indices toutes les 10 minutes
2. Afficher les résultats dans la console
3. Sauvegarder les données dans un fichier CSV

Pour arrêter le script, appuyez sur Ctrl+C.

## Structure des données

Le fichier CSV généré contient les colonnes suivantes :
- `type` : 'forex' ou 'index'
- `symbol` : le symbole de la paire de devises ou de l'indice
- `value` : la valeur actuelle
- `timestamp` : l'horodatage de la mise à jour
- Pour les indices : `change` et `change_percent` (variation)

## Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Push vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub. 