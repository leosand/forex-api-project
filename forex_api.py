import requests
import pandas as pd
from datetime import datetime
import time

API_KEY = "69N1XH27W1PNO3WP"

def get_forex_data():
    pairs = ['EUR/USD', 'GBP/USD', 'JPY/USD']
    data = []
    
    for pair in pairs:
        from_currency = pair.split('/')[0]
        to_currency = pair.split('/')[1]
        
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}'
        
        try:
            response = requests.get(url)
            result = response.json()
            
            if "Realtime Currency Exchange Rate" in result:
                exchange_rate = float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
                timestamp = result["Realtime Currency Exchange Rate"]["6. Last Refreshed"]
                
                data.append({
                    'type': 'forex',
                    'symbol': pair,
                    'value': exchange_rate,
                    'timestamp': timestamp
                })
        except Exception as e:
            print(f"Erreur lors de la récupération des données Forex pour {pair}: {str(e)}")
    
    return data

def get_index_data():
    # CAC 40 et NASDAQ-100
    indices = [
        {'symbol': 'CAC40.PAR', 'name': 'CAC40'},
        {'symbol': 'QQQ', 'name': 'NASDAQ100'}  # QQQ est l'ETF qui suit le NASDAQ-100
    ]
    data = []
    
    for index in indices:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={index["symbol"]}&apikey={API_KEY}'
        
        try:
            response = requests.get(url)
            result = response.json()
            
            if "Global Quote" in result:
                quote = result["Global Quote"]
                price = float(quote.get("05. price", 0))
                change = float(quote.get("09. change", 0))
                change_percent = float(quote.get("10. change percent", "0").replace("%", ""))
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                data.append({
                    'type': 'index',
                    'symbol': index['name'],
                    'value': price,
                    'change': change,
                    'change_percent': change_percent,
                    'timestamp': timestamp
                })
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour {index['name']}: {str(e)}")
    
    return data

def save_market_data():
    # Récupérer toutes les données
    forex_data = get_forex_data()
    index_data = get_index_data()
    all_data = forex_data + index_data
    
    # Créer un DataFrame
    df = pd.DataFrame(all_data)
    
    # Sauvegarder dans des fichiers CSV séparés
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Sauvegarder toutes les données dans un seul fichier
    output_file = "E:/market_data.csv"
    df.to_csv(output_file, index=False)
    print(f"[{timestamp}] Données sauvegardées dans {output_file}")
    
    # Afficher les données par type
    print("\nDonnées Forex :")
    print(df[df['type'] == 'forex'][['symbol', 'value', 'timestamp']])
    
    print("\nDonnées Indices :")
    indices_df = df[df['type'] == 'index']
    if not indices_df.empty:
        for _, row in indices_df.iterrows():
            print(f"{row['symbol']}: {row['value']:.2f} ({row['change_percent']:+.2f}%)")
    else:
        print("Aucune donnée d'indice disponible")
    
    return df

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