"""
LIBRERÍA DE FÓRMULAS MANUFACTURERAS
=====================================

Módulo Python con todas las fórmulas de producción y 6 Sigma.
Convierte tus cálculos de Excel a código profesional reutilizable.

Autor: Mario Romero
Fecha: Junio 2026
Versión: 1.0

CONTENIDO:
  - Cálculos de OEE (Overall Equipment Effectiveness)
  - Análisis de 6 Sigma (DPMO, Sigma Level)
  - Disponibilidad, Rendimiento, Calidad
  - Análisis de Capacidad (Cp, Cpk)
  - Cálculos de Eficiencia
"""

# ============================================================================
# SECCIÓN 1: CÁLCULOS DE OEE
# ============================================================================

def calcular_disponibilidad(tiempo_total, tiempo_parada):
    """Calcula la Disponibilidad del equipamiento.

    La Disponibilidad es el % de tiempo que la máquina estuvo operativa.

    Fórmula:
        Disponibilidad = (Tiempo Total - Tiempo de Parada) / Tiempo Total × 100

    Parámetros:
        tiempo_total (float): Tiempo total del turno en minutos
        tiempo_parada (float): Tiempo que estuvo parada la máquina en minutos

    Retorna:
        float: Porcentaje de disponibilidad (0-100)

    Ejemplo:
        >>> calcular_disponibilidad(480, 60)  # 8 horas, 1 hora parada
        87.5
    """
    if tiempo_total <= 0:
        raise ValueError("tiempo_total debe ser > 0")

    tiempo_productivo = tiempo_total - tiempo_parada
    disponibilidad = (tiempo_productivo / tiempo_total) * 100

    return disponibilidad


def calcular_rendimiento(piezas_producidas, piezas_esperadas):
    """Calcula el Rendimiento (Velocidad) de producción.

    El Rendimiento es el % de piezas que se produjeron vs lo esperado.

    Fórmula:
        Rendimiento = Piezas Producidas / Piezas Esperadas × 100

    Parámetros:
        piezas_producidas (int): Número de piezas producidas
        piezas_esperadas (int): Número de piezas que se debían producir

    Retorna:
        float: Porcentaje de rendimiento (0-100+)

    Ejemplo:
        >>> calcular_rendimiento(1450, 1500)  # Produjimos 1450 de 1500
        96.67
    """
    if piezas_esperadas <= 0:
        raise ValueError("piezas_esperadas debe ser > 0")

    rendimiento = (piezas_producidas / piezas_esperadas) * 100
    return rendimiento


def calcular_calidad(piezas_buenas, piezas_totales):
    """Calcula la Calidad (% de piezas sin defectos).

    La Calidad es el % de piezas aceptables sin defectos.

    Fórmula:
        Calidad = Piezas Buenas / Piezas Totales × 100

    Parámetros:
        piezas_buenas (int): Número de piezas sin defectos
        piezas_totales (int): Número total de piezas producidas

    Retorna:
        float: Porcentaje de calidad (0-100)

    Ejemplo:
        >>> calcular_calidad(1485, 1500)  # 1485 buenas de 1500
        99.0
    """
    if piezas_totales <= 0:
        raise ValueError("piezas_totales debe ser > 0")

    calidad = (piezas_buenas / piezas_totales) * 100
    return calidad


def calcular_oee(disponibilidad, rendimiento, calidad):
    """Calcula el OEE (Overall Equipment Effectiveness).

    OEE es la métrica de eficiencia ESTÁNDAR en manufactura.
    Combina disponibilidad, rendimiento y calidad.

    Fórmula:
        OEE = Disponibilidad × Rendimiento × Calidad
        (Nota: Usar decimales, no porcentajes. 85% = 0.85)

    Parámetros:
        disponibilidad (float): % disponibilidad en decimal (0-1)
        rendimiento (float): % rendimiento en decimal (0-1)
        calidad (float): % calidad en decimal (0-1)

    Retorna:
        float: OEE en porcentaje (0-100)

    Clasificación:
        90%+ : Excelente (World Class)
        80-89%: Bueno
        70-79%: Aceptable
        < 70%: Pobre

    Ejemplo:
        >>> calcular_oee(0.875, 0.967, 0.99)  # 87.5%, 96.7%, 99%
        83.46
    """
    oee = disponibilidad * rendimiento * calidad * 100
    return round(oee, 2)


# ============================================================================
# SECCIÓN 2: ANÁLISIS 6 SIGMA
# ============================================================================

