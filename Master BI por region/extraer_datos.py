import json
import pandas as pd
from datetime import date

HOY  = date(2026, 5, 31)
XLSX = r'C:\Users\ausisima\Desktop\DIRECCION DE PRODUCTO\Master BI por region\Master BI por región.xlsx'
JSON = r'C:\Users\ausisima\Desktop\DIRECCION DE PRODUCTO\Master BI por region\master_bi_data.json'

def dias(v):
    try:
        if pd.isna(v): return 999
        return max(0, (HOY - pd.to_datetime(v).date()).days)
    except: return 999

def safe(v):
    try:
        if pd.isna(v): return ''
        s = str(v).encode('ascii','ignore').decode('ascii').strip()
        return s
    except: return ''

def num(v):
    try:
        f = float(v); return round(f,2) if f==f else 0
    except: return 0

def fecha(v):
    try:
        if pd.isna(v): return '--'
        s = str(v).strip()
        if not s or s.lower() in ('nat','nan',''): return '--'
        dt = pd.to_datetime(s, errors='coerce')
        return '--' if pd.isna(dt) else str(dt.date())
    except: return '--'

# Leer pestaña ingreso
df_ing = pd.read_excel(XLSX, sheet_name='ingreso', header=None)
ingresos = {}
for _, r in df_ing.iterrows():
    nombre = safe(r.iloc[0])
    if nombre:
        try:
            ingresos[nombre] = str(pd.to_datetime(r.iloc[1]).date())
        except:
            ingresos[nombre] = '--'

# Leer Excel
xl = pd.read_excel(XLSX, sheet_name='B2B Repor', header=None, skiprows=2)
print(f"Filas raw: {len(xl)}")

mask_clis = xl.iloc[:,3].astype(str).str.strip().str.len() > 0
df_clis   = xl[mask_clis].copy()
mask_ejs  = mask_clis & (xl.iloc[:,1].astype(str).str.strip().str.upper() != 'VACANTE') & (xl.iloc[:,1].astype(str).str.strip() != '')
df        = xl[mask_ejs].copy()
print(f"Clientes extraidos: {len(df_clis)} | Ejecutivos activos: {len(df)}")

# Clientes
clientes = []
for _, r in df_clis.iterrows():
    if not safe(r.iloc[4]): continue
    clientes.append({
        "id"              : safe(r.iloc[4]),
        "razon_social"    : safe(r.iloc[5]),
        "nombre_com"      : safe(r.iloc[8]),
        "ejecutivo"       : safe(r.iloc[1]),
        "coordinador"     : safe(r.iloc[2]),
        "region"          : safe(r.iloc[3]),
        "cuenta_padre"    : safe(r.iloc[12]),
        "venta_mayo"      : num(r.iloc[31]),
        "venta_mayo_25"   : num(r.iloc[17]),
        "venta_acum_25"   : sum(num(r.iloc[c]) for c in range(13, 13 + HOY.month)),
        "venta_acum_26"   : num(r.iloc[39]),
        "papel"           : num(r.iloc[56]),
        "muebles"         : num(r.iloc[58]),
        "papeleria"       : num(r.iloc[60]),
        "electronicos"    : num(r.iloc[62]),
        "servicentro"     : num(r.iloc[64]),
        "dias_sin_reunion": dias(r.iloc[43]),
        "dias_sin_llamada": dias(r.iloc[45]),
        "sin_actividad"   : dias(r.iloc[43])>30 and dias(r.iloc[45])>30,
    })
print(f"Clientes extraidos: {len(clientes)}")

# Ejecutivos
ejs_raw = {}
for c in clientes:
    k = c['ejecutivo']
    if not k: continue
    if k not in ejs_raw:
        ejs_raw[k] = {'region':c['region'],'coordinador':c['coordinador'],'fecha_ingreso':ingresos.get(k,'--'),'venta_mayo':0,'venta_mayo_2025':0,
                      'venta_2026':0,'venta_acum_2025':0,'venta_acum_2026':0,'clientes':0,'papel':0,'muebles':0,'papeleria':0,
                      'electronicos':0,'servicentro':0,'ventas_totales':0,
                      'llamadas_mayo':0,'reuniones_mayo':0,
                      'ultima_reunion':'--','ultima_llamada':'--','ultima_minuta':'--',
                      'dias_sin_reunion':999,'dias_sin_llamada':999,'dias_sin_minuta':999,'conversion':0}
    e = ejs_raw[k]
    e['venta_mayo']       += c['venta_mayo']
    e['venta_mayo_2025']  += c['venta_mayo_25']
    e['venta_acum_2025']  += c['venta_acum_25']
    e['venta_acum_2026']  += c['venta_acum_26']
    e['clientes']         += 1
    e['papel']           += c['papel'];  e['muebles']      += c['muebles']
    e['papeleria']       += c['papeleria']; e['electronicos'] += c['electronicos']
    e['servicentro']     += c['servicentro']

for ej_name, row in df.groupby(df.iloc[:,1].astype(str).str.strip()).first().iterrows():
    nm = safe(row.iloc[1]) or ej_name
    if nm not in ejs_raw: continue
    e = ejs_raw[nm]
    e['venta_2026']       = num(row.iloc[39])
    e['ultima_reunion']   = fecha(row.iloc[43])
    e['ultima_llamada']   = fecha(row.iloc[45])
    e['ultima_minuta']    = fecha(row.iloc[48])
    e['dias_sin_reunion'] = dias(row.iloc[43])
    e['dias_sin_llamada'] = dias(row.iloc[45])
    e['dias_sin_minuta']  = dias(row.iloc[48])
    e['conversion']       = round(e['venta_mayo']/e['venta_mayo_2025']*100,1) if e['venta_mayo_2025']>0 else 0
    e['ventas_totales']   = e['papel']+e['muebles']+e['papeleria']+e['electronicos']+e['servicentro']

for k in ejs_raw:
    sub = [c for c in clientes if c['ejecutivo']==k]
    ejs_raw[k]['llamadas_mayo']  = sum(1 for c in sub if c['dias_sin_llamada']<=31)
    ejs_raw[k]['reuniones_mayo'] = sum(1 for c in sub if c['dias_sin_reunion']<=31)

ejecutivos = sorted([{'ejecutivo':k,**v} for k,v in ejs_raw.items()], key=lambda x:-x['venta_mayo'])
print(f"Ejecutivos: {len(ejecutivos)}")

with open(JSON,'w',encoding='utf-8') as f:
    json.dump({'ejecutivos':ejecutivos,'clientes':clientes,'hoy_dia':HOY.day}, f, ensure_ascii=True, separators=(',',':'))
print("JSON guardado OK ->", JSON)
