import streamlit as st
import requests
import pandas as pd
import numpy as np

# ==========================
# CONFIG
# ==========================

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Software Defect Predictor",
    page_icon="🔍",
    layout="wide"
)

# ==========================
# HEADER
# ==========================

st.title("🔍 Software Defect Predictor")

st.caption(
    "Machine Learning Powered Static Code Analysis"
)

st.divider()

# ==========================
# RESULT DISPLAY
# ==========================

def display_result(result):

    st.markdown("## Prediction Analysis")

    col1, col2, col3, col4 = st.columns(4)

    probability = float(
        result["probability"]
    )

    confidence = (
        abs(probability - 0.5)
        * 2
        * 100
    )

    with col1:
        st.metric(
            "Prediction",
            result["prediction"]
        )

    with col2:
        st.metric(
            "Probability",
            f"{probability * 100:.2f}%"
        )

    with col3:
        st.metric(
            "Risk Level",
            result["risk_level"]
        )

    with col4:
        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

    # -----------------------
    # Prediction Banner
    # -----------------------

    if result["prediction"] == "Defective":

        st.error(
            "🚨 Defective File Detected"
        )

    else:

        st.success(
            "✅ Non-Defective File"
        )

    # -----------------------
    # Risk Banner
    # -----------------------

    risk = result["risk_level"]

    if risk == "Low":

        st.success(
            "Low Risk"
        )

    elif risk == "Medium":

        st.warning(
            "Medium Risk"
        )

    else:

        st.error(
            "High Risk"
        )

    # -----------------------
    # Probability
    # -----------------------

    st.markdown(
        "### Defect Probability"
    )

    st.progress(
        probability
    )

    st.write(
        f"Defect Probability: "
        f"**{probability * 100:.2f}%**"
    )

    # -----------------------
    # Metrics Chart
    # -----------------------

    st.markdown(
        "### Software Metrics"
    )

    metrics = result["metrics"]

    chart_df = pd.DataFrame(
        {
            "Metric": metrics.keys(),
            "Value": metrics.values()
        }
    )

    chart_df["Value"] = np.log1p(
        chart_df["Value"]
    )

    chart_df = chart_df.set_index(
        "Metric"
    )

    st.bar_chart(
        chart_df
    )


    st.divider()
    
    st.markdown("## 🤖 AI Code Review")
    
    st.markdown(
    result["ai_review"]
)

    # -----------------------
    # Raw JSON
    # -----------------------

    with st.expander(
        "View Raw Response"
    ):
        st.json(result)

# ==========================
# TABS
# ==========================

tab1, tab2, tab3 = st.tabs(
    [
        "📁 Upload File",
        "📝 Paste Code",
        "🖼 OCR Image"
    ]
)

# ==================================================
# TAB 1 : FILE UPLOAD
# ==================================================

with tab1:

    uploaded_file = st.file_uploader(
        "Upload Python File",
        type=["py"]
    )

    if uploaded_file:

        st.success(
            f"Selected File: "
            f"{uploaded_file.name}"
        )

        with st.expander(
            "View Uploaded Code"
        ):

            st.code(
                uploaded_file
                .getvalue()
                .decode("utf-8"),
                language="python"
            )

        if st.button(
            "Analyze File",
            use_container_width=True
        ):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/plain"
                    )
                }

                response = requests.post(
                    f"{BACKEND_URL}/analyze-file",
                    files=files
                )

                if response.status_code == 200:

                    display_result(
                        response.json()
                    )

                else:

                    st.error(
                        response.json()
                        .get(
                            "detail",
                            "Unknown Error"
                        )
                    )

            except Exception as e:

                st.error(str(e))

# ==================================================
# TAB 2 : DIRECT CODE INPUT
# ==================================================

with tab2:

    code_input = st.text_area(
        "Paste Python Code",
        height=300
    )

    if st.button(
        "Analyze Code",
        use_container_width=True
    ):

        try:

            response = requests.post(
                f"{BACKEND_URL}/analyze-code",
                json={
                    "code": code_input
                }
            )

            if response.status_code == 200:

                display_result(
                    response.json()
                )

            else:

                st.error(
                    response.json()
                    .get(
                        "detail",
                        "Unknown Error"
                    )
                )

        except Exception as e:

            st.error(str(e))

# ==================================================
# TAB 3 : OCR IMAGE
# ==================================================

with tab3:

    image_file = st.file_uploader(
        "Upload Code Screenshot",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    if image_file:

        st.image(
            image_file,
            use_container_width=True
        )

        if st.button(
            "Extract Code"
        ):

            files = {
                "file": (
                    image_file.name,
                    image_file.getvalue(),
                    image_file.type
                )
            }

            response = requests.post(
                f"{BACKEND_URL}/extract-code-from-image",
                files=files
            )

            if response.status_code == 200:

                st.session_state[
                    "ocr_code"
                ] = response.json()[
                    "extracted_code"
                ]

            else:

                st.error(
                    response.json()
                    .get(
                        "detail",
                        "OCR Failed"
                    )
                )

    if "ocr_code" in st.session_state:

        edited_code = st.text_area(
            "Review / Edit Extracted Code",
            value=st.session_state[
                "ocr_code"
            ],
            height=300
        )

        if st.button(
            "Analyze OCR Code",
            use_container_width=True
        ):

            response = requests.post(
                f"{BACKEND_URL}/analyze-code",
                json={
                    "code":
                        edited_code
                }
            )

            if response.status_code == 200:

                display_result(
                    response.json()
                )

            else:

                st.error(
                    response.json()
                    .get(
                        "detail",
                        "Analysis Failed"
                    )
                )