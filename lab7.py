import requests
import json

API_KEY = "jMO7HnaoAPg2i6DJIujrPf4al10xIfJbkqyWjmVrGwCA3jNPRs9bxfsJlZlYdHc6RZfFPYRK77MBqcQjtvQ1H1"
BASE_URL = "https://api.ataix.kz"
HEADERS = {
    "X-API-Key": API_KEY,
    "accept": "application/json"
}

ORDERS_FILE = "orders.json"

def fetch_active_orders():
    url = f"{BASE_URL}/api/orders"  # <-- если нужен openOrders, попробуй /api/openOrders
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    if not data.get("status", False):
        print("❌ Ошибка при получении ордеров:", data.get("message", "Нет сообщения"))
        return []

    orders_raw = data.get("result", []) or data.get("data", [])
    orders = []

    for order in orders_raw:
        orders.append({
            "id": order.get("orderID", "unknown"),
            "symbol": order.get("symbol", "unknown"),
            "price": float(order.get("price", 0)),
            "amount": float(order.get("quantity", 0)),
            "status": order.get("status", "unknown").upper()
        })

    return orders

def save_orders_to_file(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4, ensure_ascii=False)
    print(f"✅Барлык тапсырыстар жанартылды {len(orders)} ордеров в {ORDERS_FILE}")

def main():
    orders = fetch_active_orders()
    if orders:
        save_orders_to_file(orders)

if __name__ == "__main__":
    main()
