import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def process_chunk(urls):

    chrome_options = Options()

    chrome_options.add_argument(
        "--disable-gpu"
    )

    driver = webdriver.Chrome(
        options=chrome_options
    )

    results = []

    try:

        for url in urls:

            driver.get(url)

            title = driver.title

            print(title)

            results.append(title)

    finally:

        driver.quit()

    return results


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

    chunk1 = urls[:5]

    chunk2 = urls[5:]

    print(
        f"Chunk 1: {len(chunk1)} products"
    )

    print(
        f"Chunk 2: {len(chunk2)} products"
    )

    process_chunk(chunk1)

    process_chunk(chunk2)

    end_time = time.time()

    print(
        f"\nTotal Time: "
        f"{round(end_time - start_time, 2)} sec"
    )