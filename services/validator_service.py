import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from verification.product_extractor import extract_product_details
from verification.catalogue_validator import (
    validate_title_fit,
    validate_pdp_fit,
    validate_fabric
)

from reports.report_generator import save_report


def process_file(uploaded_file):

    start_time = time.time()

    # Save uploaded file
    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    # Read Excel
    df = pd.read_excel(file_path)

    df.columns = df.columns.str.strip()

    print(
        f"\nTotal rows loaded: {len(df)}"
    )

    # Chrome Options
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")

    chrome_options.add_argument(
        "--disable-gpu"
    )

    chrome_options.add_argument(
        "--disable-dev-shm-usage"
    )

    chrome_options.add_argument(
        "--no-sandbox"
    )

    prefs = {
        "profile.managed_default_content_settings.images": 2
    }

    chrome_options.add_experimental_option(
        "prefs",
        prefs
    )

    chrome_options.page_load_strategy = "eager"

    chrome_options.add_argument(
        "--window-size=1920,1080"
    )

    # Launch Browser
    from selenium.webdriver.chrome.service import Service

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(
    service=service,
    options=chrome_options
)

    report_rows = []

    total_extraction_time = 0

    # Main Processing Loop
    for index, row in df.iterrows():

        try:

            print(
                f"\nProcessing "
                f"{index + 1}/{len(df)}"
            )

            # Restart Chrome every 50 products
            if (
                index > 0
                and
                index % 50 == 0
            ):

                print(
                    f"\nRestarting Chrome "
                    f"at row {index}"
                )

                driver.quit()

                driver = webdriver.Chrome(
                    options=chrome_options
                )

            extraction_start = time.time()

            product_details = extract_product_details(
                driver,
                row["Link"]
            )

            extraction_time = (
                time.time()
                - extraction_start
            )

            total_extraction_time += extraction_time

            print(
                f"Extraction Time: "
                f"{round(extraction_time, 2)} sec"
            )

            # Fabric Validation
            fabric_status = validate_fabric(
                row["Fabric composition"],
                product_details["fabric_text"]
            )

            # Title Fit Validation
            title_fit_status = validate_title_fit(
                row["Fit"],
                product_details["title_text"]
            )

            # PDP Fit Validation
            pdp_fit_status = validate_pdp_fit(
                row["Fit"],
                product_details["fit_text"]
            )

            report_rows.append({

                "FG CODE":
                row["FG CODE"],

                "Product Link":
                row["Link"],

                "OLABI CODE":
                row["OLABI CODE"],

                "Dataset Fabric":
                row["Fabric composition"],

                "Fabric Status":
                fabric_status,

                "Dataset Fit":
                row["Fit"],

                "Title Fit Status":
                title_fit_status,

                "PDP Fit Status":
                pdp_fit_status,

                "Website Details":
                " | ".join(
                  line.strip()
                for line in product_details[
                "product_details"
                 ].splitlines()
                 if line.strip()
)
        

            })

        except Exception as e:

            print(
                f"Error processing row "
                f"{index + 1}: {e}"
            )

            continue

    # Cleanup
    driver.quit()

    save_report(
        report_rows
    )

    end_time = time.time()

    total_time = (
        end_time
        - start_time
    )

    print("\n==========================")
    print("PERFORMANCE SUMMARY")
    print("==========================")

    print(
        f"Rows Processed: "
        f"{len(report_rows)}"
    )

    print(
        f"Total Time: "
        f"{round(total_time, 2)} sec"
    )

    if len(report_rows) > 0:

        print(
            f"Average Time/Product: "
            f"{round(total_time / len(report_rows), 2)} sec"
        )

        print(
            f"Total Selenium Time: "
            f"{round(total_extraction_time, 2)} sec"
        )

        print(
            f"Average Selenium Time: "
            f"{round(total_extraction_time / len(report_rows), 2)} sec"
        )

    return (
        f"Validation Complete!\n"
        f"Rows Processed: {len(report_rows)}\n"
        f"Time Taken: "
        f"{round(total_time, 2)} seconds\n"
        f"Report Saved:\n"
        f"reports/verification_report.xlsx"
    )