import enum
import os
import time
import logging
from alpha_vantage.foreignexchange import ForeignExchange
from functools import lru_cache

logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
if not API_KEY or API_KEY == "YOUR_API_KEY":
    raise EnvironmentError("❌ Missing or invalid ALPHAVANTAGE_API_KEY")

fx = ForeignExchange(key=API_KEY, output_format="json")


class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()


class User:
    def __init__(self, name: str, email: str, role: Role):
        self.name, self.email, self.role = name, email, role

    def send_notification(self, notification):
        print(f"\nTo: {self.name} <{self.email}>\n{notification}")


class Notification:
    def __init__(self, subject: str, message: str, attachment: str = ""):
        self.subject, self.message, self.attachment = subject, message, attachment

    def format(self):
        text = f"Subject: {self.subject}\nMessage: {self.message}"
        if self.attachment:
            text += f"\nAttachment: {self.attachment}"
        return text

    def __str__(self):
        return self.format()


class StudentNotification(Notification):
    def format(self):
        return super().format() + "\nSent via Student Portal"


class TeacherNotification(Notification):
    def format(self):
        return super().format() + "\nTeacher's Desk Notification"


class Price:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency.upper()

    def __repr__(self):
        return f"{self.amount:.2f} {self.currency}"

    def to_chf(self) -> float:
        if self.currency == "CHF":
            return self.amount
        rate = self.get_rate(self.currency, "CHF")
        return self.amount * rate

    def from_chf(self, chf_amount: float) -> float:
        if self.currency == "CHF":
            return chf_amount
        rate = self.get_rate(self.currency, "CHF")
        return chf_amount / rate

    @staticmethod
    @lru_cache(maxsize=64)
    def get_rate(from_curr: str, to_curr: str) -> float:
        try:
            data, _ = fx.get_currency_exchange_rate(from_curr, to_curr)
            return float(data["5. Exchange Rate"])
        except Exception as e:
            logging.error(f"Failed to fetch exchange rate {from_curr} -> {to_curr}: {e}")
            raise RuntimeError(f"Exchange rate error for {from_curr} to {to_curr}")

    def _operate(self, other: "Price", op) -> "Price":
        if not isinstance(other, Price):
            raise TypeError("Operands must be Price instances.")
        if self.currency == other.currency:
            res = op(self.amount, other.amount)
        else:
            chf_self = self.to_chf()
            chf_other = other.to_chf()
            result_chf = op(chf_self, chf_other)
            res = self.from_chf(result_chf)
        return Price(res, self.currency)

    def __add__(self, other):
        return self._operate(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self._operate(other, lambda x, y: x - y)


def main():
    try:
        a = Price(100, "USD")
        b = Price(2500, "UAH")
        c = a + b
        d = b - a
        print("a:", a)
        print("b:", b)
        print("a + b:", c)
        print("b - a:", d)

        student = User("John Student", "john@example.com", Role.STUDENT)
        note = StudentNotification("Greeting", "Hello!", attachment="file.txt")
        student.send_notification(note)

    except Exception as e:
        logging.error(f"Application error: {e}")


if __name__ == "__main__":
    main()