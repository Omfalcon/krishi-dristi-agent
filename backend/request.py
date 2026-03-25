import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://mausam.imd.gov.in/imd_latest/contents/"
url = BASE_URL + "rainfall_statistics_1.php"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Create folders
os.makedirs("images", exist_ok=True)

# -------- Download PDF --------
pdf_tag = soup.find("a", string=lambda x: x and "Download PDF" in x)

if pdf_tag:
    pdf_url = pdf_tag.get("href")
    pdf_url = requests.compat.urljoin(BASE_URL, pdf_url)

    pdf_data = requests.get(pdf_url).content

    with open("rainfall_data.pdf", "wb") as f:
        f.write(pdf_data)

    print("PDF downloaded!")

