# Bit√°cora de Uso de IA (Antigravity Senior Agent)

Esta bit√°cora documenta las interacciones de asistencia para construir la soluci√≥n, siguiendo la regla del enunciado de detallar sugerencias aceptadas y **rechazadas**.

## Interacci√≥n Inicial y Prompts

El candidato proporcion√≥ una serie de instrucciones (Prompts) para iniciar la estructura base del proyecto, modelos de datos, FastAPI y motores de extracci√≥n (Parsers).

### Sugerencias Aceptadas:
- **Estructura base (KISS):** Acept√© la sugerencia de crear una estructura aplanada (`models.py`, `parsers.py`, `main.py`) bajo una carpeta ra√≠z `app/`. Originalmente se sugiri√≥ una arquitectura limpia excesiva (`app/domain/...`), pero por mutuo acuerdo lo redujimos a un esquema *Flat*, que es m√°s eficiente y Pyth√≥nico para un dominio tan peque√±o de un solo endpoint.
- **Modelos Pydantic v2:** Acept√© el uso de `Optional` (y su equivalente nativo `| None`) y la definici√≥n de la clase con `Field` para autodocumentar la API.
- **FastAPI:** Implementaci√≥n del POST `/parse` recibiendo `texto plano` (con `Body(..., media_type="text/plain")`) para integrarlo de forma transparente con el body raw de los requests.
- **Regla Estricta de Nulos:** En los extractores (Regex), cumplimos la orden del candidato de devolver `None` absoluto si la data es ambigua o inexistente (como el caso del correo 2 del Banco Litoral que no tra√≠a n√∫mero de referencia).

### Sugerencias Rechazadas (CR√çTICO) üõë:
1. **Rechazo al uso de `float` para el dinero:** 
   - *Prompt original del candidato:* Suger√≠a tipar los campos financieros como `Optional[float]` y convertir extra√≠dos con `float()`.
   - *Raz√≥n del rechazo:* En sistemas transaccionales y Fintech, usar coma flotante (IEEE 754) para montos de dinero causa **p√©rdidas de precisi√≥n** (ej. $11.10 + $52.20 = $63.300000000000004). 
   - *Acci√≥n tomada:* Forc√© el uso exclusivo del m√≥dulo nativo `Decimal` en `models.py`, en el parser (`_parse_monto`), y en el script de depuraci√≥n (`conciliacion_con_errores.py`).
2. **Rechazo a nombres de modelo extremadamente largos:**
   - *Prompt original:* Suger√≠a nombrar el modelo `NotificationParseResponse`.
   - *Raz√≥n del rechazo:* Excede la verbosidad necesaria.
   - *Acci√≥n tomada:* Lo simplifiqu√© a `ParseResult` manteniendo la legibilidad sin sacrificar contexto.

### Fase 3 y 4 (Testing y Refinamiento):
- **Pruebas (Aceptado):** Se implementaron dos pruebas unitarias sÛlidas (	est_parse_correo_andino_completo y 	est_regla_no_negociable_campos_ausentes_son_null) con pytest y TestClient para validar la correcta integraciÛn de FastAPI y la regla estricta de nulos sugerida en el Prompt 7 y 8.
- **Rechazo a campos adicionales:** El Prompt 7 sugerÌa verificar 8 campos (incluyendo estado y concepto). Como la especificaciÛn pedÌa mÌnimo 6 y el exceso de lÛgica (Code Bloat) es mala pr·ctica, mantuvimos los 6 campos estrictamente necesarios.
- **Rechazo a Bancos Inexistentes (Prompt 9):** El Prompt sugerÌa agregar cÛdigo para Banco Pichincha y Guayaquil. Al revisar correos_muestra.txt, estos bancos NO existen en el set de datos. Escribir cÛdigo 'por si acaso' rompe el principio YAGNI (You Aren't Gonna Need It). Se rechazÛ por completo esta sugerencia.
- **Rechazo a refactor de fechas (Prompt 10):** Se sugerÌa limpiar fechas manuales con Regex. Ya lo habÌamos resuelto con antelaciÛn utilizando nativamente datetime.strptime() y serializando a objetos date de Python, lo cual es mucho m·s robusto que lidiar con cadenas de texto Regex.

### Fase 5 y 6 (DepuraciÛn y DiseÒo):
- **Rechazo a la correcciÛn propuesta para flotantes (Prompt 12):** La sugerencia de IA indicaba usar math.isclose() para aplicar un margen de tolerancia entre los flotantes. Esta es una soluciÛn 'parche' que enmascara el problema de fondo. Como buena pr·ctica financiera, se rechazÛ en favor de re-tipar la arquitectura entera a usar Decimal, erradicando la imprecisiÛn de raÌz.
- **AceptaciÛn de la lÛgica de Idempotencia (Prompt 13):** Se sugiriÛ validar que un estado no estuviera conciliado previamente. Aceptamos el concepto implement·ndolo de forma nativa sin aÒadir variables extras, utilizando la bandera consumido que ya existÌa en la clase CorreoBancario y simplemente faltaba asignarse a True tras un cruce exitoso.
- **AceptaciÛn de la estructura documental (Prompts 14 y 15):** Se redactÛ el ANALISIS.md argumentando sÛlidamente las diferencias entre Falso Positivo (riesgo econÛmico de fraude por doble gasto) y Falso Negativo (fricciÛn operativa en el servicio al cliente por rechazar pagos genuinos que tienen un desface natural de minutos entre el correo y el mensaje de WhatsApp).
