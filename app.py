"""
Surco Raro: tienda de ejemplo de vinilos de colección.
Discos, artistas y precios son ficticios.

Ejecutar:  streamlit run app.py
"""

import math
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Surco Raro | Vinilos de colección",
    page_icon="💿",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Estado de la sesión
# ---------------------------------------------------------------------------
if "dark" not in st.session_state:
    st.session_state.dark = True
if "cart" not in st.session_state:
    st.session_state.cart = []
if "rpm" not in st.session_state:
    st.session_state.rpm = "33⅓"
if "toast" not in st.session_state:
    st.session_state.toast = None
if "auction_end" not in st.session_state:
    st.session_state.auction_end = datetime.now() + timedelta(days=2, hours=7, minutes=13)

# ---------------------------------------------------------------------------
# Catálogo (ficticio)
# ---------------------------------------------------------------------------
RECORDS = [
    dict(id=1, titulo="Medianoche en Valparaíso", artista="Los Faroles del Puerto", anio=1967,
         genero="Jazz", edicion="Primera prensa mono, sello naranja", estado="Near Mint", copias=40,
         precio=4800, sello="#E8B04B",
         portada="linear-gradient(160deg,#0f3b57 0 55%,#e8b04b 55% 60%,#0f3b57 60%)"),
    dict(id=2, titulo="Órbita Lenta", artista="Cassandra Vélez", anio=1972,
         genero="Psicodelia", edicion="Portada desplegable firmada por la artista", estado="VG+", copias=12,
         precio=12500, sello="#D1495B",
         portada="radial-gradient(circle at 30% 35%,#f2c14e 0 18%,transparent 19%),linear-gradient(135deg,#5b2a86,#d1495b)"),
    dict(id=3, titulo="Humo Azul", artista="The Lowland Quartet", anio=1959,
         genero="Jazz", edicion="Test pressing con notas del ingeniero", estado="Near Mint", copias=3,
         precio=18900, sello="#2E4A7D",
         portada="repeating-linear-gradient(90deg,#1c2b4a 0 14px,#2e4a7d 14px 28px)"),
    dict(id=4, titulo="Neón Fantasma", artista="Kraftzeit", anio=1981,
         genero="Electrónica", edicion="Vinilo transparente, 300 copias numeradas", estado="Mint", copias=300,
         precio=3200, sello="#FF2BD6",
         portada="linear-gradient(0deg,#0b0b12 40%,#ff2bd6 40% 42%,#0b0b12 42% 60%,#2bf0ff 60% 62%,#0b0b12 62%)"),
    dict(id=5, titulo="Raíces de Cobre", artista="Coro Andino del Norte", anio=1970,
         genero="Folk", edicion="Prensado chileno retirado de circulación", estado="VG+", copias=25,
         precio=7600, sello="#B5651D",
         portada="linear-gradient(180deg,#b5651d 0 50%,#6b3e1f 50%)"),
    dict(id=6, titulo="Soul de Medianoche", artista="Delia Moore & The Velvets", anio=1968,
         genero="Soul", edicion="Promo blanco para DJ", estado="Near Mint", copias=18,
         precio=9400, sello="#E4B363",
         portada="radial-gradient(circle at 70% 70%,#e4b363 0 22%,transparent 23%),#3a0f1d"),
    dict(id=7, titulo="Catedral de Ruido", artista="Sumo Templo", anio=1985,
         genero="Rock", edicion="Picture disc de la gira cancelada", estado="Mint", copias=150,
         precio=2100, sello="#E6E6E6",
         portada="repeating-conic-gradient(#e6e6e6 0 15deg,#1a1a1a 15deg 30deg)"),
    dict(id=8, titulo="Bolero para un astronauta", artista="Trío Satélite", anio=1962,
         genero="Bolero", edicion="Primera edición con encarte de letras", estado="VG+", copias=60,
         precio=6100, sello="#F6D6AD",
         portada="radial-gradient(circle at 50% 120%,#f6d6ad 0 40%,transparent 41%),linear-gradient(#0e1a40,#3b5ba5)"),
    dict(id=9, titulo="Tormenta Eléctrica", artista="Iron Comet", anio=1974,
         genero="Rock", edicion="Error de fábrica: lado B duplicado", estado="Near Mint", copias=7,
         precio=15300, sello="#FFD400",
         portada="linear-gradient(115deg,#111 0 45%,#ffd400 45% 52%,#111 52%)"),
    dict(id=10, titulo="Tierra sin mapa", artista="Aurelio Kann", anio=1977,
         genero="Progresivo", edicion="Caja numerada de 3 LP", estado="Mint", copias=90,
         precio=8800, sello="#8AA29E",
         portada="linear-gradient(135deg,#2d4739 0 33%,#8aa29e 33% 66%,#d9d0b4 66%)"),
    dict(id=11, titulo="Cumbia del Fin del Mundo", artista="Orquesta Sideral", anio=1976,
         genero="Cumbia", edicion="Prensado original de Lima", estado="VG+", copias=55,
         precio=4100, sello="#FF6B35",
         portada="repeating-radial-gradient(circle at 50% 50%,#ff6b35 0 10px,#004e89 10px 20px)"),
    dict(id=12, titulo="Sinfonía de Vidrio", artista="Ensamble Mercurio", anio=1964,
         genero="Clásica", edicion="Edición audiófila de 180 g", estado="Near Mint", copias=80,
         precio=5500, sello="#9FB8AD",
         portada="linear-gradient(135deg,rgba(255,255,255,.6),rgba(255,255,255,0)),linear-gradient(45deg,#9fb8ad,#cfe0e3)"),
]
df = pd.DataFrame(RECORDS)
BY_ID = {r["id"]: r for r in RECORDS}


