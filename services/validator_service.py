import os
import time
import traceback
from reports.report_generator import save_report
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import streamlit as st
from verification.catalogue_validator import (
    validate_fabric,
    validate_pdp_fit,
    validate_title_fit,
)
from verification.product_extractor import extract_product_details
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def detect_column(df, keywords):
    for col in df.columns:
        col_name = str(col).strip().lower()

        for keyword in keywords:
            if keyword.lower() in col_name:
                return col

    return None


def process_file(file_path):
    start_time = time.time()
    # Read Excel
    df = pd.read_excel(file_path)

    df.columns = df.columns.str.strip()
    link_col = detect_column(df, ["link", "links", "url"])
    fabric_col = detect_column(
        df, ["composition", "fabric composition", "material"]
    )
    fit_col = detect_column(df, ["fit"])
    fg_col = detect_column(df, ["fg code"])
    olabi_col = detect_column(df, ["olabi code", "olabi code buy master"])

    print(df.columns.tolist())
    print("Link:", link_col)
    print("Fabric:", fabric_col)
    print("Fit:", fit_col)
    print("FG:", fg_col)
    print("OLABI:", olabi_col)
    print(f"\nTotal rows loaded: {len(df)}")

    # ---------------- Chrome Options ----------------

    chrome_options = Options()

    # Detect whether running locally or on Linux (Render/Streamlit)
    if os.name != "nt":
        chrome_options.binary_location = "/usr/bin/chromium"

        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-software-rasterizer")
    else:
        # Windows local debugging
        chrome_options.add_argument("--start-maximized")

    chrome_options.page_load_strategy = "eager"

    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # --- Debugging Output Before Creating Driver ---
    print("OS:", os.name)
    print(
        "Chromedriver exists:", os.path.exists("/usr/bin/chromedriver")
    )
    print("Chromium exists:", os.path.exists("/usr/bin/chromium"))

    # Windows vs Linux
    if os.name == "nt":
        service = Service(ChromeDriverManager().install())
    else:
        service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    report_rows = []

    total_extraction_time = 0

    # Main Processing Loop
    for index, row in df.iterrows():

        try:

            print(f"\nProcessing {index + 1}/{len(df)}")

            # Restart Chrome every 50 products
            if index > 0 and index % 50 == 0:

                print(f"\nRestarting Chrome at row {index}")

                driver.quit()

                driver = webdriver.Chrome(
                    service=service, options=chrome_options
                )

            extraction_start = time.time()

            try:
                product_details = extract_product_details(
                    driver, row[link_col]
                )

                print("=" * 80)
                print("PRODUCT DETAILS RETURNED")
                print(product_details)
                print("=" * 80)
            except Exception as e:
                print("=" * 80)
                print("EXTRACT PRODUCT DETAILS FAILED")
                print("URL:", row[link_col])
                print("ERROR:", repr(e))
                traceback.print_exc()
                print("=" * 80)
                raise

            extraction_time = time.time() - extraction_start

            total_extraction_time += extraction_time

            print(
                f"Extraction Time: {round(extraction_time, 2)} sec"
            )

            # Fabric Validation
            fabric_status = validate_fabric(
                row[fabric_col], product_details["fabric_text"]
            )

            # Title Fit Validation
            title_fit_status = validate_title_fit(
                row[fit_col], product_details["title_text"]
            )

            # PDP Fit Validation
            pdp_fit_status = validate_pdp_fit(
                row[fit_col], product_details["fit_text"]
            )

            report_rows.append(
                {
                    "FG CODE": row[fg_col],
                    "Product Link": row[link_col],
                    "OLABI CODE": row[olabi_col],
                    "Dataset Fabric": row[fabric_col],
                    "Fabric Status": fabric_status,
                    "Dataset Fit": row[fit_col],
                    "Title Fit Status": title_fit_status,
                    "PDP Fit Status": pdp_fit_status,
                    "Website Details": " | ".join(
                        line.strip()
                        for line in product_details[
                            "product_details"
                        ].splitlines()
                        if line.strip()
                    ),
                }
            )

        except Exception as e:
            traceback.print_exc()
            st.error(f"Error on row {index + 1}: {e}")
            raise

    # Cleanup
    driver.quit()

    save_report(report_rows)

    end_time = time.time()

    total_time = end_time - start_time

    print("\n==========================")
    print("PERFORMANCE SUMMARY")
    print("==========================")

    print(f"Rows Processed: {len(report_rows)}")

    print(f"Total Time: {round(total_time, 2)} sec")

    if len(report_rows) > 0:

        print(
            f"Average Time/Product: {round(total_time / len(report_rows), 2)} sec"
        )

        print(
            f"Total Selenium Time: {round(total_extraction_time, 2)} sec"
        )

        print(
            f"Average Selenium Time: {round(total_extraction_time / len(report_rows), 2)} sec"
        )

    return (
        f"Validation Complete!\n"
        f"Rows Processed: {len(report_rows)}\n"
        f"Time Taken: {round(total_time, 2)} seconds\n"
        f"Report Saved:\n"
        f"reports/verification_report.xlsx"
    )