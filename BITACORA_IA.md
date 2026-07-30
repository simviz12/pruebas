# Bitácora de Uso de IA (Antigravity Senior Agent)

Esta bitácora documenta las interacciones de asistencia para construir la solución, siguiendo la regla del enunciado de detallar sugerencias aceptadas y **rechazadas**.

## Interacción Inicial y Prompts

El candidato proporcionó una serie de instrucciones (Prompts) para iniciar la estructura base del proyecto, modelos de datos, FastAPI y motores de extracción (Parsers).

### Sugerencias Aceptadas:
- **Estructura base (KISS):** Acepté la sugerencia de crear una estructura aplanada (`models.py`, `parsers.py`, `main.py`) bajo una carpeta raíz `app/`. Originalmente se sugirió una arquitectura limpia excesiva (`app/domain/...`), pero por mutuo acuerdo lo redujimos a un esquema *Flat*, que es más eficiente y Pythónico para un dominio tan pequeño de un solo endpoint.
- **Modelos Pydantic v2:** Acepté el uso de `Optional` (y su equivalente nativo `| None`) y la definición de la clase con `Field` para autodocumentar la API.
- **FastAPI:** Implementación del POST `/parse` recibiendo `texto plano` (con `Body(..., media_type="text/plain")`) para integrarlo de forma transparente con el body raw de los requests.
- **Regla Estricta de Nulos:** En los extractores (Regex), cumplimos la orden del candidato de devolver `None` absoluto si la data es ambigua o inexistente (como el caso del correo 2 del Banco Litoral que no traía número de referencia).

### Sugerencias Rechazadas (CRÍTICO) 🛑:
1. **Rechazo al uso de `float` para el dinero:** 
   - *Prompt original del candidato:* Sugería tipar los campos financieros como `Optional[float]` y convertir extraídos con `float()`.
   - *Razón del rechazo:* En sistemas transaccionales y Fintech, usar coma flotante (IEEE 754) para montos de dinero causa **pérdidas de precisión** (ej. $11.10 + $52.20 = $63.300000000000004). 
   - *Acción tomada:* Forcé el uso exclusivo del módulo nativo `Decimal` en `models.py`, en el parser (`_parse_monto`), y en el script de depuración (`conciliacion_con_errores.py`).
2. **Rechazo a nombres de modelo extremadamente largos:**
   - *Prompt original:* Sugería nombrar el modelo `NotificationParseResponse`.
   - *Razón del rechazo:* Excede la verbosidad necesaria.
   - *Acción tomada:* Lo simplifiqué a `ParseResult` manteniendo la legibilidad sin sacrificar contexto.
