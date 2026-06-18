import streamlit as st
import os
from services.validator_service import process_file

st.set_page_config(
    page_title="Catalogue Validation Tool",
    layout="centered"
)

st.title("Catalogue Validation Tool")

uploaded_file = st.file_uploader(
    "Upload Catalogue Excel",

    type=["xlsx", "xlsm"]
)

if uploaded_file:

    st.write(
        f"Uploaded File: {uploaded_file.name}"
    )

    result = process_file(
        uploaded_file
    )

    st.success(result)

    report_path = (
        "reports/verification_report.xlsx"
    )

    if os.path.exists(report_path):

        with open(
            report_path,
            "rb"
        ) as file:

            st.download_button(

                label="📥 Download Report",

                data=file,

                file_name=
                "verification_report.xlsx",

                mime=
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )