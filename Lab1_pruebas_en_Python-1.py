# FUNCIÓN REAL: Calcular Disponibilidad
def calcular_disponibilidad(tiempo_total, tiempo_parada):
    """Calcula la disponibilidad del equipamiento"""
    tiempo_productivo = tiempo_total - tiempo_parada
    disponibilidad = (tiempo_productivo / tiempo_total) * 100
    return disponibilidad

# Usar la función
disp_linea_a = calcular_disponibilidad(480, 60)  # 8 horas, 1 hora parada
disp_linea_b = calcular_disponibilidad(480, 120) # 8 horas, 2 horas paradas

print(f"Disponibilidad Línea A: {disp_linea_a:.1f}%")
print(f"Disponibilidad Línea B: {disp_linea_b:.1f}%")