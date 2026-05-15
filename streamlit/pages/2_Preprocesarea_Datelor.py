import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Preprocesarea Datelor", page_icon="🎓", layout="wide")

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

span[data-baseweb="tag"] {
    background-color: #660000 !important;
    color: white !important;
}

.accent-bar {
    width: 40px;
    height: 3px;
    background: #660000;
    margin: 10px auto 20px auto;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.title("Proiect **Analiza performantelor scolare**")
st.sidebar.markdown("**Grecu Andra-Maria & Grigore-Georgescu Matei**")
st.sidebar.markdown("---")

st.markdown("<h1 style='text-align:center;'>Preprocesare Interactivă</h1>", unsafe_allow_html=True)
st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)
st.markdown("---")

if 'df' not in st.session_state:
    st.warning("Incarca mai intai fisierul CSV.")
    st.stop()

df_original = st.session_state['df']

# ══════════════════════════════════════════════════════════════════
# PASUL 1 — TRATAREA VALORILOR LIPSĂ
# df.isnull().sum() detectează NaN-uri per coloană
# fillna() / SimpleImputer / KNNImputer completează valorile lipsă
# ══════════════════════════════════════════════════════════════════
st.header("Pasul 1 — Tratarea valorilor lipsă")

col1, col2 = st.columns(2)

with col1:
    # isnull().sum() → număr NaN-uri; reset_index() transformă seria în DataFrame
    lipsa = df_original.isnull().sum()
    lipsa = lipsa[lipsa > 0].reset_index()
    lipsa.columns = ["Coloană", "Valori lipsă"]
    lipsa["Procent (%)"] = (lipsa["Valori lipsă"] / len(df_original) * 100).round(1)

    if len(lipsa) == 0:
        st.success("Nu există valori lipsă 🎉")
    else:
        st.dataframe(lipsa, use_container_width=True, hide_index=True)

with col2:
    # iterrows() parcurge DataFrame-ul rând cu rând → (index, Series)
    for _, row in lipsa.iterrows():
        st.markdown(f"**{row['Coloană']}**")
        st.progress(row["Procent (%)"] / 100)

st.subheader("Alege metoda pentru fiecare coloană")

df_pas1 = df_original.copy()

for col in lipsa["Coloană"]:

    if df_original[col].dtype == "object":
        opt = ["Mod", "Necunoscut", "Lasă lipsă"]
        default_idx = 0
    else:
        opt = [
            "Median",
            "Mean",
            "KNN Imputer",
            "0",
            "Lasă lipsă"
        ]
        default_idx = opt.index("0")

    metoda = st.selectbox(col, opt, index=default_idx, key=f"imp_{col}")

    if metoda == "Mod":
        # mode()[0] → cea mai frecventă valoare; fillna() completează NaN-urile
        df_pas1[col] = df_pas1[col].fillna(df_pas1[col].mode()[0])

    elif metoda == "Necunoscut":
        df_pas1[col] = df_pas1[col].fillna("Necunoscut")

    elif metoda == "Median":
        # fit_transform pe df[[col]] (2D) → înlocuiește NaN cu mediana coloanei
        imp = SimpleImputer(strategy="median")
        df_pas1[col] = imp.fit_transform(df_pas1[[col]])

    elif metoda == "Mean":
        imp = SimpleImputer(strategy="mean")
        df_pas1[col] = imp.fit_transform(df_pas1[[col]])

    elif metoda == "KNN Imputer":
        # KNNImputer lucrează pe toate coloanele numerice simultan
        # estimează valoarea lipsă din cei mai apropiați 5 vecini
        numeric_cols = df_pas1.select_dtypes(include='number').columns
        knn = KNNImputer(n_neighbors=5)
        df_pas1[numeric_cols] = knn.fit_transform(df_pas1[numeric_cols])

    elif metoda == "0":
        df_pas1[col] = df_pas1[col].fillna(0)

# ══════════════════════════════════════════════════════════════════
# PASUL 2 — TRATAREA OUTLIERILOR
# Detectare prin metoda IQR: outlier dacă < Q1 - 1.5*IQR sau > Q3 + 1.5*IQR
# Eliminare: boolean indexing cu df[conditie]
# Capping: clip() trunchiază valorile la percentilele 1% și 99%
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
st.header("Pasul 2 — Tratarea outlierilor")

