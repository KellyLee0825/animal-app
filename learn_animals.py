import streamlit as st
import requests

# JSON 位置
JSON_URL = "https://raw.githubusercontent.com/KellyLee0825/animal-app/master/image_list_generator/image_list.json"

@st.cache_data
def load_image_data():
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data_list = response.json()  # 讀取成 list
        # 轉換成 dict：{species: [url1, url2, ...]}
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
    species_list = list(data.keys())
    selected_species = st.selectbox("選擇一種動植物", species_list)

    images = data[selected_species]
    total = len(images)

    if "index" not in st.session_state:
        st.session_state.index = 0

    # 選擇動植物時，重設圖片索引
    if st.session_state.get("last_species") != selected_species:
        st.session_state.index = 0
        st.session_state.last_species = selected_species

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
