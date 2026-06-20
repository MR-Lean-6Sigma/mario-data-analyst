"""
SIX SIGMA INTEGRATION - Proyecto 5: DMAIC + Análisis de ROI
===========================================================

Implementación completa de un proyecto Six Sigma usando la metodología DMAIC:
- Define: Definir el problema
- Measure: Medir baselines
- Analyze: Analizar causas raíz
- Improve: Proponer mejoras
- Control: Monitorear y medir ROI

Este proyecto integra todo lo aprendido en los proyectos anteriores
y lo aplica a un caso de mejora real con impacto financiero.

Autor: Mario Romero (Six Sigma Green Belt)
Fecha: Junio 2026
Versión: 1.0
"""

import math
from pathlib import Path
from collections import defaultdict

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

ARCHIVO_SALIDA = Path(__file__).parent / "output" / "reporte_dmaic.txt"
ARCHIVO_PARETO = Path(__file__).parent / "output" / "analisis_pareto.txt"
ARCHIVO_ROI = Path(__file__).parent / "output" / "proyeccion_roi.txt"

ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)

# ============================================================================
# DATOS DEL PROYECTO DMAIC
# ============================================================================

# PHASE 1: DEFINE
PROYECTO = {
    'nombre': 'Reducir Defectos en Línea B',
    'owner': 'Mario Romero',
    'fecha_inicio': '2026-06-16',
    'fecha_target': '2026-08-31',
    'problema': 'Línea B presenta tasa de defectos de 3.05%, causando costos de retrabajo y pérdida de producción',
    'objetivo_defectos': 1.0,  # Objetivo: reducir a 1% o menos
    'objetivo_sigma': 4.0,  # Objetivo: alcanzar Sigma 4
}

# PHASE 2: MEASURE - Datos Baseline
BASELINE_LINEA_B = {
    'periodo': '16-20 Jun 2026',
    'dias_medicion': 5,
    'piezas_producidas': 1870,
    'defectos_totales': 56,
    'defectos_rate': 3.05,  # %
    'sigma_level': 3.2,  # Calculado
    'dpmo': 30500,  # Defects Per Million Opportunities
    'costo_defectos': 2800.00,
    'costo_mantenimiento': 5200.00,
    'costo_total': 8000.00,
}

# PHASE 3: ANALYZE - Análisis de Causas Raíz (Pareto)
DEFECTOS_POR_TIPO = {
    'Ensamble incorrecto': {
        'cantidad': 18,
        'porcentaje': 32.1,
        'costo_promedio': 50.00,
        'causa_raiz': 'Jig de fijación desalineado, entrenamiento insuficiente del operario',
    },
    'Acabado defectuoso': {
        'cantidad': 16,
        'porcentaje': 28.6,
        'costo_promedio': 40.00,
        'causa_raiz': 'Abrasivo desgastado, presión de contacto inconsistente',
    },
    'Dimensión incorrecta': {
        'cantidad': 14,
        'porcentaje': 25.0,
        'costo_promedio': 45.00,
        'causa_raiz': 'Calibración de máquina fuera de rango, falta de verificación entre piezas',
    },
    'Otros': {
        'cantidad': 8,
        'porcentaje': 14.3,
        'costo_promedio': 35.00,
        'causa_raiz': 'Variación de materiales, ambiente de producción (temperatura/humedad)',
    },
}

# PHASE 4: IMPROVE - Soluciones Propuestas
SOLUCIONES = {
    'Realinear jig de fijación': {
        'tipo_defecto': 'Ensamble incorrecto',
        'costo_implementacion': 800.00,
        'reduccion_esperada': 60,  # % reducción de este tipo de defecto
        'defectos_evitados': 11,  # 60% de 18
        'ahorro_esperado': 550.00,  # 11 * $50
        'tiempo_implementacion': '3 días',
    },
    'Cambiar abrasivo y revisar presión': {
        'tipo_defecto': 'Acabado defectuoso',
        'costo_implementacion': 400.00,
        'reduccion_esperada': 75,  # % reducción
        'defectos_evitados': 12,  # 75% de 16
        'ahorro_esperado': 480.00,  # 12 * $40
        'tiempo_implementacion': '2 días',
    },
    'Recalibrar máquina y crear checklist': {
        'tipo_defecto': 'Dimensión incorrecta',
        'costo_implementacion': 600.00,
        'reduccion_esperada': 70,  # % reducción
        'defectos_evitados': 10,  # 70% de 14
        'ahorro_esperado': 450.00,  # 10 * $45
        'tiempo_implementacion': '2 días',
    },
    'Implementar plan de mantenimiento preventivo': {
        'tipo_defecto': 'Todos',
        'costo_implementacion': 500.00,
        'reduccion_esperada': 30,  # % reducción global
        'defectos_evitados': 17,  # 30% de 56
        'ahorro_esperado': 510.00,
        'tiempo_implementacion': '1 semana',
    },
}

