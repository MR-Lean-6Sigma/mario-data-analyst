# Full Analytics Pipeline - ETL + Análisis Completo

## Overview

End-to-end data analytics pipeline demonstrating complete data workflow: Extract, Transform, Load (ETL), analysis, and actionable business intelligence. This is your capstone-level project showing mastery of Python data analysis.

## Why This Matters for Your Career

This project demonstrates:
1. **Real Data**: Multiple data sources (production, defects, maintenance)
2. **ETL Pipeline**: Data cleaning, transformation, standardization
3. **Complex Analysis**: Combining OEE, waste, SPC in one comprehensive view
4. **Business Intelligence**: Actionable insights with ROI impact
5. **Professional Reporting**: Executive-ready dashboards and recommendations

## Project Flow

```
RAW DATA (CSV Files)
    ↓
EXTRACT: Read from multiple sources
    ↓
TRANSFORM: Clean, validate, enrich data
    ↓
LOAD: Create unified data structures
    ↓
ANALYZE: Calculate KPIs, OEE, waste, SPC
    ↓
REPORT: Executive summary with recommendations
    ↓
BUSINESS IMPACT: Financial impact and ROI
```

## Data Sources

1. **Production Data**: Daily output by line
2. **Defect Data**: Quality issues and rework
3. **Maintenance Data**: Downtime and delays
4. **Material Data**: Inventory and waste

## Analysis Included

- Overall Equipment Effectiveness (OEE)
- Waste quantification (Muda)
- Statistical Process Control status
- Defect analysis and Pareto charts
- Maintenance effectiveness
- Financial impact analysis
- Improvement priorities ranked by ROI

## Technical Features

- Multiple CSV file handling
- Data validation and error checking
- Pandas-like data transformation (without Pandas - pure Python)
- Dictionary-based data structures for complex relationships
- Statistical analysis and aggregation
- Financial calculations
- Ranked reporting by impact

## Output Files

- `reporte_ejecutivo.txt` - Executive summary (1 page)
- `reporte_detallado.txt` - Detailed analysis (10+ pages)
- `reporte_kpis.txt` - KPI dashboard
- `reporte_recomendaciones.txt` - Improvement recommendations

## Usage

```bash
python analytics_pipeline.py
```

## Key Metrics Calculated

- **OEE Score**: Equipment effectiveness
- **Cost of Waste**: Muda financial impact
- **SPC Status**: Process control assessment
- **Defect Rate**: Quality metric
- **MTBF/MTTR**: Maintenance metrics
- **Estimated Savings**: From recommended improvements

## Skills Demonstrated

- ETL process design and implementation
- Multi-source data integration
- Data validation and quality checks
- Complex financial analysis
- Business metrics calculation
- Executive reporting
- Recommendation prioritization

## Real-World Application

This pipeline demonstrates the workflow your future employer will expect:
- "We have raw data, we need insights"
- This project says: "I can handle that - here's the pipeline"
