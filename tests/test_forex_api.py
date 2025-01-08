import pytest
from forex_api import MarketDataTracker
import pandas as pd
from pathlib import Path
import json

@pytest.fixture
def tracker():
    """Fixture pour créer une instance de MarketDataTracker avec une configuration de test."""
    config = {
        "update_interval": 60,
        "output": {
            "csv_file": "test_market_data.csv"
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
    
    # Sauvegarder la configuration temporaire
    config_path = Path("test_config.json")
    with open(config_path, "w") as f:
        json.dump(config, f)
    
    tracker = MarketDataTracker(config_file=str(config_path))
    yield tracker
    
    # Nettoyage
    config_path.unlink(missing_ok=True)
    Path("test_market_data.csv").unlink(missing_ok=True)

def test_forex_data_structure(tracker):
    """Teste la structure des données Forex."""
    forex_data = tracker.get_forex_data()
    assert isinstance(forex_data, pd.DataFrame)
    assert not forex_data.empty
    assert all(col in forex_data.columns for col in ['symbol', 'value', 'timestamp'])

def test_index_data_structure(tracker):
    """Teste la structure des données des indices."""
    index_data = tracker.get_index_data()
    assert isinstance(index_data, pd.DataFrame)
    assert not index_data.empty
    assert all(col in index_data.columns for col in ['symbol', 'value', 'change_percent', 'timestamp'])

def test_alerts(tracker):
    """Teste le système d'alertes."""
    # Créer des données de test
    forex_data = pd.DataFrame([{
        'symbol': 'EURUSD',
        'value': 1.01,  # En dessous du minimum configuré
        'timestamp': '2024-01-08 14:00:00'
    }])
    
    index_data = pd.DataFrame([{
        'symbol': '^FCHI',
        'value': 7600,  # Au-dessus du maximum configuré
        'timestamp': '2024-01-08 14:00:00',
        'change_percent': 1.5
    }])
    
    alerts = tracker.check_alerts(forex_data, index_data)
    assert len(alerts) == 2
    assert any("EURUSD" in alert for alert in alerts)
    assert any("^FCHI" in alert for alert in alerts)

def test_save_market_data(tracker):
    """Teste la sauvegarde des données."""
    forex_data = pd.DataFrame([{
        'symbol': 'EURUSD',
        'value': 1.03,
        'timestamp': '2024-01-08 14:00:00'
    }])
    
    index_data = pd.DataFrame([{
        'symbol': '^FCHI',
        'value': 7200,
        'timestamp': '2024-01-08 14:00:00',
        'change_percent': 1.5
    }])
    
    result = tracker.save_market_data(forex_data, index_data)
    assert result == True
    assert Path("test_market_data.csv").exists()

@pytest.mark.integration
def test_live_data_retrieval(tracker):
    """Teste la récupération des données en direct (marqué comme test d'intégration)."""
    forex_data = tracker.get_forex_data()
    index_data = tracker.get_index_data()
    
    assert not forex_data.empty
    assert not index_data.empty
    assert all(isinstance(value, float) for value in forex_data['value'])
    assert all(isinstance(value, float) for value in index_data['value']) 