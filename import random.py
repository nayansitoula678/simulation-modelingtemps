import random

position = 0
steps = 20

print("Step\tPosition")
for step in range(1, steps + 1):
    move = random.choice([-1, 1])  # left or right
    position += move
    print(step, "\t", position)