def calcular_dpmo(defectos, oportunidades, unidades):
    """Calcula DPMO (Defects Per Million Opportunities).

    DPMO es la métrica de 6 Sigma que mide defectos por millón de oportunidades.

    Fórmula:
        DPMO = (Defectos / (Unidades × Oportunidades por Unidad)) × 1,000,000

    Parámetros:
        defectos (int): Número total de defectos encontrados
        oportunidades (int): Número de oportunidades de error por unidad
        unidades (int): Número de unidades inspeccionadas

    Retorna:
        float: DPMO (valor entre 0 y 1,000,000)

    Ejemplo:
        >>> calcular_dpmo(5, 3, 1000)  # 5 defectos, 3 oportunidades, 1000 unidades
        1666.67
    """
    if unidades <= 0 or oportunidades <= 0:
        raise ValueError("unidades y oportunidades deben ser > 0")

    dpmo = (defectos / (unidades * oportunidades)) * 1000000
    return round(dpmo, 2)


def calcular_sigma_nivel(dpmo):
    """Calcula el Nivel Sigma basado en DPMO.

    Tabla de referencia Sigma:
        - 1 Sigma: 308,537 DPMO (69.15% bueno / 30.85% defectos) - INACEPTABLE
        - 2 Sigma: 66,807 DPMO (95.45% bueno / 4.55% defectos) - POBRE
        - 3 Sigma: 6,210 DPMO (99.73% bueno / 0.27% defectos) - ACEPTABLE
        - 4 Sigma: 233 DPMO (99.9937% bueno / 0.0063% defectos) - BUENO
        - 5 Sigma: 3.4 DPMO (99.99966% bueno / 0.00034% defectos) - EXCELENTE
        - 6 Sigma: 0.002 DPMO (99.9999998% bueno / 0.0000002% defectos) - WORLD CLASS

    Parámetros:
        dpmo (float): Defectos por millón de oportunidades

    Retorna:
        float: Nivel Sigma (1-6+)

    Ejemplo:
        >>> calcular_sigma_nivel(66807)
        2.0
    """
    # Tabla de referencia DPMO por Sigma
    sigma_table = {
        6.0: 3.4,
        5.8: 8,
        5.6: 20,
        5.4: 49,
        5.2: 117,
        5.0: 233,
        4.8: 570,
        4.6: 1350,
        4.4: 3170,
        4.2: 6210,
        4.0: 6210,
        3.8: 12200,
        3.6: 22750,
        3.4: 35930,
        3.2: 50000,
        3.0: 66807,
        2.8: 84270,
        2.6: 115070,
        2.4: 159000,
        2.2: 228000,
        2.0: 308537,
        1.8: 420000,
        1.6: 548000,
        1.4: 691000,
        1.2: 841000,
        1.0: 933000,
    }

    # Encontrar el sigma más cercano
    closest_sigma = 1.0
    min_diff = abs(dpmo - sigma_table[1.0])

    for sigma, dpmo_ref in sigma_table.items():
        diff = abs(dpmo - dpmo_ref)
        if diff < min_diff:
            min_diff = diff
            closest_sigma = sigma

    return closest_sigma


# ============================================================================
# SECCIÓN 3: ANÁLISIS DE CAPACIDAD
# ============================================================================

def calcular_cp(lse, lie, sigma):
    """Calcula Cp (Capacidad del Proceso).

    Cp mide cuánto espacio hay dentro de los límites de especificación.

    Fórmula:
        Cp = (LSE - LIE) / (6 × Sigma)

    Parámetros:
        lse (float): Límite Superior de Especificación
        lie (float): Límite Inferior de Especificación
        sigma (float): Desviación estándar del proceso

    Retorna:
        float: Valor de Cp

    Interpretación:
        Cp < 1.0: Proceso INCAPAZ
        1.0 ≤ Cp < 1.33: Proceso MARGINALMENTE CAPAZ
        Cp ≥ 1.33: Proceso CAPAZ
        Cp ≥ 1.67: Proceso MUY CAPAZ

    Ejemplo:
        >>> calcular_cp(110, 90, 5)
        0.667
    """
    if sigma == 0:
        raise ValueError("sigma no puede ser 0")

    cp = (lse - lie) / (6 * sigma)
    return round(cp, 3)


def calcular_cpk(lse, lie, media, sigma):
    """Calcula Cpk (Capacidad del Proceso considerando el centrado).

    Cpk es como Cp pero también considera si el proceso está centrado.
    Es más realista que Cp solo.

    Fórmula:
        Cpk = MIN((LSE - Media) / (3 × Sigma), (Media - LIE) / (3 × Sigma))

    Parámetros:
        lse (float): Límite Superior de Especificación
        lie (float): Límite Inferior de Especificación
        media (float): Media del proceso
        sigma (float): Desviación estándar

    Retorna:
        float: Valor de Cpk

    Ejemplo:
        >>> calcular_cpk(110, 90, 100, 5)
        0.667
    """
    if sigma == 0:
        raise ValueError("sigma no puede ser 0")

    cpu = (lse - media) / (3 * sigma)  # Capacidad superior
    cpl = (media - lie) / (3 * sigma)  # Capacidad inferior
    cpk = min(cpu, cpl)

    return round(cpk, 3)


