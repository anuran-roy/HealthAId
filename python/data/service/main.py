from fastapi import FastAPI
import uvicorn
from data.scrapers import mayoclinic

scraper_app = FastAPI(title="", description="")

@scraper_app.get("/mayoclinic")
def getMayoClinicData(query: str) -> dict[str, str]:
    mayoclinic.get_data()

if __name__ == "__main__":
    config = uvicorn.Config(app=scraper_app, host="127.0.0.1", port=)
    uvicorn.Server(config=config).serve()