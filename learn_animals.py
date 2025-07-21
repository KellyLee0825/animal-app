import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import json

st.title("台灣動植物學習小遊戲 🐢🌿")
st.write("你知道這是什麼動植物嗎？先猜猜看，再點按鈕看看答案吧！")

# 讀取 image_list.json
with open('image_list.json', 'r', encoding='utf-8') as f:
    all_images = json.load(f)

# 使用 Session State 記錄目前索引
if 'index' not in st.session_state:
    st.session_state.index = 0

def show_image(index):
    item = all_images[index]
    img_url = item['url']
    species_name = item['species']

    # 下載圖片並顯示
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    st.image(img, caption="你猜得出來嗎？", use_container_width=True)

    if st.button("顯示答案"):
        st.success(f"答案是：{species_name}")

# 顯示目前圖片
show_image(st.session_state.index)

# 上一張、下一張按鈕
col1, col2 = st.columns(2)

with col1:
    if st.button("上一張"):
        if st.session_state.index > 0:
            st.session_state.index -= 1

with col2:
    if st.button("下一張"):
        if st.session_state.index < len(all_images) - 1:
            st.session_state.index += 1
