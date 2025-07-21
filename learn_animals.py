import streamlit as st
import requests
import random
from PIL import Image
from io import BytesIO

# GitHub Repo 的 REST API 路徑（images 資料夾）
GITHUB_API_URL = "https://api.github.com/repos/KellyLee0825/animal-app/contents/images"

st.title("台灣動植物學習小遊戲 🐢🌿")
st.write("你知道這是什麼動植物嗎？你可以切換圖片來猜猜看，然後按下按鈕揭曉答案。")

# ---------- 取得 GitHub 資料夾內容 ----------
def get_folder_contents(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        st.error(f"無法載入 GitHub 資料：{res.status_code}")
        return []

# ---------- 取得所有動植物資料夾 ----------
species_folders = [item for item in get_folder_contents(GITHUB_API_URL) if item["type"] == "dir"]
species_list = [folder["name"] for folder in species_folders]

if not species_list:
    st.warning("尚未偵測到任何動植物資料夾。請確認 GitHub 的 images 資料夾結構是否正確。")
else:
    selected_species = st.selectbox("選擇一種動植物", species_list)

    # 該物種的 GitHub 資料夾 URL
    species_url = f"{GITHUB_API_URL}/{selected_species}"

    # 取得圖片清單
    species_images = [img for img in get_folder_contents(species_url)
                      if img["name"].lower().endswith(('.jpg', '.jpeg', '.png'))]

    # 檢查圖片是否存在
    if not species_images:
        st.warning(f"這個物種「{selected_species}」目前沒有圖片")
    else:
        # ---------- 初始化 session_state ----------
        if "image_index" not in st.session_state:
            st.session_state.image_index = 0

        # 若換了物種，就重設圖片 index
        if "last_species" not in st.session_state or st.session_state.last_species != selected_species:
            st.session_state.image_index = 0
            st.session_state.last_species = selected_species

        # 處理上一張 / 下一張按鈕
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ 上一張"):
                st.session_state.image_index = (st.session_state.image_index - 1) % len(species_images)
        with col3:
            if st.button("➡️ 下一張"):
                st.session_state.image_index = (st.session_state.image_index + 1) % len(species_images)

        # 顯示當前圖片
        current_image = species_images[st.session_state.image_index]
        img_response = requests.get(current_image["download_url"])

        if img_response.status_code == 200:
            image = Image.open(BytesIO(img_response.content))
            st.image(image, caption=f"第 {st.session_state.image_index + 1} 張，共 {len(species_images)} 張", use_column_width=True)

            if st.button("顯示答案"):
                st.success(f"答案是：{selected_species}")
        else:
            st.error("圖片載入失敗")
