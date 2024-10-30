import requests
import csv
from datetime import datetime

datas = [
    "2024-01-01",
    "2024-02-12",
    "2024-02-13",
    "2024-03-29",
    "2024-03-31",
    "2024-04-21",
    "2024-05-01",
    "2024-05-30",
    "2024-07-09",
    "2024-09-07",
    "2024-10-12",
]

latitude = -22.9064
longitude = -43.1822

output_file = "respostas\Python\dados.csv"


# https://archive-api.open-meteo.com/v1/archive?latitude=-22.9064&longitude=-43.1822&start_date=2024-10-14&end_date=2024-10-14&daily=temperature_2m_mean
def fetch_temperature_data(date):
    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}&longitude={longitude}"
        f"&start_date={date}&end_date={date}"
        f"&daily=temperature_2m_mean"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "date": date,
            "temperature_mean": data["daily"]["temperature_2m_mean"],
        }
    else:
        print(f"Erro ao buscar dados para {date}")
        return None


with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Data", "Temperatura Média"])

    for date in datas:
        result = fetch_temperature_data(date)
        if result:
            temperature_mean = (
                result["temperature_mean"][0]
                if isinstance(result["temperature_mean"], list)
                else result["temperature_mean"]
            )
            writer.writerow([result["date"], temperature_mean])

print(f"Dados salvos em {output_file}")
