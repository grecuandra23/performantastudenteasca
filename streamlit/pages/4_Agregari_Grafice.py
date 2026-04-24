import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Agregări & Grafice", page_icon="🎓", layout="wide")

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
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.title("Proiect **Analiza performantelor scolare**")
st.sidebar.markdown("**Grecu Andra-Maria & Grigore-Georgescu Matei**")
st.sidebar.markdown("---")

st.markdown("<h1 style='text-align:center;'>Agregări & Grafice</h1>", unsafe_allow_html=True)
st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)
st.markdown("---")

if 'df' not in st.session_state:
    st.warning("Incarca mai intai fisierul CSV.")
    st.stop()

df_original = st.session_state['df']
df_procesat = st.session_state.get('df_procesat', None)

mod = st.selectbox("Mod vizualizare:", ["Date originale", "Date preprocesate"])
if mod == "Date preprocesate":
    if df_procesat is not None:
        df = df_procesat
        st.success("Afișezi date preprocesate.")
    else:
        st.warning("Nu există date preprocesate. Mergi mai întâi la pagina de Preprocesare.")
        st.stop()
else:
    df = df_original
    st.info("Afișezi date originale.")

prag_trecere = 5 if df['Nota_Finala'].max() <= 10 else 10

cols_numerice = [c for c in ['Varsta', 'Ore_Studiu', 'Materii_Picate', 'Timp_Liber',
                              'Iesiri', 'Alcool_Saptamana', 'Alcool_Weekend',
                              'Absente', 'Nota_T1', 'Nota_T2', 'Nota_Finala'] if c in df.columns]

cols_grupare = [c for c in ['Sex', 'Mediu', 'Scoala', 'Meditatii_Private',
                             'Meditatii_Scoala', 'Internet', 'Ajutor_Familie'] if c in df.columns]

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 1 — VARIABILĂ VS NOTĂ FINALĂ
# px.scatter → scatter plot interactiv cu hover_data
# groupby().mean() → medie per categorie pentru bar chart
# add_hline() → linie orizontală de referință
# ══════════════════════════════════════════════════════════════════
st.header("1 — Variabilă vs Notă finală")

col_stanga1, col_dreapta1 = st.columns(2)

with col_stanga1:
    col_x_scatter = st.selectbox("Variabilă numerică:", cols_numerice, key="scatter_x")

    fig_scatter = px.scatter(
        df, x=col_x_scatter, y='Nota_Finala',
        hover_data=['Absente', 'Nota_T1', 'Nota_T2'],
        title=f"{col_x_scatter} vs Notă finală",
        color_discrete_sequence=["#660000"],
        opacity=0.6
    )
    fig_scatter.add_hline(y=prag_trecere, line_dash="dash", line_color="#aaa", annotation_text="Nota de trecere")
    fig_scatter.update_layout(title_x=0.5, height=450, plot_bgcolor="#FAF8F5", paper_bgcolor="#FAF8F5")
    st.plotly_chart(fig_scatter, use_container_width=True)

    with st.expander("Ce arată acest grafic?"):
        st.markdown(f"""
        Fiecare **punct reprezintă un elev**. Pe axa X este **{col_x_scatter}**, pe axa Y **Nota finală**.
        Hover pe un punct pentru a vedea detaliile elevului.
        """)

