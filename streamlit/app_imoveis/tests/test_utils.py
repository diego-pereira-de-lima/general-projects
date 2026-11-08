# tests/test_utils.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
from modules.utils import img_to_data_url, geocode_address

@patch("builtins.open", new_callable=mock_open, read_data=b"fakebytes")
def test_img_to_data_url_success(mock_file):
    result = img_to_data_url("imgs/laranja.png")
    assert result.startswith("data:image/png;base64,")

@patch("builtins.open", side_effect=FileNotFoundError("not found"))
def test_img_to_data_url_failure(mock_file):
    result = img_to_data_url("imgs/inexistente.png")
    assert result is None

@patch("modules.utils.Nominatim.geocode")
def test_geocode_address_success(mock_geocode):
    mock_location = MagicMock(latitude=-23.5, longitude=-46.6)
    mock_geocode.return_value = mock_location

    lat, lon = geocode_address("Rua A", "100", "SP", "São Paulo")
    assert lat == -23.5
    assert lon == -46.6

@patch("modules.utils.Nominatim.geocode")
def test_geocode_address_none(mock_geocode):
    mock_geocode.return_value = None
    lat, lon = geocode_address("Rua X", "0", "Z", "Y")
    assert lat is None and lon is None

@patch("modules.utils.Nominatim.geocode", side_effect=Exception("Erro"))
def test_geocode_address_exception(mock_geocode):
    lat, lon = geocode_address("Erro", "0", "A", "B")
    assert lat is None and lon is None