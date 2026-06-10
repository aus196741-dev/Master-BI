# Master BI por Región — Dashboard Comercial B2B

Dashboard interactivo de actividad y ventas del equipo B2B por región.
Datos fuente: **Master BI por región.xlsx**

---

## Archivos

| Archivo | Descripcion |
|---|---|
| `extraer_datos.py` | Lee el Excel y genera el JSON con ejecutivos y clientes (todas las regiones) |
| `Master BI.py` | Une el JSON + template + logo y genera el HTML final |
| `template.html` | Diseño completo del dashboard (HTML, CSS, JavaScript) |
| `master_bi_data.json` | Datos procesados: ejecutivos y clientes |
| `Master BI por región.html` | Dashboard final — abrir en navegador |
| `actualizar.bat` | Doble clic para regenerar todo automaticamente |

---

## Como usar

### Nuevo mes o nuevos datos en el Excel
1. Actualizar `HOY` en `extraer_datos.py` al último día del periodo reportado
2. Doble clic en `actualizar.bat`
3. Esperar a que aparezca "Dashboard listo!"
4. Abrir `Master BI por región.html` en el navegador

### Cambiar diseño, filtros o graficas
1. Editar `template.html` con cualquier editor de texto
2. Ejecutar en terminal:
   ```
   python "Master BI.py"
   ```
3. Abrir `Master BI por región.html` en el navegador

### Cambiar columnas del Excel o agregar nuevos campos
1. Editar `extraer_datos.py`
2. Doble clic en `actualizar.bat`

### Cambiar rutas, logo u otras configuraciones
1. Editar `Master BI.py`
2. Ejecutar en terminal:
   ```
   python "Master BI.py"
   ```

---

## Filtros disponibles en el dashboard

| Filtro | Descripcion | Cascada |
|---|---|---|
| Región | Filtra por región comercial | Actualiza Coordinador y Ejecutivo |
| Coordinador | Filtra ejecutivos por coordinador | Actualiza Ejecutivo |
| Ejecutivo | Filtra un ejecutivo especifico (muestra sus clientes) | — |
| Cuenta Padre | Busqueda por ID de grupo padre — muestra padre e hijos | — |
| ID Cliente | Busqueda exacta por ID de cliente | — |

### Grupos de filtros mutuamente excluyentes

| Grupo A | Grupo B |
|---|---|
| Región, Coordinador, Ejecutivo | Cuenta Padre, ID Cliente |

- Los dos grupos **no pueden combinarse**
- Si se combinan: aparece alerta y se procesan los resultados del Grupo B (búsqueda directa)
- El botón **"Cambiar a Región / Coordinador / Ejecutivo"** limpia el Grupo B y aplica el Grupo A
- Si se ingresan Cuenta Padre e ID Cliente al mismo tiempo: se conserva solo Cuenta Padre

### Otras alertas

| Situacion | Comportamiento |
|---|---|
| Cuenta Padre + ID Cliente simultaneos | Se limpia ID Cliente, se usa Cuenta Padre |
| ID no encontrado como Cuenta Padre | Sugerencia para buscar como ID Cliente con boton directo |

---

## Agrupación por Cuenta Padre (tablas de clientes)

Todas las vistas que llegan a nivel cliente muestran los clientes agrupados por Cuenta Padre:

- **Encabezado de grupo** (azul oscuro): muestra nombre del grupo, número de clientes y totales de venta
- **Filas de clientes**: ordenadas por venta dentro de cada grupo
- **Fila de subtotal**: muestra suma de ventas, variacion % y mix de producto del grupo
- **Expandir / Colapsar**: clic en el encabezado para mostrar u ocultar los clientes del grupo (▼ / ▶)

Aplica en:
- Búsqueda por Cuenta Padre
- Búsqueda por ID Cliente
- Sección Clientes del Ejecutivo

---

## Mix de Producto

- **Tabla principal:** columnas `%Papel`, `%Mueb`, `%Pap`, `%Elec`, `%Svc` por ejecutivo
- **Tabla Cuenta Padre:** mismas columnas por cliente y subtotal de grupo
- **Tabla Clientes del Ejecutivo:** mismas columnas por cliente y subtotal de grupo
- **Grafica barras apiladas:** porcentaje por categoria visible en tooltip (hover)
- **Donut Mix Global:** porcentaje visible directamente sobre cada rebanada
- **Donut Cuenta Padre:** porcentaje visible directamente sobre cada rebanada

