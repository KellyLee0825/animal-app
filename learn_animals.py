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

# 取得 images 資料夾內容（裡面每一個是物種名稱）
contents = get_github_folder_contents(REPO_API_URL)
species_dirs = [item for item in contents if item['type'] == 'dir']

all_images = []

# 每個物種資料夾內，收集圖片
for species in species_dirs:
    species_name = species['name']
    species_url = f"{REPO_API_URL}/{species_name}"
    species_contents = get_github_folder_contents(species_url)

    image_files = [item for item in species_contents
                   if item['type'] == 'file' and
                   item['name'].lower().endswith(('.jpg', '.jpeg', '.png'))]

    for img in image_files:
        all_images.append({
            'species': species_name,
            'url': img['download_url']
        })

if not all_images:
    st.warning("目前找不到任何圖片，請確認 GitHub 的 images 資料夾裡有子資料夾和圖片")
    st.stop()

# 初始化 session_state，紀錄目前索引和答案顯示狀態
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

def show_image(idx):
    selected = all_images[idx]
    img_response = requests.get(selected['url'])
    image = Image.open(BytesIO(img_response.content))
    st.image(image, caption="你猜得出來嗎？", use_container_width=True)

    if st.session_state.show_answer:
        st.success(f"答案是：{selected['species']}")

def next_image():
    if st.session_state.current_idx < len(all_images) - 1:
        st.session_state.current_idx += 1
    st.session_state.show_answer = False

def prev_image():
    if st.session_state.current_idx > 0:
        st.session_state.current_idx -= 1
    st.session_state.show_answer = False

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("上一張"):
        prev_image()

with col2:
    if st.button("顯示答案"):
        st.session_state.show_answer = True

with col3:
    if st.button("下一張"):
        next_image()

# 顯示當前圖片
show_image(st.session_state.current_idx)

# 顯示目前進度
st.write(f"第 {st.session_state.current_idx + 1} 張，共 {len(all_images)} 張")
