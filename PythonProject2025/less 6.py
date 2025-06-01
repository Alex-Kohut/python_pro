import time
import logging


logging.basicConfig(level=logging.INFO)



class TimerContext:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start
        logging.info(f"[TIMER] Elapsed: {elapsed:.2f} seconds")



GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}



class Configuration:
    def __init__(self, updates: dict, validator=None):
        self.updates = updates
        self.validator = validator
        self._original = GLOBAL_CONFIG.copy()

    def __enter__(self):
        temp_config = {**GLOBAL_CONFIG, **self.updates}
        if self.validator and not self.validator(temp_config):
            raise ValueError("Invalid configuration update.")
        GLOBAL_CONFIG.update(self.updates)
        logging.info(f"[CONFIG] Applied: {self.updates}")
        return GLOBAL_CONFIG

    def __exit__(self, exc_type, exc_value, traceback):
        GLOBAL_CONFIG.clear()
        GLOBAL_CONFIG.update(self._original)
        logging.info(f"[CONFIG] Restored: {self._original}")



def validate_config(config: dict) -> bool:
    return config.get("max_retries", 0) >= 0



print("\n--- Before:", GLOBAL_CONFIG)

with TimerContext():
    with Configuration({"max_retries": 5}, validator=validate_config):
        print("==> Inside config block:", GLOBAL_CONFIG)
        time.sleep(1.5)

print("--- After:", GLOBAL_CONFIG)


try:
    with Configuration({"max_retries": -100}, validator=validate_config):
        pass
except ValueError as e:
    print(f"\n[ERROR] {e}")