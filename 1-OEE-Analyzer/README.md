# 🏭 PROYECTO 1: OEE ANALYZER

## ¿Qué es?

**OEE Analyzer** es tu **PRIMER PROYECTO PROFESIONAL** que:
- Lee datos de producción
- Calcula OEE (Overall Equipment Effectiveness)
- Analiza 6 Sigma (DPMO, Sigma Level)
- Genera reportes profesionales
- Demuestra que sabes usar Python para manufactura

## 🎯 Objetivo

Convertir datos brutos de Excel/CSV en **análisis profesional** usando Python.

## 📁 Estructura

```
1-OEE-Analyzer/
├── README.md              ← Estás aquí
├── oee_analyzer.py        ← Script principal
├── data/
│   └── production_data.csv ← Datos de entrada
└── output/
    └── reporte_oee.txt    ← Resultado generado
```

## 🚀 Cómo funciona

### Paso 1: Prepara los datos
Tu archivo `production_data.csv` tiene formato:
```
fecha,linea,tiempo_total_min,tiempo_parada_min,piezas_producidas,piezas_esperadas,piezas_buenas,defectos
```

### Paso 2: Ejecuta el script
```bash
python oee_analyzer.py
```

### Paso 3: Lee el reporte
Se genera automáticamente en `output/reporte_oee.txt`

## 📊 Ejemplo de Salida

```
==============================================================
REPORTE OEE - ANÁLISIS DE EFICIENCIA
==============================================================
Línea: Línea A
Fecha: 2026-06-16

MÉTRICAS OEE:
  Disponibilidad: 87.5%
  Rendimiento:    96.7%
  Calidad:        99.0%
  OEE TOTAL:      83.46%

ANÁLISIS 6 SIGMA:
  DPMO:           1,666.67
  Sigma Level:    2.0
  Clasificación:  POBRE

==============================================================
```

## 💡 Conceptos Usados

- ✅ Lectura de archivos CSV
- ✅ Importar tu librería `manufacturing_formulas.py`
- ✅ Loops y análisis de datos
- ✅ Generación de reportes
- ✅ Trabajo con funciones profesionales

## 🔧 Requisitos

- Python 3.14+
- Archivo `manufacturing_formulas.py` en carpeta padre
- Datos en `data/production_data.csv`

## 📝 Notas

Este es tu **PRIMER PROYECTO REAL**. 
Demuestra que sabes:
- Leer datos
- Procesarlos
- Usar funciones reutilizables
- Generar reportes

¡Perfecto para tu portfolio en GitHub! 💪
