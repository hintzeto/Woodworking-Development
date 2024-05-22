import firebase_admin
from firebase_admin import firestore
import os
import json

os.environ["GOOGLE_CLOUD_PROJECT"] = "woodworking-inventory"  # Replace with your actual project ID


# Application Default credentials are automatically created.
default_app = firebase_admin.initialize_app()
db = firestore.client()

user_ref = db.collection("users").document("thintze")
user_ref.set({"first_name": "Talon", "last_name": "Hintze", "birth_year": 2001})

with open('Networking\\inventory.json', 'r') as file:
    data = json.load(file)

    inventory_ref = db.collection("materials").document("inventory")
    inventory_ref.set({"inventory": data})

print("Done")

#### User Inputs

