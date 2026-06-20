"""
WASTE DETECTION SYSTEM - Proyecto 2: Análisis de Muda
=====================================================

Script que analiza datos operacionales y detecta los 8 tipos de
Lean waste (Muda) en procesos de manufactura.

Identifica:
- Tipos de desperdicio
- Cantidad de unidades desperdiciadas
- Horas perdidas
- Impacto financiero
- Recomendaciones de mejora

Autor: Mario Romero
Fecha: Junio 2026
Versión: 1.0
"""

import csv
import sys
from pathlib import Path

# Agregar carpeta padre al path para importar manufacturing_formulas
sys.path.insert(0, str(Path(__file__).parent.parent))

from manufacturing_formulas import calcular_tasa_defectos

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

ARCHIVO_ENTRADA = Path(__file__).parent / "data" / "waste_data.csv"
ARCHIVO_SALIDA = Path(__file__).parent / "output" / "reporte_muda.txt"

# Crear carpeta output si no existe
ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)

# Definiciones de Muda (Lean Waste Types)
MUDA_DESCRIPTIONS = {
    'Overproduction': {
        'numero': 1,
        'nombre': 'Sobreproduccion',
        'descripcion': 'Producir mas de lo necesario o antes de ser solicitado',
        'impacto': 'Exceso de inventario, incremento de espacio, costos de almacenamiento'
    },
    'Inventory': {
        'numero': 2,
        'nombre': 'Inventario',
        'descripcion': 'Exceso de stock o Work-In-Progress (WIP)',
        'impacto': 'Capital inmovilizado, riesgo de obsolescencia, costos de manejo'
    },
    'Motion': {
        'numero': 3,
        'nombre': 'Movimiento',
        'descripcion': 'Movimientos innecesarios de operarios (buscar herramientas, caminar)',
        'impacto': 'Fatiga operaria, baja productividad, lesiones ocupacionales'
    },
    'Waiting': {
        'numero': 4,
        'nombre': 'Espera',
        'descripcion': 'Tiempo ocioso mientras se espera material, informacion o maquina',
        'impacto': 'Baja utilizacion, incremento de lead time, insatisfaccion operaria'
    },
    'Transport': {
        'numero': 5,
        'nombre': 'Transporte',
        'descripcion': 'Movimiento innecesario de materiales entre procesos',
        'impacto': 'Riesgo de danio, consumo de energia, costo de manejo'
    },
    'Over-processing': {
        'numero': 6,
        'nombre': 'Sobre-procesamiento',
        'descripcion': 'Pasos innecesarios, especificaciones excesivas, features no requeridas',
        'impacto': 'Tiempo perdido, costo adicional, complejidad innecesaria'
    },
    'Defects': {
        'numero': 7,
        'nombre': 'Defectos',
        'descripcion': 'Produccion de piezas defectuosas, retrabajo, scrap',
        'impacto': 'Retrabajo costoso, devoluciones, perdida de confiabilidad'
    },
    'Talent': {
        'numero': 8,
        'nombre': 'Talento/Habilidades',
        'descripcion': 'Subutilizacion de capacidades y conocimiento del personal',
        'impacto': 'Perdida de innovacion, baja moral, falta de improvement'
    }
}

# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================

def leer_datos_desperdicio():
    """Lee datos de desperdicio desde CSV.

    Retorna:
        list: Lista de diccionarios con datos de cada desperdicio identificado
    """
    print(f"[LEYENDO] Datos desde: {ARCHIVO_ENTRADA}")

    datos = []
    try:
        with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Convertir strings a números
                fila_convertida = {
                    'linea': fila['linea'],
                    'fecha': fila['fecha'],
                    'tipo_desperdicio': fila['tipo_desperdicio'],
                    'cantidad_unidades': int(fila['cantidad_unidades']),
                    'horas_perdidas': float(fila['horas_perdidas']),
                    'costo_unitario': float(fila['costo_unitario']),
                }
                datos.append(fila_convertida)

    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo {ARCHIVO_ENTRADA}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Leyendo archivo: {e}")
        sys.exit(1)

    print(f"[OK] Se leyeron {len(datos)} registros de desperdicio")
    return datos


