import os
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient

class Contact(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    phone_number: str

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number
        }

class DataIntractor:
    def __init__(self):
        host = os.getenv("MONGO_HOST", "localhost")
        port = os.getenv("MONGO_PORT", "27017")
        db_name = os.getenv("MONGO_NAME", "contactsdb")
    
        self.client = MongoClient(f"mongodb://{host}:{port}/", serverSelectionTimeoutMS=5000)
        self.db = self.client["contact_data"]
        self.collection = self.db["contacts"]
        self.collection.create_index("phone_number", unique=True)
        print("✓ Successfully connected to MongoDB!")

    def create_contact(self, contact_data: dict):
        result = self.collection.insert_one(contact_data)
        return (result.inserted_id)

    def get_all_contacts(self):
        contacts_list = []
        for doc in self.collection.find():
            contact = Contact(
                id=str(doc["_id"]),
                first_name=doc["first_name"],
                last_name=doc["last_name"],
                phone_number=doc["phone_number"]
            )
            contacts_list.append(contact)
        return contacts_list

    def update_contact(self, contact_id: str, contact_data: dict):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(contact_id)},
                {"$set": contact_data}
            )
            return result.modified_count > 0
        except:
            return False

    def delete_contact(self, contact_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(contact_id)})
            return result.deleted_count > 0
        except:
            return False


