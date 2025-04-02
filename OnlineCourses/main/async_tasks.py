import asyncio
import random
import time

"""
Задача 1: Простая асинхронная функция
Напишите async-функцию download_data(), которая ждёт 3 секунды (await asyncio.sleep(3)) и затем возвращает 
"Данные загружены".
Дополнительно: Вызовите её дважды, но без create_task(). Посчитайте, сколько времени выполняется программа.

 Задача 2: Параллельное выполнение с create_task()
Возьмите download_data() из первой задачи, но теперь запустите её дважды параллельно, используя asyncio.create_task().
Дополнительно: Посчитайте, сколько времени теперь выполняется программа.

Загрузка нескольких ссылок с asyncio.gather()
Напишите async-функцию fetch_data(url), которая принимает адрес сайта и имитирует его загрузку, 
await asyncio.sleep(от 1 до 3 секунд). 
Дополнительно: Запустите fetch_data() для списка сайтов параллельно, используя asyncio.gather().
"""

# Задача 1: Простая асинхронная функция
async def download_data():
    await asyncio.sleep(3)
    return "Данные загружены"

async def task1():
    print("\nЗадача 1: Последовательное выполнение")
    start_time = time.time()
    
    # Последовательный вызов функции дважды
    result1 = await download_data()
    print(f"Первый вызов: {result1}")
    
    result2 = await download_data()
    print(f"Второй вызов: {result2}")
    
    end_time = time.time()
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")

# Задача 2: Параллельное выполнение с create_task()
async def task2():
    print("\nЗадача 2: Параллельное выполнение")
    start_time = time.time()
    
    # Создаем и запускаем задачи параллельно
    task1 = asyncio.create_task(download_data())
    task2 = asyncio.create_task(download_data())
    
    # Ждем выполнения обеих задач
    result1 = await task1
    result2 = await task2
    
    print(f"Первая задача: {result1}")
    print(f"Вторая задача: {result2}")
    
    end_time = time.time()
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")

# Задача 3: Загрузка нескольких ссылок с asyncio.gather()
async def fetch_data(url):
    delay = random.uniform(1, 3)
    await asyncio.sleep(delay)
    return f"Данные с {url} загружены за {delay:.2f} секунд"

async def task3():
    print("\nЗадача 3: Параллельная загрузка с gather()")
    start_time = time.time()
    
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net",
        "https://example.edu"
    ]
    
    # Запускаем все задачи параллельно с помощью gather
    results = await asyncio.gather(*[fetch_data(url) for url in urls])
    
    # Выводим результаты
    for result in results:
        print(result)
    
    end_time = time.time()
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")

# Основная функция для запуска всех задач
async def main():
    print("Запуск асинхронных задач...")
    
    # Последовательно выполняем все три демонстрационные задачи
    await task1()
    await task2()
    await task3()

# Запускаем программу
if __name__ == "__main__":
    asyncio.run(main()) 