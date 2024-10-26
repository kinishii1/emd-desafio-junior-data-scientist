import aiohttp
import asyncio
from datetime import datetime
from collections import defaultdict
import json

# with open("respostas\Python\descriptions.json", "r") as file:
#     description_data = json.load(file)
#     print(description_data)

API_URL_HOLIDAY = "https://date.nager.at/api/v3/PublicHolidays/2024/BR"
API_URL_MEDIA_MENSAL = "https://archive-api.open-meteo.com/v1/archive?latitude=-22.9064&longitude=-43.1822&start_date=2024-01-01&end_date=2024-08-01&daily=temperature_2m_mean"
API_URL_WEATHER_CODE = "https://archive-api.open-meteo.com/v1/archive?latitude=-22.9064&longitude=-43.1822&start_date=2024-01-01&end_date=2024-08-01&daily=weather_code"
API_URL_MEDIA_WEATHER = "https://archive-api.open-meteo.com/v1/archive?latitude=-22.9064&longitude=-43.1822&start_date=2024-01-01&end_date=2024-08-01&daily=temperature_2m_mean&daily=weather_code"

answers = []


# 1
async def count_holidays_year():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_HOLIDAY) as response:
            holidays = await response.json()
            total_holidays = len(holidays)
            answers.append(f"Q1 O total de {total_holidays} feriados em 2024.")


# 2
async def month_most_holidays():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_HOLIDAY) as response:
            holidays_per_month = {}

            holidays = await response.json()

            for holiday in holidays:
                month = holiday["date"].split("-")[1]
                holidays_per_month[month] = holidays_per_month.get(month, 0) + 1

            answers.append(
                f"Q2 O mês com mais feriados é {max(holidays_per_month, key=holidays_per_month.get)}"
            )


# 3
async def count_holidays_weekdays():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_HOLIDAY) as response:
            holidays = await response.json()
            weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            count = 0
            for holiday in holidays:
                holiday_date = datetime.strptime(holiday["date"], "%Y-%m-%d")
                if holiday_date.strftime("%A") in weekdays:
                    count += 1
            answers.append(
                f"Q3 O total de {count} feriados em 2024 que caem em dias de semana."
            )


# 4
async def get_mean_temp_month():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_MEDIA_MENSAL) as response:
            data = await response.json()
            mean_temp_month = {}
            count_days_month = {}

            for i, day in enumerate(data["daily"]["time"]):
                month = day.split("-")[1]
                mean_temp_month[month] = (
                    mean_temp_month.get(month, 0)
                    + data["daily"]["temperature_2m_mean"][i]
                )
                count_days_month[month] = count_days_month.get(month, 0) + 1

            for month in mean_temp_month:
                mean_temp_month[month] /= count_days_month[month]
                mean_temp_month[month] = str(round(mean_temp_month[month], 2)) + " °C"

            answers.append(f"Q4 A média de temperatura por mês é {mean_temp_month}")


# 5
async def most_commom_weather_month():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_WEATHER_CODE) as response:
            data = await response.json()
            weather_month = defaultdict(lambda: defaultdict(int))

            for i, day in enumerate(data["daily"]["time"]):
                month = day.split("-")[1]
                weather_code = data["daily"]["weather_code"][i]
                weather_month[month][weather_code] += 1

            most_common_weather = {}
            for month, weather_codes in weather_month.items():
                most_common_weather_code = max(weather_codes, key=weather_codes.get)
                most_common_weather[month] = most_common_weather_code

            with open("respostas\Python\descriptions.json", "r") as file:
                description_data = json.load(file)

            for month, weather_code in most_common_weather.items():
                most_common_weather[month] = description_data[str(weather_code)]["day"][
                    "description"
                ]

            answers.append(f"Q5 O clima mais comum por mês é {most_common_weather}")


# 6
async def mean_temp_weather_holiday():
    async with aiohttp.ClientSession() as session:
        holidays_days = []
        mean_temp_holiday = {}
        async with session.get(API_URL_HOLIDAY) as response:
            holidays = await response.json()
            for holiday in holidays:
                holidays_days.append(holiday["date"])

        async with session.get(API_URL_MEDIA_WEATHER) as response:
            data = await response.json()
            for i, day in enumerate(data["daily"]["time"]):
                if day in holidays_days:
                    mean_temp_holiday[day] = {
                        "temp": data["daily"]["temperature_2m_mean"][i],
                        "weather_code": data["daily"]["weather_code"][i],
                    }

            with open("respostas\Python\descriptions.json", "r") as file:
                description_data = json.load(file)

            for day, info in mean_temp_holiday.items():
                weather_code = info["weather_code"]
                mean_temp_holiday[day] = {
                    **info,
                    "temp_description": description_data[str(weather_code)]["day"][
                        "description"
                    ],
                }

            if len(answers) == 5:
                answers.append(
                    f"Q6 A média de temperatura e tempo nos feriados é {mean_temp_holiday}"
                )
            else:
                return mean_temp_holiday


# 7
# - O cidadão carioca considera "frio" um dia cuja temperatura média é menor que 20ºC;
#   - Um feriado bem aproveitado no Rio de Janeiro é aquele em que se pode ir à praia;
#   - O cidadão carioca só vai à praia quando não está com frio;
#   - O cidadão carioca também só vai à praia em dias com sol, evitando dias **totalmente** nublados ou chuvosos (considere _weather_code_ para determinar as condições climáticas).
async def define_bad_holiday():
    holiday_infos = await mean_temp_weather_holiday()
    bad_holidays = {}
    good_weather = [
        "Mainly Sunny",
        "Sunny",
        "Partly Cloudy",
    ]
    for day, info in holiday_infos.items():
        if float(info["temp"]) < 20 or info["temp_description"] not in good_weather:
            bad_holidays[day] = {
                "temp": info["temp"],
                "weather": info["temp_description"],
            }

    answers.append(f"Q7 Os feriados nao aproveitados são {bad_holidays}")


async def define_best_holiday():
    holiday_infos = await mean_temp_weather_holiday()
    good_holidays = {}
    good_weather = [
        "Sunny",
        "Mainly Sunny",
        "Partly Cloudy",
    ]
    for day, info in holiday_infos.items():
        if float(info["temp"]) > 20 or info["temp_description"] in good_weather:
            good_holidays[day] = {
                "temp": info["temp"],
                "weather": info["temp_description"],
            }

    good_holidays = sorted(
        good_holidays.items(), key=lambda x: x[1]["temp"], reverse=True
    )

    answers.append(f"Q8 O melhor feriado foi {good_holidays[0]}")


if __name__ == "__main__":
    asyncio.run(count_holidays_year())
    asyncio.run(month_most_holidays())
    asyncio.run(count_holidays_weekdays())
    asyncio.run(get_mean_temp_month())
    asyncio.run(most_commom_weather_month())
    asyncio.run(mean_temp_weather_holiday())
    asyncio.run(define_bad_holiday())
    asyncio.run(define_best_holiday())
    for aswer in answers:
        print(aswer)