with col_dreapta1:
    col_x_bar = st.selectbox("Variabilă categorică:", cols_grupare, key="bar_x")

    # groupby + reset_index() → DataFrame cu mediile per categorie
    tabel_bar = df.groupby(col_x_bar)['Nota_Finala'].mean().round(2).reset_index()
    fig_bar = px.bar(
        tabel_bar, x=col_x_bar, y='Nota_Finala',
        color=col_x_bar, text='Nota_Finala',
        title=f"Medie Notă finală per {col_x_bar}",
        color_discrete_sequence=["#660000", "#cc4444", "#ff9999", "#994444"]
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.add_hline(y=prag_trecere, line_dash="dash", line_color="#aaa", annotation_text="Nota de trecere")
    fig_bar.update_layout(title_x=0.5, height=450, plot_bgcolor="#FAF8F5", paper_bgcolor="#FAF8F5", showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander("Ce arată acest grafic?"):
        st.markdown(f"""
        Graficul arată **media notei finale** pentru fiecare categorie din **{col_x_bar}**.
        Linia punctată marchează **nota de trecere (10)**.
        """)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 2 — HISTOGRAMĂ
# px.histogram cu color → suprapune distribuțiile per grup (barmode="overlay")
# add_vline() → linie verticală de referință
# ══════════════════════════════════════════════════════════════════
st.header("2 — Distribuția valorilor")

c1, c2 = st.columns(2)
with c1:
    col_hist = st.selectbox("Coloană:", cols_numerice, key="hist_col")
with c2:
    col_grup_hist = st.selectbox("Separă pe:", ['Niciunul'] + cols_grupare, key="hist_grup")

fig_hist = px.histogram(
    df,
    x=col_hist,
    color=None if col_grup_hist == 'Niciunul' else col_grup_hist,
    nbins=25,
    barmode="overlay",
    opacity=0.8,
    title=f"Distribuția {col_hist}",
    color_discrete_sequence=["#660000", "#cc4444", "#ff9999", "#994444"],
    labels={col_hist: col_hist, "count": "Nr. elevi"}
)

if col_hist in ['Nota_Finala', 'Nota_T1', 'Nota_T2']:
    fig_hist.add_vline(x=prag_trecere, line_dash="dash", line_color="#444",
                       annotation_text="Nota de trecere", annotation_position="top right")

fig_hist.update_layout(title_x=0.5, height=420, plot_bgcolor="#FAF8F5", paper_bgcolor="#FAF8F5")
st.plotly_chart(fig_hist, use_container_width=True)

with st.expander("Ce arată acest grafic?"):
    st.markdown(f"""
    Histograma arată **câți elevi** au obținut valori într-un anumit interval pentru **{col_hist}**.
    Barele mai înalte = mai mulți elevi cu acea valoare.
    {"Linia punctată marchează **nota de trecere (10)** — barele din stânga reprezintă elevii respinși." if col_hist in ['Nota_Finala', 'Nota_T1', 'Nota_T2'] else ""}
    {"Culorile diferite reprezintă grupurile după **" + col_grup_hist + "**." if col_grup_hist != 'Niciunul' else ""}
    """)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# SECȚIUNILE 4 & 5 — DONUT + EVOLUȚIE NOTE
# apply(lambda) → clasificare promovat/respins per rând
# value_counts() → frecvența fiecărei categorii
# melt() → transformă DataFrame wide → long pentru px.line
# groupby()[[]].mean() → medii pe mai multe coloane simultan
# ══════════════════════════════════════════════════════════════════
st.header("4 & 5 — Promovabilitate & Evoluție note")

c_ctrl1, c_ctrl2 = st.columns(2)
with c_ctrl1:
    col_grup_donut = st.selectbox("Promovabilitate — afișează per:", ['Total'] + cols_grupare, key="donut_grup")
with c_ctrl2:
    col_grup_linie = st.selectbox("Evoluție — grupează după:", cols_grupare, key="linie_grup")

col_stanga, col_dreapta = st.columns(2)

with col_stanga:
    if col_grup_donut == 'Total':
        df_donut = df.copy()
        df_donut['Status'] = df_donut['Nota_Finala'].apply(lambda x: 'Promovat' if x >= 10 or x >= 5 else 'Respins')
        counts = df_donut['Status'].value_counts().reset_index()
        counts.columns = ['Status', 'Count']
        fig_donut = px.pie(counts, names='Status', values='Count', hole=0.55,
                           title="Promovabilitate — Total",
                           color_discrete_sequence=["#660000", "#e8d5d5"])
    else:
        df_donut = df.copy()
        df_donut['Status'] = df_donut['Nota_Finala'].apply(lambda x: 'Promovat' if x >= 10 or x >= 5 else 'Respins')
        counts = df_donut.groupby([col_grup_donut, 'Status']).size().reset_index(name='Count')
        fig_donut = px.sunburst(counts, path=[col_grup_donut, 'Status'], values='Count',
                                title=f"Promovabilitate per {col_grup_donut}",
                                color_discrete_sequence=["#660000", "#cc4444", "#e8d5d5", "#ff9999"])

    fig_donut.update_layout(title_x=0.5, height=420, paper_bgcolor="#FAF8F5")
    st.plotly_chart(fig_donut, use_container_width=True)

    with st.expander("Ce arată acest grafic?"):
        st.markdown(f"""
        Graficul arată **proporția elevilor promovați vs respinși** (nota de trecere = 10).
        {"Fiecare felie reprezintă un grup, iar interiorul arată statusul promovării în cadrul acelui grup." if col_grup_donut != 'Total' else "Fiecare felie reprezintă procentul din totalul elevilor."}
        """)

with col_dreapta:
    # melt() transformă coloanele Nota_T1, Nota_T2, Nota_Finala într-o coloană "Trimestru"
    evolutie = df.groupby(col_grup_linie)[['Nota_T1', 'Nota_T2', 'Nota_Finala']].mean().round(2).reset_index()
    evolutie_long = evolutie.melt(id_vars=col_grup_linie, var_name="Trimestru", value_name="Medie")

    fig_line = px.line(
        evolutie_long, x="Trimestru", y="Medie", color=col_grup_linie,
        markers=True, title=f"Evoluție medie note per {col_grup_linie}",
        color_discrete_sequence=["#660000", "#cc4444", "#ff9999", "#994444"],
        text="Medie"
    )
    fig_line.update_traces(textposition="top center")
    fig_line.add_hline(y=prag_trecere, line_dash="dash", line_color="#aaa", annotation_text="Nota de trecere")
    fig_line.update_layout(title_x=0.5, height=420, plot_bgcolor="#FAF8F5", paper_bgcolor="#FAF8F5")
    st.plotly_chart(fig_line, use_container_width=True)

    with st.expander("Ce arată acest grafic?"):
        st.markdown(f"""
        Graficul urmărește **evoluția mediei notelor** de la Trimestrul 1 → Trimestrul 2 → Nota Finală pentru fiecare grup din **{col_grup_linie}**.
        O linie ascendentă indică îmbunătățire în timp, una descendentă indică o înrăutățire a performanței.
        Valorile sunt afișate direct pe puncte. Linia punctată marchează nota de trecere (10).
        """)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 6 — HEATMAP CORELAȚII
# df.corr() → matrice de corelație Pearson între toate coloanele numerice
# sns.heatmap cu annot=True → afișează valorile în celule
# ══════════════════════════════════════════════════════════════════
st.header("6 — Heatmap corelații")

corr_matrix = df[cols_numerice].corr().round(2)

fig6, ax6 = plt.subplots(figsize=(10, 7))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='Reds',
            ax=ax6, linewidths=0.5, linecolor='#FAF8F5', annot_kws={"size": 9})
ax6.set_title("Matricea de corelație", fontsize=13, fontweight='bold')
fig6.patch.set_facecolor('#FAF8F5')
st.pyplot(fig6)
plt.close(fig6)

with st.expander("Ce arată acest grafic?"):
    st.markdown("""
    Heatmap-ul arată **coeficientul de corelație Pearson** între toate variabilele numerice.
    Valorile sunt între **-1 și 1**:
    - **aproape de 1** → relație pozitivă puternică (când una crește, crește și cealaltă)
    - **aproape de -1** → relație negativă puternică (când una crește, cealaltă scade)
    - **aproape de 0** → nu există relație între ele

    Exemple relevante: `Ore_Studiu` ↔ `Nota_Finala`, `Absente` ↔ `Nota_Finala`, `Nota_T1` ↔ `Nota_T2`.
    """)
