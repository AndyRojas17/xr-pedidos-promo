import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import io
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import render_header, render_footer

st.set_page_config(
    page_title="En Tránsito — XR Panel",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_header("En Tránsito — Consulta de pedidos y lista promo")

# ── CARGA DE DATOS ────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "en_transito.csv")

@st.cache_data
def cargar_datos():
    df = pd.read_csv(DATA_PATH, dtype=str).fillna('')
    df['Cantidad']  = pd.to_numeric(df['Cantidad'],  errors='coerce').fillna(0)
    df['Precio']    = pd.to_numeric(df['Precio'],    errors='coerce')
    df['Descuento'] = pd.to_numeric(df['Descuento'], errors='coerce')
    df['Total']     = pd.to_numeric(df['Total'],     errors='coerce')
    return df

df = cargar_datos()
df_transito = df[df['Estado'] == 'En Transito']

# ── MÉTRICAS ─────────────────────────────────────────────────────────────────
total_items     = len(df_transito)
total_unidades  = int(df_transito['Cantidad'].sum())
total_inversion = df_transito['Total'].sum()
paty_count      = len(df_transito[df_transito['Fuente_Paty'] == 'Si'])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="metric-card blue">
        <div class="metric-value">{total_items}</div>
        <div class="metric-label">Ítems pedidos</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{total_unidades:,.0f}</div>
        <div class="metric-label">Unidades en tránsito</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="metric-card red">
        <div class="metric-value">S/. {total_inversion:,.0f}</div>
        <div class="metric-label">Inversión total</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="metric-card green">
        <div class="metric-value">{paty_count}</div>
        <div class="metric-label">Sugeridos por Paty</div></div>""", unsafe_allow_html=True)

st.markdown('<div style="margin-top:24px"></div>', unsafe_allow_html=True)

# ── BUSCADOR ─────────────────────────────────────────────────────────────────
st.markdown("""
<p style="color:#888;font-size:0.85rem;margin-bottom:12px">
    Escribe el código o nombre del repuesto para saber si fue pedido, su precio y descuento.
</p>
""", unsafe_allow_html=True)

query = st.text_input("", placeholder="Ej: 12391KRM840   /   pastilla freno   /   CB190R",
                      label_visibility="collapsed")

st.markdown('<div style="margin-top:8px"></div>', unsafe_allow_html=True)

# ── RESULTADOS ────────────────────────────────────────────────────────────────
if query.strip():
    terminos = [t.lower().strip() for t in query.split() if t.strip()]

    resultados = []
    for _, row in df.iterrows():
        texto = ' '.join([
            str(row['Codigo']).lower(),
            str(row['Descripcion']).lower(),
            str(row['Modelo']).lower(),
        ])
        matches = sum(1 for t in terminos if t in texto)
        if matches > 0:
            resultados.append((matches, row))

    resultados.sort(key=lambda x: (-x[0], x[1]['Estado'] != 'En Transito'))

    if not resultados:
        st.warning(f"No se encontró **\"{query}\"** en la lista promocional.")
    else:
        st.markdown(f"**{len(resultados)} resultado(s)** para *\"{query}\"*")
        st.markdown('<div style="margin-top:8px"></div>', unsafe_allow_html=True)

        for _, row in resultados:
            en_transito = row['Estado'] == 'En Transito'

            precio_str    = f"S/. {row['Precio']:.2f}"   if pd.notna(row['Precio'])    else '—'
            desc_str      = f"{row['Descuento']*100:.1f}%" if pd.notna(row['Descuento']) else '—'
            cantidad_str  = f"{int(row['Cantidad'])} uds"
            total_str     = f"S/. {row['Total']:,.2f}"   if pd.notna(row['Total'])     else '—'
            paty_badge    = ' &nbsp;<span style="background:#E8F5E9;color:#2E7D32;padding:1px 7px;border-radius:8px;font-size:0.72rem;font-weight:700">Sugerido Paty</span>' if row['Fuente_Paty'] == 'Si' else ''

            if en_transito:
                borde_color  = '#2E7D32'
                estado_bg    = '#E8F5E9'
                estado_fg    = '#2E7D32'
                estado_txt   = '✅ En Tránsito'
                detalle_html = (f'<span style="font-size:0.8rem;color:#666">📦 <b style="color:#1A1A1A">{cantidad_str}</b></span>'
                                f'&nbsp;&nbsp;<span style="font-size:0.8rem;color:#666">💲 Precio: <b>{precio_str}</b></span>'
                                f'&nbsp;&nbsp;<span style="font-size:0.8rem;color:#666">🏷️ Desc.: <b style="color:#CC0000">{desc_str}</b></span>')
            else:
                borde_color  = '#AAAAAA'
                estado_bg    = '#F5F5F5'
                estado_fg    = '#888888'
                estado_txt   = '⚠️ No solicitado'
                detalle_html = (f'<span style="font-size:0.8rem;color:#666">💲 Precio lista: <b>{precio_str}</b></span>'
                                f'&nbsp;&nbsp;<span style="font-size:0.8rem;color:#666">🏷️ Desc. promo: <b style="color:#CC0000">{desc_str}</b></span>'
                                f'&nbsp;&nbsp;<span style="font-size:0.8rem;color:#888;font-style:italic">Este repuesto no fue incluido en el pedido.</span>')

            modelo_txt = row['Modelo'] if row['Modelo'] else '—'
            card = (
                f'<div style="background:#FAFAFA;border:1px solid #E5E5E5;border-left:4px solid {borde_color};border-radius:8px;padding:14px 20px;margin-bottom:8px">'
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:6px">'
                f'<div style="flex:1;min-width:200px">'
                f'<span style="font-family:monospace;background:#F0F0F0;color:#333;padding:2px 8px;border-radius:4px;font-size:0.85rem;font-weight:700">{row["Codigo"]}</span>'
                f'<span style="font-size:0.95rem;font-weight:700;color:#1A1A1A;margin-left:10px">{row["Descripcion"]}</span>'
                f'{paty_badge}'
                f'</div>'
                f'<span style="background:{estado_bg};color:{estado_fg};padding:3px 12px;border-radius:10px;font-size:0.78rem;font-weight:700;white-space:nowrap">{estado_txt}</span>'
                f'</div>'
                f'<div style="margin-bottom:8px"><span style="font-size:0.78rem;color:#888">🏍️ {modelo_txt}</span></div>'
                f'<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center">{detalle_html}</div>'
                f'</div>'
            )
            st.markdown(card, unsafe_allow_html=True)

else:
    # Estado inicial — mostrar ítems en tránsito
    st.markdown("### Ítems actualmente en tránsito")
    st.markdown('<div style="margin-top:4px"></div>', unsafe_allow_html=True)

    for _, row in df_transito.iterrows():
        precio_str = f"S/. {row['Precio']:.2f}" if pd.notna(row['Precio']) else '—'
        desc_str   = f"{row['Descuento']*100:.1f}%" if pd.notna(row['Descuento']) else '—'
        total_str  = f"S/. {row['Total']:,.2f}" if pd.notna(row['Total']) else '—'
        paty_badge = ' &nbsp;<span style="background:#E8F5E9;color:#2E7D32;padding:1px 7px;border-radius:8px;font-size:0.72rem;font-weight:700">Sugerido Paty</span>' if row['Fuente_Paty'] == 'Si' else ''

        card = (
            f'<div style="background:#FAFAFA;border:1px solid #E5E5E5;border-left:4px solid #2E7D32;border-radius:8px;padding:12px 20px;margin-bottom:6px">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'
            f'<div style="flex:1;min-width:200px">'
            f'<span style="font-family:monospace;background:#F0F0F0;color:#333;padding:2px 8px;border-radius:4px;font-size:0.82rem;font-weight:700">{row["Codigo"]}</span>'
            f'<span style="font-size:0.9rem;font-weight:700;color:#1A1A1A;margin-left:10px">{row["Descripcion"]}</span>'
            f'{paty_badge}</div>'
            f'<div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">'
            f'<span style="font-size:0.8rem;color:#666">📦 <b>{int(row["Cantidad"])} uds</b></span>'
            f'<span style="font-size:0.8rem;color:#666">💲 <b>{precio_str}</b></span>'
            f'<span style="font-size:0.8rem;color:#666">🏷️ <b style="color:#CC0000">{desc_str}</b></span>'
            f'</div></div></div>'
        )
        st.markdown(card, unsafe_allow_html=True)

# ── DESCARGA ──────────────────────────────────────────────────────────────────
st.markdown('<div style="margin-top:32px"></div>', unsafe_allow_html=True)
st.markdown('<hr style="border:none;border-top:1px solid #EEE;margin-bottom:20px">', unsafe_allow_html=True)

def generar_excel_transito(df_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'En Tránsito'

    ws.merge_cells('A1:H1')
    c = ws['A1']
    c.value = 'XR MOTO STORE — PEDIDOS EN TRÁNSITO + LISTA PROMO MAYO 2026'
    c.font = Font(name='Arial', bold=True, size=12, color='FFFFFF')
    c.fill = PatternFill('solid', start_color='CC0000')
    c.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 24

    headers = ['Código', 'Descripción', 'Modelo', 'Precio (S/.)', 'Desc. %', 'Cantidad', 'Total (S/.)', 'Estado']
    widths  = [18, 40, 30, 14, 10, 12, 14, 18]
    thin = Side(style='thin', color='D9D9D9')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for ci, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(row=2, column=ci, value=h)
        cell.font = Font(name='Arial', bold=True, size=10, color='FFFFFF')
        cell.fill = PatternFill('solid', start_color='404040')
        cell.alignment = Alignment(horizontal='center', vertical='center')
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.row_dimensions[2].height = 20

    fill_transito = PatternFill('solid', start_color='E8F5E9')
    fill_no_solic = PatternFill('solid', start_color='F5F5F5')

    for ri, (_, row) in enumerate(df_data.iterrows()):
        er = ri + 3
        precio   = row['Precio']    if pd.notna(row['Precio'])    else ''
        desc     = row['Descuento'] if pd.notna(row['Descuento']) else ''
        cantidad = int(row['Cantidad']) if row['Cantidad'] > 0 else ''
        total    = row['Total']     if pd.notna(row['Total'])     else ''
        vals = [row['Codigo'], row['Descripcion'], row['Modelo'],
                precio, desc, cantidad, total, row['Estado']]
        fill = fill_transito if row['Estado'] == 'En Transito' else fill_no_solic

        for ci, val in enumerate(vals, 1):
            cell = ws.cell(row=er, column=ci, value=val)
            cell.border = border
            cell.font = Font(name='Arial', size=9)
            cell.alignment = Alignment(vertical='center')
            cell.fill = fill
            if ci == 1:
                cell.font = Font(name='Arial', bold=True, size=9)
            if ci == 4 and val != '':
                cell.number_format = '#,##0.00'
            if ci == 5 and val != '':
                cell.number_format = '0.0%'
            if ci == 7 and val != '':
                cell.number_format = '#,##0.00'
        ws.row_dimensions[er].height = 16

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf

col_dl, col_info = st.columns([1, 2])
with col_dl:
    clave = st.text_input("🔒 Clave de administrador", type="password",
                          placeholder="Ingresa la clave para descargar")
    if clave == "xr3010":
        excel_data = generar_excel_transito(df)
        st.download_button(
            label="⬇️  Descargar lista completa (Excel)",
            data=excel_data,
            file_name="XR_En_Transito.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    elif clave:
        st.markdown('<p style="color:#CC0000;font-size:0.82rem;margin-top:4px">Clave incorrecta.</p>',
                    unsafe_allow_html=True)
with col_info:
    st.markdown(f"""
    <p style="color:#888;font-size:0.85rem;margin-top:8px">
        Base completa: <b>{len(df)} ítems</b> de la Lista Promo Mayo 2026 —
        <b>{total_items} pedidos</b> en tránsito y
        <b>{len(df)-total_items} no solicitados</b>.
        Solo disponible para administradores.
    </p>
    """, unsafe_allow_html=True)

render_footer()
