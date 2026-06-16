"""
OEE ANALYZER - Proyecto 1: Análisis de Eficiencia
==================================================

Script que lee datos de producción y calcula:
- OEE (Overall Equipment Effectiveness)
- Análisis 6 Sigma (DPMO, Sigma Level)
- Reportes profesionales

Autor: Mario Romero
Fecha: Junio 2026
Versión: 1.0
"""

import csv
import sys
from pathlib import Path

# Agregar carpeta padre al path para importar manufacturing_formulas
sys.path.insert(0, str(Path(__file__).parent.parent))

from manufacturing_formulas import (
    calcular_disponibilidad,
    calcular_rendimiento,
    calcular_calidad,
    calcular_oee,
    calcular_dpmo,
    calcular_sigma_nivel
)

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

ARCHIVO_ENTRADA = Path(__file__).parent / "data" / "production_data.csv"
ARCHIVO_SALIDA = Path(__file__).parent / "output" / "reporte_oee.txt"

# Crear carpeta output si no existe
ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)


# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================

def leer_datos_produccion():
    """Lee datos de producción desde CSV.

    Retorna:
        list: Lista de diccionarios con datos de cada turno
    """
    print(f"📖 Leyendo datos desde: {ARCHIVO_ENTRADA}")

    datos = []
    try:
        with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Convertir strings a números
                fila_convertida = {
                    'fecha': fila['fecha'],
                    'linea': fila['linea'],
                    'tiempo_total_min': float(fila['tiempo_total_min']),
                    'tiempo_parada_min': float(fila['tiempo_parada_min']),
                    'piezas_producidas': int(fila['piezas_producidas']),
                    'piezas_esperadas': int(fila['piezas_esperadas']),
                    'piezas_buenas': int(fila['piezas_buenas']),
                    'defectos': int(fila['defectos']),
                }
                datos.append(fila_convertida)

    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo {ARCHIVO_ENTRADA}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR leyendo archivo: {e}")
        sys.exit(1)

    print(f"✅ Se leyeron {len(datos)} registros")
    return datos


def analizar_datos(datos):
    """Analiza datos de producción y calcula métricas.

    Parámetros:
        datos (list): Lista de diccionarios con datos de producción

    Retorna:
        list: Lista de diccionarios con resultados del análisis
    """
    print(f"\n⚙️  Analizando datos...")

    resultados = []

    for fila in datos:
        try:
            # Extraer valores
            fecha = fila['fecha']
            linea = fila['linea']
            tiempo_total = fila['tiempo_total_min']
            tiempo_parada = fila['tiempo_parada_min']
            piezas_producidas = fila['piezas_producidas']
            piezas_esperadas = fila['piezas_esperadas']
            piezas_buenas = fila['piezas_buenas']
            defectos = fila['defectos']

            # CÁLCULO 1: OEE (Disponibilidad, Rendimiento, Calidad)
            disp = calcular_disponibilidad(tiempo_total, tiempo_parada)
            rend = calcular_rendimiento(piezas_producidas, piezas_esperadas)
            cal = calcular_calidad(piezas_buenas, piezas_producidas)
            oee = calcular_oee(disp/100, rend/100, cal/100)

            # CÁLCULO 2: 6 Sigma (DPMO y Sigma Level)
            # Asumimos 3 oportunidades de error por unidad
            oportunidades_por_unidad = 3
            dpmo = calcular_dpmo(defectos, oportunidades_por_unidad, piezas_producidas)
            sigma_nivel = calcular_sigma_nivel(dpmo)

            # Clasificación Sigma
            if sigma_nivel < 2:
                sigma_clase = "INACEPTABLE"
            elif sigma_nivel < 3:
                sigma_clase = "POBRE"
            elif sigma_nivel < 4:
                sigma_clase = "ACEPTABLE"
            elif sigma_nivel < 5:
                sigma_clase = "BUENO"
            elif sigma_nivel < 6:
                sigma_clase = "EXCELENTE"
            else:
                sigma_clase = "WORLD CLASS"

            # Guardar resultado
            resultado = {
                'fecha': fecha,
                'linea': linea,
                'disponibilidad': disp,
                'rendimiento': rend,
                'calidad': cal,
                'oee': oee,
                'dpmo': dpmo,
                'sigma_nivel': sigma_nivel,
                'sigma_clase': sigma_clase,
            }
            resultados.append(resultado)

        except Exception as e:
            print(f"⚠️  Error analizando {linea} ({fecha}): {e}")
            continue

    print(f"✅ Se analizaron {len(resultados)} registros")
    return resultados


