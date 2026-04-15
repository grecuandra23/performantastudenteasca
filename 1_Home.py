import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Analiza Studentilor", page_icon="🎓", layout="wide")

# ── Stiluri CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Montserrat', sans-serif;
    background-color: #FAF8F5;
    font-size: 18px;
}

p { color: #444; font-size: 1.05rem; line-height: 1.6; }
h1 { font-size: 2.8rem; font-weight: 700; color: #660000; }
h2 { font-size: 2rem; font-weight: 600; color: #660000; }
h3 { font-size: 1.5rem; font-weight: 600; color: #1a1a1a; }

label { color: #660000; font-weight: 500; }

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e8e2dc;
    border-left: 5px solid #660000;
    border-radius: 10px;
    padding: 18px;
}

div[data-testid="stMetricValue"] {
    color: #660000 !important;
    font-weight: 700;
    font-size: 1.6rem;
}

div[data-testid="stSlider"] div[role="progressbar"] > div { background-color: #660000 !important; }
div[data-testid="stSlider"] [role="slider"] { background-color: #660000 !important; border-color: #660000 !important; }
div[data-testid="stSlider"] [data-testid="stThumbValue"] { color: #660000 !important; }

[data-testid="stFileUploader"] section {
    border: 2px dashed rgba(102,0,0,0.25);
    border-radius: 10px;
    padding: 20px;
    background: rgba(102,0,0,0.02);
}

button[kind="primary"] { background-color: #660000; color: white; border-radius: 6px; border: none; }

span[data-baseweb="tag"] { background-color: #660000 !important; color: white !important; }

button[data-baseweb="tab"][aria-selected="true"] { color: #660000; border-bottom: 2px solid #660000; }

.stDataFrame { border: 1px solid #e8e2dc; border-radius: 8px; }

hr { border-top: 1px solid #e8e2dc; }

.accent-bar { width: 40px; height: 3px; background: #660000; margin: 10px auto 20px auto; }

.about-card {
    background: white;
    border: 1px solid #e8e2dc;
    border-left: 5px solid #660000;
    border-radius: 10px;
    padding: 22px 24px;
}

.about-card p { color: #444; }
.about-card strong { color: #660000; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.title("Proiect **Analiza perfomantelor scolare**")
st.sidebar.markdown("**Grecu Andra-Maria & Grigore-Georgescu Matei**")
st.sidebar.markdown("---")

st.markdown("""
<h1 style='text-align:center; font-size:2.9rem; font-weight:800;
letter-spacing:0.02em; color:#1a1a1a; margin-bottom:-6px; text-transform:uppercase;'>
Analiza Performantei Scolare Portugheze
</h1>
""", unsafe_allow_html=True)

st.markdown('<p style="text-align:center; font-size:1.2rem; color:#777; margin-top:0;">Performanta academica in liceele portugheze — Gabriel Pereira si Mousinho da Silveira.</p>', unsafe_allow_html=True)
st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)

st.markdown('<div class="accent-bar" style="margin-left:0;"></div>', unsafe_allow_html=True)
st.markdown("### Despre dataset")

st.markdown("""
<div class="about-card">
    <p>Acest proiect analizeaza performanta academica a elevilor din doua licee portugheze
    (<strong>Gabriel Pereira</strong> si <strong>Mousinho da Silveira</strong>). Datele contin informatii despre:</p>
    <p>
    <strong>Caracteristici demografice</strong> — varsta, sex, mediu urban/rural<br>
    <strong>Comportament scolar</strong> — ore de studiu, absente, meditatii private<br>
    <strong>Factori sociali</strong> — suport familie, acces internet, activitati<br>
    <strong>Note</strong> — trimestrul 1, trimestrul 2 si nota finala (scala 0-20, nota de trecere: 10)
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown('<div class="accent-bar" style="margin-left:0;"></div>', unsafe_allow_html=True)
st.markdown("### Incarca datele")

# ── Încărcare CSV ─────────────────────────────────────────────────
# pd.read_csv → citește fișierul în DataFrame
# replace() → normalizează valorile yes/no în Da/Nu
# session_state → persistă DataFrame-ul între pagini
fisier = st.file_uploader("Incarca fisierul CSV", type=["csv"], label_visibility="collapsed")
if fisier is not None:
    df = pd.read_csv(fisier)
    df = df.replace({'yes': 'Da', 'no': 'Nu'})
    st.session_state['df'] = df
    st.success("Fisier incarcat cu succes")
elif 'df' in st.session_state:
    df = st.session_state['df']
else:
    st.info("Incarca fisierul .csv pentru a continua.")
    st.stop()

st.markdown("### Prezentare generala")
st.markdown('<div class="accent-bar" style="margin-left:0;"></div>', unsafe_allow_html=True)

# df.shape[1] → numărul de coloane; isnull().sum().sum() → total NaN-uri din tot DataFrame-ul
c1, c2, c3 = st.columns(3, gap="medium")
c1.metric("Inregistrari", f"{len(df):,}")
c2.metric("Coloane", f"{df.shape[1]}")
c3.metric("Valori lipsa", f"{df.isnull().sum().sum()}")

st.markdown("<br>", unsafe_allow_html=True)

st.caption(f"{len(df)} inregistrari — click pe o celulă pentru a edita, **−** pentru a șterge, **+** pentru a adăuga.")

# ── Editor interactiv ─────────────────────────────────────────────
# data_editor permite editarea directă în tabel; num_rows="dynamic" permite adăugare/ștergere rânduri
# reset_index(drop=True) reindexează după ștergeri
df_editat = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="data_editor")

if st.button("Salvează modificările"):
    st.session_state['df'] = df_editat.reset_index(drop=True)
    st.success(f"Date salvate. Total rânduri: {len(df_editat)}.")

st.markdown("---")
st.info("Navigheaza la **Vizualizare Interactiva** din sidebar pentru filtre si grafice.")
