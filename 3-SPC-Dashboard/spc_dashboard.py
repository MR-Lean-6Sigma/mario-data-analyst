"""
SPC DASHBOARD - Proyecto 3: Control Estadístico de Procesos
===========================================================

Script que implementa Statistical Process Control (SPC) para monitorear
procesos de manufactura y detectar anomalías usando control charts.

Funcionalidades:
- Calcula límites de control (±3 sigma)
- Detecta puntos fuera de control
- Identifica tendencias y cambios de proceso
- Genera alertas basadas en reglas SPC
- Crea reportes profesionales con gráficos ASCII

Reglas de Control (Western Electric):
1. 1 punto > 3 sigma: Fuera de control
2. 2 de 3 puntos > 2 sigma: Aproximándose a límite
3. 4 de 5 puntos > 1 sigma: Tendencia a límite
4. 8 puntos consecutivos en mismo lado: Cambio de proceso
5. 6 puntos consecutivos subiendo/bajando: Tendencia

Autor: Mario Romero
Fecha: Junio 2026
Versión: 1.0
"""

import csv
import sys
import math
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

ARCHIVO_ENTRADA = Path(__file__).parent / "data" / "process_measurements.csv"
ARCHIVO_SALIDA = Path(__file__).parent / "output" / "reporte_spc.txt"

ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)

# ============================================================================
# FUNCIONES DE ESTADÍSTICA
# ============================================================================

def calcular_media(valores):
    """Calcula la media aritmética de una lista de valores.

    Parámetros:
        valores (list): Lista de números

    Retorna:
        float: Media aritmética
    """
    if not valores:
        return 0
    return sum(valores) / len(valores)


def calcular_desv_std(valores, media=None):
    """Calcula la desviación estándar de una lista de valores.

    Parámetros:
        valores (list): Lista de números
        media (float): Media precalculada (opcional)

    Retorna:
        float: Desviación estándar
    """
    if not valores or len(valores) < 2:
        return 0

    if media is None:
        media = calcular_media(valores)

    suma_cuadrados = sum((x - media) ** 2 for x in valores)
    varianza = suma_cuadrados / (len(valores) - 1)
    return math.sqrt(varianza)


# ============================================================================
# LECTURA DE DATOS
# ============================================================================

def leer_mediciones_proceso():
    """Lee datos de mediciones del proceso desde CSV.

    Retorna:
        dict: Diccionario con datos organizados por línea de producción
    """
    print(f"[LEYENDO] Datos desde: {ARCHIVO_ENTRADA}")

    mediciones = {}
    try:
        with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                linea = fila['linea']
                fecha = fila['fecha']
                medicion = float(fila['medicion'])
                especificacion = float(fila['especificacion'])

                if linea not in mediciones:
                    mediciones[linea] = {
                        'fechas': [],
                        'valores': [],
                        'especificacion': especificacion,
                    }

                mediciones[linea]['fechas'].append(fecha)
                mediciones[linea]['valores'].append(medicion)

    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo {ARCHIVO_ENTRADA}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Leyendo archivo: {e}")
        sys.exit(1)

    print(f"[OK] Se leyeron {sum(len(m['valores']) for m in mediciones.values())} mediciones")
    return mediciones


# ============================================================================
# ANÁLISIS SPC
# ============================================================================