# PHASE 5: CONTROL - Proyección Post-Mejora
PROYECCION_POST_MEJORA = {
    'piezas_producidas': 1870,
    'defectos_estimados': 16,  # 56 - (11+12+10+17) = 56 - 50, pero algunos solapan
    'defectos_rate_estimada': 0.85,
    'sigma_level_estimada': 4.1,
    'dpmo_estimada': 8500,
    'costo_defectos_estimado': 800.00,
    'costo_mant_estimado': 5200.00,
    'costo_total_estimado': 6000.00,
    'ahorro_esperado_anual': (8000.00 - 6000.00) * 12,  # Proyectado a 12 meses
}

# Cálculo de costos
COSTO_TOTAL_IMPLEMENTACION = sum(s['costo_implementacion'] for s in SOLUCIONES.values())
AHORRO_TOTAL_ESPERADO_MENSUAL = sum(s['ahorro_esperado'] for s in SOLUCIONES.values())
AHORRO_TOTAL_ANUAL = AHORRO_TOTAL_ESPERADO_MENSUAL * 12

ROI = ((AHORRO_TOTAL_ANUAL - COSTO_TOTAL_IMPLEMENTACION) / COSTO_TOTAL_IMPLEMENTACION * 100) if COSTO_TOTAL_IMPLEMENTACION > 0 else 0
PAYBACK_PERIOD = COSTO_TOTAL_IMPLEMENTACION / max(AHORRO_TOTAL_ESPERADO_MENSUAL, 1)

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def calcular_sigma_level(defecto_rate):
    """Calcula el nivel Sigma basado en el defect rate."""
    if defecto_rate <= 0.3:
        return 5.0
    elif defecto_rate <= 0.7:
        return 4.5
    elif defecto_rate <= 1.3:
        return 4.0
    elif defecto_rate <= 3.4:
        return 3.5
    elif defecto_rate <= 6.7:
        return 3.0
    else:
        return 2.0


# ============================================================================
# GENERACIÓN DE REPORTES
# ============================================================================

