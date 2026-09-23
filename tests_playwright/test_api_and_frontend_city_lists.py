import pytest

# 1. Список городов с фронта (54 шт.)
FRONTEND_CITIES = [
    "Tel Aviv", "Jerusalem", "Haifa", "Rishon LeZion", "Petah Tikva", "Ashdod",
    "Netanya", "Beersheba", "Bnei Brak", "Holon", "Ramat Gan", "Ashkelon",
    "Rehovot", "Bat Yam", "Beit Shemesh", "Kfar Saba", "Herzliya", "Hadera",
    "Modi'in-Maccabim-Re'ut", "Nazareth", "Lod", "Ramla", "Ra'anana",
    "Rosh HaAyin", "Acre", "Eilat", "Kiryat Ata", "Kiryat Gat", "Kiryat Yam",
    "Kiryat Motzkin", "Kiryat Bialik", "Nahariya", "Tiberias", "Safed",
    "Afula", "Carmiel", "Nes Ziona", "Yavne", "Or Yehuda", "Givatayim",
    "Kiryat Ono", "Umm al-Fahm", "Sakhnin", "Tamra", "Tayibe", "Tira",
    "Ma'alot-Tarshiha", "Migdal HaEmek", "Sderot", "Arad", "Dimona",
    "Ofakim", "Yeruham", "Kiryat Shmona"
]

# 2. Сырые данные из Swagger (массив объектов)
SWAGGER_DATA = {
  "cities": [
    {"city": "Beer Sheva", "lat": 31.252, "lng": 34.7916},
    {"city": "Qiryat Motzkin", "lat": 32.8333, "lng": 35.0833},
    {"city": "Rehovot", "lat": 31.8833, "lng": 34.8167},
    {"city": "Bat Yam", "lat": 32.0167, "lng": 34.75},
    {"city": "Qiryat Yam", "lat": 32.8333, "lng": 35.0833},
    {"city": "Qiryat Malakhi", "lat": 32.8333, "lng": 35.0833},
    {"city": "Qiryat Shemona", "lat": 32.8333, "lng": 35.0833},
    {"city": "Haifa", "lat": 32.794, "lng": 34.9896},
    {"city": "Givatayim", "lat": 32.0667, "lng": 34.7833},
    {"city": "Sderot", "lat": 31.5333, "lng": 34.5},
    {"city": "Qiryat Bialik", "lat": 32.8333, "lng": 35.0833},
    {"city": "Qiryat Yovel", "lat": 32.8333, "lng": 35.0833},
    {"city": "Tiberias", "lat": 32.8, "lng": 35.5333},
    {"city": "Kfar Saba", "lat": 32.1833, "lng": 34.9},
    {"city": "Qiryat Gat", "lat": 31.61, "lng": 34.7647},
    {"city": "Qiryat Tivon", "lat": 32.8333, "lng": 35.0833},
    {"city": "Ashdod", "lat": 31.8015, "lng": 34.6496},
    {"city": "Raanana", "lat": 32.1833, "lng": 34.8667},
    {"city": "Modiin", "lat": 31.9, "lng": 35.0167},
    {"city": "Petah Tikva", "lat": 32.0853, "lng": 34.8553},
    {"city": "Qiryat Ata", "lat": 32.7, "lng": 35.2},
    {"city": "Bnei Brak", "lat": 32.0833, "lng": 34.8333},
    {"city": "Tel Aviv", "lat": 32.0853, "lng": 34.7818},
    {"city": "Jerusalem", "lat": 31.7683, "lng": 35.2137},
    {"city": "Eilat", "lat": 29.5581, "lng": 34.9482},
    {"city": "Hadera", "lat": 32.4417, "lng": 34.9194},
    {"city": "Holon", "lat": 32.0114, "lng": 34.7745},
    {"city": "Nazareth", "lat": 32.7, "lng": 35.3},
    {"city": "Qiryat Ye'arim", "lat": 32.8333, "lng": 35.0833},
    {"city": "Herzliya", "lat": 32.1667, "lng": 34.8333},
    { "city": "Ramat Gan", "lat": 32.08, "lng": 34.82},
    {"city": "Hod HaSharon", "lat": 32.1667, "lng": 34.8667},
    {"city": "Rishon LeZion", "lat": 31.9566, "lng": 34.8048},
    {"city": "Qiryat Ono", "lat": 32.8333, "lng": 35.0833},
    {"city": "Netanya", "lat": 32.325, "lng": 34.8553},
    {"city": "Dimona", "lat": 31.0667, "lng": 35},
    {"city": "Ashkelon", "lat": 31.6667, "lng": 34.5833}
  ]
}

# Извлекаем чистый список строк из JSON Swagger
swagger_cities_list = [item["city"] for item in SWAGGER_DATA["cities"]]

# Находим те города, которые есть и там, и там
matching_cities = sorted(list(set(swagger_cities_list) & set(FRONTEND_CITIES)))

@pytest.mark.api
@pytest.mark.regression
def test_compare_lists():
    """Тест проверки соответствия списков между бэкендом и фронтендом"""
    set_swagger = set(swagger_cities_list)
    set_front = set(FRONTEND_CITIES)

    only_in_swagger = set_swagger - set_front
    only_in_front = set_front - set_swagger

    print("\n================== ОТЧЕТ ПО СПИСКАМ =================")
    print(f"Всего в Swagger: {len(swagger_cities_list)}")
    print(f"Всего на фронте: {len(FRONTEND_CITIES)}")
    print(f"Совпадающих городов: {len(matching_cities)}")
    print(f"Есть только в Swagger ({len(only_in_swagger)}): {sorted(list(only_in_swagger))}")
    print(f"Есть только на фронте ({len(only_in_front)}): {sorted(list(only_in_front))}")
    print("======================================================")

    # Если логика проекта требует полного совпадения списков 1 в 1, раскомментируй строчку ниже:
    # assert set_swagger == set_front, "Списки городов на бэке и фронте не совпадают!"