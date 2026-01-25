import random

position = 0
steps = 10

print("Step\tMovement\tPosition")

for step in range(1, steps + 1):
    move = random.choice([-1, 1])
    position = position + move

    if move == 1:
        direction = "Right"
    else:
        direction = "Left"

    print(step, "\t", direction, "\t\t", position)