def generar_reporte_dmaic():
    """Genera reporte completo DMAIC."""
    print(f"\n[REPORT] Generando reporte DMAIC...")

    reporte = []
    reporte.append("=" * 100)
    reporte.append("PROYECTO SIX SIGMA - METODOLOGÍA DMAIC")
    reporte.append("=" * 100)
    reporte.append("")

    # PHASE 1: DEFINE
    reporte.append("FASE 1: DEFINE (Definir el Problema)")
    reporte.append("-" * 100)
    reporte.append("")
    reporte.append(f"Proyecto: {PROYECTO['nombre']}")
    reporte.append(f"Owner: {PROYECTO['owner']} (Green Belt)")
    reporte.append(f"Período: {PROYECTO['fecha_inicio']} a {PROYECTO['fecha_target']}")
    reporte.append(f"Problema: {PROYECTO['problema']}")
    reporte.append("")
    reporte.append("OBJETIVOS DEL PROYECTO:")
    reporte.append(f"  - Reducir defect rate de 3.05% a {PROYECTO['objetivo_defectos']}% o menos")
    reporte.append(f"  - Mejorar Sigma Level de 3.2 a {PROYECTO['objetivo_sigma']}")
    reporte.append(f"  - Ahorrar ${PROYECCION_POST_MEJORA['ahorro_esperado_anual']:,.2f} anuales")
    reporte.append("")
    reporte.append("SCOPE DEL PROYECTO:")
    reporte.append("  - Línea B de producción")
    reporte.append("  - Todas las categorías de defectos")
    reporte.append("  - Período de medición: 5 días")
    reporte.append("")
    reporte.append("")

    # PHASE 2: MEASURE
    reporte.append("FASE 2: MEASURE (Medir Baseline)")
    reporte.append("-" * 100)
    reporte.append("")
    reporte.append("DATOS BASELINE (16-20 Junio 2026):")
    reporte.append(f"  Período de Medición: {BASELINE_LINEA_B['periodo']}")
    reporte.append(f"  Piezas Producidas: {BASELINE_LINEA_B['piezas_producidas']:,}")
    reporte.append(f"  Defectos Totales: {BASELINE_LINEA_B['defectos_totales']}")
    reporte.append(f"  Defect Rate: {BASELINE_LINEA_B['defectos_rate']:.2f}%")
    reporte.append(f"  DPMO (Defects Per Million Opportunities): {BASELINE_LINEA_B['dpmo']:,}")
    reporte.append(f"  Sigma Level: {BASELINE_LINEA_B['sigma_level']:.1f}")
    reporte.append(f"  Costo de Defectos: ${BASELINE_LINEA_B['costo_defectos']:,.2f}")
    reporte.append(f"  Costo de Mantenimiento: ${BASELINE_LINEA_B['costo_mantenimiento']:,.2f}")
    reporte.append(f"  Costo Total Línea B: ${BASELINE_LINEA_B['costo_total']:,.2f}")
    reporte.append("")
    reporte.append("SISTEMA DE MEDICIÓN:")
    reporte.append("  - Inspección 100% al final de línea")
    reporte.append("  - Registro diario de defectos por tipo")
    reporte.append("  - Cálculo de DPMO y Sigma nivel automático")
    reporte.append("  - Validación de datos por supervisor")
    reporte.append("")
    reporte.append("")

    # PHASE 3: ANALYZE
    reporte.append("FASE 3: ANALYZE (Analizar Causas Raíz)")
    reporte.append("-" * 100)
    reporte.append("")
    reporte.append("ANÁLISIS DE PARETO (80/20 Rule):")
    reporte.append("")

    acumulado = 0
    for tipo, datos in sorted(DEFECTOS_POR_TIPO.items(), key=lambda x: x[1]['cantidad'], reverse=True):
        acumulado += datos['cantidad']
        reporte.append(f"{tipo}:")
        reporte.append(f"  Cantidad: {datos['cantidad']} defectos ({datos['porcentaje']:.1f}%)")
        reporte.append(f"  Acumulado: {acumulado} ({acumulado/56*100:.1f}%)")
        reporte.append(f"  Costo Promedio por Defecto: ${datos['costo_promedio']:.2f}")
        reporte.append(f"  Causa Raíz Identificada: {datos['causa_raiz']}")
        reporte.append("")

    reporte.append("CONCLUSIONES DEL ANÁLISIS:")
    reporte.append("  - 3 tipos de defecto representan 85.7% del total (Ensamble, Acabado, Dimensión)")
    reporte.append("  - Top 2 defectos (Ensamble + Acabado) = 60.7% del problema")
    reporte.append("  - Enfoque: 20% de causas generan 80% del impacto")
    reporte.append("  - Estrategia: Enfocarse en Ensamble (32.1%) y Acabado (28.6%)")
    reporte.append("")
    reporte.append("")

    # PHASE 4: IMPROVE
    reporte.append("FASE 4: IMPROVE (Proponer Mejoras)")
    reporte.append("-" * 100)
    reporte.append("")
    reporte.append("SOLUCIONES PROPUESTAS Y ANÁLISIS:")
    reporte.append("")

    for i, (solucion, datos) in enumerate(SOLUCIONES.items(), 1):
        reporte.append(f"{i}. {solucion.upper()}")
        reporte.append(f"   Objetivo: {datos['tipo_defecto']}")
        reporte.append(f"   Reducción Esperada: {datos['reduccion_esperada']}%")
        reporte.append(f"   Defectos Evitados: {datos['defectos_evitados']}")
        reporte.append(f"   Ahorro Esperado: ${datos['ahorro_esperado']:.2f}")
        reporte.append(f"   Costo de Implementación: ${datos['costo_implementacion']:.2f}")
        reporte.append(f"   Tiempo de Implementación: {datos['tiempo_implementacion']}")
        reporte.append("")

    reporte.append("RESUMEN DE INVERSIÓN Y RETORNO:")
    reporte.append(f"  Costo Total de Implementación: ${COSTO_TOTAL_IMPLEMENTACION:,.2f}")
    reporte.append(f"  Ahorro Esperado (Mensual): ${AHORRO_TOTAL_ESPERADO_MENSUAL:,.2f}")
    reporte.append(f"  Ahorro Esperado (Anual): ${AHORRO_TOTAL_ANUAL:,.2f}")
    reporte.append(f"  ROI Esperado: {ROI:.1f}%")
    reporte.append(f"  Payback Period: {PAYBACK_PERIOD:.1f} meses")
    reporte.append("")
    reporte.append("")

    # PHASE 5: CONTROL
    reporte.append("FASE 5: CONTROL (Monitorear y Sostener)")
    reporte.append("-" * 100)
    reporte.append("")
    reporte.append("PROYECCIÓN POST-MEJORA:")
    reporte.append(f"  Piezas Producidas (esperado): {PROYECCION_POST_MEJORA['piezas_producidas']:,}")
    reporte.append(f"  Defectos Estimados: {PROYECCION_POST_MEJORA['defectos_estimados']}")
    reporte.append(f"  Defect Rate Estimada: {PROYECCION_POST_MEJORA['defectos_rate_estimada']:.2f}%")
    reporte.append(f"  Sigma Level Estimado: {PROYECCION_POST_MEJORA['sigma_level_estimada']:.1f}")
    reporte.append(f"  DPMO Estimado: {PROYECCION_POST_MEJORA['dpmo_estimada']:,}")
    reporte.append("")
    reporte.append("MEJORA EN COSTOS:")
    reporte.append(f"  Costo Actual (Mensual): ${BASELINE_LINEA_B['costo_total']/5:,.2f}")
    reporte.append(f"  Costo Estimado (Mensual): ${PROYECCION_POST_MEJORA['costo_total_estimado']/5:,.2f}")
    reporte.append(f"  Ahorro (Mensual): ${(BASELINE_LINEA_B['costo_total'] - PROYECCION_POST_MEJORA['costo_total_estimado'])/5:,.2f}")
    reporte.append(f"  Ahorro (Anual): ${PROYECCION_POST_MEJORA['ahorro_esperado_anual']:,.2f}")
    reporte.append("")
    reporte.append("PLAN DE CONTROL:")
    reporte.append("  - Mantener inspección 100% durante 4 semanas")
    reporte.append("  - Muestreo de 5% después de 4 semanas si mejora se sostiene")
    reporte.append("  - Auditoría mensual de proceso")
    reporte.append("  - Re-entrenamiento trimestral de operarios")
    reporte.append("  - Mantenimiento preventivo según schedule")
    reporte.append("")
    reporte.append("")

    # CONCLUSIÓN
    reporte.append("=" * 100)
    reporte.append("CONCLUSIÓN Y RECOMENDACIÓN")
    reporte.append("=" * 100)
    reporte.append("")
    reporte.append(f"Este proyecto Six Sigma propone inversión de ${COSTO_TOTAL_IMPLEMENTACION:,.2f} para generar")
    reporte.append(f"un ahorro anual de ${AHORRO_TOTAL_ANUAL:,.2f}, con ROI de {ROI:.1f}%.")
    reporte.append("")
    reporte.append(f"Payback period de {PAYBACK_PERIOD:.1f} meses es aceptable para implementación inmediata.")
    reporte.append("")
    reporte.append("RECOMENDACIÓN: APROBAR PARA IMPLEMENTACIÓN INMEDIATA")
    reporte.append("")
    reporte.append("El proyecto representa una oportunidad clara de mejora con impacto financiero")
    reporte.append("significativo y bajo riesgo de implementación.")
    reporte.append("")
    reporte.append("=" * 100)

    contenido = "\n".join(reporte)
    try:
        with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"[OK] Reporte DMAIC guardado")
    except Exception as e:
        print(f"[ERROR] Guardando reporte DMAIC: {e}")

    print(contenido)


