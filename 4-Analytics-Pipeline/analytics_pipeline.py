"""
FULL ANALYTICS PIPELINE - Proyecto 4: ETL + Análisis Completo
==============================================================

Pipeline completo de análisis que integra múltiples fuentes de datos
y genera inteligencia empresarial procesable.

Flujo ETL:
1. EXTRACT: Lee datos desde múltiples CSV
2. TRANSFORM: Limpia, valida, enriquece datos
3. LOAD: Crea estructuras de datos unificadas
4. ANALYZE: Calcula KPIs, OEE, desperdicio, SPC
5. REPORT: Genera reportes ejecutivos y detallados

Datos Integrados:
- Producción diaria por línea
- Defectos y retrabajo
- Mantenimiento preventivo/correctivo
- Análisis financiero de impacto

Autor: Mario Romero
Fecha: Junio 2026
Versión: 1.0
"""

import csv
import sys
import math
from pathlib import Path
from collections import defaultdict

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

CARPETA_DATOS = Path(__file__).parent / "data"
CARPETA_SALIDA = Path(__file__).parent / "output"

ARCHIVO_PRODUCCION = CARPETA_DATOS / "produccion.csv"
ARCHIVO_DEFECTOS = CARPETA_DATOS / "defectos.csv"
ARCHIVO_MANTENIMIENTO = CARPETA_DATOS / "mantenimiento.csv"

ARCHIVO_RESUMEN = CARPETA_SALIDA / "reporte_ejecutivo.txt"
ARCHIVO_DETALLADO = CARPETA_SALIDA / "reporte_detallado.txt"
ARCHIVO_KPIS = CARPETA_SALIDA / "reporte_kpis.txt"
ARCHIVO_RECOMENDACIONES = CARPETA_SALIDA / "reporte_recomendaciones.txt"

CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def calcular_media(valores):
    """Calcula la media de una lista de valores."""
    return sum(valores) / len(valores) if valores else 0


def calcular_desv_std(valores):
    """Calcula desviación estándar."""
    if not valores or len(valores) < 2:
        return 0
    media = calcular_media(valores)
    varianza = sum((x - media) ** 2 for x in valores) / (len(valores) - 1)
    return math.sqrt(varianza)


# ============================================================================
# PHASE 1: EXTRACT
# ============================================================================