def money(n: float) -> str:
    return "US$ " + f"{n:,.0f}".replace(",", ".")


# ---------------------------------------------------------------------------
# Tema: tokens de color
# ---------------------------------------------------------------------------
LIGHT = dict(bg="#E4E8E1", bg2="#D6DDD3", surface="#F3F5F0", ink="#1D2A26", muted="#5A6963",
             accent="#7A1F3D", accent_ink="#FFFFFF", gold="#9A7712", line="rgba(29,42,38,.18)",
             glow="rgba(122,31,61,.10)")
DARK = dict(bg="#15171C", bg2="#1C1F26", surface="#23262E", ink="#ECE6D8", muted="#A39E92",
            accent="#C24A6E", accent_ink="#FFFFFF", gold="#D9B54A", line="rgba(236,230,216,.14)",
            glow="rgba(217,181,74,.10)")
T = DARK if st.session_state.dark else LIGHT


def html(markup: str) -> None:
    """Inyecta HTML sin sangrías (Markdown convierte las sangrías en bloques de código)."""
    st.markdown("\n".join(l.strip() for l in markup.splitlines() if l.strip()), unsafe_allow_html=True)


FONTS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&family=Work+Sans:wght@300..700&display=swap');
</style>
"""

VARS = "<style>:root{" + "".join(f"--{k.replace('_', '-')}:{v};" for k, v in T.items()) + "}</style>"

CSS = """
<style>
html, body, .stApp, [data-testid="stAppViewContainer"] {
  background-color: var(--bg);
  color: var(--ink);
  font-family: 'Work Sans', system-ui, sans-serif;
  transition: background-color .6s ease, color .6s ease;
}
.stApp {
  background-image: radial-gradient(1200px 600px at 85% -10%, var(--glow), transparent 70%);
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
  background-color: var(--bg2);
  border-right: 1px solid var(--line);
  transition: background-color .6s ease;
}
.stApp p, .stApp li, .stApp label, .stApp span, .stApp h1, .stApp h2, .stApp h3,
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"],
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] p, [data-testid="stCaptionContainer"] {
  color: var(--ink);
}
.stApp h1, .stApp h2, .stApp h3 { font-family: 'Bodoni Moda', Georgia, serif; }

/* Campos de formulario */
[data-baseweb="select"] > div, [data-baseweb="input"] > div, .stTextInput input {
  background-color: var(--surface) !important;
  color: var(--ink) !important;
  border-color: var(--line) !important;
}
[data-baseweb="popover"] ul, [data-baseweb="popover"] li { background-color: var(--surface) !important; color: var(--ink) !important; }
[data-baseweb="tag"] { background-color: var(--accent) !important; }
[data-baseweb="tag"] span { color: var(--accent-ink) !important; }