def generar_analisis_pareto():
    """Genera análisis de Pareto."""
    print(f"\n[REPORT] Generando análisis de Pareto...")

    reporte = []
    reporte.append("=" * 90)
    reporte.append("ANÁLISIS DE PARETO - ROOT CAUSE ANALYSIS")
    reporte.append("=" * 90)
    reporte.append("")
    reporte.append("El Principio de Pareto (80/20): 80% de los problemas vienen de 20% de las causas")
    reporte.append("")

    acumulado_defectos = 0
    acumulado_costo = 0
    total_costo = sum(d['cantidad'] * d['costo_promedio'] for d in DEFECTOS_POR_TIPO.values())

    reporte.append("RANKING POR CANTIDAD DE DEFECTOS:")
    reporte.append("")
    reporte.append(f"{'Tipo Defecto':<30} {'Cantidad':>8} {'%':>6} {'Acum%':>6} {'Estado':<15}")
    reporte.append("-" * 90)

    for tipo, datos in sorted(DEFECTOS_POR_TIPO.items(), key=lambda x: x[1]['cantidad'], reverse=True):
        acumulado_defectos += datos['cantidad']
        acum_pct = acumulado_defectos / 56 * 100
        estado = "VITAL" if acum_pct <= 80 else "TRIVIAL"
        reporte.append(f"{tipo:<30} {datos['cantidad']:>8} {datos['porcentaje']:>6.1f}% {acum_pct:>6.1f}% {estado:<15}")

    reporte.append("")
    reporte.append("RANKING POR IMPACTO FINANCIERO:")
    reporte.append("")
    reporte.append(f"{'Tipo Defecto':<30} {'Impacto $':>12} {'%':>6} {'Acum%':>6} {'Estado':<15}")
    reporte.append("-" * 90)

    acumulado_costo = 0
    for tipo, datos in sorted(DEFECTOS_POR_TIPO.items(), key=lambda x: x[1]['cantidad'] * x[1]['costo_promedio'], reverse=True):
        impacto = datos['cantidad'] * datos['costo_promedio']
        acumulado_costo += impacto
        acum_pct = acumulado_costo / total_costo * 100
        estado = "VITAL" if acum_pct <= 80 else "TRIVIAL"
        reporte.append(f"{tipo:<30} ${impacto:>11,.2f} {impacto/total_costo*100:>6.1f}% {acum_pct:>6.1f}% {estado:<15}")

    reporte.append("")
    reporte.append("CONCLUSIONES:")
    reporte.append("  1. 3 tipos de defecto (Ensamble, Acabado, Dimensión) representan 85.7% del volumen")
    reporte.append("  2. Los 2 primeros tipos representan 60.7% del problema")
    reporte.append("  3. Enfoque en estos 2-3 tipos eliminará 80% del impacto")
    reporte.append("  4. Estrategia 80/20 permite maximizar ROI focalizando en pocas causas")
    reporte.append("")
    reporte.append("=" * 90)

    contenido = "\n".join(reporte)
    try:
        with open(ARCHIVO_PARETO, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"[OK] Análisis de Pareto guardado")
    except Exception as e:
        print(f"[ERROR] Guardando análisis de Pareto: {e}")

    print(contenido)


