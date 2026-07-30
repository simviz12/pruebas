# BITACORA_IA.md — Registro de Asistencia de Inteligencia Artificial

**Proyecto:** Servicio de Parseo y Conciliación de Notificaciones Bancarias
**Entorno de Trabajo / Editor:** AntiGravity + FastAPI / Python 3.12
**Desarrollador / Lead:** Carlos Julián Benavides Burbano

## 1. Resumen de la Colaboración
Durante el desarrollo del proyecto, la Inteligencia Artificial fue utilizada como una herramienta de soporte para la estructuración modular del código, generación de patrones de Regex deterministas, diseño de flujos de trabajo en Git (Conventional Commits) y redacción de análisis de arquitectura. Todas las decisiones finales de implementación y las restricciones de negocio fueron auditadas y validadas manualmente.

## 2. Sugerencias Aceptadas

| Categoría | Sugerencia de la IA | Justificación Técnica | Impacto en el Proyecto |
|---|---|---|---|
| **Arquitectura** | Dividir la generación del código en 20 prompts modulares. | Evita el desbordamiento de ventana de contexto en AntiGravity y mantiene cada módulo enfocado en un solo objetivo (Single Responsibility). | Código limpio, testeable y sin code bloat. |
| **Control de Versiones** | Adoptar la convención Conventional Commits (feat, fix, test, docs). | Garantiza un historial de Git limpio, legible y con cambios atómicos para la revisión técnica en GitHub. | Historial con nivel de ingeniería Senior. |
| **Seguridad de Datos** | Retornar `None` (`null` en JSON) en campos ausentes o dudosos. | Cumple de forma estricta con la Regla No Negociable: previene la alucinación de datos y evita poblar la base de datos con valores basura (`""`, `0.0`). | Cero falsos datos en la extracción de notificaciones. |
| **Conciliación (Fix)** | Reemplazar la igualdad estricta `monto1 == monto2` por tolerancia de flotantes (`math.isclose` / `round`). | La representación binaria en coma flotante en Python causa errores imperceptibles (ej. `0.1 + 0.2 != 0.3`). | Evita fallas en la conciliación de pagos válidos. |
| **Idempotencia (Fix)** | Agregar la bandera `conciliado == True` y control de duplicidad por referencia + hora. | Bloquea la posibilidad de procesar dos veces la misma transacción ante reintentos o capturas duplicadas. | Prevención de fraude y dobles cobros. |

## 3. Sugerencias Rechazadas y Correcciones Aplicadas

| Sugerencia de la IA | Razón de Rechazo / Corrección | Decisión Final del Desarrollador |
|---|---|---|
| Uso de LLM/IA Dinámica para parsear el texto de los correos en tiempo real. | Alto costo de API, latencia no determinista y riesgo de alucinación en montos o fechas. | **Rechazado.** Se optó por un enfoque 100% determinista mediante Expresiones Regulares (`re`) y Pydantic. |
| Asignar valores por defecto (ej. `"DESCONOCIDO"` o `"00:00"`) cuando no se encuentre un campo. | Viola explícitamente la Regla No Negociable de la prueba técnica. | **Rechazado.** Todos los atributos opcionales se inicializan estrictamente en `None`. |
| Generación masiva del proyecto en un solo commit ("Commit final de entrega"). | Un solo commit dificulta la trazabilidad de la arquitectura y la evaluación del proceso de pensamiento. | **Rechazado.** Se implementó una secuencia de commits atómicos según cada fase completada. |

## 4. Prompts de Control y Auditoría Utilizados en la Sesión

* **System Prompt de Restricción de Código:** Estableció las reglas de KISS, DRY, prohibición de código muerto (code bloat) y generación de comandos de Conventional Commits por cada fase.
* **Prompt de Modularización (20 Pasos):** Guió la construcción progresiva del servidor FastAPI, modelos Pydantic, suite de pruebas pytest y la lógica de conciliación.
* **Prompt de Auditoría Senior (Code Review / QA):** Verificó el cumplimiento al 100% de la Regla No Negociable, manejo seguro de errores, ejecución de pruebas automatizadas y documentación en Markdown.

## 5. Conclusión de la Auditoría
La solución técnica generada cumple con todos los criterios de rendimiento, mantenibilidad y robustez exigidos. El uso de la IA fue puramente estratégico, guiado por criterios estrictos de arquitectura backend y buenas prácticas de ingeniería de software.
