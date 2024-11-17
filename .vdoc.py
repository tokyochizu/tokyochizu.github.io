# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
import geopandas as gpd

blocks = gpd.read_file("../ASS2/GIS/bounds/r2ka13.shp")
blocks = blocks[blocks.CITY_NAME.notna()]
blocks = blocks[(blocks.CITY_NAME.str.contains("区"))]
blocks["cityblockmerge"] = blocks.CITY_NAME.str.strip() + blocks.S_NAME.str.strip()
blocks = blocks.drop(blocks.columns[[0, 1, 2, 3, 4, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]], axis=1)

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
import pandas as pd
disaster = pd.read_excel("../ASS2/disasteredit.xlsx")
disaster.columns = ["Ward", "Block", "Geo Class", "Building Collapse Risk (Building / ha)", "Building Collapse Risk Ranking", "Building Risk Grade", 
                    "Fire Risk (Building / ha)", "Fire Risk Ranking", "Fire Risk Grade", "Disaster Relief Difficulty Rating", 
                    "Combined Risk (Building / ha)", "Combined Risk Ranking", "Combined Risk Grade"]
disaster = disaster[(disaster.Ward.str.contains("区"))]
disaster["blockmergename"] = disaster.Ward + disaster.Block
disaster = disaster.drop(disaster.columns[[4, 7, 11]], axis=1)

num = {"１": "一", "２": "二", "３": "三", "４": "四", "５": "五", "６": "六", "７": "七", "８": "八", "９": "九"}
chars = {"ケ": "ヶ"}
for k, v in num.items():
    disaster.blockmergename = disaster.blockmergename.str.replace(k,v)
for k, v in chars.items():
    blocks.cityblockmerge = blocks.cityblockmerge.str.replace(k,v)
    disaster.blockmergename = disaster.blockmergename.str.replace(k,v)

merged_df = blocks.merge(disaster, left_on="cityblockmerge", right_on="blockmergename", how="outer",indicator=True)


#
#
#
