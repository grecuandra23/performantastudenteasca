import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_white
from statsmodels.stats.stattools import jarque_bera

st.set_page_config(page_title="Stats Model ML", page_icon="🎓", layout="wide")

# ── Stiluri CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
html, body, .stApp { font-family: 'Montserrat', sans-serif; background-color: #FAF8F5; font-size: 18px; }
p { color: #444; font-size: 1.05rem; line-height: 1.6; }
h1 { font-size: 2.8rem; font-weight: 700; color: #660000; }
h2 { font-size: 2rem; font-weight: 600; color: #660000; }
h3 { font-size: 1.5rem; font-weight: 600; color: #1a1a1a; }
label { color: #660000; font-weight: 500; }
div[data-testid="stMetric"] {
    background: white; border: 1px solid #e8e2dc;
    border-left: 5px solid #660000; border-radius: 10px; padding: 18px;
}
div[data-testid="stMetricValue"] { color: #660000 !important; font-weight: 700; font-size: 1.6rem; }
span[data-baseweb="tag"] { background-color: #660000 !important; color: white !important; }
.accent-bar { width: 40px; height: 3px; background: #660000; margin: 10px auto 20px auto; }
table.eviews { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
table.eviews th { background: #660000; color: white; padding: 8px 12px; text-align: center; }
table.eviews td { padding: 7px 12px; border-bottom: 1px solid #e8e2dc; text-align: right; }
table.eviews td:first-child { text-align: left; font-weight: 500; }
table.eviews tr:nth-child(even) { background: #f5f0eb; }
table.eviews .sig { color: #660000; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.title("Proiect **Analiza performantelor scolare**")
st.sidebar.markdown("**Grecu Andra-Maria & Grigore-Georgescu Matei**")
st.sidebar.markdown("---")

st.markdown("<h1 style='text-align:center;'>Statsmodels — Regresie Multiplă</h1>", unsafe_allow_html=True)
st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)
st.markdown("---")

if 'df' not in st.session_state:
    st.warning("Incarca mai intai fisierul CSV.")
    st.stop()

if st.session_state.get('df_procesat') is None:
    st.warning("Datele trebuie preprocesate înainte de a folosi această pagină. Mergi la **Preprocesarea Datelor** și finalizează preprocesarea.")
    st.stop()

df = st.session_state['df_procesat']
st.success("Date preprocesate încărcate.")

cols_numerice = [c for c in ['Varsta', 'Ore_Studiu', 'Materii_Picate', 'Timp_Liber',
                              'Iesiri', 'Alcool_Saptamana', 'Alcool_Weekend',
                              'Absente', 'Nota_T1', 'Nota_T2'] if c in df.columns]

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 1 — CONFIGURARE MODEL
# sm.add_constant() → adaugă coloana de interceptare (β₀)
# sm.OLS(y, X).fit() → estimează coeficienții prin metoda celor mai mici pătrate
# ══════════════════════════════════════════════════════════════════
st.header("1 — Configurare regresie multiplă")

st.markdown("""
**Regresia multiplă** estimează relația dintre o variabilă dependentă și mai mulți predictori.

`Y = β₀ + β₁·X₁ + β₂·X₂ + ... + βₙ·Xₙ + ε`
""")

variabila_dep = st.selectbox("Variabilă dependentă:", ['Nota_Finala', 'Nota_T2', 'Nota_T1'])
predictori_num = st.multiselect(
    "Variabile numerice:",
    cols_numerice,
    default=[c for c in ['Ore_Studiu', 'Absente', 'Nota_T1', 'Nota_T2'] if c in cols_numerice]
)

if len(predictori_num) < 1:
    st.warning("Selectează cel puțin un predictor.")
    st.stop()

df_combined = df[predictori_num + [variabila_dep]].dropna()
X_raw = df_combined[predictori_num]
y     = df_combined[variabila_dep]

# sm.add_constant → adaugă coloana "const" = 1 pentru interceptare
X = sm.add_constant(X_raw)
model = sm.OLS(y, X).fit()

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 2 — OUTPUT STIL EVIEWS
# model.params, model.bse, model.tvalues, model.pvalues → statistici coeficienți
# stele de semnificație: *** p<0.01 / ** p<0.05 / * p<0.10
# model.rsquared, model.rsquared_adj, model.fvalue, model.f_pvalue → sumar model
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
st.header("2 — Rezultate regresie")

def stele(p):
    if p < 0.01: return "***"
    if p < 0.05: return "**"
    if p < 0.10: return "*"
    return ""

# ── Metrici sumar ─────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("R²",            f"{model.rsquared:.4f}")
m2.metric("R² ajustat",    f"{model.rsquared_adj:.4f}")
m3.metric("Statistică F",  f"{model.fvalue:.2f}")
m4.metric("Prob. (F)",     f"{model.f_pvalue:.4f}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabel coeficienți ─────────────────────────────────────────────
coef_df = pd.DataFrame({
    'Coeficient':  model.params.round(4),
    't-Statistic': model.tvalues.round(4),
    'Prob.':       model.pvalues.round(4),
    'Sig.':        [stele(p) for p in model.pvalues]
})
coef_df.index.name = 'Variabilă'

st.dataframe(coef_df, use_container_width=True)
st.caption("Semnificație: *** p<0.01 | ** p<0.05 | * p<0.10")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 3 — HISTOGRAMĂ NORMALITATE REZIDUURI + TEST WHITE
# model.resid → reziduurile (y − ŷ)
# het_white → testează heteroscheasticitatea (H₀: varianță constantă)
# ══════════════════════════════════════════════════════════════════
st.header("3 — Diagnostice reziduuri")

resid = model.resid

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.subheader("Distribuția reziduurilor")
    fig_hist_r = px.histogram(
        x=resid,
        nbins=30,
        labels={"x": "Reziduuri", "y": "Frecvență"},
        color_discrete_sequence=["#660000"],
        opacity=0.8
    )
    fig_hist_r.add_vline(x=0, line_dash="dash", line_color="#aaa")
    fig_hist_r.update_layout(height=380, plot_bgcolor="#FAF8F5", paper_bgcolor="#FAF8F5")
    st.plotly_chart(fig_hist_r, use_container_width=True)

with col_r2:
    st.subheader("Testul Jarque-Bera — normalitate reziduuri")
    st.markdown("""
    **H₀:** reziduurile sunt distribuite normal

    **H₁:** reziduurile nu sunt distribuite normal
    """)

    # jarque_bera → (statistică, p-value, skewness, kurtosis)
    jb_stat, jb_pval, jb_skew, jb_kurt = jarque_bera(resid)

    j1, j2 = st.columns(2)
    j1.metric("JB Statistic", f"{jb_stat:.4f}")
    j2.metric("Prob. (JB)",   f"{jb_pval:.4f}")
    j1.metric("Skewness",     f"{jb_skew:.4f}")
    j2.metric("Kurtosis",     f"{jb_kurt:.4f}")


st.subheader("Testul White — heteroscheasticitate")
st.markdown("""
**H₀:** varianța erorilor este constantă (homoscheasticitate) &nbsp;|&nbsp;
**H₁:** varianța erorilor nu este constantă (heteroscheasticitate)
""")

lm_stat, lm_pval, f_stat, f_pval = het_white(resid, X)

w1, w2, w3, w4 = st.columns(4)
w1.metric("LM Statistic", f"{lm_stat:.4f}")
w2.metric("Prob. (LM)",   f"{lm_pval:.4f}")
w3.metric("F Statistic",  f"{f_stat:.4f}")
w4.metric("Prob. (F)",    f"{f_pval:.4f}")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 4 — VIF
# variance_inflation_factor → detectează corelații puternice între predictori
# ══════════════════════════════════════════════════════════════════
st.header("4 — Multicolinearitate (VIF)")

X_vif = X_raw.copy()
if len(X_vif.columns) >= 2:
    vif_data = pd.DataFrame({
        'Variabilă': X_vif.columns,
        'VIF': [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
    }).round(2).set_index('Variabilă')

    fig_vif = px.bar(
        vif_data.reset_index(), x='Variabilă', y='VIF',
        color='VIF',
        color_continuous_scale=['#2ca02c', '#ff7f0e', '#d62728'],
        text='VIF'
    )
    fig_vif.add_hline(y=5,  line_dash="dash", line_color="#ff7f0e", annotation_text="5")
    fig_vif.add_hline(y=10, line_dash="dash", line_color="#d62728", annotation_text="10")
    fig_vif.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_vif.update_layout(height=380, plot_bgcolor="#FAF8F5", paper_bgcolor="#FAF8F5")
    st.plotly_chart(fig_vif, use_container_width=True)
    st.dataframe(vif_data, use_container_width=True)
else:
    st.info("VIF necesită cel puțin 2 predictori.")
