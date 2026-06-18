import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from verification.product_extractor import extract_product_details
from verification.catalogue_validator import (
    validate_fit,
    validate_fabric
)
from reports.report_generator import save_report


start_time = time.time()

print("Catalogue Improvement System Started")

file_path = "data/Copy of Test- Maanya1.xlsm"

df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

print("Total rows loaded:", len(df))


# -------------------------
# Chrome Options
# -------------------------

chrome_options = Options()

prefs = {
    "profile.managed_default_content_settings.images": 2
}

chrome_options.add_experimental_option(
    "prefs",
    prefs
)

chrome_options.page_load_strategy = "eager"

chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")


# -------------------------
# Launch Browser
# -------------------------

driver = webdriver.Chrome(
    options=chrome_options
)

report_rows = []


# -------------------------
# Main Loop
# -------------------------

for index, row in df.iterrows():

    # Restart browser every 50 products
    if index > 0 and index % 50 == 0:

        print(
            f"\nRestarting Chrome at product {index}..."
        )

        save_report(report_rows)

        driver.quit()

        driver = webdriver.Chrome(
            options=chrome_options
        )

    elapsed = (
        time.time() - start_time
    ) / 60

    print(
        f"Processing {index + 1}/{len(df)} "
        f"| Elapsed: {elapsed:.1f} min"
    )

    try:

        product_url = row["Link"]

        product_details = extract_product_details(
            driver,
            product_url
        )

        fabric_status = validate_fabric(
            row["Fabric composition"],
            product_details["fabric_text"]
        )

        fit_status = validate_fit(
            row["Fit"],
            product_details["title_text"],
            product_details["fit_text"]
        )

        report_rows.append({

            "FG CODE":
            row["FG CODE"],

            "OLABI CODE":
            row["OLABI CODE"],

            "Dataset Fabric":
            row["Fabric composition"],

            "Fabric Status":
            fabric_status,

            "Dataset Fit":
            row["Fit"],

            "Fit Status":
            fit_status,

            "Website Details":
            product_details[
                "product_details"
            ].replace(
                "\n",
                " | "
            ),

            "Link":
            product_url

        })

    except Exception as e:

        print(
            f"Error processing row "
            f"{index + 1}: {e}"
        )

        continue


# -------------------------
# Close Browser
# -------------------------

driver.quit()


# -------------------------
# Final Report Save
# -------------------------

save_report(report_rows)

end_time = time.time()

print(
    f"\nProcess Completed!"
    f"\nTime taken: "
    f"{end_time - start_time:.2f} seconds"
)