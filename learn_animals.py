import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import random

# GitHub repo 路徑
REPO_API_URL = "https://api.github.com/repos/KellyLee0825/animal-app/contents/images"

st.title("台灣動植物學習小遊戲 🐢🌿")
st.write("你知道這是什麼動植物嗎？先猜猜看，再點按鈕看看答案吧！")

def get_github_folder_contents(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("無法讀取 GitHub 資料夾內容")
        return []

# 取得 images 資料夾內容
contents = get_github_folder_contents(REPO_API_URL)

# 找出資料夾名稱（物種名稱）
species_list = [item['name'] for item in contents if item['type'] == 'dir']

if not species_list:
    st.warning("資料夾裡還沒有動植物資料夾，請先放一些進來喔！")
else:
    selected_species = st.selectbox("選擇一種動植物", species_list)

    # 取得該物種資料夾裡的檔案列表
    species_api_url = f"{REPO_API_URL}/{selected_species}"
    species_contents = get_github_folder_contents(species_api_url)

    # 找圖片檔案（只要副檔名是 jpg/png/jpeg）
    image_files = [item for item in species_contents
                   if item['type'] == 'file' and
                   item['name'].lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        st.warning(f"這個動植物「{selected_species}」目前還沒有圖片")
    else:
        # 隨機選一張圖片
        selected_image = random.choice(image_files)
        image_url = selected_image['download_url']  # GitHub 直接下載連結

        # 下載圖片並顯示
        img_response = requests.get(image_url)
        image = Image.open(BytesIO(img_response.content))
        st.image(image, caption="你猜得出來嗎？", use_column_width=True)

        if st.button("顯示答案"):
            st.success(f"答案是：{selected_species}")

