import pandas as pd
import time

from multiprocessing import Pool

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def process_url(url):

    chrome_options = Options()

    chrome_options.add_argument(
        "--disable-gpu"
    )

    driver = webdriver.Chrome(
        options=chrome_options
    )

    try:

        driver.get(url)

        title = driver.title

        print(title)

        return title

    finally:

        driver.quit()


if __name__ == "__main__":

    start_time = time.time()

    file_path = "data/Copy of Test- Maanya1.xlsm"

    df = pd.read_excel(file_path)

    df.columns = df.columns.str.strip()

    urls = (
        df["Link"]
        .head(10)
        .tolist()
    )

    with Pool(2) as pool:

        results = pool.map(
            process_url,
            urls
        )

    end_time = time.time()

    print("\nCompleted!")

    print(
        f"Products Processed: {len(results)}"
    )

    print(
        f"Total Time: "
        f"{round(end_time - start_time, 2)} sec"
    )

    print(
        f"Average Time/Product: "
        f"{round((end_time - start_time) / len(results), 2)} sec"
    )