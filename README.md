# Parseo de Notificaciones Bancarias (Proyecto Final)

Este repositorio contiene un microservicio **FastAPI** que parsea notificaciones bancarias en texto plano y las transforma en datos estructurados y tipados.

## 🚀 Estado del proyecto
- ✅ Docker configurado y funcionando (`docker build` y `docker run` exitosos).
- ✅ Todas las pruebas pasan (`pytest -q`).
- ✅ Documentación completa en **GUIA_SECRETA_ENTREVISTA.md** (conceptos, preguntas de entrevista, checklist de despliegue).
- ✅ Código limpio: `conciliacion_con_errores.py` refinado y sin lógica ejecutable directa.

## 📦 Requisitos
- Python 3.12+ (recomendado entorno virtual)
- Docker (opcional para pruebas en contenedor)

## 🛠️ Instalación
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución local
```bash
uvicorn app.main:app --reload
```
Visita `http://127.0.0.1:8000/docs` para la OpenAPI UI.

## 🐳 Ejecutar con Docker
```bash
docker build -t fastapi-notificaciones .
docker run -p 8000:8000 fastapi-notificaciones
```

## ✅ Pruebas
```bash
pytest -q app/test_main.py
```

## 📈 Cobertura
```bash
pip install coverage
coverage run -m pytest -q app/test_main.py
coverage report -m
```

## 📚 Documentación adicional
- **GUIA_SECRETA_ENTREVISTA.md**: guía exhaustiva para entrevistas, conceptos a estudiar y checklist de validación.
- **ANALISIS.md** y **BITACORA_IA.md**: decisiones de diseño y registro de iteraciones.

---
> **Nota:** El proyecto está listo para ser evaluado y desplegado. Si deseas contribuir, abre un Pull Request.