def generar_reporte(resultados):
    """Genera reporte profesional y lo guarda.

    Parámetros:
        resultados (list): Lista de diccionarios con análisis
    """
    print(f"\n📝 Generando reporte...")

    reporte = []
    reporte.append("=" * 70)
    reporte.append("REPORTE OEE - ANÁLISIS DE EFICIENCIA DE PRODUCCIÓN")
    reporte.append("=" * 70)
    reporte.append("")

    # Datos por línea
    lineas_unicas = {}
    for resultado in resultados:
        linea = resultado['linea']
        if linea not in lineas_unicas:
            lineas_unicas[linea] = []
        lineas_unicas[linea].append(resultado)

    # Análisis por línea
    for linea, datos_linea in sorted(lineas_unicas.items()):
        reporte.append(f"LÍNEA: {linea}")
        reporte.append("-" * 70)
        reporte.append("")

        # Promedios de la línea
        disp_prom = sum(d['disponibilidad'] for d in datos_linea) / len(datos_linea)
        rend_prom = sum(d['rendimiento'] for d in datos_linea) / len(datos_linea)
        cal_prom = sum(d['calidad'] for d in datos_linea) / len(datos_linea)
        oee_prom = sum(d['oee'] for d in datos_linea) / len(datos_linea)

        reporte.append(f"  Disponibilidad (Promedio): {disp_prom:>6.1f}%")
        reporte.append(f"  Rendimiento (Promedio):    {rend_prom:>6.1f}%")
        reporte.append(f"  Calidad (Promedio):        {cal_prom:>6.1f}%")
        reporte.append(f"  ─────────────────────────────────────")
        reporte.append(f"  OEE TOTAL (Promedio):      {oee_prom:>6.2f}%")
        reporte.append("")

        # Detalle por día
        reporte.append("  Detalle por turno:")
        for dato in datos_linea:
            reporte.append(f"    {dato['fecha']} | OEE: {dato['oee']:>6.2f}% | " +
                          f"Sigma: {dato['sigma_nivel']:.1f} ({dato['sigma_clase']})")

        reporte.append("")
        reporte.append("")

    # Resumen general
    reporte.append("=" * 70)
    reporte.append("RESUMEN GENERAL")
    reporte.append("=" * 70)

    oee_general = sum(r['oee'] for r in resultados) / len(resultados)
    sigma_general = sum(r['sigma_nivel'] for r in resultados) / len(resultados)

    reporte.append(f"OEE Promedio (Todas las líneas): {oee_general:.2f}%")
    reporte.append(f"Sigma Promedio:                  {sigma_general:.1f}")
    reporte.append("")

    # Clasificación final
    if oee_general >= 90:
        clase_oee = "EXCELENTE"
    elif oee_general >= 80:
        clase_oee = "BUENO"
    elif oee_general >= 70:
        clase_oee = "ACEPTABLE"
    else:
        clase_oee = "POBRE - REQUIERE MEJORA"

    reporte.append(f"Clasificación OEE: {clase_oee}")
    reporte.append("=" * 70)

    # Guardar reporte
    contenido_reporte = "\n".join(reporte)

    try:
        with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_reporte)
        print(f"✅ Reporte guardado en: {ARCHIVO_SALIDA}")
    except Exception as e:
        print(f"❌ Error guardando reporte: {e}")
        return

    # Mostrar reporte en pantalla
    print("\n" + contenido_reporte)


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que orquesta todo."""
    print("\n" + "=" * 70)
    print("🏭 OEE ANALYZER - PROYECTO 1")
    print("=" * 70 + "\n")

    # Paso 1: Leer datos
    datos = leer_datos_produccion()

    # Paso 2: Analizar
    resultados = analizar_datos(datos)

    # Paso 3: Generar reporte
    generar_reporte(resultados)

    print("\n✅ ¡ANÁLISIS COMPLETADO!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