def analizar_spc(mediciones):
    """Realiza análisis SPC completo por línea de producción.

    Parámetros:
        mediciones (dict): Datos de mediciones por línea

    Retorna:
        dict: Análisis SPC completo con alertas
    """
    print(f"\n[ANALIZANDO] Datos con Statistical Process Control...")

    analisis = {}

    for linea, datos in mediciones.items():
        valores = datos['valores']
        fechas = datos['fechas']

        # Calcular estadísticas
        media = calcular_media(valores)
        desv_std = calcular_desv_std(valores, media)

        # Límites de control (±3 sigma)
        lcl = media - 3 * desv_std  # Lower Control Limit
        ucl = media + 3 * desv_std  # Upper Control Limit
        lwa = media - 2 * desv_std  # Lower Warning Limit (2 sigma)
        uwa = media + 2 * desv_std  # Upper Warning Limit (2 sigma)
        lal = media - 1 * desv_std  # Lower Alert Limit (1 sigma)
        ual = media + 1 * desv_std  # Upper Alert Limit (1 sigma)

        # Detectar puntos fuera de control y alertas
        puntos_ooc = []  # Out of control
        puntos_warning = []
        puntos_alert = []
        puntos_normales = []

        for i, valor in enumerate(valores):
            punto_info = {
                'indice': i,
                'fecha': fechas[i],
                'valor': valor,
                'desv_de_media': valor - media,
            }

            if valor < lcl or valor > ucl:
                punto_info['estado'] = 'OUT_OF_CONTROL'
                puntos_ooc.append(punto_info)
            elif valor < lwa or valor > uwa:
                punto_info['estado'] = 'WARNING'
                puntos_warning.append(punto_info)
            elif valor < lal or valor > ual:
                punto_info['estado'] = 'ALERT'
                puntos_alert.append(punto_info)
            else:
                punto_info['estado'] = 'NORMAL'
                puntos_normales.append(punto_info)

        # Detectar tendencias (6 puntos consecutivos subiendo o bajando)
        tendencias = []
        for i in range(len(valores) - 5):
            ventana = valores[i:i+6]
            # Verificar si todos suben
            if all(ventana[j] < ventana[j+1] for j in range(5)):
                tendencias.append({
                    'tipo': 'INCREASING',
                    'inicio': i,
                    'fin': i+5,
                    'fecha_inicio': fechas[i],
                    'fecha_fin': fechas[i+5],
                })
            # Verificar si todos bajan
            elif all(ventana[j] > ventana[j+1] for j in range(5)):
                tendencias.append({
                    'tipo': 'DECREASING',
                    'inicio': i,
                    'fin': i+5,
                    'fecha_inicio': fechas[i],
                    'fecha_fin': fechas[i+5],
                })

        # Detectar cambio de proceso (8 puntos consecutivos en mismo lado)
        cambios_proceso = []
        for i in range(len(valores) - 7):
            ventana = valores[i:i+8]
            arriba_de_media = sum(1 for v in ventana if v > media)
            if arriba_de_media == 8:
                cambios_proceso.append({
                    'tipo': 'ABOVE_CENTER',
                    'inicio': i,
                    'fin': i+7,
                    'fecha_inicio': fechas[i],
                    'fecha_fin': fechas[i+7],
                })
            elif arriba_de_media == 0:
                cambios_proceso.append({
                    'tipo': 'BELOW_CENTER',
                    'inicio': i,
                    'fin': i+7,
                    'fecha_inicio': fechas[i],
                    'fecha_fin': fechas[i+7],
                })

        # Calcular capacidad del proceso
        rango = max(valores) - min(valores)
        cpk_potencial = (ucl - lcl) / (6 * desv_std) if desv_std > 0 else 0

        # Clasificación general
        if puntos_ooc:
            clasificacion = 'OUT_OF_CONTROL'
        elif cambios_proceso or tendencias:
            clasificacion = 'WARNING'
        elif puntos_warning:
            clasificacion = 'CAUTION'
        else:
            clasificacion = 'IN_CONTROL'

        analisis[linea] = {
            'media': media,
            'desv_std': desv_std,
            'lcl': lcl,
            'ucl': ucl,
            'lwa': lwa,
            'uwa': uwa,
            'lal': lal,
            'ual': ual,
            'min': min(valores),
            'max': max(valores),
            'rango': rango,
            'cpk': cpk_potencial,
            'especificacion': datos['especificacion'],
            'total_mediciones': len(valores),
            'puntos_ooc': puntos_ooc,
            'puntos_warning': puntos_warning,
            'puntos_alert': puntos_alert,
            'puntos_normales': puntos_normales,
            'tendencias': tendencias,
            'cambios_proceso': cambios_proceso,
            'clasificacion': clasificacion,
            'valores': valores,
            'fechas': fechas,
        }

    print(f"[OK] Se completó análisis SPC de {len(analisis)} líneas")
    return analisis


# ============================================================================
# GENERACIÓN DE REPORTES
# ============================================================================

