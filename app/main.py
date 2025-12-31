from fastapi import FastAPI, HTTPException
from data_interactor import DataIntractor, Contact
import uvicorn

app = FastAPI()
db = DataIntractor()


@app.get("/contacts")
def read_contacts():
    contacts = db.get_all_contacts()
    return contacts

@app.post("/contacts")
def create_contact(contact: Contact):
    new_id = db.create_contact(contact.to_dict())
    return {"message": "Contact created successfully", "id": str(new_id)}

@app.put("/contacts/{id}")
def update_contact(id: str, contact: Contact):
    success = db.update_contact(id, contact.model_dump())
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact updated successfully"}

@app.delete("/contacts/{id}")
def delete_contact(id: str):
    success = db.delete_contact(id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
