# SPC Dashboard - Control Estadístico de Procesos

## Overview

Statistical Process Control (SPC) dashboard that monitors production processes and detects anomalies using control charts. Demonstrates mastery of data analysis, statistical thinking, and professional reporting.

## What is SPC?

SPC uses statistical methods to monitor and control manufacturing processes:

- **Control Limits**: Upper and lower bounds for normal process variation
- **Special Cause Variation**: When process goes out of control (requires investigation)
- **Common Cause Variation**: Normal random variation (expected)
- **Trend Detection**: Identifies deteriorating processes before defects occur

## Features

- Calculates process mean and standard deviation
- Establishes control limits (±3 sigma from mean)
- Detects out-of-control points
- Identifies trends (consecutive points moving in one direction)
- Generates professional control charts in text format
- Creates actionable alerts and recommendations

## Technical Skills Demonstrated

- **Statistics**: Mean, standard deviation, control limits
- **Loops**: Iterating through time series data
- **Conditionals**: Detecting out-of-control conditions
- **Data Analysis**: Trend detection algorithms
- **Professional Reporting**: ASCII control charts, alerts, recommendations

## Control Chart Rules (Western Electric)

The script detects SPC violations:

1. **1 Point Beyond 3-Sigma**: Single point outside control limits
2. **2 of 3 Points Beyond 2-Sigma**: Two consecutive points nearing limits
3. **4 of 5 Points Beyond 1-Sigma**: Trend toward limit
4. **8 Consecutive Points on Same Side**: Process shift detected
5. **6 Points Increasing/Decreasing**: Trend detected

## Usage

```bash
python spc_dashboard.py
```

## Output

Generates `output/reporte_spc.txt` with:
- Control chart visualization (ASCII)
- Out-of-control point alerts
- Trend analysis
- Process capability assessment
- Recommendations for corrective action

## Data Format

Input: `data/process_measurements.csv`

Columns:
- `linea`: Production line (A, B, C)
- `fecha`: Date of measurement
- `medicion`: Measured value (e.g., dimension, weight)
- `especificacion`: Specification/target value

## Files

- `spc_dashboard.py` - Main SPC analysis script
- `data/process_measurements.csv` - Sample process measurement data
- `output/reporte_spc.txt` - Generated SPC report with control charts

## Interpretation

- **GREEN**: Process in control, stable
- **YELLOW**: Warning - trending toward limits
- **RED**: Out of control - immediate action required

## Real-World Application

In your 30 years of manufacturing experience, SPC is the tool that tells operators:
- "Your process is drifting, fix it NOW before defects happen"
- vs waiting for defects to appear
- This is preventive vs reactive maintenance
