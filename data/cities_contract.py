# data/cities_contract.py

UI_CITIES = [
    "Tel Aviv", "Jerusalem", "Haifa", "Rishon LeZion", "Petah Tikva", "Ashdod",
    "Netanya", "Beersheba", "Bnei Brak", "Holon", "Ramat Gan", "Ashkelon",
    "Rehovot", "Bat Yam", "Beit Shemesh", "Kfar Saba", "Herzliya", "Hadera",
    "Modi'in-Maccabim-Re'ut", "Nazareth", "Lod", "Ramla", "Ra'anana",
    "Rosh HaAyin", "Acre", "Eilat", "Kiryat Ata", "Kiryat Gat", "Kiryat Yam",
    "Kiryat Motzkin", "Kiryat Bialik", "Nahariya", "Tiberias", "Safed",
    "Afula", "Carmiel", "Nes Ziona", "Yavne", "Or Yehuda", "Givatayim",
    "Kiryat Ono", "Umm al-Fahm", "Sakhnin", "Tamra", "Tayibe", "Tira",
    "Ma'alot-Tarshiha", "Migdal HaEmek", "Sderot", "Arad", "Dimona",
    "Ofakim", "Yeruham", "Kiryat Shmona", "Hod HaSharon"
]

SWAGGER_CITIES = [
    "Beer Sheva", "Qiryat Motzkin", "Rehovot", "Bat Yam", "Qiryat Yam",
    "Qiryat Malakhi", "Qiryat Shemona", "Haifa", "Givatayim", "Sderot",
    "Qiryat Bialik", "Qiryat Yovel", "Tiberias", "Kfar Saba", "Qiryat Gat",
    "Qiryat Tivon", "Ashdod", "Raanana", "Modiin", "Petah Tikva", "Qiryat Ata",
    "Bnei Brak", "Tel Aviv", "Jerusalem", "Eilat", "Hadera", "Holon",
    "Nazareth", "Qiryat Ye'arim", "Herzliya", "Ramat Gan", "Hod HaSharon",
    "Rishon LeZion", "Qiryat Ono", "Netanya", "Dimona", "Ashkelon"
]

# Гарантированное пересечение (города, которые есть и там, и там, с учетом маппинга названий)
GUARANTEED_CITIES = [
    "Tel Aviv", "Jerusalem", "Haifa", "Rishon LeZion", "Petah Tikva",
    "Ashdod", "Netanya", "Bnei Brak", "Holon", "Ramat Gan",
    "Ashkelon", "Rehovot", "Bat Yam", "Kfar Saba", "Herzliya",
    "Hadera", "Nazareth", "Lod", "Ramla", "Rosh HaAyin",
    "Eilat", "Nahariya", "Tiberias", "Hod HaSharon", "Givatayim", "Sderot", "Dimona"
]