from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

def scrape_imdb():
    options = webdriver.ChromeOptions()
    # Comment headless for debugging
    # options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    url = "https://www.imdb.com/chart/top/"
    driver.get(url)
    time.sleep(6)

    movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

    data = []
    rank = 1

    for movie in movies:
        try:
            title = movie.find_element(By.TAG_NAME, "h3").text
            rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star").text

            data.append({
                "Rank": rank,
                "Movie": title,
                "IMDb Rating": rating
            })
            rank += 1
        except:
            continue

    driver.quit()

    if not os.path.exists("csv"):
        os.mkdir("csv")

    df = pd.DataFrame(data)
    df.to_csv("csv/imdb_top_250_movies.csv", index=False, mode="w")
    print("✅ IMDb data scraped and saved to CSV")

if __name__ == "__main__":

    scrape_imdb()
