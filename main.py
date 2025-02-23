from fastapi import FastAPI
import json

app = FastAPI()

# Load JSON Data
with open("official_crime.test101_new.json", "r", encoding="utf-8") as file:
    crime_data = json.load(file)

@app.get("/")
def home():
    return {"message": "Crime Data API is running!"}

@app.get("/crimes")
def get_all_crimes():
    """Return all crime records"""
    return crime_data

@app.get("/crimes/{crime_id}")
def get_crime_by_id(crime_id: str):
    """Fetch crime data by _id"""
    for crime in crime_data:
        if crime["_id"]["$oid"] == crime_id:
            return crime
    return {"error": "Crime ID not found"}

@app.get("/crimes/location/{latitude}/{longitude}")
def get_crimes_by_location(latitude: float, longitude: float):
    """Find crimes near a given latitude & longitude"""
    nearby_crimes = [
        crime for crime in crime_data 
        if abs(crime["Latitude"] - latitude) < 0.01 and abs(crime["Longitude"] - longitude) < 0.01
    ]
    return nearby_crimes if nearby_crimes else {"message": "No crimes found near this location"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