def analizar_desperdicio(datos):
    """Analiza datos de desperdicio y calcula métricas de Muda.

    Parámetros:
        datos (list): Lista de diccionarios con datos de desperdicio

    Retorna:
        dict: Diccionario con análisis completo de desperdicio por línea y tipo
    """
    print(f"\n[ANALIZANDO] Datos de desperdicio...")

    # Estructura: linea -> tipo_desperdicio -> lista de registros
    analisis = {}

    for registro in datos:
        linea = registro['linea']
        tipo = registro['tipo_desperdicio']

        # Inicializar estructura si no existe
        if linea not in analisis:
            analisis[linea] = {}

        if tipo not in analisis[linea]:
            analisis[linea][tipo] = {
                'cantidad_total_unidades': 0,
                'horas_totales_perdidas': 0,
                'costo_total': 0,
                'registros': 0,
                'costo_promedio_unitario': 0,
            }

        # Acumular valores
        analisis[linea][tipo]['cantidad_total_unidades'] += registro['cantidad_unidades']
        analisis[linea][tipo]['horas_totales_perdidas'] += registro['horas_perdidas']
        costo_registro = registro['cantidad_unidades'] * registro['costo_unitario']
        analisis[linea][tipo]['costo_total'] += costo_registro
        analisis[linea][tipo]['registros'] += 1

    # Calcular promedios
    for linea in analisis:
        for tipo in analisis[linea]:
            datos_tipo = analisis[linea][tipo]
            if datos_tipo['cantidad_total_unidades'] > 0:
                datos_tipo['costo_promedio_unitario'] = (
                    datos_tipo['costo_total'] / datos_tipo['cantidad_total_unidades']
                )

    print(f"[OK] Se analizaron {sum(len(v) for v in analisis.values())} tipos de desperdicio")
    return analisis


def calcular_resumen_global(analisis):
    """Calcula métricas globales de desperdicio.

    Parámetros:
        analisis (dict): Análisis de desperdicio por línea y tipo

    Retorna:
        dict: Resumen global con totales y promedios
    """
    resumen = {
        'total_unidades_desperdiciadas': 0,
        'total_horas_perdidas': 0,
        'costo_total_desperdicio': 0,
        'desperdicio_por_tipo': {},
        'lineas_analizadas': list(analisis.keys()),
    }

    # Recorrer cada línea y tipo
    for linea in analisis:
        for tipo in analisis[linea]:
            datos_tipo = analisis[linea][tipo]

            # Acumular totales
            resumen['total_unidades_desperdiciadas'] += datos_tipo['cantidad_total_unidades']
            resumen['total_horas_perdidas'] += datos_tipo['horas_totales_perdidas']
            resumen['costo_total_desperdicio'] += datos_tipo['costo_total']

            # Agrupar por tipo de desperdicio
            if tipo not in resumen['desperdicio_por_tipo']:
                resumen['desperdicio_por_tipo'][tipo] = {
                    'unidades': 0,
                    'horas': 0,
                    'costo': 0,
                    'lineas': [],
                }

            resumen['desperdicio_por_tipo'][tipo]['unidades'] += datos_tipo['cantidad_total_unidades']
            resumen['desperdicio_por_tipo'][tipo]['horas'] += datos_tipo['horas_totales_perdidas']
            resumen['desperdicio_por_tipo'][tipo]['costo'] += datos_tipo['costo_total']
            if linea not in resumen['desperdicio_por_tipo'][tipo]['lineas']:
                resumen['desperdicio_por_tipo'][tipo]['lineas'].append(linea)

    return resumen


