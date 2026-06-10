import json, base64

BASE     = r'C:\Users\ausisima\Desktop\DIRECCION DE PRODUCTO\Master BI por region'
JSON     = BASE + r'\master_bi_data.json'
TEMPLATE = BASE + r'\template.html'
OUTPUT   = BASE + r'\Master BI por región.html'
LOGO     = r'C:\Users\ausisima\Desktop\DIRECCION DE PRODUCTO\lock_and_fell\logo odemas Vt color.png'

with open(JSON, encoding='utf-8') as f:
    data = json.load(f)

MESES_ES = ['enero','febrero','marzo','abril','mayo','junio',
            'julio','agosto','septiembre','octubre','noviembre','diciembre']

ejs_js   = json.dumps(data['ejecutivos'], ensure_ascii=True, separators=(',',':'))
clis_js  = json.dumps(data['clientes'],   ensure_ascii=True, separators=(',',':'))
hoy_dia  = str(data.get('hoy_dia', 31))
hoy_str  = data.get('hoy_str', '')
if not hoy_str:
    # Construir desde el JSON si no viene explícito
    from datetime import date as _date
    import sys, importlib.util
    _spec = importlib.util.spec_from_file_location('ed', BASE + r'\extraer_datos.py')
    _ed   = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_ed)
    _h    = _ed.HOY
    hoy_str = f'{_h.day} de {MESES_ES[_h.month-1]} de {_h.year}'
logo_b64 = base64.b64encode(open(LOGO,'rb').read()).decode('ascii')

html = open(TEMPLATE, encoding='utf-8').read()
html = html.replace('{{EJS_DATA}}',  ejs_js)
html = html.replace('{{CLIS_DATA}}', clis_js)
html = html.replace('{{HOY_DIA}}',   hoy_dia)
html = html.replace('{{HOY_STR}}',   hoy_str)
html = html.replace('{{LOGO}}',      logo_b64)

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html)

print("Master BI.html generado OK ->", OUTPUT)
