import streamlit as st
import requests
import random

# JSON 位置
JSON_URL = "https://raw.githubusercontent.com/KellyLee0825/animal-app/master/image_list_generator/image_list.json"

@st.cache_data
def load_image_data():
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data_list = response.json()
        data_dict = {}
        for item in data_list:
            sp = item['species']
            url = item['url']
            if sp not in data_dict:
                data_dict[sp] = []
            data_dict[sp].append(url)
        return data_dict
    except Exception as e:
        st.error(f"讀取 JSON 時出錯: {e}")
        return None

data = load_image_data()

st.title("台灣動植物學習小遊戲 🐢🌿")

if data is None:
    st.error("無法載入圖片清單，請確認 image_list.json 是否存在且格式正確。")
else:
    # 把所有圖片攤平成 list，元素是 (species, img_url)
    all_images = []
    for species, urls in data.items():
        for url in urls:
            all_images.append((species, url))

    if "current_index" not in st.session_state:
        # 第一次先隨機選一張
        st.session_state.current_index = random.randint(0, len(all_images) - 1)
        st.session_state.show_answer = False

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if st.button("⬅️ 隨機上一張"):
            st.session_state.current_index = (st.session_state.current_index - 1) % len(all_images)
            st.session_state.show_answer = False

    with col3:
        if st.button("➡️ 隨機下一張"):
            st.session_state.current_index = (st.session_state.current_index + 1) % len(all_images)
            st.session_state.show_answer = False

    species, img_url = all_images[st.session_state.current_index]
    st.image(img_url, caption=f"猜猜這是什麼？（第 {st.session_state.current_index + 1} 張 / 共 {len(all_images)} 張）", use_container_width=True)

    if st.button("顯示答案"):
        st.session_state.show_answer = True

    if st.session_state.show_answer:
        st.success(f"答案是：{species}")
