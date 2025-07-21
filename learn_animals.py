import streamlit as st
import requests
import json

# JSON 位置 
JSON_URL = "https://raw.githubusercontent.com/KellyLee0825/animal-app/master/image_list_generator/image_list.json"


# 讀取圖片清單
@st.cache_data
def load_image_data():
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        return response.json()
    except:
        return None

data = load_image_data()

st.title("台灣動植物學習小遊戲 🐢🌿")

if data is None:
    st.error("無法載入圖片清單，請確認 image_list.json 是否存在且格式正確。")
else:
    species_list = list(data.keys())
    selected_species = st.selectbox("選擇一種動植物", species_list)

    images = data[selected_species]
    total = len(images)

    if "index" not in st.session_state:
        st.session_state.index = 0

    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("⬅️ 上一張") and st.session_state.index > 0:
            st.session_state.index -= 1
    with col3:
        if st.button("➡️ 下一張") and st.session_state.index < total - 1:
            st.session_state.index += 1

    img_url = images[st.session_state.index]
    st.image(img_url, caption=f"{selected_species}（第 {st.session_state.index + 1} 張 / 共 {total} 張）", use_column_width=True)

    if st.button("顯示答案"):
        st.success(f"答案是：{selected_species}")