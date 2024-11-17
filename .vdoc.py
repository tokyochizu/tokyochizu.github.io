# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
import geopandas as gpd
import folium


wardlist = ["千代田区", "中央区", "港区", "新宿区", "文京区", "台東区", "墨田区", "江東区", 
        "品川区", "目黒区", "大田区", "世田谷区", "渋谷区", "中野区", "杉並区", "豊島区", "北区", 
        "荒川区", "板橋区", "練馬区", "足立区", "葛飾区", "江戸川区"]
ward2roman = {
    "千代田区": "Chiyoda",
    "中央区": "Chuo",
    "港区": "Minato",
    "新宿区": "Shinjuku",
    "文京区": "Bunkyo",
    "台東区": "Taito",
    "墨田区": "Sumida",
    "江東区": "Koto",
    "品川区": "Shinagawa",
    "目黒区": "Meguro",
    "大田区": "Ota",
    "世田谷区": "Setagaya",
    "渋谷区": "Shibuya",
    "中野区": "Nakano",
    "杉並区": "Suginami",
    "豊島区": "Toshima",
    "北区": "Kita",
    "荒川区": "Arakawa",
    "板橋区": "Itabashi",
    "練馬区": "Nerima",
    "足立区": "Adachi",
    "葛飾区": "Katsushika",
    "江戸川区": "Edogawa"
}

wards = gpd.read_file("../GIS/tokyoshp/N03-20240101_13.shp")
wards = wards[wards.N03_004.isin(wardlist)]
wards = wards.drop(wards.columns[[0, 1, 2, 4, 5]], axis=1)
wards.columns = ["Ward", "geometry"]
wards["Ward Rom"] = wards["Ward"].map(ward2roman)


blocks = gpd.read_file("../ASS2/GIS/bounds/r2ka13.shp")
blocks = blocks[blocks.CITY_NAME.notna()]
blocks = blocks[(blocks.CITY_NAME.str.contains("区"))]
blocks = blocks.drop(blocks.columns[[0, 1, 2, 3, 4, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]], axis=1)
blocks.columns = ["Ward", "Block", "Area", "geometry"]
blocks["Ward Rom"] = blocks["Ward"].map(ward2roman)
blocks.insert(1, "Ward Rom", blocks.pop("Ward Rom"))

m = folium.Map([35.66, 139.74], zoom_start=11)

folium.GeoJson(
    blocks,
    name="Blocks",
    style_function=lambda x: {
        "fillColor": "#ff8700",
        "color": "#000000",
        "fillOpacity": 0.3,
        "weight": 1
    }, 
    show=False,
    tooltip=folium.GeoJsonTooltip(fields=["Ward", "Ward Rom", "Block", "Area"])
).add_to(m)

folium.GeoJson(
    wards,
    name="Wards",
    style_function=lambda x: {
        "fillColor": "#0078ff",
        "color": "#000000",
        "fillOpacity": 0.3,
        "weight": 2
    },
    tooltip=folium.GeoJsonTooltip(fields=["Ward", "Ward Rom"])
).add_to(m)

folium.LayerControl().add_to(m)
m
#
#
#
