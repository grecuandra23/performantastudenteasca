import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import linkage, fcluster
import plotly.figure_factory as ff
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, silhouette_score)

st.set_page_config(page_title="Scikit-Learn ML", page_icon="🎓", layout="wide")

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

st.sidebar.title("Proiect **Analiza performantelor scolare**")
st.sidebar.markdown("**Grecu Andra-Maria & Grigore-Georgescu Matei**")
st.sidebar.markdown("---")

st.markdown("<h1 style='text-align:center;'>Scikit-Learn ML</h1>", unsafe_allow_html=True)
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
                              'Absente', 'Nota_T1', 'Nota_T2', 'Nota_Finala'] if c in df.columns]

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 1 — CLUSTERING IERARHIC
# ══════════════════════════════════════════════════════════════════
st.header("1 — Clusterizare")
st.subheader("1a — Clustering ierarhic (dendogramă)")

c1, c2, c3 = st.columns(3)
with c1:
    cols_cluster = st.multiselect(
        "Variabile pentru clustering:",
        cols_numerice,
        default=['Ore_Studiu', 'Absente', 'Nota_Finala']
    )
with c2:
    metoda_link = st.selectbox("Metodă linkage:", ["ward", "complete", "average", "single"])
    n_clusters = st.slider("Număr clustere (pentru statistici):", 2, 6, 3)
with c3:
    max_sample = st.slider("Număr maxim de puncte afișate:", 20, 100, 50, step=10)

if len(cols_cluster) < 2:
    st.warning("Selectează cel puțin 2 variabile pentru clustering.")
