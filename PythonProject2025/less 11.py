from datetime import datetime, timedelta
import queue
import threading
import time
import random

OrderRequestBody = tuple[str, datetime]

storage = {
    "users": [],
    "dishes": [
        {"id": 1, "name": "Salad", "value": 1099, "restaurant": "Silpo"},
        {"id": 2, "name": "Soda", "value": 199, "restaurant": "Silpo"},
        {"id": 3, "name": "Pizza", "value": 599, "restaurant": "Kvadrat"},
    ],
}


class Scheduler:
    def __init__(self, delivery_queue: queue.Queue):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()
        self.delivery_queue = delivery_queue

    def process_orders(self) -> None:
        print("📦 Scheduler started...")
        while True:
            order = self.orders.get(True)
            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                print(f"\n🕓 Order '{order[0]}' is ready — sending to delivery")
                self.delivery_queue.put(order)

    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n📝 Order '{order[0]}' added for processing")


class DeliveryProcessor:
    def __init__(self):
        self.delivery_queue: queue.Queue[OrderRequestBody] = queue.Queue()
        self.providers = ["uklon", "uber"]
        self.active_deliveries = {"uklon": 0, "uber": 0}
        self.lock = threading.Lock()

    def choose_provider(self) -> str:
        with self.lock:
            return min(self.active_deliveries, key=self.active_deliveries.get)

    def process_deliveries(self) -> None:
        print("🚚 Delivery processor started...")
        while True:
            order = self.delivery_queue.get(True)
            provider = self.choose_provider()

            with self.lock:
                self.active_deliveries[provider] += 1

            print(f"🚗 '{order[0]}' assigned to {provider.upper()} delivery...")

            # Simulate delivery time
            if provider == "uklon":
                time.sleep(5)
            elif provider == "uber":
                time.sleep(3)

            print(f"✅ '{order[0]}' delivered via {provider.upper()}!")

            with self.lock:
                self.active_deliveries[provider] -= 1


def main():
    delivery = DeliveryProcessor()
    scheduler = Scheduler(delivery.delivery_queue)

    scheduler_thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    delivery_thread = threading.Thread(target=delivery.process_deliveries, daemon=True)

    scheduler_thread.start()
    delivery_thread.start()

    while True:
        try:
            order_input = input("\n📨 Enter order (format: Name Seconds): ").strip()
            name, sec = order_input.split()
            delay = datetime.now() + timedelta(seconds=int(sec))
            scheduler.add_order((name, delay))
        except ValueError:
            print("⚠️ Invalid input. Please enter in format: 'Pizza 10'")
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break


if __name__ == "__main__":
    main()