# ============================================================================
# SECCIÓN 4: CÁLCULOS ADICIONALES
# ============================================================================

def calcular_eficiencia_global(piezas_buenas, tiempo_turno_minutos):
    """Calcula Eficiencia Global simple.

    Parámetros:
        piezas_buenas (int): Piezas sin defectos producidas
        tiempo_turno_minutos (float): Minutos del turno

    Retorna:
        float: Eficiencia en % (piezas buenas / minutos × 100)

    Ejemplo:
        >>> calcular_eficiencia_global(1485, 480)
        309.38
    """
    if tiempo_turno_minutos <= 0:
        raise ValueError("tiempo_turno_minutos debe ser > 0")

    eficiencia = (piezas_buenas / tiempo_turno_minutos) * 100
    return round(eficiencia, 2)


def calcular_tasa_defectos(defectos, total_producido):
    """Calcula la Tasa de Defectos en %.

    Parámetros:
        defectos (int): Número de piezas defectuosas
        total_producido (int): Total de piezas producidas

    Retorna:
        float: Porcentaje de defectos (0-100)

    Ejemplo:
        >>> calcular_tasa_defectos(15, 1500)
        1.0
    """
    if total_producido <= 0:
        raise ValueError("total_producido debe ser > 0")

    tasa = (defectos / total_producido) * 100
    return round(tasa, 2)


# ============================================================================
# SECCIÓN 5: REPORTES
# ============================================================================

def generar_reporte_oee(disponibilidad_pct, rendimiento_pct, calidad_pct):
    """Genera un reporte visual de OEE.

    Parámetros:
        disponibilidad_pct (float): % de disponibilidad (0-100)
        rendimiento_pct (float): % de rendimiento (0-100)
        calidad_pct (float): % de calidad (0-100)

    Retorna:
        str: Reporte formateado

    Ejemplo:
        >>> print(generar_reporte_oee(87.5, 96.7, 99.0))
    """
    # Convertir porcentajes a decimales
    disp_decimal = disponibilidad_pct / 100
    rend_decimal = rendimiento_pct / 100
    cal_decimal = calidad_pct / 100

    # Calcular OEE
    oee = calcular_oee(disp_decimal, rend_decimal, cal_decimal)

    # Generar reporte
    reporte = f"""
{'='*60}
REPORTE DE OEE (Overall Equipment Effectiveness)
{'='*60}
Disponibilidad (A):        {disponibilidad_pct:>6.1f}%
Rendimiento (P):           {rendimiento_pct:>6.1f}%
Calidad (Q):               {calidad_pct:>6.1f}%
{'-'*60}
OEE = A × P × Q =          {oee:>6.2f}%
{'='*60}

Clasificación:
"""

    if oee >= 90:
        reporte += "  EXCELENTE (World Class) - 90%+\n"
    elif oee >= 80:
        reporte += "  BUENO - 80-89%\n"
    elif oee >= 70:
        reporte += "  ACEPTABLE - 70-79%\n"
    else:
        reporte += "  POBRE - <70% (Requiere mejora)\n"

    reporte += "="*60

    return reporte


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  LIBRERÍA DE FÓRMULAS MANUFACTURERAS                       ║
    ║  Manufacturing Formulas Library                            ║
    ║                                                            ║
    ║  Uso: from manufacturing_formulas import *                ║
    ║  O:   import manufacturing_formulas as mf                 ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    # EJEMPLO 1: Calcular OEE simple
    print("\nEJEMPLO 1: Calcular OEE")
    print("-" * 60)

    disp = calcular_disponibilidad(480, 60)    # 8 horas, 1 hora parada
    rend = calcular_rendimiento(1450, 1500)    # 1450 de 1500 piezas
    cal = calcular_calidad(1435, 1450)         # 1435 buenas de 1450

    print(f"Disponibilidad: {disp:.1f}%")
    print(f"Rendimiento:    {rend:.1f}%")
    print(f"Calidad:        {cal:.1f}%")

    oee = calcular_oee(disp/100, rend/100, cal/100)
    print(f"\nOEE Total: {oee:.2f}%")

    # EJEMPLO 2: Análisis 6 Sigma
    print("\n\nEJEMPLO 2: Análisis 6 Sigma")
    print("-" * 60)

    dpmo = calcular_dpmo(5, 3, 1000)
    sigma = calcular_sigma_nivel(dpmo)

    print(f"DPMO: {dpmo:.2f}")
    print(f"Sigma Level: {sigma:.1f}")

    # EJEMPLO 3: Reporte completo
    print(generar_reporte_oee(87.5, 96.7, 99.0))