def generar_proyeccion_roi():
    """Genera proyección de ROI."""
    print(f"\n[REPORT] Generando proyección de ROI...")

    reporte = []
    reporte.append("=" * 90)
    reporte.append("PROYECCIÓN DE ROI - ANÁLISIS FINANCIERO")
    reporte.append("=" * 90)
    reporte.append("")

    # Timeline
    reporte.append("TIMELINE DE PROYECTO:")
    reporte.append("")
    reporte.append("  Semana 1-2: Definir y Medir")
    reporte.append("  Semana 3-4: Analizar e Implementar Mejoras")
    reporte.append("  Semana 5-8: Monitorear y Validar Resultados")
    reporte.append("  Mes 3+: Sostener y Optimizar")
    reporte.append("")

    # Costos
    reporte.append("ANÁLISIS DE COSTOS:")
    reporte.append("")
    total_impl = 0
    for solucion, datos in SOLUCIONES.items():
        reporte.append(f"  {solucion}: ${datos['costo_implementacion']:.2f}")
        total_impl += datos['costo_implementacion']
    reporte.append(f"  TOTAL IMPLEMENTACIÓN: ${total_impl:,.2f}")
    reporte.append("")

    # Beneficios
    reporte.append("ANÁLISIS DE BENEFICIOS:")
    reporte.append("")
    ahorro_mensual = 0
    for solucion, datos in SOLUCIONES.items():
        ahorro = datos['ahorro_esperado']
        reporte.append(f"  {solucion}: ${ahorro:.2f}/mes")
        ahorro_mensual += ahorro
    reporte.append(f"  TOTAL MENSUAL: ${ahorro_mensual:,.2f}")
    reporte.append(f"  TOTAL ANUAL (Año 1): ${ahorro_mensual * 12:,.2f}")
    reporte.append("")

    # ROI
    reporte.append("CÁLCULO DE ROI:")
    reporte.append("")
    ahorro_anual = ahorro_mensual * 12
    roi = ((ahorro_anual - COSTO_TOTAL_IMPLEMENTACION) / COSTO_TOTAL_IMPLEMENTACION) * 100
    reporte.append(f"  Ahorro Anual: ${ahorro_anual:,.2f}")
    reporte.append(f"  Menos Inversión: ${COSTO_TOTAL_IMPLEMENTACION:,.2f}")
    reporte.append(f"  Beneficio Neto (Año 1): ${ahorro_anual - COSTO_TOTAL_IMPLEMENTACION:,.2f}")
    reporte.append(f"  ROI Año 1: {roi:.1f}%")
    reporte.append(f"  Payback Period: {COSTO_TOTAL_IMPLEMENTACION/ahorro_mensual:.1f} meses")
    reporte.append("")

    # Proyección multi-año
    reporte.append("PROYECCIÓN 3 AÑOS:")
    reporte.append("")
    for año in range(1, 4):
        beneficio_neto = ahorro_anual * año - COSTO_TOTAL_IMPLEMENTACION
        reporte.append(f"  Año {año}: ${beneficio_neto:,.2f} (ROI: {beneficio_neto/COSTO_TOTAL_IMPLEMENTACION*100:.1f}%)")
    reporte.append("")

    # Riesgos y supuestos
    reporte.append("SUPUESTOS Y RIESGOS:")
    reporte.append("")
    reporte.append("  SUPUESTOS:")
    reporte.append("    - Tasa de defectos mejora según proyección")
    reporte.append("    - Costo unitario de defecto permanece constante")
    reporte.append("    - Volumen de producción constante")
    reporte.append("    - Mejoras se sostienen después de implementación")
    reporte.append("")
    reporte.append("  RIESGOS:")
    reporte.append("    - BAJO: Riesgos técnicos de implementación son bajos")
    reporte.append("    - BAJO: Cambio organizacional bien definido")
    reporte.append("    - BAJO: Soluciones probadas en otras líneas")
    reporte.append("")

    reporte.append("=" * 90)
    reporte.append(f"CONCLUSIÓN: Proyecto con ROI de {roi:.1f}% y payback de {COSTO_TOTAL_IMPLEMENTACION/ahorro_mensual:.1f} meses")
    reporte.append("es FINANCIERAMENTE VIABLE y altamente recomendado para implementación.")
    reporte.append("=" * 90)

    contenido = "\n".join(reporte)
    try:
        with open(ARCHIVO_ROI, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"[OK] Proyección de ROI guardada")
    except Exception as e:
        print(f"[ERROR] Guardando proyección de ROI: {e}")

    print(contenido)


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

def main():
    """Ejecuta el proyecto DMAIC completo."""
    print("\n" + "=" * 90)
    print("SIX SIGMA INTEGRATION - PROYECTO 5: DMAIC + ROI ANALYSIS")
    print("=" * 90 + "\n")

    generar_reporte_dmaic()
    generar_analisis_pareto()
    generar_proyeccion_roi()

    print("\n[COMPLETADO] Proyecto DMAIC finalizado!")
    print("=" * 90 + "\n")


if __name__ == "__main__":
    main()
