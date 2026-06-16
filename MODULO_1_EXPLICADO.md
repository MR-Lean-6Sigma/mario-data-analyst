# MODULO 1: ¡HOLA, PYTHON! - EXPLICACION COMPLETA

**Por:** Claude  
**Para:** Mario Romero (Carrera en Análisis de Datos)  
**Nivel:** Principiante

---

## 1. PRINT() - Tu Primera Línea de Código

### ¿Qué es print()?
`print()` es una **función** que muestra texto en la pantalla.

**Sintaxis:**
```python
print("texto aquí")
```

### ¿Por qué es importante?
Sin `print()`, Python calcula cosas pero NO las vemos. Es como hacer un análisis sin mostrar los resultados.

### EJEMPLOS:

**Ejemplo 1: Mostrar texto simple**
```python
print("Hola, Python!")
```
Resultado:
```
Hola, Python!
```

**Ejemplo 2: Mostrar un número**
```python
print(42)
```
Resultado:
```
42
```

**Ejemplo 3: REAL - De tu industria (OEE)**
```python
print("OEE de línea A: 85%")
```
Resultado:
```
OEE de línea A: 85%
```

---

## 2. VARIABLES - "Cajas" para Guardar Datos

### ¿Qué es una variable?
Una **variable** es un contenedor que guarda un valor.

Piénsalo como una **caja etiquetada**:
- El **nombre** es la etiqueta
- Lo **adentro** es el valor
- Usamos `=` para poner algo dentro

**Sintaxis:**
```python
nombre_variable = valor
```

### ¿Por qué usar variables?
✅ **Claridad:** El código es más fácil de leer  
✅ **Reutilización:** Usas la variable muchas veces  
✅ **Mantenimiento:** Si cambian datos, cambias 1 lugar  

### EJEMPLO REAL:
```python
turno_minutos = 480          # Un turno = 480 minutos (8 horas)
tiempo_parada = 120          # La máquina estuvo parada 120 minutos
produccion_piezas = 1500     # Se produjeron 1500 piezas

print(turno_minutos)
print(tiempo_parada)
print(produccion_piezas)
```

Resultado:
```
480
120
1500
```

---

## 3. TIPOS DE DATOS - Los 4 Principales

### ¿Qué son los tipos de datos?
Python tiene diferentes TIPOS de datos. Los 4 principales son:

| Tipo  | Ejemplo    | Explicación                 |
|-------|------------|---------------------------|
| int   | 42         | Números SIN decimales      |
| float | 3.14       | Números CON decimales      |
| str   | "Hola"     | TEXTO (siempre con comillas) |
| bool  | True/False | Verdadero o Falso          |

### ¿Por qué importa?
Porque Python trata cada tipo diferente. No puedes sumar "texto" + número sin cuidado.

### EJEMPLO 1: int (enteros)
```python
defectos = 5
print(f"Defectos: {defectos}")
print(f"Tipo: {type(defectos)}")
```

Resultado:
```
Defectos: 5
Tipo: <class 'int'>
```

### EJEMPLO 2: float (decimales)
```python
oee_porcentaje = 85.5
print(f"OEE: {oee_porcentaje}%")
print(f"Tipo: {type(oee_porcentaje)}")
```

Resultado:
```
OEE: 85.5%
Tipo: <class 'float'>
```

### EJEMPLO 3: str (texto)
```python
linea_produccion = "Línea A"
print(f"Línea: {linea_produccion}")
print(f"Tipo: {type(linea_produccion)}")
```

Resultado:
```
Línea: Línea A
Tipo: <class 'str'>
```

### EJEMPLO 4: bool (Verdadero/Falso)
```python
maquina_activa = True
print(f"¿Máquina activa?: {maquina_activa}")
print(f"Tipo: {type(maquina_activa)}")
```

Resultado:
```
¿Máquina activa?: True
Tipo: <class 'bool'>
```

---

## 4. OPERACIONES ARITMETICAS - Matemáticas en Python

### Operadores matemáticos

| Símbolo | Operación      | Ejemplo     |
|---------|----------------|-------------|
| +       | Suma           | 10 + 5 = 15 |
| -       | Resta          | 10 - 5 = 5  |
| *       | Multiplicar    | 10 * 5 = 50 |
| /       | Dividir        | 10 / 5 = 2.0 |
| **      | Potencia       | 2 ** 3 = 8 |
| //      | División entera | 10 // 3 = 3 |
| %       | Módulo (resto) | 10 % 3 = 1 |

