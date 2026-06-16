#!/usr/bin/env python3
"""
MÓDULO 1: ¡Hola, Python! - GUÍA INTERACTIVA
=============================================

Este script te guía paso a paso a través de cada concepto del Módulo 1.
Ejecuta: python module_1_interactive_guide.py
"""

def pause():
    """Pausa para que el usuario lea"""
    input("\n➜ Presiona ENTER para continuar...")

def section_title(titulo):
    """Imprime un título de sección"""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70)

def subsection_title(titulo):
    """Imprime un subtítulo"""
    print(f"\n📌 {titulo}")
    print("-" * 70)

# ============================================================================
# INICIO
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║         🐍 MÓDULO 1: ¡HOLA, PYTHON! - GUÍA INTERACTIVA 🐍              ║
║                                                                          ║
║  Por: Claude  |  Para: Mario Romero (Pivoting to Data Analytics)      ║
║                                                                          ║
║  Este tutorial explica CADA CONCEPTO paso a paso.                      ║
║  No solo código. También el POR QUÉ.                                   ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
""")

pause()

# ============================================================================
# 1. PRINT()
# ============================================================================

section_title("1️⃣  PRINT() - Tu Primera Línea de Código")

subsection_title("¿Qué es print()?")
print("""
print() es una FUNCIÓN que muestra texto en la pantalla.

Sintaxis básica:
    print("tu texto aquí")

¿Por qué es importante?
Sin print(), Python calcula cosas pero NO las vemos.
Es como analizar datos pero no mostrar los resultados.
""")

pause()

print("\n🔥 EJEMPLO 1: Mostrar un texto simple")
print("Código: print('Hola, Python!')")
print("Resultado:")
print("─" * 50)
print("Hola, Python!")
print("─" * 50)

pause()

print("\n🔥 EJEMPLO 2: Mostrar un número")
print("Código: print(42)")
print("Resultado:")
print("─" * 50)
print(42)
print("─" * 50)

pause()

print("\n🔥 EJEMPLO 3: REAL - De tu industria (OEE)")
print("Código: print('OEE de línea A: 85%')")
print("Resultado:")
print("─" * 50)
print("OEE de línea A: 85%")
print("─" * 50)

pause()

# ============================================================================
# 2. VARIABLES
# ============================================================================

section_title("2️⃣  VARIABLES - 'Cajas' para Guardar Datos")

subsection_title("¿Qué es una variable?")
print("""
Una VARIABLE es un contenedor que guarda un valor.

Piénsalo como una CAJA ETIQUETADA:
  📦 [Etiqueta: "turno_minutos"]
  📦 [Contenido: 480]

Sintaxis:
    nombre_variable = valor

Ejemplo:
    turno_minutos = 480
    tiempo_parada = 120
""")

pause()

print("\n🔥 EJEMPLO 1: Variables de producción")
print("Código:")
print("  turno_minutos = 480")
print("  tiempo_parada = 60")
print("  print(turno_minutos)")
print("  print(tiempo_parada)")
print("\nResultado:")
print("─" * 50)

turno_minutos = 480
tiempo_parada = 60
print(turno_minutos)
print(tiempo_parada)

print("─" * 50)

pause()

subsection_title("¿Por qué usar variables?")
print("""
✅ Claridad: El código es más fácil de leer
✅ Reutilización: Usas la variable muchas veces
✅ Mantenimiento: Si cambian datos, cambias 1 lugar

Ejemplo SIN variables (MALO):
    print(480 - 60)
    print(480 - 120)
    print(480 - 90)

Ejemplo CON variables (BUENO):
    turno = 480
    parada1 = 60
    parada2 = 120
    parada3 = 90
    print(turno - parada1)
    print(turno - parada2)
    print(turno - parada3)
""")

pause()

# ============================================================================
# 3. TIPOS DE DATOS
# ============================================================================

section_title("3️⃣  TIPOS DE DATOS - Los 4 Principales")

subsection_title("¿Qué son los tipos de datos?")
print("""
Python tiene diferentes TIPOS de datos. Los 4 principales:

┌─────────┬─────────────┬───────────────────────────────┐
│ Tipo    │ Ejemplo     │ Explicación                   │
├─────────┼─────────────┼───────────────────────────────┤
│ int     │ 42          │ Números SIN decimales         │
│ float   │ 3.14        │ Números CON decimales         │
│ str     │ "Hola"      │ TEXTO (entre comillas)        │
│ bool    │ True/False  │ Verdadero o Falso             │
└─────────┴─────────────┴───────────────────────────────┘

