import requests
import pandas as pd
from datetime import datetime
import time
import json
import os

API_KEY = "69N1XH27W1PNO3WP"

# Configuration des alertes (à charger depuis un fichier de configuration)
PRICE_ALERTS = {
    'forex': {
        'EUR/USD': {'min': 1.02, 'max': 1.04},
        'GBP/USD': {'min': 1.23, 'max': 1.25},
        'JPY/USD': {'min': 0.006, 'max': 0.007}
    },
    'index': {
        'CAC40': {'min': 7000, 'max': 7500},
        'NASDAQ100': {'min': 500, 'max': 520}
    }
}

def load_config():
    config_file = 'config.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {
        'alerts': PRICE_ALERTS,
        'pairs': ['EUR/USD', 'GBP/USD', 'JPY/USD', 'CHF/USD', 'AUD/USD', 'CAD/USD'],
        'indices': [
            {'symbol': 'CAC40.PAR', 'name': 'CAC40'},
            {'symbol': 'QQQ', 'name': 'NASDAQ100'},
            {'symbol': 'SPY', 'name': 'S&P500'},
            {'symbol': 'DAX.DEX', 'name': 'DAX'}
        ]
    }

def check_alerts(data_type, symbol, value):
    alerts = PRICE_ALERTS.get(data_type, {}).get(symbol)
    if alerts:
        if value < alerts['min']:
            print(f"⚠️ ALERTE: {symbol} est en dessous du seuil minimum ({value:.4f} < {alerts['min']})")
        elif value > alerts['max']:
            print(f"⚠️ ALERTE: {symbol} est au-dessus du seuil maximum ({value:.4f} > {alerts['max']})")

def get_forex_data():
    config = load_config()
    pairs = config['pairs']
    data = []
    
    for pair in pairs:
        from_currency = pair.split('/')[0]
        to_currency = pair.split('/')[1]
        
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}'
        print(f"\nRécupération des données pour {pair}...")
        
        try:
            response = requests.get(url, timeout=10)
            result = response.json()
            
            if "Note" in result:
                print(f"Limite d'API atteinte: {result['Note']}")
                continue
                
            if "Error Message" in result:
                print(f"Erreur API: {result['Error Message']}")
                continue
            
            if "Realtime Currency Exchange Rate" in result:
                exchange_rate = float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
                timestamp = result["Realtime Currency Exchange Rate"]["6. Last Refreshed"]
                
                # Vérifier les alertes
                check_alerts('forex', pair, exchange_rate)
                
                data.append({
                    'type': 'forex',
                    'symbol': pair,
                    'value': exchange_rate,
                    'timestamp': timestamp
                })
                print(f"✓ {pair}: {exchange_rate}")
            else:
                print(f"Format de réponse inattendu pour {pair}: {result}")
        except requests.exceptions.Timeout:
            print(f"Timeout lors de la récupération des données pour {pair}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau pour {pair}: {str(e)}")
        except json.JSONDecodeError:
            print(f"Erreur de décodage JSON pour {pair}")
        except Exception as e:
            print(f"Erreur inattendue pour {pair}: {str(e)}")
    
    return data

def get_index_data():
    config = load_config()
    indices = config['indices']
    data = []
    
    for index in indices:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={index["symbol"]}&apikey={API_KEY}'
        print(f"\nRécupération des données pour {index['name']}...")
        
        try:
            response = requests.get(url, timeout=10)
            result = response.json()
            
            if "Note" in result:
                print(f"Limite d'API atteinte: {result['Note']}")
                continue
                
            if "Error Message" in result:
                print(f"Erreur API: {result['Error Message']}")
                continue
            
            if "Global Quote" in result:
                quote = result["Global Quote"]
                if not quote:
                    print(f"Pas de données disponibles pour {index['name']}")
                    continue
                    
                price = float(quote.get("05. price", 0))
                change = float(quote.get("09. change", 0))
                change_percent = float(quote.get("10. change percent", "0").replace("%", ""))
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Vérifier les alertes
                check_alerts('index', index['name'], price)
                
                data.append({
                    'type': 'index',
                    'symbol': index['name'],
                    'value': price,
                    'change': change,
                    'change_percent': change_percent,
                    'timestamp': timestamp
                })
                print(f"✓ {index['name']}: {price} ({change_percent:+.2f}%)")
            else:
                print(f"Format de réponse inattendu pour {index['name']}: {result}")
        except requests.exceptions.Timeout:
            print(f"Timeout lors de la récupération des données pour {index['name']}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau pour {index['name']}: {str(e)}")
        except json.JSONDecodeError:
            print(f"Erreur de décodage JSON pour {index['name']}")
        except Exception as e:
            print(f"Erreur inattendue pour {index['name']}: {str(e)}")
    
    return data

def save_market_data():
    try:
        # Récupérer toutes les données
        forex_data = get_forex_data()
        index_data = get_index_data()
        
        if not forex_data and not index_data:
            print("Aucune donnée n'a pu être récupérée")
            return None
            
        all_data = []
        if forex_data:
            all_data.extend(forex_data)
        if index_data:
            all_data.extend(index_data)
        
        # Créer un DataFrame
        df = pd.DataFrame(all_data)
        
        # Sauvegarder dans des fichiers CSV séparés
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Sauvegarder toutes les données dans un seul fichier
        output_file = "E:/market_data.csv"
        if not df.empty:
            df.to_csv(output_file, index=False)
            print(f"[{timestamp}] Données sauvegardées dans {output_file}")
        
        # Afficher les données par type
        print("\nDonnées Forex :")
        if forex_data:
            forex_df = pd.DataFrame(forex_data)
            print(forex_df[['symbol', 'value', 'timestamp']])
        else:
            print("Aucune donnée Forex disponible")
        
        print("\nDonnées Indices :")
        if index_data:
            indices_df = pd.DataFrame(index_data)
            for _, row in indices_df.iterrows():
                print(f"{row['symbol']}: {row['value']:.2f} ({row['change_percent']:+.2f}%)")
        else:
            print("Aucune donnée d'indice disponible")
        
        return df
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {str(e)}")
        return None

def run_continuous_updates():
    print("Démarrage de la surveillance des marchés...")
    print("Le programme va mettre à jour les données toutes les 10 minutes.")
    print("Appuyez sur Ctrl+C pour arrêter le programme.")
    
    while True:
        try:
            save_market_data()
            print("\nEn attente de la prochaine mise à jour dans 10 minutes...")
            time.sleep(600)  # 600 secondes = 10 minutes
        except KeyboardInterrupt:
            print("\nArrêt du programme...")
            break
        except Exception as e:
            print(f"\nErreur inattendue : {str(e)}")
            print("Nouvelle tentative dans 10 minutes...")
            time.sleep(600)

if __name__ == "__main__":
    run_continuous_updates() 