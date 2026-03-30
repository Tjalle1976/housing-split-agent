import math

print("Housing split agent started")

# TEST DATA (later vervangen we dit met echte scraping)
properties = [
    {
        "address": "Utrecht voorbeeldstraat 1",
        "price": 450000,
        "living_area": 150,
        "url": "https://www.funda.nl/koop/"
    },
    {
        "address": "Amersfoort voorbeeldstraat 2",
        "price": 375000,
        "living_area": 130,
        "url": "https://www.funda.nl/koop/"
    },
    {
        "address": "Utrecht groot pand",
        "price": 600000,
        "living_area": 220,
        "url": "https://www.funda.nl/koop/"
    }
]


def estimate_units(m2):
    if m2 >= 200:
        return 3
    if m2 >= 140:
        return 2
    return 1


def resale_price_per_m2(m2):
    # simpele marktinschatting
    if m2 >= 200:
        return 5500
    if m2 >= 140:
        return 6000
    return 6500


def calculate(property):
    price = property["price"]
    m2 = property["living_area"]

    price_per_m2 = price / m2

    renovation = m2 * 1200
    extra_costs = price * 0.10
    total_cost = price + renovation + extra_costs

    units = estimate_units(m2)

    exit_m2_price = resale_price_per_m2(m2)
    exit_value = m2 * exit_m2_price

    profit = exit_value - total_cost

    return {
        **property,
        "price_per_m2": round(price_per_m2),
        "renovation": renovation,
        "total_cost": round(total_cost),
        "units": units,
        "exit_value": exit_value,
        "profit": round(profit)
    }


results = [calculate(p) for p in properties]

# sorteer op winst
results.sort(key=lambda x: x["profit"], reverse=True)

print("\n=== TOP DEALS ===\n")

for r in results:
    print(f"Adres: {r['address']}")
    print(f"Prijs: € {r['price']:,}".replace(",", "."))
    print(f"m²: {r['living_area']}")
    print(f"€/m²: € {r['price_per_m2']}")
    print(f"Units: {r['units']}")
    print(f"Verbouwing: € {int(r['renovation']):,}".replace(",", "."))
    print(f"Totaal investering: € {r['total_cost']:,}".replace(",", "."))
    print(f"Verkoopwaarde: € {int(r['exit_value']):,}".replace(",", "."))
    print(f"Winst: € {r['profit']:,}".replace(",", "."))
    print(f"Link: {r['url']}")
    print("")

print("Script finished WITHOUT crashing")
