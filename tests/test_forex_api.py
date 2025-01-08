import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json
import pandas as pd
import time
from io import StringIO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from forex_api import get_forex_data, get_index_data, check_alerts, save_market_data, load_config

class TestForexAPI(unittest.TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.test_config = {
            'alerts': {
                'forex': {
                    'EUR/USD': {'min': 1.02, 'max': 1.04}
                },
                'index': {
                    'CAC40': {'min': 7000, 'max': 7500}
                }
            }
        }

    @patch('requests.get')
    def test_get_forex_data(self, mock_get):
        # Simuler une réponse API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Realtime Currency Exchange Rate": {
                "5. Exchange Rate": "1.0234",
                "6. Last Refreshed": "2025-01-08 13:00:01"
            }
        }
        mock_get.return_value = mock_response

        data = get_forex_data()
        
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['type'], 'forex')
        self.assertIn('EUR/USD', [item['symbol'] for item in data])

    @patch('requests.get')
    def test_get_index_data(self, mock_get):
        # Simuler une réponse API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Global Quote": {
                "05. price": "7500.50",
                "09. change": "25.5",
                "10. change percent": "0.34%"
            }
        }
        mock_get.return_value = mock_response

        data = get_index_data()
        
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['type'], 'index')
        self.assertIn('CAC40', [item['symbol'] for item in data])

    def test_price_format(self):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "Realtime Currency Exchange Rate": {
                    "5. Exchange Rate": "1.0234",
                    "6. Last Refreshed": "2025-01-08 13:00:01"
                }
            }
            mock_get.return_value = mock_response

            data = get_forex_data()
            
            # Vérifier que les valeurs sont bien des nombres
            for item in data:
                self.assertIsInstance(item['value'], float)

    @patch('builtins.print')
    def test_price_alerts(self, mock_print):
        # Test d'alerte pour valeur trop basse
        check_alerts('forex', 'EUR/USD', 1.01)
        mock_print.assert_called_with("⚠️ ALERTE: EUR/USD est en dessous du seuil minimum (1.0100 < 1.02)")
        
        # Test d'alerte pour valeur trop haute
        check_alerts('forex', 'EUR/USD', 1.05)
        mock_print.assert_called_with("⚠️ ALERTE: EUR/USD est au-dessus du seuil maximum (1.0500 > 1.04)")
        
        # Test sans alerte
        check_alerts('forex', 'EUR/USD', 1.03)
        self.assertEqual(mock_print.call_count, 2)  # Pas d'appel supplémentaire

    @patch('requests.get')
    def test_error_handling(self, mock_get):
        # Simuler une erreur API
        mock_get.side_effect = Exception("API Error")
        
        # Vérifier que l'erreur est gérée sans crash
        data = get_forex_data()
        self.assertEqual(len(data), 0)

    @patch('requests.get')
    def test_data_saving(self, mock_get):
        # Simuler des données
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Realtime Currency Exchange Rate": {
                "5. Exchange Rate": "1.0234",
                "6. Last Refreshed": "2025-01-08 13:00:01"
            }
        }
        mock_get.return_value = mock_response

        # Test de sauvegarde
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            df = save_market_data()
            mock_to_csv.assert_called_once()
            self.assertIsInstance(df, pd.DataFrame)

    def test_performance(self):
        # Test de performance pour la récupération des données
        start_time = time.time()
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "Realtime Currency Exchange Rate": {
                    "5. Exchange Rate": "1.0234",
                    "6. Last Refreshed": "2025-01-08 13:00:01"
                }
            }
            mock_get.return_value = mock_response
            
            get_forex_data()
        
        execution_time = time.time() - start_time
        self.assertLess(execution_time, 1.0)  # Le test doit s'exécuter en moins d'une seconde

    def test_config_loading(self):
        # Test du chargement de la configuration
        config = load_config()
        self.assertIn('alerts', config)
        self.assertIn('pairs', config)
        self.assertIn('indices', config)

if __name__ == '__main__':
    unittest.main() 