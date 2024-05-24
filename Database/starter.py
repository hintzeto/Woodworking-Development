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

print("Database initialized and default values populated")

#### User Inputs

def input_data():
    data_dict = {}
    print("Enter the data for the document. Type 'done' when finished.")
    while True:
        key = input("Enter field name: ")
        if key.lower() == 'done':
            break
        value = input(f"Enter value for '{key}': ")
        data_dict[key] = value
    return data_dict


while True:
    try:
        answer = int(input("1. View Tables\n2. Add Data\n3. Remove Data\n-------------\nEnter Option: "))

        if answer == 1: # View Collections
            count = 1
            collections = db.collections()
            collection_list = []
            print("Collections in the database:")
            for collection in collections:
                collection_list.append(collection.id)
                print(f'{count}. {collection.id}')
                count += 1
            print()

            collection_choice = int(input("Enter the number of the collection you would like to view: "))
            if 1 <= collection_choice < count:
                selected_collection_id = collection_list[collection_choice - 1]
                selected_collection_ref = db.collection(selected_collection_id)
                docs = selected_collection_ref.stream()
                print(f"Documents in {selected_collection_id}:")
                for doc in docs:
                    print(f'{doc.id} => {doc.to_dict()}')
                print()
            else:
                print("Invalid collection number. Please try again.")



        elif answer == 2: # Add Data
            input_choice = int(input("Where would you like to add data?\n1. Add a New Collection\n2. Add To an Existing Collection: "))
            if input_choice == 1:
                collection_name = input("Enter the name of the new collection: ")
                num_docs = int(input("How many documents do you want to add? "))
                for i in range(num_docs):
                    use_custom_id = input(f"Do you want to specify a custom ID for document {i+1}? (y/n): ").strip().lower()
                    if use_custom_id == 'y':
                        doc_id = input(f"Enter document ID for document {i+1}: ")
                    else:
                        doc_id = None  # Let Firestore auto-generate the ID
                        
                    data_dict = input_data()
                    if doc_id:
                        db.collection(collection_name).document(doc_id).set(data_dict)
                        print(f"Document {doc_id} added to collection {collection_name}.")
                    else:
                        doc_ref = db.collection(collection_name).add(data_dict)
                        print(f"Document with auto-generated ID {doc_ref[1].id} added to collection {collection_name}.")
                        
            elif input_choice == 2:
                collections = db.collections()
                collection_list = []
                print("Collections in the database:")
                for collection in collections:
                    print(f'{len(collection_list) + 1}. {collection.id}')
                    collection_list.append(collection.id)
                collection_choice = int(input("Enter the number of the collection you want to add data to: "))
                if 1 <= collection_choice <= len(collection_list):
                    collection_name = collection_list[collection_choice - 1]
                    num_docs = int(input("How many documents do you want to add? "))
                    for i in range(num_docs):
                        use_custom_id = input(f"Do you want to specify a custom ID for document {i+1}? (y/n): ").strip().lower()
                        if use_custom_id == 'y':
                            doc_id = input(f"Enter document ID for document {i+1}: ")
                        else:
                            doc_id = None  # Let Firestore auto-generate the ID

                        data_dict = input_data()
                        if doc_id:
                            db.collection(collection_name).document(doc_id).set(data_dict)
                            print(f"Document {doc_id} added to collection {collection_name}.")
                        else:
                            doc_ref = db.collection(collection_name).add(data_dict)
                            print(f"Document with auto-generated ID {doc_ref[1].id} added to collection {collection_name}.")
                else:
                    print("Invalid collection number. Please try again.")
            else:
                print("Invalid choice. Please try again.")
                continue
                    

        
        elif answer == 3:
            count = 1
            collections = db.collections()
            collection_list = []
            print("Collections in the database:")
            for collection in collections:
                print(f'{count}. {collection.id}')
                collection_list.append(collection.id)
                count += 1
            print()

            collection_choice = int(input("Enter the number of the collection you would like to remove a document from: "))
            if 1 <= collection_choice < count:
                selected_collection_id = collection_list[collection_choice - 1]
                selected_collection_ref = db.collection(selected_collection_id)
                docs = selected_collection_ref.stream()
                print(f"Documents in {selected_collection_id}:")
                doc_list = []
                doc_count = 1
                for doc in docs:
                    print(f'{doc_count}. {doc.id} => {doc.to_dict()}')
                    doc_list.append(doc.id)
                    doc_count += 1
                print()

                doc_choice = int(input("Enter the number of the document you would like to remove: "))
                if 1 <= doc_choice < doc_count:
                    selected_doc_id = doc_list[doc_choice - 1]
                    db.collection(selected_collection_id).document(selected_doc_id).delete()
                    print(f"Document {selected_doc_id} removed from collection {selected_collection_id}.")
                else:
                    print("Invalid document number. Please try again.")
            else:
                print("Invalid collection number. Please try again.")


        elif answer == 0:
            break

        else:
            print("Invalid option. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

