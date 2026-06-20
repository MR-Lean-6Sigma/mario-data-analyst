# 🏭 Project 2: Waste Detection System (Muda Analysis)

## Overview

Identifies and quantifies **Lean waste (Muda)** in manufacturing and operational processes. This project demonstrates the 8 types of waste in Lean manufacturing and calculates financial impact.

## 8 Types of Muda (Waste)

1. **Overproduction** - Making more than needed
2. **Inventory** - Excess stock/work-in-progress
3. **Motion** - Unnecessary employee movements
4. **Waiting** - Downtime/idle time
5. **Transport** - Unnecessary movement of materials
6. **Over-processing** - Unnecessary steps/features
7. **Defects** - Rework and scrap
8. **Talent/Skills** - Underutilized employee capabilities

## Features

- Analyzes production data for waste patterns
- Quantifies waste in both units and financial terms
- Categorizes by waste type
- Calculates total waste and financial impact
- Generates professional waste analysis reports

## Technical Skills Demonstrated

- **Loops**: Iterating through process data to identify waste patterns
- **Conditionals**: Classifying waste types and thresholds
- **String manipulation**: Building detailed waste descriptions
- **Data analysis**: Calculating waste metrics and impacts
- **File I/O**: Reading and writing analysis files

## Usage

```bash
python waste_analyzer.py
```

## Output

Generates `output/reporte_muda.txt` with:
- Waste breakdown by type
- Financial impact analysis
- Production line recommendations
- Total waste summary

## Data Format

Input: `data/waste_data.csv`

Columns:
- `linea`: Production line (A, B, C, etc.)
- `fecha`: Date of observation
- `tipo_desperdicio`: Type of waste (overproduction, inventory, motion, etc.)
- `cantidad_unidades`: Units of waste
- `horas_perdidas`: Hours lost
- `costo_unitario`: Cost per unit

## Files

- `waste_analyzer.py` - Main analysis script
- `data/waste_data.csv` - Sample waste data
- `output/reporte_muda.txt` - Generated waste report
