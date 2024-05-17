import firebase_admin
from firebase_admin import firestore
import os
import json

os.environ["GOOGLE_CLOUD_PROJECT"] = "woodworking-inventory"  # Replace with your actual project ID


# Application Default credentials are automatically created.
default_app = firebase_admin.initialize_app()
db = firestore.client()

doc_ref = db.collection("users").document("thintze")
doc_ref.set({"first": "Talon", "last": "Hintze", "born": 2001})

with open('Networking\inventory.json', 'r') as file:
    data = json.load(file)

db.collection("Inventory")