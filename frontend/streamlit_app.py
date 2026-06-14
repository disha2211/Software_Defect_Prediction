import streamlit as st
import requests
import pandas as pd

# =====================================
# Page Config
# =====================================

st.set_page_config(
    page_title="Software Defect Predictor",
    page_icon="🔍",
    layout="wide"
)

# =====================================
# Header
# =====================================

st.title("🔍 Software Defect Predictor")
st.markdown(
    """
    Upload a Python file and predict whether it is likely
    to be defective based on static code metrics and
    machine learning analysis.
    """
)

st.divider()

# =====================================
# File Upload
# =====================================

uploaded_file = st.file_uploader(
    "Upload a Python File",
    type=["py"]
)

# =====================================
# Prediction Button
# =====================================

if uploaded_file is not None:

    #--------------Show Uploaded Code
    if uploaded_file is not None:

        st.success(f"Selected File: {uploaded_file.name}")

        with st.expander("View Uploaded Code"):
            st.code(
                uploaded_file.getvalue().decode("utf-8"),
                language="python"
            )

    if st.button("Predict Defect Risk", use_container_width=True):

        try:

            with st.spinner("Analyzing code and generating prediction..."):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/plain"
                    )
                }

                response = requests.post(
                    "http://localhost:8000/analyze-file",
                    files=files,
                    timeout=60
                )

                if response.status_code != 200:

                    error_message = response.json().get(
                        "detail",
                        "Unknown error"
                    )

                    st.error(error_message)

                else:

                    result = response.json()

                    # existing UI code

            st.divider()

            # =====================================
            # Prediction Section
            # =====================================

            st.subheader("Prediction Result")

            col1, col2, col3, col4 = st.columns(4)


            with col1:
                st.metric(
                    label="Prediction",
                    value=result["prediction"]
                )

            with col2:
                st.metric(
                    label="Probability",
                    value=f"{result['probability'] * 100:.2f}%"
                )

            with col3:
                st.metric(
                    label="Risk Level",
                    value=result["risk_level"]
                )

            with col4:
                confidence = (
                        abs(float(result["probability"]) - 0.5)
                        * 2
                        * 100
                )

                st.metric(
                    "Confidence",
                    f"{confidence:.2f}%"
                )


            #-----------Color-Coded Prediction Card
            if result["prediction"] == "Defective":
                st.error("🚨 Defective File Detected")
            else:
                st.success("✅ Non-Defective File")

            # =====================================
            # Risk Indicator
            # =====================================

            risk = result["risk_level"]

            if risk == "Low":
                st.success("✅ Low Risk File")

            elif risk == "Medium":
                st.warning("⚠️ Medium Risk File")

            else:
                st.error("🚨 High Risk File")

            # =====================================
            # Probability Progress Bar
            # =====================================

            st.subheader("Defect Probability")

            probability = float(result["probability"])

            st.progress(probability)

            st.write(
                f"Predicted Defect Probability: "
                f"**{probability * 100:.2f}%**"
            )

            st.divider()


            # =====================================
            # Metrics Section
            # =====================================

            metrics = result["metrics"]

            metrics_df = pd.DataFrame(
                list(metrics.items()),
                columns=["Metric", "Value"]
            )

            # Keep only numeric metrics
            metrics_df = metrics_df[
                pd.to_numeric(
                    metrics_df["Value"],
                    errors="coerce"
                ).notnull()
            ]

            metrics_df = metrics_df.set_index(
                "Metric"
            )

            import numpy as np

            st.subheader("Code Metrics Visualization")

            metrics = result["metrics"]

            chart_df = pd.DataFrame(
                {
                    "Metric": metrics.keys(),
                    "Value": metrics.values()
                }
            )

            chart_df["Value"] = np.log1p(chart_df["Value"])

            chart_df = chart_df.set_index("Metric")

            st.bar_chart(chart_df)

            # =====================================
            # Raw JSON (Optional)
            # =====================================

            with st.expander("View Raw API Response"):
                st.json(result)

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI backend.\n\n"
                "Make sure your FastAPI server is running on:\n"
                "http://localhost:8000"
            )

        except requests.exceptions.Timeout:

            st.error(
                "Request timed out while waiting for prediction."
            )

        except requests.exceptions.HTTPError as e:

            st.error(
                f"Backend returned an error:\n\n{e}"
            )

        except Exception as e:

            st.error(
                f"Unexpected error:\n\n{str(e)}"
            )

else:

    st.info("Upload a .py file to begin analysis.")