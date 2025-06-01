import getpass


users = [
    {"username": "john", "password": "john123"},
    {"username": "alice", "password": "alice321"},
]

authorized_user = None

def auth(func):
    def wrapper(*args, **kwargs):
        global authorized_user

        if authorized_user:
            return func(*args, **kwargs)

        while True:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            for user in users:
                if user["username"] == username and user["password"] == password:
                    print(f"\n✅ Welcome, {username}!\n")
                    authorized_user = username
                    return func(*args, **kwargs)

            print("❌ Invalid credentials. Try again.\n")

    return wrapper


class Price:
    exchange_rates = {
        "USD": 0.9,
        "EUR": 0.95,
        "CHF": 1.0,
        "UAH": 0.025,
    }

    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency.upper()

    def __repr__(self):
        return f"{self.amount:.2f} {self.currency}"

    def convert_to_chf(self):
        rate = self.exchange_rates.get(self.currency)
        return self.amount * rate

    def convert_from_chf(self, chf_amount, target_currency):
        rate = self.exchange_rates.get(target_currency)
        return chf_amount / rate

    def _operate(self, other, op):
        if not isinstance(other, Price):
            raise TypeError("Operands must be Price instances.")

        if self.currency == other.currency:
            amount = op(self.amount, other.amount)
        else:
            chf_self = self.convert_to_chf()
            chf_other = other.convert_to_chf()
            result_chf = op(chf_self, chf_other)
            amount = self.convert_from_chf(result_chf, self.currency)

        return Price(amount, self.currency)

    def __add__(self, other):
        return self._operate(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self._operate(other, lambda x, y: x - y)


@auth
def command(payload):
    global authorized_user

    parts = payload.strip().split()

    if not parts:
        print("⚠️ Empty command.")
        return

    cmd = parts[0].lower()

    if cmd == "logout":
        authorized_user = None
        print("🔒 You have been logged out.\n")
        return

    if cmd == "exit":
        print("👋 Goodbye!")
        exit(0)

    if cmd in ("add", "sub"):
        if len(parts) != 5:
            print("⚠️ Usage: add|sub <amount1> <currency1> <amount2> <currency2>")
            return
        try:
            amount1 = float(parts[1])
            currency1 = parts[2].upper()
            amount2 = float(parts[3])
            currency2 = parts[4].upper()

            p1 = Price(amount1, currency1)
            p2 = Price(amount2, currency2)

            result = p1 + p2 if cmd == "add" else p1 - p2
            print(f"✅ Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"❓ Unknown command: {cmd}")


if __name__ == "__main__":
    print("💰 Welcome to the Price Calculator with Auth & Commands 💬")
    print("Available commands: `add`, `sub`, `logout`, `exit`\n")

    try:
        while True:
            user_input = input(">>> ")
            if user_input.strip():
                command(user_input)
    except KeyboardInterrupt:
        print("\n👋 Exiting. Bye!")