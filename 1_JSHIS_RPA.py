import os
import csv
import json
import requests

class Building:
    def __init__(self, No,name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def fetch_data(self):
        url_template = "https://www.j-shis.bosai.go.jp/map/api/pshm/Y2022/AVR/TTL_MTTL/meshinfo.geojson?position={lon},{lat}&epsg=4612&attr={attr}"
        urls = [
            url_template.format(lon=self.longitude, lat=self.latitude, attr="T30_I45_PS"),
            url_template.format(lon=self.longitude, lat=self.latitude, attr="T30_I50_PS"),
            url_template.format(lon=self.longitude, lat=self.latitude, attr="T30_I55_PS"),
            url_template.format(lon=self.longitude, lat=self.latitude, attr="T30_I60_PS")
        ]

        data = {}
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                attr = url.split("=")[-1]
                if attr == "T30_I45_PS":
                    intensity = "30年で震度5弱以上となる確率"
                elif attr == "T30_I50_PS":
                    intensity = "30年で震度5強以上となる確率"
                elif attr == "T30_I55_PS":
                    intensity = "30年で震度6弱以上となる確率"
                elif attr == "T30_I60_PS":
                    intensity = "30年で震度6強以上となる確率"
                else:
                    intensity = attr
                data[intensity] = response.json()["features"][0]["properties"][attr]
            else:
                print("Failed to fetch data from URL:", url)

        return data

    def save_data_as_csv(self, data):
        filename = f"output/{self.name}.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            header = [
                "建物名",
                "30年で震度5弱以上となる確率",
                "30年で震度5強以上となる確率",
                "30年で震度6弱以上となる確率",
                "30年で震度6強以上となる確率"
            ]
            writer.writerow(header)
            row = [
                self.name,
                data.get("30年で震度5弱以上となる確率", ""),
                data.get("30年で震度5強以上となる確率", ""),
                data.get("30年で震度6弱以上となる確率", ""),
                data.get("30年で震度6強以上となる確率", "")
            ]
            writer.writerow(row)

def main():
    # Create the output folder if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Read address.csv and process each building
    with open("input/address.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            No, name, latitude, longitude = row
            building = Building(No, name, latitude, longitude)
            data = building.fetch_data()
            building.save_data_as_csv(data)

if __name__ == "__main__":
    main()