else:
    df_cluster = df[cols_cluster].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_cluster)

    # Dendogramă pe un eșantion pentru lizibilitate
    sample_idx = df_cluster.sample(min(max_sample, len(df_cluster)), random_state=42).index
    X_sample = scaler.transform(df_cluster.loc[sample_idx])

    fig_dendo = ff.create_dendrogram(
        X_sample,
        linkagefun=lambda x: linkage(x, method=metoda_link),
        colorscale=["#330000", "#660000", "#994444", "#cc4444", "#ff9999", "#ffcccc"]
    )
    fig_dendo.update_layout(
        title=f"Dendogramă — linkage: {metoda_link}",
        title_x=0.5,
        height=500,
        xaxis_title="Observații",
        yaxis_title="Distanță",
        plot_bgcolor="#FAF8F5",
        paper_bgcolor="#FAF8F5"
    )
    st.plotly_chart(fig_dendo, use_container_width=True)

    with st.expander("Cum se citește dendograma?"):
        st.markdown("""
        - **Axa Y** — distanța la care se unesc două grupuri. Cu cât mai sus se unesc, cu atât sunt mai diferite.
        - **Tăierea orizontală** — dacă trasezi o linie orizontală, numărul de ramuri tăiate = numărul de clustere.
        - **Metodă linkage:**
          - `ward` — minimizează varianța intra-cluster (cel mai compact)
          - `complete` — distanța între cele mai îndepărtate puncte din două clustere
          - `average` — media distanțelor
          - `single` — distanța între cele mai apropiate puncte (tendință de lanț)
        """)

    # Asignare clustere și statistici
    Z = linkage(X_scaled, method=metoda_link)
    labels = fcluster(Z, t=n_clusters, criterion='maxclust')

    df_viz = df.loc[df_cluster.index].copy()
    df_viz['Cluster'] = labels.astype(str)

    sil_score = silhouette_score(X_scaled, labels)

    st.subheader("Metrici clustering")
    mc1, mc2 = st.columns(2)
    mc1.metric("Număr clustere", n_clusters)
    mc2.metric("Silhouette Score", f"{sil_score:.3f}")

    st.subheader("Statistici per cluster")
    stats_cluster = df_viz.groupby('Cluster')[cols_cluster].mean().round(2)
    st.dataframe(stats_cluster, use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 1b — K-MEANS
# ══════════════════════════════════════════════════════════════════
st.subheader("1b — K-Means")

if len(cols_cluster) < 2:
    st.warning("Selectează cel puțin 2 variabile pentru clustering (din secțiunea 1a).")
else:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels_km = kmeans.fit_predict(X_scaled)

    df_km = df.loc[df_cluster.index].copy()
    df_km['Cluster'] = labels_km.astype(int)

    sil_km = silhouette_score(X_scaled, labels_km)

    km1, km2, km3 = st.columns(3)
    km1.metric("Număr clustere", n_clusters)
    km2.metric("Silhouette Score", f"{sil_km:.3f}")
    km3.metric("Inerție", f"{kmeans.inertia_:.1f}")

    with st.expander("Cum se interpretează metricile?"):
        st.markdown("""
        - **Silhouette Score** — între -1 și 1. Aproape de **1** = clustere bine separate.
        - **Inerție** — suma distanțelor față de centroid. Mai mică = clustere mai compacte. Scade când crești k.
        """)

    col_x_viz = st.selectbox("Axa X vizualizare:", cols_numerice,
                              index=cols_numerice.index('Ore_Studiu') if 'Ore_Studiu' in cols_numerice else 0)
    col_y_viz = st.selectbox("Axa Y vizualizare:", cols_numerice,
                              index=cols_numerice.index('Nota_Finala') if 'Nota_Finala' in cols_numerice else 1)

    df_km['Cluster'] = df_km['Cluster'].astype(str)

    fig_km = px.scatter(
        df_km, x=col_x_viz, y=col_y_viz,
        color='Cluster',
        title=f"Clustere K-Means — {col_x_viz} vs {col_y_viz}",
        color_discrete_sequence=["#1f77b4", "#e6550d", "#2ca02c", "#9467bd", "#d62728", "#8c564b"],
        opacity=0.8
    )
    fig_km.update_layout(title_x=0.5, height=450, plot_bgcolor="#FAF8F5", paper_bgcolor="#FAF8F5")
    st.plotly_chart(fig_km, use_container_width=True)

    st.subheader("Statistici per cluster")
    st.dataframe(df_km.groupby('Cluster')[cols_cluster].mean().round(2), use_container_width=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════
# SECȚIUNEA 2 — REGRESIE LOGISTICĂ
# ══════════════════════════════════════════════════════════════════
st.header("2 — Regresie Logistică — Predicție promovare")

st.markdown("Modelul prezice dacă un elev este **promovat (≥10)** sau **respins (<10)** pe baza variabilelor selectate.")

cols_features = st.multiselect(
    "Variabile predictor:",
    cols_numerice,
    default=[c for c in ['Ore_Studiu', 'Absente', 'Nota_T1', 'Nota_T2'] if c in cols_numerice]
)

test_size = st.slider("Proporție date de test:", 0.1, 0.4, 0.2, step=0.05)

if len(cols_features) < 1:
    st.warning("Selectează cel puțin o variabilă predictor.")
else:
    df_model = df[cols_features + ['Nota_Finala']].dropna().copy()
    df_model['Promovat'] = (df_model['Nota_Finala'] >= 10).astype(int)

    X = df_model[cols_features]
    y = df_model['Promovat']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    scaler2 = StandardScaler()
    X_train_sc = scaler2.fit_transform(X_train)
    X_test_sc = scaler2.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_sc, y_train)
    y_pred = model.predict(X_test_sc)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    # Metrici
    st.subheader("Metrici model")
    c1, c2, c3 = st.columns(3)
    c1.metric("Precizie", f"{prec:.3f}")
    c2.metric("Sensibilitate", f"{rec:.3f}")
    c3.metric("Scor F1", f"{f1:.3f}")

    with st.expander("Cum se interpretează metricile?"):
        st.markdown("""
        - **Precizie** — din toți elevii prezisi ca promovați, câți chiar sunt promovați.
        - **Sensibilitate** — din toți elevii promovați, câți au fost detectați corect de model.
        - **Scor F1** — media harmonică între Precizie și Sensibilitate. Util când clasele sunt dezechilibrate.
        """)

    # Confusion Matrix
    st.subheader("Matrice de confuzie")
    cm = confusion_matrix(y_test, y_pred)

    tn, fp, fn, tp = cm.ravel()
    acc_respins  = tn / (tn + fp) if (tn + fp) > 0 else 0
    acc_promovat = tp / (tp + fn) if (tp + fn) > 0 else 0

    # Matrice extinsă 3x3: contine si acuratetea per grup si totala
    z = [
        [tn,  fp,  acc_respins],
        [fn,  tp,  acc_promovat],
        [None, None, acc],
    ]
    text = [
        [str(tn),               str(fp),               f"{acc_respins:.1%}"],
        [str(fn),               str(tp),               f"{acc_promovat:.1%}"],
        ["",                    "",                    f"{acc:.1%}"],
    ]

    fig_cm = go.Figure(go.Heatmap(
        z=z,
        text=text,
        texttemplate="%{text}",
        textfont={"size": 16},
        colorscale="Blues",
        showscale=False,
        xgap=3, ygap=3,
        x=["Respins", "Promovat", "Acuratețe"],
        y=["Respins", "Promovat", "Acuratețe totală"],
    ))
    fig_cm.update_layout(
        height=380,
        paper_bgcolor="#FAF8F5",
        plot_bgcolor="#FAF8F5",
        xaxis=dict(title="Prezis", side="top"),
        yaxis=dict(title="Real", autorange="reversed")
    )
    st.plotly_chart(fig_cm, use_container_width=True)

    # Coeficienți
    st.subheader("Importanța variabilelor")
    coef_df = pd.DataFrame({
        'Variabilă': cols_features,
        'Coeficient': model.coef_[0].round(4)
    }).sort_values('Coeficient', ascending=False)

    fig_coef = px.bar(
        coef_df, x='Variabilă', y='Coeficient',
        color='Coeficient',
        color_continuous_scale='Reds',
        title="Coeficienții regresiei logistice"
    )
    fig_coef.update_layout(title_x=0.5, height=380, plot_bgcolor="#FAF8F5", paper_bgcolor="#FAF8F5")
    st.plotly_chart(fig_coef, use_container_width=True)

    with st.expander("Cum se interpretează coeficienții?"):
        st.markdown("""
        Coeficienții pozitivi → variabila **crește** șansa de promovare.
        Coeficienții negativi → variabila **scade** șansa de promovare.
        Cu cât valoarea absolută e mai mare, cu atât influența e mai puternică.
        """)