### EJEMPLO REAL: Calcular Disponibilidad

**Fórmula:** Disponibilidad = (Tiempo Total - Parada) / Tiempo Total

```python
tiempo_total = 480        # 8 horas en minutos
tiempo_parada = 60        # 1 hora parada

tiempo_productivo = tiempo_total - tiempo_parada
disponibilidad = tiempo_productivo / tiempo_total
disponibilidad_porcentaje = disponibilidad * 100

print(f"Tiempo total: {tiempo_total} minutos")
print(f"Tiempo parada: {tiempo_parada} minutos")
print(f"Tiempo productivo: {tiempo_productivo} minutos")
print(f"Disponibilidad: {disponibilidad_porcentaje:.1f}%")
```

Resultado:
```
Tiempo total: 480 minutos
Tiempo parada: 60 minutos
Tiempo productivo: 420 minutos
Disponibilidad: 87.5%
```

---

## 5. COMPARACIONES - Preguntas que Python Responde

### Operadores de Comparación

| Símbolo | Significado      | Ejemplo       |
|---------|------------------|---------------|
| ==      | ¿Igual?          | 5 == 5 → True |
| !=      | ¿Diferente?      | 5 != 3 → True |
| >       | ¿Mayor que?      | 5 > 3 → True |
| <       | ¿Menor que?      | 5 < 3 → False |
| >=      | ¿Mayor o igual?  | 5 >= 5 → True |
| <=      | ¿Menor o igual?  | 5 <= 5 → True |

### ⚠️ IMPORTANTE: = vs ==
- `=` **ASIGNA** un valor (guarda en variable)
- `==` **COMPARA** valores (pregunta si son iguales)

### EJEMPLO REAL: ¿OEE cumple objetivo?

```python
oee_actual = 85.5
oee_objetivo = 85.0

print(f"OEE Actual: {oee_actual}")
print(f"OEE Objetivo: {oee_objetivo}")
print()
print(f"¿OEE cumple objetivo? {oee_actual >= oee_objetivo}")
print(f"¿OEE es mejor que objetivo? {oee_actual > oee_objetivo}")
```

Resultado:
```
OEE Actual: 85.5
OEE Objetivo: 85.0

¿OEE cumple objetivo? True
¿OEE es mejor que objetivo? True
```

---

## 6. CONDICIONALES (if/else) - Tomar Decisiones

### ¿Qué es un condicional?
Un condicional es una **decisión** que Python toma:
- IF (Si) la condición es TRUE → ejecuta esto
- ELSE (Si no) → ejecuta esto otro

**Sintaxis:**
```python
if condición:
    # código si es verdadero
else:
    # código si es falso
```

### ⚠️ IMPORTANTE: Indentación
En Python, los espacios **importan**. El código dentro del `if` debe estar indentado (con espacios al inicio).

### EJEMPLO 1: Alerta por baja calidad

```python
defectos = 10
limite_critico = 15  # Si hay más de 15 defectos, ALERTA

if defectos > limite_critico:
    print("ALERTA: Demasiados defectos! Revisar proceso.")
else:
    print("OK: Calidad dentro de límites normales")
```

Resultado:
```
OK: Calidad dentro de límites normales
```

### EJEMPLO 2: Clasificación de OEE

```python
oee = 78.5

if oee >= 85:
    print("Excelente")
else:
    print("Por mejorar")
```

Resultado:
```
Por mejorar
```

---

## 7. FUNCIONES - Código Reutilizable

### ¿Qué es una función?
Una **función** es un bloque de código que:
1. Tiene un **nombre**
2. Puede recibir **parámetros** (datos que le pasas)
3. Hace algo
4. Devuelve un **resultado**

### ¿Por qué usarlas?
En lugar de escribir el mismo código 100 veces, lo escribes 1 vez en una función y la reutilizas.

**Sintaxis:**
```python
def nombre_funcion(parametros):
    # código
    return resultado
```

### EJEMPLO REAL: Calcular Disponibilidad como Función