def extraer_produccion():
    """EXTRACT: Lee datos de producción desde CSV."""
    print(f"[EXTRACT] Leyendo datos de producción...")
    datos = []
    try:
        with open(ARCHIVO_PRODUCCION, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                datos.append({
                    'fecha': fila['fecha'],
                    'linea': fila['linea'],
                    'tiempo_total_min': int(fila['tiempo_total_min']),
                    'tiempo_parada_min': int(fila['tiempo_parada_min']),
                    'piezas_producidas': int(fila['piezas_producidas']),
                    'piezas_esperadas': int(fila['piezas_esperadas']),
                    'piezas_buenas': int(fila['piezas_buenas']),
                })
    except Exception as e:
        print(f"[ERROR] Leyendo producción: {e}")
        return []
    print(f"[OK] {len(datos)} registros de producción")
    return datos


def extraer_defectos():
    """EXTRACT: Lee datos de defectos desde CSV."""
    print(f"[EXTRACT] Leyendo datos de defectos...")
    datos = []
    try:
        with open(ARCHIVO_DEFECTOS, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                datos.append({
                    'fecha': fila['fecha'],
                    'linea': fila['linea'],
                    'defectos_totales': int(fila['defectos_totales']),
                    'defectos_retrabajados': int(fila['defectos_retrabajados']),
                    'defectos_scrap': int(fila['defectos_scrap']),
                    'tipo_defecto_principal': fila['tipo_defecto_principal'],
                    'costo_retrabajo': float(fila['costo_retrabajo']),
                })
    except Exception as e:
        print(f"[ERROR] Leyendo defectos: {e}")
        return []
    print(f"[OK] {len(datos)} registros de defectos")
    return datos


def extraer_mantenimiento():
    """EXTRACT: Lee datos de mantenimiento desde CSV."""
    print(f"[EXTRACT] Leyendo datos de mantenimiento...")
    datos = []
    try:
        with open(ARCHIVO_MANTENIMIENTO, 'r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                datos.append({
                    'fecha': fila['fecha'],
                    'linea': fila['linea'],
                    'tipo_mantenimiento': fila['tipo_mantenimiento'],
                    'tiempo_parada_min': int(fila['tiempo_parada_min']),
                    'costo': float(fila['costo']),
                    'causa': fila['causa'],
                })
    except Exception as e:
        print(f"[ERROR] Leyendo mantenimiento: {e}")
        return []
    print(f"[OK] {len(datos)} registros de mantenimiento")
    return datos


# ============================================================================
# PHASE 2: TRANSFORM
# ============================================================================

def transformar_y_validar(prod, defec, mant):
    """TRANSFORM: Limpia, valida y enriquece datos."""
    print(f"\n[TRANSFORM] Validando y transformando datos...")

    # Validación básica
    errores = 0
    if not prod:
        print("[ERROR] No hay datos de producción")
        errores += 1
    if not defec:
        print("[WARNING] No hay datos de defectos")
    if not mant:
        print("[WARNING] No hay datos de mantenimiento")

    # Crear índices para búsqueda rápida
    defectos_por_linea_fecha = defaultdict(dict)
    for d in defec:
        clave = (d['linea'], d['fecha'])
        defectos_por_linea_fecha[clave] = d

    mant_por_linea_fecha = defaultdict(list)
    for m in mant:
        clave = (m['linea'], m['fecha'])
        mant_por_linea_fecha[clave].append(m)

    # Enriquecer datos de producción con defectos y mantenimiento
    for registro in prod:
        clave = (registro['linea'], registro['fecha'])

        # Agregar datos de defectos
        if clave in defectos_por_linea_fecha:
            defecto_data = defectos_por_linea_fecha[clave]
            registro['defectos_totales'] = defecto_data['defectos_totales']
            registro['defectos_retrabajados'] = defecto_data['defectos_retrabajados']
            registro['defectos_scrap'] = defecto_data['defectos_scrap']
            registro['tipo_defecto'] = defecto_data['tipo_defecto_principal']
            registro['costo_retrabajo'] = defecto_data['costo_retrabajo']
        else:
            registro['defectos_totales'] = 0
            registro['defectos_retrabajados'] = 0
            registro['defectos_scrap'] = 0
            registro['tipo_defecto'] = 'N/A'
            registro['costo_retrabajo'] = 0

        # Agregar datos de mantenimiento
        if clave in mant_por_linea_fecha:
            mant_list = mant_por_linea_fecha[clave]
            registro['eventos_mant'] = len(mant_list)
            registro['tiempo_mant_total'] = sum(m['tiempo_parada_min'] for m in mant_list)
            registro['costo_mant_total'] = sum(m['costo'] for m in mant_list)
            registro['tipos_mant'] = [m['tipo_mantenimiento'] for m in mant_list]
        else:
            registro['eventos_mant'] = 0
            registro['tiempo_mant_total'] = 0
            registro['costo_mant_total'] = 0
            registro['tipos_mant'] = []

    print(f"[OK] Datos validados y enriquecidos")
    return prod


# ============================================================================
# PHASE 3: LOAD
# ============================================================================

def cargar_datos_unificados(datos_produccion):
    """LOAD: Crea estructuras de datos unificadas por línea."""
    print(f"\n[LOAD] Creando estructuras de datos unificadas...")

    datos_por_linea = defaultdict(lambda: {
        'registros': [],
        'oee_list': [],
        'defecto_rate_list': [],
        'disponibilidad_list': [],
        'rendimiento_list': [],
        'calidad_list': [],
        'costo_total': 0,
    })

    for registro in datos_produccion:
        linea = registro['linea']

        # Calcular métricas OEE
        tiempo_productivo = registro['tiempo_total_min'] - registro['tiempo_parada_min']
        disponibilidad = (tiempo_productivo / registro['tiempo_total_min'] * 100) if registro['tiempo_total_min'] > 0 else 0
        rendimiento = (registro['piezas_producidas'] / registro['piezas_esperadas'] * 100) if registro['piezas_esperadas'] > 0 else 0
        calidad = (registro['piezas_buenas'] / registro['piezas_producidas'] * 100) if registro['piezas_producidas'] > 0 else 0
        oee = (disponibilidad / 100) * (rendimiento / 100) * (calidad / 100) * 100

        # Defect rate
        defecto_rate = (registro['defectos_totales'] / registro['piezas_producidas'] * 100) if registro['piezas_producidas'] > 0 else 0

        # Enriquecer registro
        registro['disponibilidad'] = disponibilidad
        registro['rendimiento'] = rendimiento
        registro['calidad'] = calidad
        registro['oee'] = oee
        registro['defecto_rate'] = defecto_rate

        # Calcular costo total del día
        costo_defectos = registro['costo_retrabajo']
        costo_mant = registro['costo_mant_total']
        costo_total = costo_defectos + costo_mant
        registro['costo_total'] = costo_total

        # Agregar a estructura por línea
        datos_por_linea[linea]['registros'].append(registro)
        datos_por_linea[linea]['oee_list'].append(oee)
        datos_por_linea[linea]['defecto_rate_list'].append(defecto_rate)
        datos_por_linea[linea]['disponibilidad_list'].append(disponibilidad)
        datos_por_linea[linea]['rendimiento_list'].append(rendimiento)
        datos_por_linea[linea]['calidad_list'].append(calidad)
        datos_por_linea[linea]['costo_total'] += costo_total

    print(f"[OK] {len(datos_por_linea)} líneas de producción cargadas")
    return dict(datos_por_linea)


# ============================================================================
# PHASE 4: ANALYZE
# ============================================================================

def analizar_datos(datos_por_linea):
    """ANALYZE: Calcula KPIs y métricas principales."""
    print(f"\n[ANALYZE] Calculando KPIs...")

    analisis = {}

    for linea, datos in datos_por_linea.items():
        registros = datos['registros']

        # Calcular promedios
        oee_promedio = calcular_media(datos['oee_list'])
        defecto_rate_promedio = calcular_media(datos['defecto_rate_list'])
        disponibilidad_promedio = calcular_media(datos['disponibilidad_list'])
        rendimiento_promedio = calcular_media(datos['rendimiento_list'])
        calidad_promedio = calcular_media(datos['calidad_list'])

        # Calcular variabilidad
        desv_oee = calcular_desv_std(datos['oee_list'])

        # Sumar totales
        total_piezas = sum(r['piezas_producidas'] for r in registros)
        total_defectos = sum(r['defectos_totales'] for r in registros)
        total_paradas = sum(r['tiempo_parada_min'] for r in registros)
        total_costos = datos['costo_total']

        # Calcular MTBF (Mean Time Between Failures) y MTTR (Mean Time To Repair)
        # Si hay eventos de mantenimiento
        eventos_correctivos = sum(1 for r in registros for t in r['tipos_mant'] if t == 'Correctivo')
        tiempo_mant_correctivo = sum(r['tiempo_mant_total'] for r in registros)
        mtbf = (sum(r['tiempo_total_min'] for r in registros) / max(eventos_correctivos, 1)) if eventos_correctivos > 0 else 0
        mttr = (tiempo_mant_correctivo / max(eventos_correctivos, 1)) if eventos_correctivos > 0 else 0

        # Clasificación de estado
        if oee_promedio >= 85:
            estado = 'EXCELENTE'
        elif oee_promedio >= 75:
            estado = 'BUENO'
        elif oee_promedio >= 65:
            estado = 'ACEPTABLE'
        else:
            estado = 'POBRE'

        # Identificar tipo de defecto más frecuente
        defecto_tipos = defaultdict(int)
        for r in registros:
            if r['tipo_defecto'] != 'N/A':
                defecto_tipos[r['tipo_defecto']] += 1
        defecto_principal = max(defecto_tipos.items(), key=lambda x: x[1])[0] if defecto_tipos else 'N/A'

        analisis[linea] = {
            'estado': estado,
            'oee_promedio': oee_promedio,
            'desv_oee': desv_oee,
            'disponibilidad_promedio': disponibilidad_promedio,
            'rendimiento_promedio': rendimiento_promedio,
            'calidad_promedio': calidad_promedio,
            'defecto_rate_promedio': defecto_rate_promedio,
            'total_piezas': total_piezas,
            'total_defectos': total_defectos,
            'total_paradas': total_paradas,
            'total_costos': total_costos,
            'mtbf': mtbf,
            'mttr': mttr,
            'defecto_principal': defecto_principal,
            'registros': registros,
        }

    print(f"[OK] Análisis completado para {len(analisis)} líneas")
    return analisis


# ============================================================================
# PHASE 5: REPORT
# ============================================================================

def generar_reporte_ejecutivo(analisis):
    """Genera reporte ejecutivo (1 página)."""
    print(f"\n[REPORT] Generando reporte ejecutivo...")

    reporte = []
    reporte.append("=" * 80)
    reporte.append("REPORTE EJECUTIVO - ANALYTICS PIPELINE")
    reporte.append("=" * 80)
    reporte.append("")

    # Resumen global
    total_oee = calcular_media([a['oee_promedio'] for a in analisis.values()])
    total_defectos = sum(a['total_defectos'] for a in analisis.values())
    total_costos = sum(a['total_costos'] for a in analisis.values())

    reporte.append(f"OEE PROMEDIO GLOBAL: {total_oee:.1f}%")
    reporte.append(f"DEFECTOS TOTALES: {total_defectos}")
    reporte.append(f"COSTO TOTAL: $ {total_costos:,.2f}")
    reporte.append("")

    # Estado por línea
    reporte.append("ESTADO POR LINEA:")
    for linea in sorted(analisis.keys()):
        a = analisis[linea]
        reporte.append(f"  {linea}: OEE {a['oee_promedio']:>5.1f}% ({a['estado']}) - Defectos: {a['total_defectos']} - Costo: ${a['total_costos']:>10,.2f}")

    reporte.append("")
    reporte.append("=" * 80)

    contenido = "\n".join(reporte)
    try:
        with open(ARCHIVO_RESUMEN, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"[OK] Reporte ejecutivo guardado")
    except Exception as e:
        print(f"[ERROR] Guardando reporte ejecutivo: {e}")

    print(contenido)


def generar_reporte_detallado(analisis):
    """Genera reporte detallado completo."""
    print(f"\n[REPORT] Generando reporte detallado...")

    reporte = []
    reporte.append("=" * 90)
    reporte.append("REPORTE DETALLADO - ANÁLISIS COMPLETO DE PRODUCCIÓN")
    reporte.append("=" * 90)
    reporte.append("")

    for linea in sorted(analisis.keys()):
        a = analisis[linea]
        reporte.append(f"LINEA: {linea}")
        reporte.append("-" * 90)
        reporte.append("")

        # KPIs principales
        reporte.append("INDICADORES PRINCIPALES:")
        reporte.append(f"  Estado General:              {a['estado']}")
        reporte.append(f"  OEE Promedio:                {a['oee_promedio']:>6.2f}%  (Desv: {a['desv_oee']:.2f}%)")
        reporte.append(f"  Disponibilidad Promedio:     {a['disponibilidad_promedio']:>6.2f}%")
        reporte.append(f"  Rendimiento Promedio:        {a['rendimiento_promedio']:>6.2f}%")
        reporte.append(f"  Calidad Promedio:            {a['calidad_promedio']:>6.2f}%")
        reporte.append("")

        # Defectos
        reporte.append("ANÁLISIS DE CALIDAD:")
        reporte.append(f"  Total Piezas Producidas:     {a['total_piezas']:>6}")
        reporte.append(f"  Total Defectos:              {a['total_defectos']:>6}")
        reporte.append(f"  Defect Rate Promedio:        {a['defecto_rate_promedio']:>6.2f}%")
        reporte.append(f"  Defecto Tipo Principal:      {a['defecto_principal']}")
        reporte.append("")

        # Mantenimiento
        reporte.append("ANÁLISIS DE MANTENIMIENTO:")
        reporte.append(f"  Horas Parada Total:          {a['total_paradas']:>6.0f} min ({a['total_paradas']/60:.1f} horas)")
        reporte.append(f"  MTBF (Mean Time Between Failures): {a['mtbf']:>6.0f} min")
        reporte.append(f"  MTTR (Mean Time To Repair):  {a['mttr']:>6.0f} min")
        reporte.append("")

        # Costos
        reporte.append("ANÁLISIS FINANCIERO:")
        reporte.append(f"  Costo Total del Período:     $ {a['total_costos']:>10,.2f}")
        reporte.append(f"  Costo Promedio por Día:      $ {a['total_costos']/len(a['registros']):>10,.2f}")
        reporte.append("")

        # Detalle diario
        reporte.append("DETALLE DIARIO:")
        for r in a['registros']:
            reporte.append(f"  {r['fecha']}: OEE {r['oee']:>5.1f}% - Defectos: {r['defectos_totales']:>2} - Costo: ${r['costo_total']:>8,.2f}")

        reporte.append("")
        reporte.append("")

    reporte.append("=" * 90)

    contenido = "\n".join(reporte)
    try:
        with open(ARCHIVO_DETALLADO, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"[OK] Reporte detallado guardado")
    except Exception as e:
        print(f"[ERROR] Guardando reporte detallado: {e}")

    print(contenido)


def generar_recomendaciones(analisis):
    """Genera recomendaciones de mejora priorizadas por ROI."""
    print(f"\n[REPORT] Generando recomendaciones...")

    reporte = []
    reporte.append("=" * 90)
    reporte.append("RECOMENDACIONES DE MEJORA - PRIORIZADO POR ROI")
    reporte.append("=" * 90)
    reporte.append("")

    mejoras = []

    for linea, a in analisis.items():
        # Oportunidad 1: OEE bajo
        if a['oee_promedio'] < 85:
            impacto_potencial = a['total_costos'] * 0.15  # 15% improvement potential
            mejoras.append({
                'linea': linea,
                'tipo': 'OEE',
                'descripcion': f'Mejorar OEE de {a["oee_promedio"]:.1f}% a 85%+',
                'impacto_potencial': impacto_potencial,
                'prioridad': 'ALTA' if a['oee_promedio'] < 70 else 'MEDIA',
            })

        # Oportunidad 2: Defectos altos
        if a['defecto_rate_promedio'] > 2:
            impacto_potencial = a['total_defectos'] * 50  # $50 per defect
            mejoras.append({
                'linea': linea,
                'tipo': 'DEFECTOS',
                'descripcion': f'Reducir defectos de {a["defecto_rate_promedio"]:.2f}% al 1% (Enfoque: {a["defecto_principal"]})',
                'impacto_potencial': impacto_potencial,
                'prioridad': 'ALTA',
            })

        # Oportunidad 3: Mantenimiento correctivo alto
        eventos_correctivos = sum(1 for r in a['registros'] for t in r['tipos_mant'] if t == 'Correctivo')
        if eventos_correctivos > 0:
            impacto_potencial = eventos_correctivos * 500  # $500 per corrective event saved
            mejoras.append({
                'linea': linea,
                'tipo': 'MANT_PREVENTIVO',
                'descripcion': f'Aumentar mantenimiento preventivo (Eventos correctivos: {eventos_correctivos})',
                'impacto_potencial': impacto_potencial,
                'prioridad': 'MEDIA',
            })

    # Ordenar por impacto potencial
    mejoras.sort(key=lambda x: x['impacto_potencial'], reverse=True)

    reporte.append(f"Total Oportunidades Identificadas: {len(mejoras)}")
    reporte.append(f"Ahorro Potencial Total: $ {sum(m['impacto_potencial'] for m in mejoras):,.2f}")
    reporte.append("")

    for i, mejora in enumerate(mejoras[:10], 1):  # Top 10
        reporte.append(f"{i}. [{mejora['prioridad']}] {mejora['linea']} - {mejora['tipo']}")
        reporte.append(f"   {mejora['descripcion']}")
        reporte.append(f"   Ahorro Potencial: $ {mejora['impacto_potencial']:,.2f}")
        reporte.append("")

    reporte.append("=" * 90)

    contenido = "\n".join(reporte)
    try:
        with open(ARCHIVO_RECOMENDACIONES, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"[OK] Recomendaciones guardadas")
    except Exception as e:
        print(f"[ERROR] Guardando recomendaciones: {e}")

    print(contenido)


# ============================================================================
# EJECUCIÓN PRINCIPAL - ETL PIPELINE
# ============================================================================

def main():
    """Ejecuta el pipeline completo ETL."""
    print("\n" + "=" * 90)
    print("FULL ANALYTICS PIPELINE - PROYECTO 4: ETL + ANÁLISIS COMPLETO")
    print("=" * 90 + "\n")

    # PHASE 1: EXTRACT
    produccion = extraer_produccion()
    defectos = extraer_defectos()
    mantenimiento = extraer_mantenimiento()

    if not produccion:
        print("[ERROR] No se pueden cargar datos de producción")
        sys.exit(1)

    # PHASE 2: TRANSFORM
    datos_transformados = transformar_y_validar(produccion, defectos, mantenimiento)

    # PHASE 3: LOAD
    datos_por_linea = cargar_datos_unificados(datos_transformados)

    # PHASE 4: ANALYZE
    analisis = analizar_datos(datos_por_linea)

    # PHASE 5: REPORT
    generar_reporte_ejecutivo(analisis)
    generar_reporte_detallado(analisis)
    generar_recomendaciones(analisis)

    print("\n[COMPLETADO] Pipeline ETL finalizado!")
    print("=" * 90 + "\n")


if __name__ == "__main__":
    main()
