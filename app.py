from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
import json

app = FastAPI()

class Inspection(BaseModel):
    id: Optional[str]
    name: str
    description: str
    product: str
    criteria: str
    image_url: Optional[str] = None
    inspection_outcome: Optional[str] = None

def read_inspections_from_file():
    try:
        with open("inspections.json", "r") as file:
            return json.load(file) # Load inspections data from JSON file
    except FileNotFoundError:
        return [] # Return an empty list if file not found

def write_inspections_to_file(inspections):
    with open("inspections.json", "w") as file:
        json.dump(inspections, file, indent=4) # Write inspections data to JSON file

inspections = read_inspections_from_file()# Read inspections data initially

# API endpoint to create a inspection
@app.post("/inspections/", response_model=List[Inspection])
def create_inspections(inspections_list: List[Inspection]):
    for inspection in inspections_list:
        existing_inspection = next((i for i in inspections if i.get("id") == inspection.id), None)
        if existing_inspection:                  # If inspection ID already exists, update it
            existing_inspection.update(inspection.dict())
        else:                                    # Otherwise, generate a new ID and add it to the list
            if inspection.id is None:
                inspection.id = str(uuid4())
            inspections.append(inspection.dict())
    write_inspections_to_file(inspections) # write updated data to JSON file
    return inspections_list # Return the list of inspections

# API endpoint to read inspections with optional filtering and pagination
@app.get("/inspections/", response_model=List[Inspection])
def read_inspections(skip: int = 0, limit: int = 10,
                     inspection_station: Optional[str] = Query(None),
                     product: Optional[str] = Query(None)):
    filtered_inspections = inspections
    if inspection_station:
        filtered_inspections = [i for i in filtered_inspections if i["name"] == inspection_station]
    if product:
        filtered_inspections = [i for i in filtered_inspections if i["product"] == product]
    return filtered_inspections[skip: skip + limit]   # Return filtered and paginated inspections

# API endpoint to read a specific inspection based on ID 
@app.get("/inspections/{inspection_id}", response_model=Inspection)
def read_inspection(inspection_id: str):
    for inspection in inspections:
        if inspection.get("id") == inspection_id:
            return inspection           # Return inspection if ID matches
    raise HTTPException(status_code=404, detail="Inspection not found")  # Raise exception if not found

# API endpoint to update inspection details
@app.put("/inspections/{inspection_id}", response_model=Inspection)
def update_inspection(inspection_id: str, updated_inspection: Inspection):
    for index, inspection in enumerate(inspections):
        if inspection.get("id") == inspection_id:
            inspections[index] = updated_inspection.dict() # Update inspection data
            inspections[index]["id"] = inspection_id  # Update inspection ID
            write_inspections_to_file(inspections) # Write updated data to JSON file
            return inspections[index] # Return updated inspection
    raise HTTPException(status_code=404, detail="Inspection not found") # Raise exception if not found

# API endpoint to delete inspection
@app.delete("/inspections/{inspection_id}")
def delete_inspection(inspection_id: str): 
    global inspections
    inspections = [i for i in inspections if i.get("id") != inspection_id] # Remove inspection by ID
    write_inspections_to_file(inspections) # Write updated data to JSON file
    return {"detail": "Inspection deleted"} # Return success message
