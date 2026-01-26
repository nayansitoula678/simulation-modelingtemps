energy = 100
time = 0

while energy > 0:
    print(f"Minute {time}: Energy = {energy}")
    energy -= 7      # fatigue rate
    time += 1

print("Athlete is exhausted")