¿Por qué importa?
Python trata cada tipo diferente.
No puedes sumar "texto" + número sin cuidado.
""")

pause()

print("\n🔥 EJEMPLO 1: int (números enteros)")
print("Código:")
print("  defectos = 5")
print("  print(f'Defectos: {defectos}')")
print("  print(f'Tipo: {type(defectos)}')")
print("\nResultado:")
print("─" * 50)

defectos = 5
print(f"Defectos: {defectos}")
print(f"Tipo: {type(defectos)}")

print("─" * 50)

pause()

print("\n🔥 EJEMPLO 2: float (decimales)")
print("Código:")
print("  oee_porcentaje = 85.5")
print("  print(f'OEE: {oee_porcentaje}%')")
print("  print(f'Tipo: {type(oee_porcentaje)}')")
print("\nResultado:")
print("─" * 50)

oee_porcentaje = 85.5
print(f"OEE: {oee_porcentaje}%")
print(f"Tipo: {type(oee_porcentaje)}")

print("─" * 50)

pause()

print("\n🔥 EJEMPLO 3: str (texto/string)")
print("Código:")
print("  linea = 'Línea A'")
print("  print(f'Línea: {linea}')")
print("  print(f'Tipo: {type(linea)}')")
print("\nResultado:")
print("─" * 50)

linea = "Línea A"
print(f"Línea: {linea}")
print(f"Tipo: {type(linea)}")

print("─" * 50)

pause()

print("\n🔥 EJEMPLO 4: bool (Verdadero/Falso)")
print("Código:")
print("  maquina_activa = True")
print("  print(f'¿Activa?: {maquina_activa}')")
print("  print(f'Tipo: {type(maquina_activa)}')")
print("\nResultado:")
print("─" * 50)

maquina_activa = True
print(f"¿Activa?: {maquina_activa}")
print(f"Tipo: {type(maquina_activa)}")

print("─" * 50)

pause()

# ============================================================================
# 4. OPERACIONES ARITMÉTICAS
# ============================================================================

section_title("4️⃣  OPERACIONES ARITMÉTICAS - Matemáticas en Python")

subsection_title("Operadores matemáticos")
print("""
┌──────────┬──────────────┬─────────────────┐
│ Símbolo  │ Operación    │ Ejemplo         │
├──────────┼──────────────┼─────────────────┤
│ +        │ Suma         │ 10 + 5 = 15     │
│ -        │ Resta        │ 10 - 5 = 5      │
│ *        │ Multiplicar  │ 10 * 5 = 50     │
│ /        │ Dividir      │ 10 / 5 = 2.0    │
│ **       │ Potencia     │ 2 ** 3 = 8      │
│ //       │ División entera│ 10 // 3 = 3   │
│ %        │ Módulo (resto)│ 10 % 3 = 1     │
└──────────┴──────────────┴─────────────────┘
""")

pause()

print("\n🔥 EJEMPLO REAL: Calcular Disponibilidad de Equipamiento")
print("""
Fórmula: Disponibilidad = (Tiempo Total - Parada) / Tiempo Total
""")
print("\nCódigo:")
print("""
  tiempo_total = 480        # 8 horas en minutos
  tiempo_parada = 60        # 1 hora parada

  tiempo_productivo = tiempo_total - tiempo_parada
  disponibilidad = tiempo_productivo / tiempo_total
  disponibilidad_pct = disponibilidad * 100

  print(f'Disponibilidad: {disponibilidad_pct:.1f}%')
""")

print("\nResultado:")
print("─" * 50)

tiempo_total = 480
tiempo_parada = 60

tiempo_productivo = tiempo_total - tiempo_parada
disponibilidad = tiempo_productivo / tiempo_total
disponibilidad_pct = disponibilidad * 100

print(f"Disponibilidad: {disponibilidad_pct:.1f}%")

print("─" * 50)

pause()

# ============================================================================
# 5. COMPARACIONES
# ============================================================================

section_title("5️⃣  COMPARACIONES - Preguntas que Python Responde")

subsection_title("Operadores de Comparación")
print("""
┌──────────┬──────────────────┬──────────────┐
│ Símbolo  │ Significado      │ Resultado    │
├──────────┼──────────────────┼──────────────┤
│ ==       │ ¿Igual?          │ True/False   │
│ !=       │ ¿Diferente?      │ True/False   │
│ >        │ ¿Mayor que?      │ True/False   │
│ <        │ ¿Menor que?      │ True/False   │
│ >=       │ ¿Mayor o igual?  │ True/False   │
│ <=       │ ¿Menor o igual?  │ True/False   │
└──────────┴──────────────────┴──────────────┘

