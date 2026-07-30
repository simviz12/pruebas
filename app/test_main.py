import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

CORREO_ANDINO_COMPLETO = """
De: notificaciones@bancoandino.ec
Para: contacto@minimarketlaesquina.ec
Asunto: Notificacion de movimiento en su cuenta
Fecha: Mar, 14 Jul 2026 14:28:11 -0500

Estimado cliente,

Le informamos que se ha registrado el siguiente movimiento en su cuenta
Corriente terminada en 4471:

  Tipo de movimiento : Credito
  Concepto           : Transferencia recibida
  Valor              : USD 45.50
  Fecha              : 14/07/2026
  Hora               : 14:28
  Referencia         : 0294817365
  Estado             : Aprobada
"""

CORREO_LITORAL_INCOMPLETO = """
De: alertas@bancodellitoral.ec
Para: contacto@minimarketlaesquina.ec

Hola,
Le confirmamos que el dia 16/07/2026 a las 10:46 su cuenta recibio una acreditacion por USD 310.00. El valor ya se encuentra disponible.
"""

def test_parse_correo_andino_completo():
    """Valida la extracción exacta de todos los campos de un correo regular."""
    response = client.post("/parse", content=CORREO_ANDINO_COMPLETO.encode("utf-8"), headers={"Content-Type": "text/plain"})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["banco"] == "Banco Andino"
    assert data["tipo_movimiento"] == "Credito"
    assert data["concepto"] == "Transferencia recibida"
    assert data["monto"] == "45.50"
    assert data["fecha"] == "2026-07-14"
    assert data["hora"] == "14:28:00"
    assert data["estado"] == "Aprobada"
    assert data["referencia"] == "0294817365"

def test_regla_no_negociable_campos_ausentes_son_null():
    """Valida que si falta la referencia o el banco no la manda, el valor es estrictamente None (null)."""
    response = client.post("/parse", content=CORREO_LITORAL_INCOMPLETO.encode("utf-8"), headers={"Content-Type": "text/plain"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Campos que sí están
    assert data["banco"] == "Banco del Litoral"
    assert data["tipo_movimiento"] == "Credito"
    assert data["monto"] == "310.00"
    assert data["fecha"] == "2026-07-16"
    assert data["hora"] == "10:46:00"
    
    # REGLA NO NEGOCIABLE: Campos que faltan deben ser null
    assert data["concepto"] is None
    assert data["estado"] is None
    assert data["referencia"] is None
