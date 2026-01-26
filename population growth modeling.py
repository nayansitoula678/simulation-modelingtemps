population = 50
growth_rate = 0.1
years = 10

for year in range(1, years + 1):
    population += population * growth_rate
    print(f"Year {year}: {int(population)} individuals")