def generar_grafico_ascii(valores, media, lcl, ucl, lwa, uwa, ancho=60, alto=20):
    """Genera un gráfico ASCII de control chart.

    Parámetros:
        valores (list): Valores del proceso
        media (float): Media del proceso
        lcl (float): Lower Control Limit
        ucl (float): Upper Control Limit
        lwa (float): Lower Warning Limit
        uwa (float): Upper Warning Limit
        ancho (int): Ancho del gráfico en caracteres
        alto (int): Alto del gráfico en líneas

    Retorna:
        str: Gráfico ASCII como string
    """
    if not valores:
        return "No data"

    # Determinar escala
    min_val = min(valores + [lcl, lwa])
    max_val = max(valores + [ucl, uwa])
    rango = max_val - min_val
    if rango == 0:
        rango = 1

    # Crear matriz de caracteres
    grafico = [['.' for _ in range(ancho)] for _ in range(alto)]

    # Dibujar líneas de control
    for col in range(ancho):
        # UCL
        row_ucl = int((1 - (ucl - min_val) / rango) * (alto - 1))
        row_ucl = max(0, min(alto - 1, row_ucl))
        grafico[row_ucl][col] = '-'

        # LCL
        row_lcl = int((1 - (lcl - min_val) / rango) * (alto - 1))
        row_lcl = max(0, min(alto - 1, row_lcl))
        grafico[row_lcl][col] = '-'

        # Media
        row_media = int((1 - (media - min_val) / rango) * (alto - 1))
        row_media = max(0, min(alto - 1, row_media))
        grafico[row_media][col] = '='

    # Plotear valores
    for i, valor in enumerate(valores):
        col = int((i / max(1, len(valores) - 1)) * (ancho - 1))
        row = int((1 - (valor - min_val) / rango) * (alto - 1))
        row = max(0, min(alto - 1, row))

        if valor < lcl or valor > ucl:
            grafico[row][col] = 'X'
        elif valor < lwa or valor > uwa:
            grafico[row][col] = 'W'
        else:
            grafico[row][col] = '*'

    # Convertir a string
    resultado = '\n'.join(''.join(fila) for fila in grafico)
    return resultado


