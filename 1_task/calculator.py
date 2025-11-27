class Calculator:
    def add(self, a, b):
        self._check_types(a, b)
        return a + b

    def subtract(self, a, b):
        self._check_types(a, b)
        return a - b

    def multiply(self, a, b):
        self._check_types(a, b)
        return a * b

    def divide(self, a, b):
        self._check_types(a, b)
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return a / b

    def _check_types(self, a, b):
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numbers")