/* Pestañas */
.stTabs [data-baseweb="tab-list"] { gap: 1.5rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] p { font-size: 1.05rem; color: var(--muted); }
.stTabs [aria-selected="true"] p { color: var(--ink); font-weight: 600; }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--accent); }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Botones */
.stButton > button {
  background: transparent;
  color: var(--ink);
  border: 1px solid var(--ink);
  border-radius: 999px;
  padding: .35rem 1.1rem;
  transition: background-color .25s ease, color .25s ease, border-color .25s ease, transform .15s ease;
}
.stButton > button p { color: inherit; }
.stButton > button:hover { background: var(--accent); border-color: var(--accent); color: var(--accent-ink); }
.stButton > button:active { transform: scale(.97); }
.stButton > button:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }
.stButton > button:disabled { opacity: .55; border-style: dashed; }

/* ---------- Hero con tocadiscos ---------- */
.hero { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 2rem; margin: .5rem 0 2.5rem; }
.hero-copy { flex: 1 1 340px; max-width: 34rem; }
.hero-copy h1 {
  font-family: 'Bodoni Moda', Georgia, serif;
  font-size: clamp(3.2rem, 8vw, 6.4rem);
  font-weight: 800;
  font-style: italic;
  line-height: .92;
  letter-spacing: -.03em;
  margin: 0 0 1.2rem;
  padding: 0;
  color: var(--ink);
}
.hero-copy p { font-size: 1.12rem; line-height: 1.6; color: var(--muted); margin: 0; }

