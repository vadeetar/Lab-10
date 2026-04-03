import requests
import time
import psutil
import sys

def get_process_memory(process_name):
    """Находит процесс по имени и возвращает использование памяти в МБ."""
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return proc.info['memory_info'].rss / (1024 * 1024)  # в МБ
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def test_service(url, service_name):
    print(f"\n=== Тестирование {service_name} ===")
    # Замер памяти до теста
    mem_before = get_process_memory(service_name)
    if mem_before is None:
        print(f"Не удалось найти процесс {service_name}. Убедитесь, что сервер запущен.")
        return None
    
    print(f"Память до нагрузки: {mem_before:.2f} МБ")
    
    # Нагрузка
    start = time.time()
    for _ in range(1000):
        try:
            requests.get(url)
        except:
            pass
    elapsed = time.time() - start
    rps = 1000 / elapsed
    
    # Замер памяти после
    mem_after = get_process_memory(service_name)
    mem_delta = mem_after - mem_before if mem_after else 0
    print(f"Память после нагрузки: {mem_after:.2f} МБ")
    print(f"Потребление дополнительно: {mem_delta:.2f} МБ")
    print(f"Время: {elapsed:.2f} сек")
    print(f"RPS: {rps:.2f}")
    return {"time": elapsed, "rps": rps, "mem_delta": mem_delta}

if __name__ == "__main__":
    # Убедитесь, что оба сервера запущены!
    print("Перед запуском теста убедитесь, что серверы работают:")
    print("Go: go run main.go (порт 8080)")
    print("Python: uvicorn main:app --reload (порт 8000)")
    input("Нажмите Enter, если серверы запущены...")
    
    go_result = test_service("http://localhost:8080/ping", "go")
    py_result = test_service("http://127.0.0.1:8000/", "python")
    
    print("\n=== ИТОГОВОЕ СРАВНЕНИЕ ===")
    if go_result:
        print(f"Go   - RPS: {go_result['rps']:.2f}, доп. память: {go_result['mem_delta']:.2f} МБ")
    if py_result:
        print(f"Python - RPS: {py_result['rps']:.2f}, доп. память: {py_result['mem_delta']:.2f} МБ")