# Análisis de la Prueba Técnica

## Parte 2 — Depuración: Errores en `conciliacion_con_errores.py`

He identificado dos errores críticos de negocio y programación en la función original:

### 1. El Error del Doble Gasto (Falta de consumo del correo)
**El código parecía correcto porque:** En el bucle se filtraba por `if correo.consumido: continue`, asumiendo que un correo ya utilizado no se volvería a usar.
**El error real:** Al confirmar una conciliación (`if candidato is not None:`), **nunca se estaba modificando el estado del candidato** (`candidato.consumido = True`).
**Consecuencia concreta en el negocio:** Si un comerciante reportaba dos ventas por el mismo monto ($45.50) en ventanas de tiempo cercanas (ej. `V-002` y `V-003`), ambas ventas se aprobarían contra **el mismo y único correo bancario** (`C-002`). El comerciante regalaría producto/servicio creyendo que le pagaron dos veces, perdiendo dinero directo.

### 2. El Error de Precisión de Dinero (Uso de flotantes)
**El código parecía correcto porque:** Matemáticamente `11.10 + 52.20` suma `63.30`.
**El error real:** Python y la mayoría de lenguajes usan punto flotante IEEE 754, donde `11.10 + 52.20` en realidad da `63.300000000000004`. Cuando el código comparaba `correo.monto != venta.monto`, fallaba para la venta `V-001` vs el correo `C-001`.
**Consecuencia concreta en el negocio:** Ventas perfectamente legítimas donde el monto derivaba de una suma de productos, jamás cruzarían con su correo equivalente (ej. $63.30). El comerciante vería el dinero en el banco, pero el sistema le diría "Pago no recibido". Generaría quejas inmediatas y desconfianza en la plataforma.
*(Solución aplicada: Migrar de `float` a `Decimal`).*
