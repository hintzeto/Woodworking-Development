import json

# Default inventory data
default_inventory = {
    "Epoxy Tape": 1,
    "Shims": 6,
    "Epoxy mixing buckets": 12,
    "MICA powder": 1,
    "Titebond 3": 1,
    "Sandpaper": {
        "120 grit": 5,
        "180 grit": 5,
        "220 grit": 5,
    }
}

# File where the default inventory will be saved
inventory_file = "inventory.json"

# Save the default inventory data to the file
with open(inventory_file, 'w') as file:
    json.dump(default_inventory, file, indent=4)

print(f"Default inventory saved to {inventory_file}")