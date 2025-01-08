import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import json
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MarketDataTracker:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.forex_pairs = [
            'EURUSD=X', 'GBPUSD=X', 'JPYUSD=X', 
            'CHFUSD=X', 'AUDUSD=X', 'CADUSD=X'
        ]
        self.indices = [
            '^FCHI',  # CAC40
            '^NDX',   # NASDAQ-100
            '^GSPC',  # S&P500
            '^GDAXI'  # DAX
        ]
        
    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"Fichier de configuration {config_file} non trouvé. Utilisation des paramètres par défaut.")
            return {
                "update_interval": 600,
                "output": {
                    "csv_file": "market_data.csv"
                },
                "alerts": {
                    "forex": {},
                    "index": {}
                }
            }

    def get_forex_data(self):
        data = []
        for symbol in self.forex_pairs:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                if 'regularMarketPrice' in info:
                    data.append({
                        'symbol': symbol.replace('=X', ''),
                        'value': info['regularMarketPrice'],
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            except Exception as e:
                logging.error(f"Erreur lors de la récupération des données pour {symbol}: {str(e)}")
        
        return pd.DataFrame(data)

    def get_index_data(self):
        data = []
        for symbol in self.indices:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                if 'regularMarketPrice' in info and 'regularMarketChangePercent' in info:
                    data.append({
                        'symbol': symbol,
                        'value': info['regularMarketPrice'],
                        'change_percent': info['regularMarketChangePercent'],
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            except Exception as e:
                logging.error(f"Erreur lors de la récupération des données pour {symbol}: {str(e)}")
        
        return pd.DataFrame(data)

    def check_alerts(self, forex_data, index_data):
        alerts = []
        
        # Vérification des alertes Forex
        for _, row in forex_data.iterrows():
            symbol = row['symbol']
            value = row['value']
            if symbol in self.config['alerts']['forex']:
                alert_config = self.config['alerts']['forex'][symbol]
                if value < alert_config.get('min', float('-inf')):
                    alerts.append(f"ALERTE: {symbol} est en dessous du seuil minimum ({value:.4f})")
                if value > alert_config.get('max', float('inf')):
                    alerts.append(f"ALERTE: {symbol} est au-dessus du seuil maximum ({value:.4f})")
        
        # Vérification des alertes Indices
        for _, row in index_data.iterrows():
            symbol = row['symbol']
            value = row['value']
            if symbol in self.config['alerts']['index']:
                alert_config = self.config['alerts']['index'][symbol]
                if value < alert_config.get('min', float('-inf')):
                    alerts.append(f"ALERTE: {symbol} est en dessous du seuil minimum ({value:.2f})")
                if value > alert_config.get('max', float('inf')):
                    alerts.append(f"ALERTE: {symbol} est au-dessus du seuil maximum ({value:.2f})")
        
        return alerts

    def save_market_data(self, forex_data, index_data):
        try:
            # Fusion des données
            all_data = pd.concat([forex_data, index_data], ignore_index=True)
            
            # Sauvegarde dans un fichier CSV
            csv_path = Path(self.config['output']['csv_file'])
            all_data.to_csv(csv_path, index=False)
            logging.info(f"Données sauvegardées dans {csv_path}")
            
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde des données: {str(e)}")
            return False

    def display_market_data(self, forex_data, index_data):
        print("\nDonnées Forex :")
        if not forex_data.empty:
            print(forex_data.to_string(index=False))
        else:
            print("Aucune donnée Forex disponible")

        print("\nDonnées Indices :")
        if not index_data.empty:
            for _, row in index_data.iterrows():
                print(f"{row['symbol']}: {row['value']:.2f} ({row['change_percent']:.2f}%)")
        else:
            print("Aucune donnée d'indice disponible")

    def run(self):
        logging.info("Démarrage de la surveillance des marchés...")
        print("Le programme va mettre à jour les données toutes les", 
              self.config['update_interval'], "secondes.")
        print("Appuyez sur Ctrl+C pour arrêter le programme.")
        
        while True:
            try:
                # Récupération des données
                forex_data = self.get_forex_data()
                index_data = self.get_index_data()
                
                # Vérification des alertes
                alerts = self.check_alerts(forex_data, index_data)
                for alert in alerts:
                    logging.warning(alert)
                
                # Sauvegarde et affichage des données
                self.save_market_data(forex_data, index_data)
                self.display_market_data(forex_data, index_data)
                
                print(f"\nEn attente de la prochaine mise à jour dans {self.config['update_interval']} secondes...")
                time.sleep(self.config['update_interval'])
                
            except KeyboardInterrupt:
                logging.info("Arrêt du programme...")
                break
            except Exception as e:
                logging.error(f"Erreur inattendue : {str(e)}")
                print(f"Nouvelle tentative dans {self.config['update_interval']} secondes...")
                time.sleep(self.config['update_interval'])

if __name__ == "__main__":
    tracker = MarketDataTracker()
    tracker.run() 