---

## Semaforo de Actividad — Reglas por semana vencida

La meta acumulada se calcula automáticamente según el día del periodo reportado (`HOY`):

| Semana | Días del mes | Meta visitas | Meta llamadas |
|---|---|---|---|
| Semana 1 | 1 – 7 | 15 | 15 |
| Semana 2 | 8 – 14 | 30 | 30 |
| Semana 3 | 15 – 21 | 45 | 45 |
| Semana 4 | 22 – 31 | 60 | 60 |

| Color | Regla |
|---|---|
| 🟢 Verde | Realizadas >= 100% de la meta |
| 🟡 Amarillo | Realizadas >= 70% de la meta |
| 🔴 Rojo | Realizadas < 70% de la meta |

> El semáforo muestra en su título la semana activa, la meta vigente y la fecha de corte de los datos.

---

## Fecha de corte de datos

La fecha de corte (`HOY` en `extraer_datos.py`) aparece en:
1. **Header del dashboard** — siempre visible arriba
2. **Badge junto al semáforo** — en amarillo para mayor visibilidad

Se actualiza automáticamente cada vez que se corre `actualizar.bat`.

---

## Ejecutivos ocultos en graficas y tablas

Los siguientes conceptos se **excluyen de graficas, tablas y semáforo** pero **sí suman a los KPI totales**:

- VACANTE
- SPS SIN
- COORDINADOR
- GRV
- SP COORDINADOR

Para agregar o quitar conceptos, editar el arreglo `OCULTOS` en `template.html`.

---

## KPIs principales

| KPI | Descripcion |
|---|---|
| Venta Mayo 2026 | Venta del mes actual con variacion vs Mayo 2025 |
| Venta Mayo 2025 | Venta del mismo mes año anterior |
| Acum. 2026 | Venta acumulada año 2026 (columna AN del Excel) |
| Acum. 2025 | Venta acumulada 2025 hasta el mismo mes que 2026 |
| Total Clientes | Clientes activos en el periodo |
| Sin Actividad | Clientes sin llamada Y sin visita en 30+ dias |
| Ejecutivos | Total de ejecutivos en el filtro activo |

---

## Columnas clave del Excel (hoja B2B Repor)

| Columna | Indice | Campo |
|---|---|---|
| B | 1 | Ejecutivo |
| C | 2 | Coordinador |
| D | 3 | Region |
| E | 4 | ID Cliente |
| F | 5 | Razon Social |
| I | 8 | Nombre Comercial |
| M | 12 | Cuenta Padre (ID Grupo) |
| R | 17 | Venta Mayo 2025 |
| N–R | 13–17 | Ventas mensuales 2025 (ene–may) |
| AF | 31 | Venta Mayo 2026 |
| AN | 39 | Venta Acumulada 2026 |
| AR | 43 | Ultima Reunion |
| AT | 45 | Ultima Llamada |
| AW | 48 | Fecha Ultima Minuta |
| BE | 56 | 207-Papel |
| BG | 58 | 1-Muebles |
| BI | 60 | 2-Papeleria |
| BK | 62 | 3-Electronicos |
| BM | 64 | 7-Servicentro |

Hoja `ingreso`: columna A = nombre ejecutivo, columna B = fecha de ingreso

---

## Rutas de archivos

- **Excel fuente:** `C:\Users\ausisima\Desktop\DIRECCION DE PRODUCTO\Master BI por region\Master BI por región.xlsx`
- **Logo:** `C:\Users\ausisima\Desktop\DIRECCION DE PRODUCTO\lock_and_fell\logo odemas Vt color.png`
- **Carpeta Dashboard:** `C:\Users\ausisima\Desktop\DIRECCION DE PRODUCTO\Master BI por region\`

---

## Resumen rapido

| Que quiero hacer | Que ejecuto |
|---|---|
| Nuevo mes / nuevos datos | Actualizar `HOY` en `extraer_datos.py` → `actualizar.bat` |
| Cambiar diseño o funcionalidad | Editar `template.html` → correr `Master BI.py` |
| Cambiar columnas del Excel | Editar `extraer_datos.py` → correr `actualizar.bat` |
| Cambiar rutas o logo | Editar `Master BI.py` → correrlo |
| Agregar/quitar ejecutivos ocultos | Editar arreglo `OCULTOS` en `template.html` → correr `Master BI.py` |