```python
def calcular_disponibilidad(tiempo_total, tiempo_parada):
    """Calcula la disponibilidad del equipamiento"""
    tiempo_productivo = tiempo_total - tiempo_parada
    disponibilidad = (tiempo_productivo / tiempo_total) * 100
    return disponibilidad

# Usar la función
disp_linea_a = calcular_disponibilidad(480, 60)   # 8 horas, 1 hora parada
disp_linea_b = calcular_disponibilidad(480, 120)  # 8 horas, 2 horas paradas

print(f"Disponibilidad Línea A: {disp_linea_a:.1f}%")
print(f"Disponibilidad Línea B: {disp_linea_b:.1f}%")
```

Resultado:
```
Disponibilidad Línea A: 87.5%
Disponibilidad Línea B: 75.0%
```

---

## 8. LISTAS - Colecciones de Datos

### ¿Qué es una lista?
Una **lista** es un contenedor que guarda **múltiples valores**.

**Sintaxis:**
```python
mi_lista = [valor1, valor2, valor3]
```

### ¿Por qué usarlas?
En lugar de crear 100 variables para 100 valores, los guardas en 1 lista.

### Índices (Posiciones)
Python empieza a **contar desde 0**:
```
[10, 20, 30, 40]
 0   1   2   3
```

### EJEMPLO REAL: Defectos por día de semana

```python
defectos_semana = [12, 15, 8, 10, 18, 14, 9]
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

print(f"Defectos Lunes: {defectos_semana[0]}")
print(f"Defectos Martes: {defectos_semana[1]}")
print(f"Máximo defectos: {max(defectos_semana)}")
print(f"Mínimo defectos: {min(defectos_semana)}")
print(f"Promedio defectos: {sum(defectos_semana) / len(defectos_semana):.1f}")
```

Resultado:
```
Defectos Lunes: 12
Defectos Martes: 15
Máximo defectos: 18
Mínimo defectos: 8
Promedio defectos: 12.3
```

---

## 9. LOOPS (for) - Repetir Código

### ¿Qué es un loop?
Un **loop** es un código que se **repite**.

En lugar de escribir `print()` 7 veces, usas un loop que lo hace 7 veces automáticamente.

**Sintaxis:**
```python
for variable in lista:
    # código que se repite
```

### ¿Cuándo usarla?
- Procesar cada elemento de una lista
- Repetir una acción N veces

### EJEMPLO 1: Mostrar defectos de cada día

```python
defectos_semana = [12, 15, 8, 10, 18, 14, 9]
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

for i in range(len(dias)):
    print(f"{dias[i]}: {defectos_semana[i]} defectos")
```

Resultado:
```
Lunes: 12 defectos
Martes: 15 defectos
Miércoles: 8 defectos
Jueves: 10 defectos
Viernes: 18 defectos
Sábado: 14 defectos
Domingo: 9 defectos
```

### EJEMPLO 2: Loop con condicional

```python
defectos_semana = [12, 15, 8, 10, 18, 14, 9]

for defectos in defectos_semana:
    if defectos > 15:
        print(f"ALERTA: {defectos} defectos!")
    else:
        print(f"OK: {defectos} defectos")
```

Resultado:
```
OK: 12 defectos
OK: 15 defectos
OK: 8 defectos
OK: 10 defectos
ALERTA: 18 defectos!
OK: 14 defectos
OK: 9 defectos
```

---

## RESUMEN DEL MÓDULO 1

| Concepto       | Para qué                                           |
|----------------|---------------------------------------------------|
| print()        | Mostrar valores en pantalla                      |
| Variables      | Guardar datos en "cajas" etiquetadas            |
| Tipos          | int, float, str, bool (tipos diferentes)        |
| Operaciones    | Matemáticas: +, -, *, /, **, //, %            |
| Comparaciones  | Preguntas: ==, !=, >, <, >=, <=               |
| Condicionales  | Decisiones: if/else                            |
| Funciones      | Código reutilizable con parámetros             |
| Listas         | Guardar múltiples valores                       |
| Loops          | Repetir código múltiples veces                  |

---

## SIGUIENTE PASO

**¡FELICIDADES! HAS COMPLETADO EL MÓDULO 1**

Ahora que entiendes los conceptos básicos, vamos al **SIGUIENTE NIVEL**:

### PROYECTO 1: OEE ANALYZER

Ahí aplicarás TODO esto para crear algo REAL:
- Calcular eficiencia de equipos
- Analizar defectos
- Generar reportes de producción

Todo uniendo Python + tu experiencia en manufactura!

---

**Fecha de creación:** Junio 16, 2026  
**Status:** Completado ✅  
**Próximo paso:** Proyecto 1 - OEE Analyzer