⚠️ IMPORTANTE: = vs ==
  = ASIGNA un valor
  == COMPARA valores
""")

pause()

print("\n🔥 EJEMPLO REAL: ¿OEE cumple objetivo?")
print("Código:")
print("""
  oee_actual = 85.5
  oee_objetivo = 85.0

  print(oee_actual >= oee_objetivo)
""")

print("\nResultado:")
print("─" * 50)

oee_actual = 85.5
oee_objetivo = 85.0

resultado = oee_actual >= oee_objetivo
print(f"¿OEE cumple objetivo? {resultado}")

print("─" * 50)

pause()

# ============================================================================
# 6. CONDICIONALES
# ============================================================================

section_title("6️⃣  CONDICIONALES (if/else) - Tomar Decisiones")

subsection_title("¿Qué es un condicional?")
print("""
Un condicional es una DECISIÓN:
  IF (Si) la condición es TRUE → ejecuta esto
  ELSE (Si no) → ejecuta esto otro

Sintaxis:
  if condición:
      # código si es verdadero
  else:
      # código si es falso

⚠️ INDENTACIÓN: Los espacios IMPORTAN en Python
              El código dentro del if debe estar indentado
""")

pause()

print("\n🔥 EJEMPLO 1: Alerta por defectos")
print("Código:")
print("""
  defectos = 10
  limite_critico = 15

  if defectos > limite_critico:
      print("⚠️ ALERTA: Revisar proceso!")
  else:
      print("✅ Calidad normal")
""")

print("\nResultado:")
print("─" * 50)

defectos = 10
limite_critico = 15

if defectos > limite_critico:
    print("⚠️ ALERTA: Revisar proceso!")
else:
    print("✅ Calidad normal")

print("─" * 50)

pause()

print("\n🔥 EJEMPLO 2: Clasificación de OEE")
print("Código:")
print("""
  oee = 78.5

  if oee >= 85:
      print("✅ Excelente")
  else:
      print("⚠️ Por mejorar")
""")

print("\nResultado:")
print("─" * 50)

oee = 78.5

if oee >= 85:
    print("✅ Excelente")
else:
    print("⚠️ Por mejorar")

print("─" * 50)

pause()

# ============================================================================
# 7. FUNCIONES
# ============================================================================

section_title("7️⃣  FUNCIONES - Código Reutilizable")

subsection_title("¿Qué es una función?")
print("""
Una FUNCIÓN es un bloque de código que:
  1. Tiene un NOMBRE
  2. Puede recibir PARÁMETROS (datos que le pasas)
  3. HACE algo
  4. DEVUELVE un resultado

¿Por qué usarlas?
En lugar de escribir código 100 veces, lo escribes 1 vez
en una función y la reutilizas.

Sintaxis:
  def nombre_funcion(parametro1, parametro2):
      # código
      return resultado
""")

pause()

print("\n🔥 EJEMPLO REAL: Calcular Disponibilidad como Función")
print("Código:")
print("""
  def calcular_disponibilidad(tiempo_total, tiempo_parada):
      tiempo_productivo = tiempo_total - tiempo_parada
      disponibilidad = (tiempo_productivo / tiempo_total) * 100
      return disponibilidad

  # Usar la función
  disp_a = calcular_disponibilidad(480, 60)
  disp_b = calcular_disponibilidad(480, 120)

  print(f'Línea A: {disp_a:.1f}%')
  print(f'Línea B: {disp_b:.1f}%')
""")

print("\nResultado:")
print("─" * 50)

def calcular_disponibilidad(tiempo_total, tiempo_parada):
    tiempo_productivo = tiempo_total - tiempo_parada
    disponibilidad = (tiempo_productivo / tiempo_total) * 100
    return disponibilidad

disp_a = calcular_disponibilidad(480, 60)
disp_b = calcular_disponibilidad(480, 120)

print(f"Línea A: {disp_a:.1f}%")
print(f"Línea B: {disp_b:.1f}%")

print("─" * 50)

pause()

# ============================================================================
# 8. LISTAS
# ============================================================================

section_title("8️⃣  LISTAS - Colecciones de Datos")

subsection_title("¿Qué es una lista?")
print("""
Una LISTA es un contenedor que guarda MÚLTIPLES valores.

