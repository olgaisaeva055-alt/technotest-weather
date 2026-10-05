import urllib.request
import urllib.parse
import json

# Шаг 3: Создание модели WeatherData
class WeatherData:
    def __init__(self, city, temp_c, country):
        self.city = city
        self.temp_c = int(temp_c)
        self.country = country

    # Метод для красивого вывода (Задание 4)
    def __str__(self):
        temp_str = f"+{self.temp_c}" if self.temp_c > 0 else str(self.temp_c)
        return f"{self.city}, {self.country} {temp_str} °C"

# Шаг 1: Загрузка списка городов из файла
def load_cities(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Читаем строки, убираем пробелы, отбрасываем пустые строки
            cities = [line.strip() for line in file if line.strip()]
        # Убираем дубликаты, сохраняя порядок
        return list(dict.fromkeys(cities))
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден. Убедитесь, что он лежит рядом со скриптом.")
        return []

# Шаг 2: Получение данных через API
def fetch_weather(city):
    # Кодируем название города для URL (на случай пробелов или спецсимволов)
    safe_city = urllib.parse.quote(city)
    url = f"https://wttr.in/{safe_city}?format=j1"
    
    # wttr.in требует User-Agent, иначе возвращает 403
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # Извлекаем нужные поля из JSON
            country = data['nearest_area'][0]['country'][0]['value']
            temp_c = data['current_condition'][0]['temp_C']
            
            return WeatherData(city, temp_c, country)
    except Exception as e:
        print(f"Ошибка при получении данных для города {city}: {e}")
        return None

def main():
    filename = 'cities.txt'
    cities = load_cities(filename)
    
    if not cities:
        return

    weather_list = []

    # Шаг 4: Вывод информации по каждому городу
    print("--- Вывод по каждому городу ---")
    for city in cities:
        weather = fetch_weather(city)
        if weather:
            weather_list.append(weather)
            print(weather)

    # Шаг 5: Группировка по странам и вывод статистики
    print("\n--- Статистика по странам ---")
    country_stats = {}

    for w in weather_list:
        if w.country not in country_stats:
            country_stats[w.country] = []
        country_stats[w.country].append(w.temp_c)

    for country, temps in country_stats.items():
        count = len(temps)
        avg_temp = sum(temps) / count
        min_temp = min(temps)
        max_temp = max(temps)
        
        # Форматирование вывода (добавляем + для положительных температур)
        avg_str = f"+{avg_temp:.0f}" if avg_temp > 0 else f"{avg_temp:.0f}"
        min_str = f"+{min_temp}" if min_temp > 0 else str(min_temp)
        max_str = f"+{max_temp}" if max_temp > 0 else str(max_temp)
        
        print(f"{country} - {count} cities, avg: {avg_str} °C, min: {min_str} °C, max: {max_str} °C")

if __name__ == "__main__":
    main()