def generar_reporte(analisis, resumen):
    """Genera reporte profesional de análisis de Muda y lo guarda.

    Parámetros:
        analisis (dict): Análisis detallado de desperdicio
        resumen (dict): Resumen global de métricas
    """
    print(f"\n[GENERANDO] Reporte de Muda...")

    reporte = []
    reporte.append("=" * 80)
    reporte.append("REPORTE MUDA - ANÁLISIS DE DESPERDICIO EN PROCESOS")
    reporte.append("=" * 80)
    reporte.append("")

    # SECCIÓN 1: Análisis por línea de producción
    reporte.append("PARTE I: ANÁLISIS POR LÍNEA DE PRODUCCIÓN")
    reporte.append("-" * 80)
    reporte.append("")

    for linea in sorted(analisis.keys()):
        reporte.append(f"LINEA: {linea}")
        reporte.append("-" * 80)
        reporte.append("")

        # Totales por línea
        total_unidades_linea = sum(
            analisis[linea][tipo]['cantidad_total_unidades']
            for tipo in analisis[linea]
        )
        total_horas_linea = sum(
            analisis[linea][tipo]['horas_totales_perdidas']
            for tipo in analisis[linea]
        )
        total_costo_linea = sum(
            analisis[linea][tipo]['costo_total']
            for tipo in analisis[linea]
        )

        reporte.append(f"  RESUMEN DE LA LINEA:")
        reporte.append(f"    Total Unidades Desperdiciadas: {total_unidades_linea:>6} unidades")
        reporte.append(f"    Total Horas Perdidas:          {total_horas_linea:>6.1f} horas")
        reporte.append(f"    Costo Total Desperdicio:       $ {total_costo_linea:>10,.2f}")
        reporte.append(f"    Costo Promedio por Hora:       $ {total_costo_linea / max(total_horas_linea, 1):>10,.2f}")
        reporte.append("")

        # Detalle por tipo de desperdicio
        reporte.append(f"  DESPERDICIO POR TIPO:")
        reporte.append("")

        for tipo in sorted(analisis[linea].keys()):
            datos_tipo = analisis[linea][tipo]
            reporte.append(f"    {tipo}:")
            reporte.append(f"      Unidades:        {datos_tipo['cantidad_total_unidades']:>6} unidades")
            reporte.append(f"      Horas Perdidas:  {datos_tipo['horas_totales_perdidas']:>6.1f} horas")
            reporte.append(f"      Costo:           $ {datos_tipo['costo_total']:>10,.2f}")
            reporte.append(f"      % del Total:     {(datos_tipo['costo_total'] / max(total_costo_linea, 1)) * 100:>6.1f}%")
            reporte.append("")

        reporte.append("")

    # SECCIÓN 2: Análisis global por tipo de desperdicio
    reporte.append("PARTE II: ANÁLISIS GLOBAL POR TIPO DE DESPERDICIO (8 TIPOS DE MUDA)")
    reporte.append("-" * 80)
    reporte.append("")

    # Ordenar por costo descendente
    tipos_ordenados = sorted(
        resumen['desperdicio_por_tipo'].items(),
        key=lambda x: x[1]['costo'],
        reverse=True
    )

    for tipo, datos in tipos_ordenados:
        if tipo in MUDA_DESCRIPTIONS:
            info = MUDA_DESCRIPTIONS[tipo]
            reporte.append(f"MUDA #{info['numero']}: {info['nombre'].upper()}")
            reporte.append(f"Descripcion: {info['descripcion']}")
            reporte.append(f"Impacto: {info['impacto']}")
            reporte.append("")
            reporte.append(f"  Estadisticas:")
            reporte.append(f"    Unidades Desperdiciadas:  {datos['unidades']:>6} unidades")
            reporte.append(f"    Horas Perdidas:           {datos['horas']:>6.1f} horas")
            reporte.append(f"    Costo Total:              $ {datos['costo']:>10,.2f}")
            reporte.append(f"    % del Total Global:       {(datos['costo'] / max(resumen['costo_total_desperdicio'], 1)) * 100:>6.1f}%")
            reporte.append(f"    Lineas Afectadas:         {', '.join(datos['lineas'])}")
            reporte.append("")

    # SECCIÓN 3: Resumen global y recomendaciones
    reporte.append("=" * 80)
    reporte.append("RESUMEN GLOBAL Y RECOMENDACIONES")
    reporte.append("=" * 80)
    reporte.append("")

    reporte.append(f"Total de Unidades Desperdiciadas:   {resumen['total_unidades_desperdiciadas']:>6} unidades")
    reporte.append(f"Total de Horas Perdidas:            {resumen['total_horas_perdidas']:>6.1f} horas")
    reporte.append(f"COSTO TOTAL DE DESPERDICIO:         $ {resumen['costo_total_desperdicio']:>10,.2f}")
    reporte.append("")

    # Calcular costo por línea
    reporte.append("COSTO DE DESPERDICIO POR LINEA:")
    for linea in sorted(analisis.keys()):
        costo_linea = sum(
            analisis[linea][tipo]['costo_total']
            for tipo in analisis[linea]
        )
        reporte.append(f"  {linea}: $ {costo_linea:>10,.2f}")
    reporte.append("")

    # Top 3 prioridades
    reporte.append("PRIORIDADES DE MEJORA (Top 3 tipos de desperdicio por costo):")
    for i, (tipo, datos) in enumerate(tipos_ordenados[:3], 1):
        if tipo in MUDA_DESCRIPTIONS:
            info = MUDA_DESCRIPTIONS[tipo]
            reporte.append(f"  {i}. {info['nombre'].upper()} - $ {datos['costo']:,.2f}")
    reporte.append("")

    # Calificación general
    reporte.append("=" * 80)
    reporte.append("EVALUACION GENERAL")
    reporte.append("=" * 80)

    # Usar costo por línea como métrica
    promedio_costo_linea = resumen['costo_total_desperdicio'] / max(len(resumen['lineas_analizadas']), 1)

    if resumen['costo_total_desperdicio'] > 100000:
        clasificacion = "CRITICO - REQUIERE ACCION INMEDIATA"
    elif resumen['costo_total_desperdicio'] > 50000:
        clasificacion = "ALTO - MEJORA URGENTE RECOMENDADA"
    elif resumen['costo_total_desperdicio'] > 20000:
        clasificacion = "MODERADO - MEJORA NECESARIA"
    else:
        clasificacion = "BAJO - MONITOREAR"

    reporte.append(f"Nivel de Desperdicio: {clasificacion}")
    reporte.append(f"Costo Promedio por Linea: $ {promedio_costo_linea:,.2f}")
    reporte.append("")
    reporte.append("NOTA: Estos costos representan pérdidas directas en eficiencia operativa.")
    reporte.append("Se recomienda implementar mejoras Lean para reducir el desperdicio.")
    reporte.append("=" * 80)

    # Guardar reporte
    contenido_reporte = "\n".join(reporte)

    try:
        with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_reporte)
        print(f"[OK] Reporte guardado en: {ARCHIVO_SALIDA}")
    except Exception as e:
        print(f"[ERROR] Guardando reporte: {e}")
        return

    # Mostrar reporte en pantalla
    print("\n" + contenido_reporte)


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que orquesta todo."""
    print("\n" + "=" * 80)
    print("WASTE DETECTION SYSTEM - PROYECTO 2: ANÁLISIS DE MUDA")
    print("=" * 80 + "\n")

    # Paso 1: Leer datos
    datos = leer_datos_desperdicio()

    # Paso 2: Analizar desperdicio
    analisis = analizar_desperdicio(datos)

    # Paso 3: Calcular resumen global
    resumen = calcular_resumen_global(analisis)

    # Paso 4: Generar reporte
    generar_reporte(analisis, resumen)

    print("\n[COMPLETADO] Análisis de Muda finalizado!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
