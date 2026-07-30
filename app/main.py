from fastapi import FastAPI, Body
from app.models import ParseResult
from app.parsers import parse_email

app = FastAPI(
    title="Servicio de Parseo de Correos Bancarios",
    description="API para convertir notificaciones de bancos en esquemas de datos estructurados."
)

@app.post("/parse", response_model=ParseResult)
def parse_correo(texto: str = Body(..., media_type="text/plain")):
    """
    Recibe el texto plano de un correo bancario y devuelve los datos estructurados.
    Si el banco no es soportado, retorna el modelo con campos nulos.
    """
    return parse_email(texto)
