import random

class EfficientCode:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def better_conditions(self):
        return self.x * self.y if self.x > 10 and self.y < 5 and self.x + self.y > 20 else self.y ** 2 if self.y > 15 else self.x + self.y

    def optimized_recursion(self, n, memo={0: 1}):
        if n not in memo:
            memo[n] = n * self.optimized_recursion(n - 1, memo)
        return memo[n]

if __name__ == "__main__":
    obj = EfficientCode(20, 10)
    print(obj.better_conditions())
    print(obj.optimized_recursion(10))