cols_out = [
    "Varsta", "Ore_Studiu", "Materii_Picate", "Timp_Liber",
    "Iesiri", "Alcool_Saptamana", "Alcool_Weekend",
    "Absente", "Nota_T1", "Nota_T2", "Nota_Finala"
]

_cols_pastreaza = {"Ore_Studiu", "Materii_Picate", "Iesiri", "Nota_T1", "Nota_Finala"}
for _col in cols_out:
    if f"out_{_col}" not in st.session_state:
        if _col == "Varsta":
            st.session_state[f"out_{_col}"] = "Elimină rândurile outlieri"
        elif _col in _cols_pastreaza:
            st.session_state[f"out_{_col}"] = "Păstrează toți outlierii"
        else:
            st.session_state[f"out_{_col}"] = "Capping la percentile"

def aplica_metoda_outlier(df, col, metoda):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    if metoda == "Elimină rândurile outlieri":
        # boolean indexing: păstrează doar rândurile în intervalul [Q1-1.5*IQR, Q3+1.5*IQR]
        return df[(df[col] >= q1 - 1.5 * iqr) & (df[col] <= q3 + 1.5 * iqr)]
    elif metoda == "Capping la percentile":
        df = df.copy()
        # clip() limitează valorile între percentila 1% și 99%
        df[col] = df[col].clip(df[col].quantile(0.01), df[col].quantile(0.99))
        return df
    return df

