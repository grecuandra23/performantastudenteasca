import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vizualizare Interactiva", page_icon="🎓", layout="wide")

# ── Stiluri CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

html, body, .stApp { font-family: 'Montserrat', sans-serif; background-color: #FAF8F5; font-size: 18px; }
p { color: #444; font-size: 1.05rem; line-height: 1.6; }
h1 { font-size: 2.8rem; font-weight: 700; color: #660000; }
label { color: #660000; font-weight: 500; }
div[data-testid="stMetric"] {
    background: white; border: 1px solid #e8e2dc;
    border-left: 5px solid #660000; border-radius: 10px; padding: 18px;
}
div[data-testid="stMetricValue"] { color: #660000 !important; font-weight: 700; font-size: 1.6rem; }
span[data-baseweb="tag"] { background-color: #660000 !important; color: white !important; }
.accent-bar { width: 40px; height: 3px; background: #660000; margin: 10px auto 20px auto; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.title("Proiect **Analiza performantelor scolare**")
st.sidebar.markdown("**Grecu Andra-Maria & Grigore-Georgescu Matei**")
st.sidebar.markdown("---")

st.markdown("<h1 style='text-align:center;'>Vizualizare Interactiva</h1>", unsafe_allow_html=True)
st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)
st.markdown("---")

if 'df' not in st.session_state:
    st.warning("Incarca mai intai fisierul CSV.")
    st.stop()

df_original = st.session_state["df"]
df_procesat = st.session_state.get("df_procesat", None)

# ── Selectare mod vizualizare ─────────────────────────────────────
mod_viz = st.selectbox("Mod vizualizare:", ["Date originale", "Date preprocesate"])

if mod_viz == "Date originale":
    df = df_original
    st.info("Afișezi date ORIGINALE")
elif mod_viz == "Date preprocesate":
    if df_procesat is not None:
        df = df_procesat
        st.success("Afișezi date PREPROCESATE")
    else:
        st.warning("Nu există date preprocesate")
        st.stop()

# ══════════════════════════════════════════════════════════════════
# METRICI GENERALE
# .sum() / len(df) → procente; .mean() → medie coloană numerică
# ══════════════════════════════════════════════════════════════════
st.markdown("### Statistici generale")

pct_meditatii = ((df['Meditatii_Private'] == 'Da') | (df['Meditatii_Private'] == 0)).sum() / len(df) * 100
pct_familie   = ((df['Ajutor_Familie'] == 'Da') | (df['Ajutor_Familie'] == 0)).sum() / len(df) * 100
pct_bursa     = ((df['Meditatii_Scoala'] == 'Da') | (df['Meditatii_Scoala'] == 0)).sum() / len(df) * 100 if 'Meditatii_Scoala' in df.columns else 0

c1, c2, c3 = st.columns(3)
c1.metric("Total studenti", len(df))
c2.metric("Medie nota finala", f"{df['Nota_Finala'].mean():.1f} / 20")
c3.metric("Varsta medie", f"{df['Varsta'].mean():.1f}")

c4, c5, c6 = st.columns(3)
c4.metric("Pregatire privata", f"{pct_meditatii:.1f}%")
c5.metric("Suport familie", f"{pct_familie:.1f}%")
c6.metric("Medie absente", f"{df['Absente'].mean():.1f}")

c7, c8, c9 = st.columns(3)
c7.metric("Meditatii scoala", f"{pct_bursa:.1f}%")
c8.metric("Promovati ", ((df['Nota_Finala'] >= 10) | (df['Nota_Finala'] >= 5)).sum())
c9.metric("Nepromovati ", ((df['Nota_Finala'] < 10) & (df['Nota_Finala'] < 5)).sum())

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# FILTRE
# isin() → filtrare pe valori multiple; between() → interval numeric
# df.loc[mask] → selectare rânduri pe baza măștii booleene
# &= → compunere condiții cu AND
# ══════════════════════════════════════════════════════════════════
st.markdown("### Filtre")

f1, f2, f3 = st.columns(3)
with f1:
    scoala_sel = st.multiselect("Scoala", df_original['Scoala'].unique(), default=df_original['Scoala'].unique())
with f2:
    sex_sel = st.multiselect("Sex", df_original['Sex'].unique(), default=df_original['Sex'].unique())
with f3:
    mediu_sel = st.multiselect("Mediu", df_original['Mediu'].unique(), default=df_original['Mediu'].unique())

f4, f5, f6 = st.columns(3)
with f4:
    meditatii_sel = st.multiselect("Meditatii private", df_original['Meditatii_Private'].unique(), default=df_original['Meditatii_Private'].unique())
with f5:
    internet_sel = st.multiselect("Internet", df_original['Internet'].unique(), default=df_original['Internet'].unique())
with f6:
    varsta_opt = st.selectbox("Varsta", ["Toate", "15-16", "17-18", "19+"])

absente_range = st.slider(
    "Absente",
    int(df_original['Absente'].min()),
    int(df_original['Absente'].max()),
    (int(df_original['Absente'].min()), int(df_original['Absente'].max()))
)

mask = (
    df_original['Scoala'].isin(scoala_sel) &
    df_original['Sex'].isin(sex_sel) &
    df_original['Mediu'].isin(mediu_sel) &
    df_original['Meditatii_Private'].isin(meditatii_sel) &
    df_original['Internet'].isin(internet_sel) &
    df_original['Absente'].between(absente_range[0], absente_range[1])
)

if varsta_opt == "15-16":
    mask &= df_original['Varsta'].between(15, 16)
elif varsta_opt == "17-18":
    mask &= df_original['Varsta'].between(17, 18)
elif varsta_opt == "19+":
    mask &= df_original['Varsta'] >= 19

df_filtrat = df.loc[mask]

if len(df_filtrat) == 0:
    st.warning("Nu exista rezultate.")
    st.stop()

# ══════════════════════════════════════════════════════════════════
# TABEL REZULTATE
# df[coloane].head(nr) → primele nr rânduri din coloanele selectate
# ══════════════════════════════════════════════════════════════════
st.markdown("### Tabel rezultate filtrate")

nr = st.slider("Cate randuri afisam?", 1, len(df_filtrat), min(10, len(df_filtrat)))

coloane = st.multiselect("Ce coloane afisam?", df.columns, default=df.columns[:6])

st.caption(f"Afisare {nr} din {len(df_filtrat)} rezultate")
st.dataframe(df_filtrat[coloane].head(nr), use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# COMPARATIE A vs B
# df[df[criteriu] == valoare] → filtrare pe o valoare exactă
# .mean() → media grupului selectat
# ══════════════════════════════════════════════════════════════════
st.markdown("### Comparatie A vs B")

criteriu = st.radio(
    "Alege criteriul de comparatie:",
    ["Scoala", "Sex", "Mediu", "Meditatii_Private", "Internet", "Ajutor_Familie"],
    horizontal=True,
    key="criteriu_comp"
)

valori = list(df_original[criteriu].unique())

colA, colB = st.columns(2)

with colA:
    st.markdown("#### Grup A")
    opt_A = st.selectbox("Valoare A", valori, key="A")
    idx_A = df_original[df_original[criteriu] == opt_A].index
    df_A = df.loc[idx_A]
    st.metric("Nota medie A", f"{df_A['Nota_Finala'].mean():.2f}")
    st.metric("Absente medii A", f"{df_A['Absente'].mean():.2f}")
    nr_A = st.slider("Randuri A", 1, len(df_A), min(10, len(df_A)), key="nrA")
    coloane_A = st.multiselect("Coloane A", df.columns, default=df.columns[:5], key="colA")
    st.dataframe(df_A[coloane_A].head(nr_A), use_container_width=True)

with colB:
    st.markdown("#### Grup B")
    opt_B = st.selectbox("Valoare B", valori, key="B")
    idx_B = df_original[df_original[criteriu] == opt_B].index
    df_B = df.loc[idx_B]
    st.metric("Nota medie B", f"{df_B['Nota_Finala'].mean():.2f}")
    st.metric("Absente medii B", f"{df_B['Absente'].mean():.2f}")
    nr_B = st.slider("Randuri B", 1, len(df_B), min(10, len(df_B)), key="nrB")
    coloane_B = st.multiselect("Coloane B", df.columns, default=df.columns[:5], key="colB")
    st.dataframe(df_B[coloane_B].head(nr_B), use_container_width=True)

# ── Interpretare automată ─────────────────────────────────────────
st.markdown("### Interpretare rezultate")

diff_nota    = df_A['Nota_Finala'].mean() - df_B['Nota_Finala'].mean()
diff_absente = df_A['Absente'].mean() - df_B['Absente'].mean()

if diff_nota > 0:
    st.success(f"Grupul A are o nota medie mai mare cu {diff_nota:.2f} puncte.")
else:
    st.warning(f"Grupul B are o nota medie mai mare cu {abs(diff_nota):.2f} puncte.")

if diff_absente < 0:
    st.success(f"Grupul A are mai putine absente in medie cu {abs(diff_absente):.2f}.")
else:
    st.warning(f"Grupul B are mai putine absente in medie cu {abs(diff_absente):.2f}.")