def generar_reporte(analisis):
    """Genera reporte profesional de SPC y lo guarda.

    Parámetros:
        analisis (dict): Análisis SPC de todas las líneas
    """
    print(f"\n[GENERANDO] Reporte de SPC...")

    reporte = []
    reporte.append("=" * 90)
    reporte.append("SPC DASHBOARD - CONTROL ESTADÍSTICO DE PROCESOS")
    reporte.append("=" * 90)
    reporte.append("")

    # PARTE I: Análisis por línea
    reporte.append("PARTE I: ANÁLISIS POR LÍNEA DE PRODUCCIÓN")
    reporte.append("-" * 90)
    reporte.append("")

    for linea in sorted(analisis.keys()):
        datos = analisis[linea]
        reporte.append(f"LINEA: {linea}")
        reporte.append(f"Estado: {datos['clasificacion']}")
        reporte.append("-" * 90)
        reporte.append("")

        # Estadísticas básicas
        reporte.append("ESTADÍSTICAS:")
        reporte.append(f"  Media (Centro):           {datos['media']:>8.2f}")
        reporte.append(f"  Desviación Estándar:      {datos['desv_std']:>8.4f}")
        reporte.append(f"  Valor Mínimo:             {datos['min']:>8.2f}")
        reporte.append(f"  Valor Máximo:             {datos['max']:>8.2f}")
        reporte.append(f"  Rango:                    {datos['rango']:>8.2f}")
        reporte.append("")

        # Límites de control
        reporte.append("LÍMITES DE CONTROL:")
        reporte.append(f"  Upper Control Limit (+3s):  {datos['ucl']:>8.2f}  (Crítico)")
        reporte.append(f"  Upper Warning Limit (+2s):  {datos['uwa']:>8.2f}  (Advertencia)")
        reporte.append(f"  Upper Alert Limit (+1s):    {datos['ual']:>8.2f}  (Alerta)")
        reporte.append(f"  CENTER (Media):              {datos['media']:>8.2f}")
        reporte.append(f"  Lower Alert Limit (-1s):    {datos['lal']:>8.2f}  (Alerta)")
        reporte.append(f"  Lower Warning Limit (-2s):  {datos['lwa']:>8.2f}  (Advertencia)")
        reporte.append(f"  Lower Control Limit (-3s):  {datos['lcl']:>8.2f}  (Crítico)")
        reporte.append("")

        # Control Chart
        reporte.append("CONTROL CHART (ASCII):")
        reporte.append(f"  * = Normal  W = Warning  X = Out of Control")
        reporte.append("")
        grafico = generar_grafico_ascii(
            datos['valores'], datos['media'], datos['lcl'], datos['ucl'],
            datos['lwa'], datos['uwa']
        )
        for linea_grafico in grafico.split('\n'):
            reporte.append(f"  {linea_grafico}")
        reporte.append("")

        # Resumen de estado
        reporte.append("ESTADO DEL PROCESO:")
        reporte.append(f"  Total Mediciones:            {datos['total_mediciones']:>3}")
        reporte.append(f"  Puntos Normales:             {len(datos['puntos_normales']):>3}")
        reporte.append(f"  Puntos en Alerta (+1s):      {len(datos['puntos_alert']):>3}")
        reporte.append(f"  Puntos en Advertencia (+2s): {len(datos['puntos_warning']):>3}")
        reporte.append(f"  Puntos Fuera de Control:     {len(datos['puntos_ooc']):>3}")
        reporte.append("")

        # Alertas específicas
        if datos['puntos_ooc']:
            reporte.append("PUNTOS FUERA DE CONTROL (CRÍTICO):")
            for punto in datos['puntos_ooc']:
                reporte.append(f"  {punto['fecha']}: {punto['valor']:>8.2f}  (Desv: {punto['desv_de_media']:>+6.2f}s)")
            reporte.append("")

        if datos['cambios_proceso']:
            reporte.append("CAMBIOS DE PROCESO DETECTADOS:")
            for cambio in datos['cambios_proceso']:
                tipo = "ARRIBA de centro" if cambio['tipo'] == 'ABOVE_CENTER' else "ABAJO de centro"
                reporte.append(f"  {cambio['fecha_inicio']} a {cambio['fecha_fin']}: 8 puntos consecutivos {tipo}")
            reporte.append("")

        if datos['tendencias']:
            reporte.append("TENDENCIAS DETECTADAS:")
            for tendencia in datos['tendencias']:
                tipo = "SUBIENDO" if tendencia['tipo'] == 'INCREASING' else "BAJANDO"
                reporte.append(f"  {tendencia['fecha_inicio']} a {tendencia['fecha_fin']}: 6 puntos consecutivos {tipo}")
            reporte.append("")

        # Recomendaciones
        reporte.append("RECOMENDACIONES:")
        if datos['clasificacion'] == 'OUT_OF_CONTROL':
            reporte.append("  [CRÍTICO] Proceso FUERA DE CONTROL. Acción inmediata requerida:")
            reporte.append("  - Detener y revisar el proceso")
            reporte.append("  - Investigar causa raíz de variación")
            reporte.append("  - Aplicar correcciones antes de continuar")
        elif datos['clasificacion'] == 'WARNING':
            reporte.append("  [ADVERTENCIA] Proceso muestra tendencias o cambios:")
            reporte.append("  - Monitorear de cerca")
            reporte.append("  - Investigar causa de la tendencia")
            reporte.append("  - Prevenir que se salga de control")
        elif datos['clasificacion'] == 'CAUTION':
            reporte.append("  [PRECAUCIÓN] Proceso acercándose a límites:")
            reporte.append("  - Incrementar frecuencia de muestreo")
            reporte.append("  - Revisar parámetros del proceso")
            reporte.append("  - Prevenir deterioro futuro")
        else:
            reporte.append("  [BUENO] Proceso en control estadístico:")
            reporte.append("  - Continuar monitoreo normal")
            reporte.append("  - Mantener registros de SPC")

        reporte.append("")
        reporte.append("")

    # PARTE II: Resumen global
    reporte.append("=" * 90)
    reporte.append("PARTE II: RESUMEN GLOBAL")
    reporte.append("=" * 90)
    reporte.append("")

    estados = {}
    for linea, datos in analisis.items():
        estado = datos['clasificacion']
        if estado not in estados:
            estados[estado] = []
        estados[estado].append(linea)

    reporte.append("ESTADO GENERAL DE PROCESOS:")
    for estado in ['OUT_OF_CONTROL', 'WARNING', 'CAUTION', 'IN_CONTROL']:
        if estado in estados:
            lineas = ', '.join(estados[estado])
            reporte.append(f"  {estado}: {lineas}")

    reporte.append("")
    reporte.append("PROCESOS EN CONTROL: Continuar operación normal")
    reporte.append("PROCESOS EN ADVERTENCIA: Aumentar supervisión")
    reporte.append("PROCESOS FUERA DE CONTROL: Acción inmediata requerida")
    reporte.append("")
    reporte.append("=" * 90)

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
    print("\n" + "=" * 90)
    print("SPC DASHBOARD - PROYECTO 3: CONTROL ESTADÍSTICO DE PROCESOS")
    print("=" * 90 + "\n")

    # Paso 1: Leer mediciones
    mediciones = leer_mediciones_proceso()

    # Paso 2: Realizar análisis SPC
    analisis = analizar_spc(mediciones)

    # Paso 3: Generar reporte
    generar_reporte(analisis)

    print("\n[COMPLETADO] Análisis SPC finalizado!")
    print("=" * 90 + "\n")


if __name__ == "__main__":
    main()
