import random

teamA = 0
teamB = 0

for minute in range(1, 91):
    if random.random() < 0.03:
        teamA += 1
    if random.random() < 0.025:
        teamB += 1

print("Final Score:")
print("Team A:", teamA)
print("Team B:", teamB)
