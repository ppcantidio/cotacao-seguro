import uvicorn
from fastapi import FastAPI

from src import service
from src.schemas import CotarSeguroPayload, CotarSeguroResponse

app = FastAPI()


@app.post("/cotacao", response_model=CotarSeguroResponse)
async def cotar_seguro(resquest: CotarSeguroPayload):
    result = service.cotar_seguro_service(request=resquest)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