.deck { --size: min(340px, 78vw); position: relative; width: calc(var(--size) * 1.18); height: var(--size); flex: 0 0 auto; }
.platter {
  position: absolute; left: 0; top: 0; width: var(--size); height: var(--size);
  border-radius: 50%; box-shadow: 0 30px 60px rgba(0,0,0,.35);
}
.platter::after {
  /* El brillo queda fijo mientras el disco gira, como la luz real sobre un vinilo */
  content: ""; position: absolute; inset: 0; border-radius: 50%; pointer-events: none;
  background: conic-gradient(from 20deg, transparent 0 30deg, rgba(255,255,255,.16) 50deg, transparent 75deg 205deg, rgba(255,255,255,.10) 228deg, transparent 250deg);
}
.record {
  position: absolute; inset: 0; border-radius: 50%;
  background:
    radial-gradient(circle, transparent 0 33%, rgba(0,0,0,.6) 33.5% 34.5%, transparent 35%),
    repeating-radial-gradient(circle, #101010 0 1.6px, #1d1d1d 1.6px 3.2px);
  animation: spin var(--dur) linear infinite;
}
.deck.paused .record { animation-play-state: paused; }
.lbl {
  position: absolute; inset: 33%; border-radius: 50%;
  background: radial-gradient(circle, var(--bg) 0 6%, var(--accent) 6.5%);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.lbl b { font-family: 'Bodoni Moda', Georgia, serif; font-style: italic; font-size: 1.5rem; color: var(--accent-ink); line-height: 1; transform: translateY(-.9rem); }
.lbl small { font-size: .62rem; color: var(--accent-ink); opacity: .85; transform: translateY(.9rem); }
.arm {
  position: absolute; right: 2%; top: 4%; width: 7px; height: 66%;
  background: linear-gradient(90deg, #9a9a9a, #e2e2e2, #8a8a8a); border-radius: 4px;
  transform-origin: 50% 4%; transform: rotate(24deg);
  transition: transform 1.2s cubic-bezier(.3,.7,.2,1);
}
.arm::before { content: ""; position: absolute; top: -10px; left: -10px; width: 27px; height: 27px; border-radius: 50%; background: var(--muted); }
.arm::after { content: ""; position: absolute; bottom: -14px; left: -6px; width: 19px; height: 26px; border-radius: 3px; background: var(--gold); }
.deck.paused .arm { transform: rotate(4deg); }
@keyframes spin { to { transform: rotate(360deg); } }

/* ---------- Tarjetas del catálogo ---------- */
.card {
  background: var(--surface); border: 1px solid var(--line); border-radius: 6px;
  padding: 18px 18px 14px; margin-bottom: .6rem;
  transition: background-color .6s ease, border-color .3s ease;
}
.card:hover { border-color: var(--accent); }
.sleeve-zone { position: relative; width: 76%; aspect-ratio: 1; margin: 2px 0 18px; }
.sleeve { position: absolute; inset: 0; z-index: 2; border-radius: 3px; box-shadow: 0 10px 22px rgba(0,0,0,.28); }
.disc {
  position: absolute; inset: 3%; z-index: 1; border-radius: 50%;
  background:
    radial-gradient(circle, #0c0c0c 0 3%, var(--lbl) 3.5% 30%, #0c0c0c 30.5%),
    repeating-radial-gradient(circle, #121212 0 1.5px, #232323 1.5px 3px);
  transition: transform .8s cubic-bezier(.2,.8,.2,1);
}
.card:hover .disc { transform: translateX(28%) rotate(220deg); }
.artist { font-size: .9rem; color: var(--muted) !important; margin: 0; }
.card h3 { font-size: 1.35rem; line-height: 1.15; margin: .15rem 0 .35rem; padding: 0; }
.meta { font-size: .88rem; color: var(--muted) !important; margin: 0 0 .5rem; }
.edition { font-size: .95rem; margin: 0 0 .75rem; }
.row { display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; margin-bottom: .6rem; }
.badge { font-size: .78rem; padding: .15rem .55rem; border: 1px solid var(--gold); color: var(--gold) !important; border-radius: 999px; }
.copies { font-size: .8rem; color: var(--muted) !important; }
.price { font-family: 'Bodoni Moda', Georgia, serif; font-size: 1.6rem; font-weight: 700; margin: 0; }

/* ---------- Carrito ---------- */
.mini { width: 46px; height: 46px; border-radius: 50%;
  background: radial-gradient(circle, #0c0c0c 0 5%, var(--lbl) 6% 32%, #0c0c0c 33%), repeating-radial-gradient(circle, #121212 0 1.5px, #232323 1.5px 3px); }
.cart-title { font-family: 'Bodoni Moda', Georgia, serif; font-size: 1.15rem; margin: 0; }
.cart-sub { font-size: .85rem; color: var(--muted) !important; margin: 0; }
.total { font-family: 'Bodoni Moda', Georgia, serif; font-size: 2.2rem; font-weight: 700; margin: .2rem 0 1rem; }

.foot { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--line); font-size: .85rem; color: var(--muted) !important; }

@media (prefers-reduced-motion: reduce) {
  .record { animation: none; }
  .disc, .arm, .stApp, .card { transition: none; }
}
</style>
"""

html(FONTS)
html(VARS)
html(CSS)

# Mensaje pendiente de una acción anterior
if st.session_state.toast:
    st.toast(st.session_state.toast, icon="💿")
    st.session_state.toast = None

# ---------------------------------------------------------------------------
# Acciones
# ---------------------------------------------------------------------------
def add_to_cart(rid: int) -> None:
    if rid not in st.session_state.cart:
        st.session_state.cart.append(rid)
        st.session_state.toast = f"«{BY_ID[rid]['titulo']}» añadido al carrito"


def remove_from_cart(rid: int) -> None:
    if rid in st.session_state.cart:
        st.session_state.cart.remove(rid)
        st.session_state.toast = f"«{BY_ID[rid]['titulo']}» quitado del carrito"


def confirm_order() -> None:
    st.session_state.cart = []
    st.session_state.order_done = True


# ---------------------------------------------------------------------------
# Barra superior: tema y tocadiscos
# ---------------------------------------------------------------------------
_, c_theme, c_rpm = st.columns([5, 1.3, 2.2])
with c_theme:
    st.toggle("Modo oscuro", key="dark")
with c_rpm:
    st.radio("Tocadiscos", ["33⅓", "45", "Pausa"], key="rpm", horizontal=True)

rpm = st.session_state.rpm
dur = {"33⅓": 1.8, "45": 1.333}.get(rpm, 1.8)
deck_state = "paused" if rpm == "Pausa" else "playing"
rpm_label = "33⅓" if rpm == "Pausa" else rpm

html(f"""
<div class="hero">
<div class="hero-copy">
<h1>Surco Raro</h1>
<p>Primeras prensas, ediciones numeradas y errores de fábrica que nunca debieron salir.
Cada disco se revisa a mano, se fotografía y se envía asegurado con certificado de autenticidad.</p>
</div>
<div class="deck {deck_state}" style="--dur:{dur}s" aria-hidden="true">
<div class="platter"><div class="record"><div class="lbl"><b>SR</b><small>{rpm_label} RPM</small></div></div></div>
<div class="arm"></div>
</div>
</div>
""")

# ---------------------------------------------------------------------------
# Filtros (barra lateral)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Buscar en el catálogo")
    q = st.text_input("Título o artista", placeholder="Ej.: Humo Azul")
    generos = st.multiselect("Género", sorted(df.genero.unique()))
    anios = st.slider("Año de edición", int(df.anio.min()), int(df.anio.max()),
                      (int(df.anio.min()), int(df.anio.max())))
    precio = st.slider("Precio (US$)", 0, 20000, (0, 20000), step=500)
    estados = st.multiselect("Estado", ["Mint", "Near Mint", "VG+"])
    orden = st.selectbox("Ordenar por", ["Más caros primero", "Más baratos primero",
                                         "Más antiguos primero", "Más raros primero"])

view = df.copy()
if q:
    mask = view.titulo.str.contains(q, case=False) | view.artista.str.contains(q, case=False)
    view = view[mask]
if generos:
    view = view[view.genero.isin(generos)]
if estados:
    view = view[view.estado.isin(estados)]
view = view[view.anio.between(*anios) & view.precio.between(*precio)]
sort_map = {
    "Más caros primero": ("precio", False),
    "Más baratos primero": ("precio", True),
    "Más antiguos primero": ("anio", True),
    "Más raros primero": ("copias", True),
}
col, asc = sort_map[orden]
view = view.sort_values(col, ascending=asc)

# ---------------------------------------------------------------------------
# Pestañas
# ---------------------------------------------------------------------------
n_cart = len(st.session_state.cart)
tab_cat, tab_mkt, tab_cart = st.tabs(["Catálogo", "Mercado", f"Carrito ({n_cart})"])

# ----- Catálogo -----
with tab_cat:
    # Subasta con cuenta regresiva en vivo (JavaScript dentro de un iframe)
    end_ms = int(st.session_state.auction_end.timestamp() * 1000)
    st.iframe(f"""
<div style="font-family:'Work Sans',system-ui,sans-serif;background:{T['surface']};color:{T['ink']};
border:1px solid {T['gold']};border-radius:6px;padding:16px 20px;display:flex;flex-wrap:wrap;
gap:12px 32px;align-items:center;justify-content:space-between">
  <div>
    <div style="font-size:.9rem;color:{T['muted']}">Subasta de la semana</div>
    <div style="font-family:'Bodoni Moda',Georgia,serif;font-size:1.4rem;font-weight:700">
      Humo Azul, The Lowland Quartet (1959)</div>
    <div style="font-size:.9rem;color:{T['muted']}">Test pressing con notas del ingeniero. Puja actual: {money(21400)}</div>
  </div>
  <div id="cd" style="font-family:'Bodoni Moda',Georgia,serif;font-size:2rem;font-weight:700;color:{T['gold']}"></div>
</div>
<script>
const end = {end_ms};
const el = document.getElementById('cd');
const pad = n => String(n).padStart(2, '0');
function tick() {{
  let s = Math.max(0, Math.floor((end - Date.now()) / 1000));
  const d = Math.floor(s / 86400); s %= 86400;
  const h = Math.floor(s / 3600); s %= 3600;
  const m = Math.floor(s / 60); s %= 60;
  el.textContent = d + 'd ' + pad(h) + ':' + pad(m) + ':' + pad(s);
}}
tick(); setInterval(tick, 1000);
</script>
""", height=130)

    st.write("")
    if view.empty:
        st.info("Ningún disco coincide con los filtros. Amplía el rango de precio o quita algún género.")
    else:
        st.caption(f"{len(view)} discos. Pasa el cursor sobre una portada para sacar el vinilo.")
        cols = st.columns(3, gap="large")
        for i, r in enumerate(view.to_dict("records")):
            with cols[i % 3]:
                html(f"""
<div class="card">
<div class="sleeve-zone">
<div class="disc" style="--lbl:{r['sello']}"></div>
<div class="sleeve" style="background:{r['portada']}"></div>
</div>
<p class="artist">{r['artista']}</p>
<h3>{r['titulo']}</h3>
<p class="meta">{r['anio']}, {r['genero']}</p>
<p class="edition">{r['edicion']}</p>
<div class="row"><span class="badge">{r['estado']}</span>
<span class="copies">{r['copias']} copias conocidas</span></div>
<p class="price">{money(r['precio'])}</p>
</div>
""")
                in_cart = r["id"] in st.session_state.cart
                st.button(
                    "En el carrito" if in_cart else "Añadir al carrito",
                    key=f"add_{r['id']}",
                    disabled=in_cart,
                    on_click=add_to_cart,
                    args=(r["id"],),
                )
                st.write("")

# ----- Mercado -----
def style_fig(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark" if st.session_state.dark else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Work Sans, sans-serif", color=T["ink"]),
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        transition_duration=500,
    )
    fig.update_xaxes(gridcolor=T["line"], zeroline=False)
    fig.update_yaxes(gridcolor=T["line"], zeroline=False)
    return fig


with tab_mkt:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Discos en catálogo", len(df))
    m2.metric("Precio promedio", money(df.precio.mean()))
    top = df.loc[df.precio.idxmax()]
    m3.metric("Pieza más cara", money(top.precio), top.titulo, delta_color="off")
    m4.metric("Copias conocidas (mediana)", int(df.copias.median()))

    palette = [T["accent"], T["gold"], "#4F8A8B", "#8E7DBE", "#D17A22", "#5A9E6F", "#B3446C", "#6C8EBF"]

    g1, g2 = st.columns(2, gap="large")
    with g1:
        fig = px.scatter(
            df, x="anio", y="precio", size=1000 / df.copias, color="genero",
            hover_name="titulo", hover_data={"artista": True, "copias": True, "anio": False},
            color_discrete_sequence=palette,
            labels={"anio": "Año", "precio": "Precio (US$)", "genero": "Género"},
            title="Precio según año (tamaño = rareza)",
        )
        st.plotly_chart(style_fig(fig), width="stretch", theme=None)
    with g2:
        avg = df.groupby("genero", as_index=False).precio.mean().sort_values("precio")
        fig = px.bar(avg, x="precio", y="genero", orientation="h",
                     labels={"precio": "Precio promedio (US$)", "genero": ""},
                     title="Precio promedio por género")
        fig.update_traces(marker_color=T["accent"])
        st.plotly_chart(style_fig(fig), width="stretch", theme=None)

    meses = pd.date_range("2024-01-01", "2026-11-01", freq="MS")
    indice = [100 + i * 1.9 + 6 * math.sin(i / 2.3) for i in range(len(meses))]
    fig = go.Figure(go.Scatter(x=meses, y=indice, mode="lines", fill="tozeroy",
                               line=dict(color=T["gold"], width=3),
                               fillcolor=T["glow"], name="Índice"))
    fig.update_layout(title="Índice de precios de vinilo de colección (base 100 = ene 2024)",
                      yaxis_range=[80, max(indice) + 10])
    st.plotly_chart(style_fig(fig), width="stretch", theme=None)

# ----- Carrito -----
with tab_cart:
    if st.session_state.pop("order_done", False):
        st.balloons()
        st.success("Pedido confirmado. Esto es una demo: no se procesó ningún pago.")

    if not st.session_state.cart:
        st.info("Tu carrito está vacío. Elige un disco en el catálogo para empezar.")
    else:
        subtotal = 0
        for rid in list(st.session_state.cart):
            r = BY_ID[rid]
            subtotal += r["precio"]
            c1, c2, c3, c4 = st.columns([0.6, 5, 2, 1.6], vertical_alignment="center")
            with c1:
                html(f'<div class="mini" style="--lbl:{r["sello"]}"></div>')
            with c2:
                html(f'<p class="cart-title">{r["titulo"]}</p><p class="cart-sub">{r["artista"]}, {r["anio"]}. {r["edicion"]}</p>')
            with c3:
                html(f'<p class="price" style="font-size:1.2rem">{money(r["precio"])}</p>')
            with c4:
                st.button("Quitar", key=f"rm_{rid}", on_click=remove_from_cart, args=(rid,))

        envio = max(45, subtotal * 0.02)
        st.divider()
        st.write(f"Subtotal: {money(subtotal)}")
        st.write(f"Envío asegurado (2 %, mínimo US$ 45): {money(envio)}")
        html(f'<p class="total">Total {money(subtotal + envio)}</p>')
        st.button("Confirmar pedido", key="checkout", on_click=confirm_order)

html('<p class="foot">Sitio de ejemplo hecho con Streamlit. Los discos, artistas y precios son ficticios.</p>')
