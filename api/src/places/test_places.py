import pytest
from flask import url_for

from src.places.models import Country


@pytest.mark.slow
@pytest.mark.usefixtures('reset_db')
@pytest.mark.parametrize('code, name', [('US', 'United States'),
                                        ('EC', 'Ecuador'),
                                        ('TH', 'Thailand')])
def test_read_country(client, code, name):
    count = Country.load_from_file()
    print(f"READ {count} COUNTRIES")
    assert count > 0
    resp = client.get(url_for('places.read_countries', country_code=code, locale='en-US'))
    assert resp.status_code == 200
    print("RESP", resp.json)
    assert resp.json['name'] == name


@pytest.mark.slow
@pytest.mark.usefixtures('reset_db')
def test_read_all_countries(client):
    count = Country.load_from_file()
    print(f"READ {count} COUNTRIES")
    assert count > 0
    resp = client.get(url_for('places.read_countries', locale='en-US'))
    assert resp.status_code == 200
    assert len(resp.json) == count
