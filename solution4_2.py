class Value:

    def __init__(self):
        self.amount = None

    def __set__(self, instance, value):
        self.amount = int(value * (1 - instance.commission))

    def __get__(self, instance, owner):
        return self.amount


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
