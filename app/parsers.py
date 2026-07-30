import re
from datetime import datetime, date, time
from decimal import Decimal
from app.models import ParseResult

def _parse_monto(monto_str: str) -> Decimal | None:
    if not monto_str: return None
    # Limpiamos el string de todo lo que no sea dígito, coma o punto
    clean_str = re.sub(r'[^\d.,]', '', monto_str).rstrip('.,')
    if not clean_str: return None
    
    # Manejo de separadores decimales (ej. Produbank usa 1.234,56 y otros 45.50)
    if ',' in clean_str and '.' in clean_str:
        clean_str = clean_str.replace('.', '').replace(',', '.')
    elif ',' in clean_str:
        clean_str = clean_str.replace(',', '.')
        
    try:
        return Decimal(clean_str)
    except Exception:
        return None

def _parse_fecha(fecha_str: str) -> date | None:
    try:
        return datetime.strptime(fecha_str.strip(), "%d/%m/%Y").date()
    except Exception:
        return None

def _parse_hora(hora_str: str) -> time | None:
    try:
        return datetime.strptime(hora_str.strip(), "%H:%M").time()
    except Exception:
        return None

def parse_andino(texto: str) -> ParseResult:
    tipo = re.search(r'Tipo de movimiento\s*:\s*(.*)', texto)
    concepto = re.search(r'Concepto\s*:\s*(.*)', texto)
    monto = re.search(r'Valor\s*:\s*(.*)', texto)
    fecha = re.search(r'Fecha\s*:\s*([\d/]+)', texto)
    hora = re.search(r'Hora\s*:\s*([\d:]+)', texto)
    ref = re.search(r'Referencia\s*:\s*(\d+)', texto)
    estado = re.search(r'Estado\s*:\s*(.*)', texto)

    return ParseResult(
        banco="Banco Andino",
        tipo_movimiento=tipo.group(1).strip() if tipo else None,
        concepto=concepto.group(1).strip() if concepto else None,
        monto=_parse_monto(monto.group(1)) if monto else None,
        fecha=_parse_fecha(fecha.group(1)) if fecha else None,
        hora=_parse_hora(hora.group(1)) if hora else None,
        estado=estado.group(1).strip() if estado else None,
        referencia=ref.group(1).strip() if ref else None
    )

def parse_litoral(texto: str) -> ParseResult:
    fecha = re.search(r'el dia ([\d/]+)', texto)
    hora = re.search(r'a las ([\d:]+)', texto)
    monto = re.search(r'por USD ([\d.,]+)', texto)
    ref = re.search(r'referencia (\d+)', texto)
    tipo = "Credito" if re.search(r'acreditacion', texto, re.IGNORECASE) else None

    return ParseResult(
        banco="Banco del Litoral",
        tipo_movimiento=tipo,
        concepto=None,
        monto=_parse_monto(monto.group(1)) if monto else None,
        fecha=_parse_fecha(fecha.group(1)) if fecha else None,
        hora=_parse_hora(hora.group(1)) if hora else None,
        estado=None,
        referencia=ref.group(1).strip() if ref else None
    )

def parse_produbank(texto: str) -> ParseResult:
    tipo = re.search(r'Operacion:\s*(.*)', texto)
    monto = re.search(r'Monto:\s*(.*)', texto)
    fecha = re.search(r'Fecha de proceso:\s*([\d/]+)', texto)
    hora = re.search(r'Hora de proceso:\s*([\d:]+)', texto)
    ref = re.search(r'Nro\. de referencia:\s*(\d+)', texto)
    estado = re.search(r'Estado:\s*(.*)', texto)

    return ParseResult(
        banco="Produbank",
        tipo_movimiento=tipo.group(1).strip() if tipo else None,
        concepto=tipo.group(1).strip() if tipo else None,
        monto=_parse_monto(monto.group(1)) if monto else None,
        fecha=_parse_fecha(fecha.group(1)) if fecha else None,
        hora=_parse_hora(hora.group(1)) if hora else None,
        estado=estado.group(1).strip() if estado else None,
        referencia=ref.group(1).strip() if ref else None
    )

def parse_email(texto: str) -> ParseResult:
    texto_lower = texto.lower()
    if "bancoandino.ec" in texto_lower or "banco andino" in texto_lower:
        return parse_andino(texto)
    if "bancodellitoral.ec" in texto_lower or "banco del litoral" in texto_lower:
        return parse_litoral(texto)
    if "produbank" in texto_lower:
        return parse_produbank(texto)
    
    return ParseResult()