Sintaxis:
  mi_lista = [valor1, valor2, valor3]

¿Por qué usarlas?
En lugar de 100 variables para 100 valores,
guardas todo en 1 lista.

Índices (Posiciones):
Python empieza a contar desde 0:
  [10, 20, 30, 40]
   0   1   2   3
""")

pause()

print("\n🔥 EJEMPLO REAL: Defectos por día de semana")
print("Código:")
print("""
  defectos_semana = [12, 15, 8, 10, 18, 14, 9]
  dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

  print(f'Lunes: {defectos_semana[0]} defectos')
  print(f'Máximo: {max(defectos_semana)}')
  print(f'Mínimo: {min(defectos_semana)}')
  print(f'Promedio: {sum(defectos_semana) / len(defectos_semana):.1f}')
""")

print("\nResultado:")
print("─" * 50)

defectos_semana = [12, 15, 8, 10, 18, 14, 9]
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

print(f"Lunes: {defectos_semana[0]} defectos")
print(f"Máximo de la semana: {max(defectos_semana)}")
print(f"Mínimo de la semana: {min(defectos_semana)}")
print(f"Promedio: {sum(defectos_semana) / len(defectos_semana):.1f}")

print("─" * 50)

pause()

# ============================================================================
# 9. LOOPS
# ============================================================================

section_title("9️⃣  LOOPS (for) - Repetir Código")

subsection_title("¿Qué es un loop?")
print("""
Un LOOP es código que se REPITE.

En lugar de escribir print() 7 veces,
usas un loop que lo hace 7 veces automáticamente.

Sintaxis:
  for variable in lista:
      # código que se repite

¿Cuándo usarla?
- Procesar cada elemento de una lista
- Repetir una acción N veces
""")

pause()

print("\n🔥 EJEMPLO REAL: Mostrar defectos de cada día")
print("Código:")
print("""
  defectos_semana = [12, 15, 8, 10, 18, 14, 9]
  dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

  for i in range(len(dias)):
      print(f"{dias[i]}: {defectos_semana[i]} defectos")
""")

print("\nResultado:")
print("─" * 50)

defectos_semana = [12, 15, 8, 10, 18, 14, 14, 9]
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

for i in range(len(dias)):
    print(f"{dias[i]}: {defectos_semana[i]} defectos")

print("─" * 50)

pause()

# ============================================================================
# RESUMEN
# ============================================================================

section_title("🎯 RESUMEN DEL MÓDULO 1")

print("""
┌────────────────┬──────────────────────────────────────────────────────┐
│ Concepto       │ Para qué                                             │
├────────────────┼──────────────────────────────────────────────────────┤
│ print()        │ Mostrar valores en pantalla                          │
│ Variables      │ Guardar datos en "cajas" etiquetadas                │
│ Tipos          │ int, float, str, bool (tipos diferentes)            │
│ Operaciones    │ Matemáticas: +, -, *, /, **, //, %                │
│ Comparaciones  │ Preguntas: ==, !=, >, <, >=, <=                    │
│ Condicionales  │ Decisiones: if/else                                 │
│ Funciones      │ Código reutilizable con parámetros                 │
│ Listas         │ Guardar múltiples valores                           │
│ Loops          │ Repetir código múltiples veces                      │
└────────────────┴──────────────────────────────────────────────────────┘
""")

pause()

print("""
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║  ✅ ¡FELICIDADES! HAS COMPLETADO EL MÓDULO 1                          ║
║                                                                        ║
║  Ahora que entiendes los CONCEPTOS BÁSICOS,                           ║
║  vamos al SIGUIENTE NIVEL:                                            ║
║                                                                        ║
║  🚀 PROYECTO 1: OEE ANALYZER                                          ║
║                                                                        ║
║  Ahí aplicarás TODO esto para crear algo REAL:                       ║
║  - Calcular eficiencia de equipos                                     ║
║  - Analizar defectos                                                  ║
║  - Generar reportes de producción                                     ║
║                                                                        ║
║  Todo uniendo Python + tu experiencia en manufactura 💪               ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
""")

print("\n¿Listo para el Proyecto 1? 🚀\n")
