import random
import requests
from bs4 import BeautifulSoup


def humidity_sensor():
    random_bool = random.choice([True, False])
    return random_bool


def ph_sensor():
    random_float = round(random.uniform(4.0, 8.0), 1)
    return random_float


def salinity_sensor():
    random_float = round(random.uniform(0.5, 2.0), 1)
    return random_float


def lightness_sensor():
    random_int = round(random.randrange(9000, 13000, 100), 0)
    return random_int


def temperature():
    try:
        url = 'https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n'
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')

    except ConnectionError:
        print(f"ConnectionError!")
    except:
        return "Nema podataka"

    else:
        results = soup.find(
            'table', attrs={'id': 'table-aktualni-podaci'}).find('tbody').find_all('tr')

        for i in range(1):
            temp = results[i].find_all('td')

        temperatura = temp[3]

        print("Temperatura: " + temperatura.get_text())
        return float(temperatura.get_text())
