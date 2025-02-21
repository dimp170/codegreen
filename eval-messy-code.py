import os
import sys
import random
import math
import time


class HugeMess:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.large_list = [random.randint(1, 100) for _ in range(1000)]
        self.create_nested_dict()

    def create_nested_dict(self):
        self.nested_dict = {i: {j: {k: random.randint(1, 100) for k in range(10)} for j in range(10)} for i in
                            range(10)}

    def deeply_nested_conditions(self):
        if self.x > 10:
            if self.y < 5:
                if self.x + self.y > 20:
                    if self.x % 2 == 0:
                        return self.x * self.y
                    elif self.x % 3 == 0:
                        return self.x / self.y
                    else:
                        return self.x - self.y
                else:
                    return self.y - self.x
            elif self.y > 15:
                return self.y ** 2
            else:
                return self.x + self.y

    def inefficient_recursion(self, n):
        if n <= 0:
            return 1
        return n * self.inefficient_recursion(n - 1)

    def pointless_loop(self):
        for i in range(100000):
            for j in range(1000):
                for k in range(100):
                    _ = i + j + k  # Completely useless operation

    def unused_function(self):
        x = 100
        y = x ** 2
        z = y + x
        return z


if __name__ == "__main__":
    obj = HugeMess(20, 10)
    print(obj.deeply_nested_conditions())
    print(obj.inefficient_recursion(10))
    obj.pointless_loop()