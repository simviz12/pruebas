# Parseo de Notificaciones Bancarias (Prueba Técnica)

Microservicio en FastAPI encargado de recibir correos de notificaciones bancarias en texto plano y transformarlos en datos estructurados y tipados. Implementa una **arquitectura plana (Flat)** priorizando el principio **KISS (Keep It Simple, Stupid)** debido al alcance centrado en un único endpoint.

## 🚀 Requisitos Previos

- Python 3.12+
- (Recomendado) Entorno virtual activo

## ⚙️ Instalación y Ejecución

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Levantar el servicio:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   El servicio estará disponible en `http://127.0.0.1:8000`. Puedes acceder a la documentación interactiva en `http://127.0.0.1:8000/docs`.

3. **Ejecutar Pruebas Automatizadas:**
   ```bash
   python -m pytest -v app/test_main.py
   ```

## 📁 Estructura del Proyecto

* `app/models.py`: Define la estructura inmutable y estricta usando Pydantic v2. Se usa `Decimal` para precisión financiera.
* `app/parsers.py`: Motores de extracción basados en Expresiones Regulares robustas. Cumplen con la **regla de no inventar datos**, retornando `None` si la extracción es incierta.
* `app/main.py`: Punto de entrada de FastAPI.
* `app/test_main.py`: Pruebas de integración sobre el endpoint.
* `conciliacion_con_errores.py`: Script original refactorizado corrigiendo bugs lógicos y numéricos.
* `ANALISIS.md`: Explicación de los bugs de depuración y decisiones de diseño técnico-empresarial.
* `BITACORA_IA.md`: Registro de uso de inteligencia artificial, destacando las sugerencias rechazadas en favor de mejores prácticas (ej. rechazo a `float` y `math.isclose`).

## 👨‍💻 Decisiones Técnicas Relevantes

1. **`Decimal` vs `float`:** No se utiliza `float` en ninguna parte de la lógica financiera para evitar discrepancias por la precisión de coma flotante de IEEE 754.
2. **Strict Nulls (`| None = None`):** En Pydantic v2, se implementan Union Types nativos forzando defaults de nulos, previniendo inicializaciones con cadenas vacías en caso de carencia de datos.
3. **Idempotencia implícita:** Corrección del error de doble gasto consumiendo formalmente los estados en los scripts de prueba bancarios para prevenir que el comerciante consolide una venta múltiples veces con la misma referencia.
## 📊 Cobertura de pruebas

Para obtener un reporte de cobertura sin depender de la variable `PATH`:

```bash
python -m pip install coverage
python -m coverage run -m pytest -v app/test_main.py
python -m coverage report -m
```

> Si prefieres usar los comandos `coverage` directamente, añade el directorio
> `C:\Users\usuario\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts`
> a tu variable de entorno **PATH**.