for col in cols_out:
    if col not in df_pas1.columns:
        continue

    Q1 = df_pas1[col].quantile(0.25)
    Q3 = df_pas1[col].quantile(0.75)
    IQR = Q3 - Q1
    n_out = int(((df_pas1[col] < Q1 - 1.5 * IQR) | (df_pas1[col] > Q3 + 1.5 * IQR)).sum())
    metoda_curenta = st.session_state.get(f"out_{col}", "Păstrează toți outlierii")

    label = f"{col} — {n_out} outlieri  |  {metoda_curenta}"

    with st.expander(label):
        col1, col2 = st.columns([2, 1])

        with col1:
            fig = px.box(
                df_pas1,
                x="Mediu",
                y=col,
                color="Mediu",
                title=f"Boxplot {col}"
            )
            fig.update_layout(
                height=500,
                title_x=0.5,
                title_font_size=18,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.metric("Q1 (25%)", f"{Q1:.2f}")
            st.metric("Q3 (75%)", f"{Q3:.2f}")
            st.metric("IQR", f"{IQR:.2f}")
            st.metric("Outlieri detectați", n_out)

            st.selectbox(
                "Metodă:",
                ["Păstrează toți outlierii", "Elimină rândurile outlieri", "Capping la percentile"],
                index=2,
                key=f"out_{col}"
            )

# Aplică metodele alese și construiește df_pas2
# df.loc[conditie] folosit indirect prin boolean indexing în aplica_metoda_outlier
df_pas2 = df_pas1.copy()
for col in cols_out:
    if col not in df_pas2.columns:
        continue
    df_pas2 = aplica_metoda_outlier(
        df_pas2, col,
        st.session_state.get(f"out_{col}", "Păstrează toți outlierii")
    )

col1, col2, col3 = st.columns(3)
col1.metric("Rânduri originale", len(df_pas1))
col2.metric("Rânduri după tratare outlieri", len(df_pas2))
col3.metric("Rânduri eliminate", len(df_pas1) - len(df_pas2))

# ══════════════════════════════════════════════════════════════════
# PASUL 3 — ENCODING VARIABILE CATEGORIALE
# Label Encoding: LabelEncoder → mapare string → int (alfabetic)
# One-Hot Encoding: pd.get_dummies() → coloană nouă per categorie (0/1)
#   pd.concat([df, dummies], axis=1) adaugă coloanele noi
#   df.drop(columns=[col]) elimină coloana originală
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
st.header("Pasul 3 — Encoding variabile categoriale")

df_pas3 = df_pas2.copy()

# select_dtypes(include='object') → selectează doar coloanele de tip string
categorical_cols = list(df_pas3.select_dtypes(include='object').columns)

for _col in categorical_cols:
    if f"enc_{_col}" not in st.session_state:
        st.session_state[f"enc_{_col}"] = "One-Hot Encoding" if _col == "Sex" else "Label Encoding"

cols_per_row = 3
for i in range(0, len(categorical_cols), cols_per_row):
    grup = categorical_cols[i:i + cols_per_row]
    row_cols = st.columns(cols_per_row)
    for j, col in enumerate(grup):
        with row_cols[j]:
            default_enc_idx = 1 if col == "Sex" else 0
            st.selectbox(
                f"{col}",
                ["Label Encoding", "One-Hot Encoding", "Nu modifica"],
                index=default_enc_idx,
                key=f"enc_{col}"
            )

for col in categorical_cols:
    metoda = st.session_state.get(f"enc_{col}", "Nu modifica")

    if metoda == "Label Encoding":
        # fit_transform: învață categoriile și le transformă în întregi
        le = LabelEncoder()
        df_pas3[col] = le.fit_transform(df_pas3[col])

    elif metoda == "One-Hot Encoding":
        # get_dummies: creează câte o coloană binară per valoare unică
        # concat pe axis=1 → alătură coloanele noi la DataFrame
        dummies = pd.get_dummies(df_pas3[col], prefix=col)
        df_pas3 = pd.concat([df_pas3, dummies], axis=1)
        df_pas3 = df_pas3.drop(columns=[col])

# Scala note (Nota_T1, Nota_T2, Nota_Finala)
cols_note = [c for c in ["Nota_T1", "Nota_T2", "Nota_Finala"] if c in df_pas3.columns]
if cols_note:
    if "scala_note" not in st.session_state:
        st.session_state["scala_note"] = "Sistem românesc (1–10)"
    st.markdown("**Scale note**")
    scala_note = st.selectbox(
        "Nota_T1 / Nota_T2 / Nota_Finala",
        ["Sistem portughez (0–20)", "Sistem românesc (1–10)"],
        key="scala_note"
    )
    if scala_note == "Sistem românesc (1–10)":
        # nota_ro = nota / 2, clip(lower=1) asigură minimul 1
        for col in cols_note:
            df_pas3[col] = (df_pas3[col] / 2).clip(lower=1).round(2)

# ══════════════════════════════════════════════════════════════════
# REZULTAT FINAL
# df.head(nr) → primele nr rânduri din DataFrame
# ══════════════════════════════════════════════════════════════════
st.markdown("---")
st.header("Rezultat final")

col1, col2 = st.columns(2)
col1.metric("Rânduri finale", len(df_pas3))
col2.metric("Coloane finale", len(df_pas3.columns))

nr = st.slider(
    "Cate randuri afisam?",
    1,
    len(df_pas3),
    min(10, len(df_pas3))
)

st.caption(f"Afisare {nr} din {len(df_pas3)} rezultate")

st.dataframe(
    df_pas3.head(nr),
    use_container_width=True
)

st.markdown("---")
st.header("Sumar — alegerile tale de preprocesare")

st.markdown("Acestea sunt deciziile aplicate asupra datelor.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Pasul 1 — Valori lipsă**")

    if len(lipsa) == 0:
        st.markdown("✔️ Nu au existat valori lipsă")
    else:
        for c in lipsa["Coloană"]:
            m = st.session_state.get(f"imp_{c}", "N/A")
            st.markdown(f"- `{c}` → **{m}**")

with col2:
    st.markdown("**Pasul 2 — Outlieri**")

    for col in cols_out:
        metoda_col = st.session_state.get(f"out_{col}", "Păstrează toți outlierii")
        st.markdown(f"- `{col}` → **{metoda_col}**")
    st.markdown(f"- Rânduri rămase: **{len(df_pas2)}** din {len(df_original)}")

with col3:
    st.markdown("**Pasul 3 — Encoding**")

    categorical_cols = df_pas2.select_dtypes(include='object').columns

    if len(categorical_cols) == 0:
        st.markdown("✔️ Nu există coloane categoriale")
    else:
        for c in categorical_cols:
            m = st.session_state.get(f"enc_{c}", "N/A")
            st.markdown(f"- `{c}` → **{m}**")

    scala = st.session_state.get("scala_note", "Sistem portughez (0–20)")
    st.markdown(f"- Note → **{scala}**")
    st.markdown(f"- Coloane finale: **{len(df_pas3.columns)}**")

st.markdown("<br>", unsafe_allow_html=True)

# Salvează df_pas3 în session_state pentru a fi disponibil în paginile următoare
st.session_state["df_procesat"] = df_pas3

st.success("Preprocesare completă!")
