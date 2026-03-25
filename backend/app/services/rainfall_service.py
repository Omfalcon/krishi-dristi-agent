import pandas as pd
import datetime
import ast
import math

def get_rainfall_data(csv_file, query):
    # 1. Load Data
    df = pd.read_csv(csv_file)
    
    # 2. Get Current Month (e.g., 'MAR')
    now = datetime.datetime.now()
    month_col = now.strftime('%b').upper() 
    
    # Clean column names
    df.columns = df.columns.str.strip()

    # 3. Helper to parse the 'coord' column
    def parse_coords(coord_str):
        try:
            # Converts string "{'lon': ...}" to a Python dict
            return ast.literal_eval(coord_str)
        except:
            return None

    # 4. Search by Coordinates
    if isinstance(query, (list, tuple)) and len(query) == 2:
        user_lat, user_lon = query
        min_dist = float('inf')
        closest_row = None

        for _, row in df.iterrows():
            d_coords = parse_coords(row['coord'])
            if d_coords:
                # Euclidean distance calculation
                dist = math.sqrt((d_coords['lat'] - user_lat)**2 + (d_coords['lon'] - user_lon)**2)
                if dist < min_dist:
                    min_dist = dist
                    closest_row = row
        
        if closest_row is not None:
            return (f"Nearest District: {closest_row['DISTRICT']}\n"
                    f"Month: {month_col}\n"
                    f"Rainfall: {closest_row[month_col]} mm")

    # 5. Search by Name (District or State)
    query_str = str(query).strip().upper()
    
    # Try District Match
    dist_match = df[df['DISTRICT'].str.upper() == query_str]
    if not dist_match.empty:
        return f"District: {query_str} | {month_col} Rainfall: {dist_match.iloc[0][month_col]} mm"

    # Try State Match
    state_match = df[df['STATE_UT_NAME'].str.upper() == query_str]
    if not state_match.empty:
        avg = state_match[month_col].mean()
        return f"State: {query_str} | Average {month_col} Rainfall: {avg:.2f} mm"

    return "No match found for your input."






# import requests
# from bs4 import BeautifulSoup
# import os
# import camelot
# import pandas as pd


# # =========================================
# # CLASS 1: PDF SCRAPER
# # =========================================
# class IMDRainfallScraper:
#     BASE_URL = "https://mausam.imd.gov.in/imd_latest/contents/"
#     PAGE = "rainfall_statistics_1.php"

#     def __init__(self, save_path="rainfall_data.pdf"):
#         self.url = self.BASE_URL + self.PAGE
#         self.save_path = save_path
#         self.headers = {"User-Agent": "Mozilla/5.0"}

#     def download_pdf(self):
#         response = requests.get(self.url, headers=self.headers)
#         soup = BeautifulSoup(response.text, "html.parser")

#         pdf_tag = soup.find("a", string=lambda x: x and "Download PDF" in x)

#         if not pdf_tag:
#             print("❌ PDF link not found")
#             return None

#         pdf_url = requests.compat.urljoin(self.BASE_URL, pdf_tag.get("href"))
#         pdf_data = requests.get(pdf_url).content

#         with open(self.save_path, "wb") as f:
#             f.write(pdf_data)

#         print("✅ PDF downloaded!")
#         return self.save_path



# import camelot
# import pandas as pd
# import re

# class RainfallDataProcessor:
#     def __init__(self, pdf_path):
#         self.pdf_path = pdf_path
#         self.df = None

#     # -------------------------------
#     # STEP 1: Extract Tables
#     # -------------------------------
#     def extract_tables(self):
#         tables = camelot.read_pdf(self.pdf_path, pages="all")

#         dfs = []
#         for table in tables:
#             df = table.df

#             # Remove empty columns
#             df = df.dropna(axis=1, how='all')

#             # Keep only first 4 columns
#             if df.shape[1] >= 4:
#                 df = df.iloc[:, :4]

#             dfs.append(df)

#         self.df = pd.concat(dfs, ignore_index=True)

#     # -------------------------------
#     # STEP 2: Clean Data
#     # -------------------------------
#     def clean_data(self):
#         df = self.df.copy()

#         # Fix column mismatch safely
#         df = df.iloc[:, :4]
#         df.columns = ["S_NO", "Region", "Rain_11_Mar", "Rain_18_Mar"]

#         # Remove repeated headers
#         df = df[~df.astype(str).apply(
#             lambda row: row.str.contains("MET. SUBDIVION", na=False)
#         ).any(axis=1)]

#         # Remove PERIOD rows
#         df = df[~df["S_NO"].astype(str).str.contains("PERIOD", na=False)]

#         # Remove rows where Region contains multiple lines (bad extraction)
#         df = df[~df["Region"].astype(str).str.contains("\n")]

#         # Remove junk numeric regions
#         df = df[~df["Region"].astype(str).str.match(r'^\d+(\.\d+)?$')]

#         # Remove S_NO invalid values
#         df = df[df["S_NO"].astype(str).str.match(r'^\d+$')]

#         # Clean Region column
#         df["Region"] = df["Region"].astype(str).str.replace('"', '').str.strip()

#         # ❗ Remove STATE HEADERS (important fix)
#         df = df[~df["Region"].str.contains(
#             r'KERALA|ASSAM|BIHAR|UTTAR PRADESH|WEST BENGAL|ODISHA|INDIA',
#             case=False,
#             na=False
#         )]

#         # Clean rainfall columns
#         df["Rain_11_Mar"] = pd.to_numeric(
#             df["Rain_11_Mar"].astype(str).str.replace('%',''),
#             errors='coerce'
#         )

#         df["Rain_18_Mar"] = pd.to_numeric(
#             df["Rain_18_Mar"].astype(str).str.replace('%',''),
#             errors='coerce'
#         )

#         # Fill missing values
#         df["Rain_11_Mar"] = df["Rain_11_Mar"].fillna(0)
#         df["Rain_18_Mar"] = df["Rain_18_Mar"].fillna(0)

#         # Final cleanup
#         df.reset_index(drop=True, inplace=True)

#         self.df = df

#     # -------------------------------
#     # STEP 3: Save
#     # -------------------------------
#     def save(self, output_path="final_clean_dataset.csv"):
#         self.df.to_csv(output_path, index=False)
#         print("✅ Clean dataset saved!")

#     def get_data(self):
#         return self.df


# # =========================================
# # MAIN EXECUTION
# # =========================================
# # if __name__ == "__main__":
# #     scraper = IMDRainfallScraper()
# #     pdf_path = scraper.download_pdf()

# #     if pdf_path:
# #         processor = RainfallDataProcessor(pdf_path)
# #         processor.extract_tables()
# #         processor.clean_data()
# #         processor.save()

# #         print(processor.get_data().head())
# if __name__ == "__main__":
#     #--- EXAMPLES OF USE ---
#     result = get_rainfall_data('rain_fall_distribution.csv', 'LOHIT')
#     print(result)
#     result = get_rainfall_data('rain_fall_distribution.csv', (28.68, 77.06)) # Lat, Lon
#     print(result)