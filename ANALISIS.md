# AnÃ¡lisis de la Prueba TÃ©cnica

## Parte 2 â€” DepuraciÃ³n: Errores en `conciliacion_con_errores.py`

He identificado dos errores crÃ­ticos de negocio y programaciÃ³n en la funciÃ³n original:

### 1. El Error del Doble Gasto (Falta de consumo del correo)
**El cÃ³digo parecÃ­a correcto porque:** En el bucle se filtraba por `if correo.consumido: continue`, asumiendo que un correo ya utilizado no se volverÃ­a a usar.
**El error real:** Al confirmar una conciliaciÃ³n (`if candidato is not None:`), **nunca se estaba modificando el estado del candidato** (`candidato.consumido = True`).
**Consecuencia concreta en el negocio:** Si un comerciante reportaba dos ventas por el mismo monto ($45.50) en ventanas de tiempo cercanas (ej. `V-002` y `V-003`), ambas ventas se aprobarÃ­an contra **el mismo y Ãºnico correo bancario** (`C-002`). El comerciante regalarÃ­a producto/servicio creyendo que le pagaron dos veces, perdiendo dinero directo.

### 2. El Error de PrecisiÃ³n de Dinero (Uso de flotantes)
**El cÃ³digo parecÃ­a correcto porque:** MatemÃ¡ticamente `11.10 + 52.20` suma `63.30`.
**El error real:** Python y la mayorÃ­a de lenguajes usan punto flotante IEEE 754, donde `11.10 + 52.20` en realidad da `63.300000000000004`. Cuando el cÃ³digo comparaba `correo.monto != venta.monto`, fallaba para la venta `V-001` vs el correo `C-001`.
**Consecuencia concreta en el negocio:** Ventas perfectamente legÃ­timas donde el monto derivaba de una suma de productos, jamÃ¡s cruzarÃ­an con su correo equivalente (ej. $63.30). El comerciante verÃ­a el dinero en el banco, pero el sistema le dirÃ­a "Pago no recibido". GenerarÃ­a quejas inmediatas y desconfianza en la plataforma.
*(SoluciÃ³n aplicada: Migrar de `float` a `Decimal`).*

## Parte 3 — Decisión de diseño

**Situación:** El cliente envía el pantallazo a las 14:32, pero el correo bancario con la misma referencia y monto llegó a las 14:28.

**Decisión:** El pago **DEBE SER CONCILIADO Y ACEPTADO**.

### Justificación:
El flujo lógico de un pago en la vida real es el siguiente:
1. El cliente de WhatsApp realiza la transferencia desde su app bancaria (14:28).
2. El banco procesa la transacción de inmediato y dispara el correo electrónico de notificación al comercio (14:28).
3. El cliente ve la confirmación en su pantalla, le toma un pantallazo, abre WhatsApp, busca el chat del micro-comercio, adjunta la imagen y la envía (lo cual toma tiempo humano, resultando en las 14:32).

Es decir, es físicamente imposible que el cliente envíe el pantallazo *antes* de que ocurra la transacción. Lo natural y esperado es que el pantallazo llegue minutos *después* del correo.

### Implicaciones de equivocarse:
* **Si nos equivocamos rechazando (Falso Negativo):** Causamos fricción operativa. Un pago 100% real es declinado automáticamente. El comerciante no entrega el producto, el cliente se queja, y se requiere intervención manual de soporte para liberar la venta, lo cual destruye la propuesta de valor del producto (ahorrar tiempo sin llevar contabilidad manual).
* **Si nos equivocamos aceptando (Falso Positivo):** Existe riesgo económico. Sin embargo, en este escenario específico, validar monto y número de referencia exactos es un control estricto. El único vector de ataque sería que el cliente re-envíe un pantallazo viejo, lo cual ya mitigamos en la Parte 2 al asegurar que los correos bancarios se marcan como consumido = True y no se pueden reutilizar para múltiples ventas.
