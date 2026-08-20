import streamlit as st
import pandas as pd
import joblib
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Real Estate Price Prediction",
    page_icon="🏠",
    layout="wide"
)


# ============================================================
# FILE PATHS
# ============================================================

MODEL_PATH = "models/decision_tree_model.pkl"

SCRAPED_PATH = "scraper/scraped_data.csv"


# ============================================================
# LOAD DECISION TREE MODEL
# ============================================================

try:

    model = joblib.load(MODEL_PATH)

except FileNotFoundError:

    st.error("❌ Decision Tree model not found.")

    st.info(
        "Make sure this file exists:\n\n"
        "models/decision_tree_model.pkl"
    )

    st.stop()

except Exception as e:

    st.error("❌ Model could not be loaded.")

    st.error(str(e))

    st.stop()


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🏠 Real Estate Property Price Prediction")

st.write(
    "Real Estate Property Price Prediction and Pattern Mining"
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏠 Real Estate Predictor")

st.sidebar.markdown(
    """
    ### Project Modules

    🏠 Price Prediction  
    🤖 Model Comparison  
    🔵 K-Means Clustering  
    🔗 Association Rules  
    🌐 Web Scraping  

    ---

    ### Model

    **Algorithm:** Decision Tree Classifier

    **Target:** Price Category

    **Classes:**
    - Low
    - Medium
    - High
    - Premium
    """
)


# ============================================================
# TOP PROJECT SUMMARY
# ============================================================

st.header("📊 Project Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Decision Tree",
        "Best Model"
    )

with col2:

    st.metric(
        "Clusters",
        "K = 6"
    )

with col3:

    st.metric(
        "Association Rules",
        "306"
    )

with col4:

    st.metric(
        "Strong Rules",
        "255"
    )


st.divider()


# ============================================================
# PROPERTY INPUT
# ============================================================

st.header("📋 Property Details")

col1, col2 = st.columns(2)


with col1:

    bedroom = st.number_input(
        "🛏️ Number of Bedrooms",
        min_value=0,
        max_value=50,
        value=3,
        step=1
    )

    bathroom = st.number_input(
        "🛁 Number of Bathrooms",
        min_value=0,
        max_value=50,
        value=2,
        step=1
    )

    floors = st.number_input(
        "🏢 Number of Floors",
        min_value=0,
        max_value=20,
        value=2,
        step=1
    )

    parking = st.number_input(
        "🚗 Number of Parking Spaces",
        min_value=0,
        max_value=20,
        value=1,
        step=1
    )


with col2:

    year = st.number_input(
        "📅 Construction Year",
        min_value=1900,
        max_value=2100,
        value=2020,
        step=1
    )

    road_width_ft = st.number_input(
        "🛣️ Road Width (feet)",
        min_value=0.0,
        max_value=200.0,
        value=13.0,
        step=0.5
    )

    area_sqft = st.number_input(
        "📐 Land Area (sq. ft.)",
        min_value=0.0,
        max_value=1000000.0,
        value=1700.0,
        step=10.0
    )

    build_area_sqft = st.number_input(
        "🏠 Build Area (sq. ft.)",
        min_value=0.0,
        max_value=1000000.0,
        value=1500.0,
        step=10.0
    )


st.divider()


# ============================================================
# PREDICTION
# ============================================================

st.header("🔮 Price Prediction")


if st.button(
    "🔮 Predict Price Category",
    use_container_width=True
):

    # --------------------------------------------------------
    # EXACT 8 FEATURES USED DURING TRAINING
    # --------------------------------------------------------

    input_data = pd.DataFrame(
        {
            "bedroom": [bedroom],
            "bathroom": [bathroom],
            "floors": [floors],
            "parking": [parking],
            "year": [year],
            "road_width_ft": [road_width_ft],
            "area_sqft": [area_sqft],
            "build_area_sqft": [build_area_sqft]
        }
    )


    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    try:

        prediction = model.predict(input_data)[0]

    except Exception as e:

        st.error("❌ Prediction failed.")

        st.exception(e)

        st.stop()


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    st.subheader("🎯 Prediction Result")


    if str(prediction).lower() == "low":

        st.success(
            f"🟢 Predicted Price Category: **{prediction}**"
        )

    elif str(prediction).lower() == "medium":

        st.info(
            f"🔵 Predicted Price Category: **{prediction}**"
        )

    elif str(prediction).lower() == "high":

        st.warning(
            f"🟠 Predicted Price Category: **{prediction}**"
        )

    elif str(prediction).lower() == "premium":

        st.error(
            f"🔴 Predicted Price Category: **{prediction}**"
        )

    else:

        st.success(
            f"Predicted Price Category: **{prediction}**"
        )


    # --------------------------------------------------------
    # SHOW INPUT DATA
    # --------------------------------------------------------

    st.subheader("📊 Property Information")

    display_data = pd.DataFrame(
        {
            "Feature": [
                "Bedroom",
                "Bathroom",
                "Floors",
                "Parking",
                "Year",
                "Road Width (ft)",
                "Area (sq. ft.)",
                "Build Area (sq. ft.)"
            ],

            "Value": [
                bedroom,
                bathroom,
                floors,
                parking,
                year,
                road_width_ft,
                area_sqft,
                build_area_sqft
            ]
        }
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # PREDICTION PROBABILITY
    # --------------------------------------------------------

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            input_data
        )[0]

        probability_data = pd.DataFrame(
            {
                "Price Category": model.classes_,

                "Probability (%)": (
                    probabilities * 100
                ).round(2)
            }
        )

        st.subheader("📈 Prediction Probability")

        st.dataframe(
            probability_data,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            probability_data.set_index(
                "Price Category"
            )["Probability (%)"]
        )


st.divider()


# ============================================================
# MODEL COMPARISON
# ============================================================

st.header("🤖 Classification Model Comparison")

st.write(
    "Comparison of the classification models used in the project."
)

model_comparison = pd.DataFrame(
    {
        "Model": [
            "Decision Tree",
            "KNN"
        ],

        "Performance": [
            44.05,
            43.00
        ]
    }
)

st.bar_chart(
    model_comparison.set_index(
        "Model"
    )["Performance"]
)

st.success(
    "🏆 Decision Tree is selected as the best classification model."
)


st.divider()


# ============================================================
# K-MEANS CLUSTERING
# ============================================================

st.header("🔵 K-Means Clustering")

st.write(
    "K-Means was evaluated for different values of K "
    "using inertia and silhouette score."
)


kmeans_data = pd.DataFrame(
    {
        "K": [
            2, 3, 4, 5, 6,
            7, 8, 9, 10
        ],

        "Inertia": [
            7699.669504,
            6197.217093,
            5141.430321,
            4467.220525,
            3894.402837,
            3492.200572,
            3140.851119,
            2895.326471,
            2649.433662
        ],

        "Silhouette Score": [
            0.431137,
            0.455361,
            0.467175,
            0.473295,
            0.487375,
            0.439660,
            0.446080,
            0.454390,
            0.466480
        ]
    }
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("📉 Elbow Method")

    st.line_chart(
        kmeans_data.set_index("K")[
            "Inertia"
        ]
    )


with col2:

    st.subheader("📈 Silhouette Score")

    st.line_chart(
        kmeans_data.set_index("K")[
            "Silhouette Score"
        ]
    )


best_k = kmeans_data.loc[
    kmeans_data["Silhouette Score"].idxmax()
]


st.success(
    f"Best clustering result: K = {int(best_k['K'])}"
)


st.subheader("K-Means Results")

st.dataframe(
    kmeans_data,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# ASSOCIATION RULE MINING
# ============================================================

st.header("🔗 Association Rule Mining")

st.write(
    "Apriori algorithm was used to discover relationships "
    "among area, bedroom, bathroom, parking and price categories."
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Total Rules",
        "306"
    )


with col2:

    st.metric(
        "Strong Rules",
        "255"
    )


# ------------------------------------------------------------
# STRONG RULES
# ------------------------------------------------------------

rules_data = pd.DataFrame(
    {
        "Antecedent": [

            "Medium Area + Many Bedrooms",

            "Many Bedrooms + Many Parking",

            "Many Bathrooms + High Price",

            "Many Bedrooms",

            "Many Bathrooms",

            "Many Parking + Price"

        ],

        "Consequent": [

            "Many Bathrooms + High Price",

            "Many Bathrooms",

            "Many Bedrooms",

            "High Price",

            "High Price",

            "Many Bathrooms"

        ],

        "Support": [

            0.059701,

            0.055631,

            0.144731,

            0.194030,

            0.183627,

            0.069652

        ],

        "Confidence": [

            0.663317,

            0.866197,

            0.788177,

            0.684211,

            0.725000,

            0.806283

        ],

        "Lift": [

            3.612298,

            3.419932,

            2.779362,

            2.052632,

            2.175000,

            3.183377

        ]
    }
)


st.subheader("⭐ Strong Association Rules")


st.dataframe(
    rules_data,
    use_container_width=True,
    hide_index=True
)


st.info(
    "Higher lift indicates a stronger relationship between "
    "the antecedent and consequent."
)


st.divider()


# ============================================================
# WEB SCRAPING
# ============================================================

st.header("🌐 Real Estate Web Scraping")

st.write(
    "The project scraped real estate property information "
    "from Nepal Homes."
)


if os.path.exists(SCRAPED_PATH):

    scraped_data = pd.read_csv(
        SCRAPED_PATH
    )


    # --------------------------------------------------------
    # SCRAPING SUMMARY
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Properties Scraped",
            len(scraped_data)
        )


    with col2:

        st.metric(
            "Dataset Columns",
            len(scraped_data.columns)
        )


    with col3:

        st.metric(
            "Property Type",
            "House"
        )


    # --------------------------------------------------------
    # SCRAPED DATA
    # --------------------------------------------------------

    st.subheader(
        "🏘️ Scraped Property Dataset"
    )


    st.dataframe(
        scraped_data,
        use_container_width=True,
        hide_index=True
    )


else:

    st.warning(
        "⚠️ scraper/scraped_data.csv was not found."
    )


st.divider()


# ============================================================
# PROJECT WORKFLOW
# ============================================================

st.header("🔄 Project Workflow")

workflow = pd.DataFrame(
    {
        "Step": [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6"
        ],

        "Process": [
            "Web Scraping",
            "Data Preprocessing",
            "Decision Tree Classification",
            "K-Means Clustering",
            "Association Rule Mining",
            "Price Category Prediction"
        ]
    }
)

st.dataframe(
    workflow,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Real Estate Property Price Prediction and Pattern Mining Project"
)

st.caption(
    "Machine Learning Model: Decision Tree Classifier"
)