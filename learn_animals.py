import streamlit as st
import os
import random
from PIL import Image

# 設定圖片資料夾根目錄
IMAGE_ROOT = r"https://raw.githubusercontent.com/KellyLee0825/animal-app/main/images"

st.title("台灣動植物學習小遊戲 🐢🌿")
st.write("你知道這是什麼動植物嗎？先猜猜看，再點按鈕看看答案吧！")

# 確認資料夾存在
if not os.path.exists(IMAGE_ROOT):
    st.error(f"找不到圖片資料夾：{IMAGE_ROOT}")
else:
    # 取得所有動植物資料夾（也就是名稱）
    species_list = [name for name in os.listdir(IMAGE_ROOT)
                    if os.path.isdir(os.path.join(IMAGE_ROOT, name))]

    if not species_list:
        st.warning("資料夾裡還沒有動植物圖片，請先放一些進來喔！")
    else:
        # 下拉選單選一種動植物（固定顯示哪一種）
        selected_species = st.selectbox("選擇一種動植物", species_list)

        # 該動植物的圖片路徑
        species_path = os.path.join(IMAGE_ROOT, selected_species)

        # 找出裡面的圖片（只支援 jpg、png）
        image_files = [f for f in os.listdir(species_path)
                       if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

        if not image_files:
            st.warning(f"這個動植物「{selected_species}」目前還沒有圖片")
        else:
            # 隨機選一張圖片
            selected_image_file = random.choice(image_files)
            image_path = os.path.join(species_path, selected_image_file)

            # 顯示圖片
            image = Image.open(image_path)
            st.image(image, caption="你猜得出來嗎？", use_column_width=True)

            # 按鈕顯示答案
            if st.button("顯示答案"):
                st.success(f"答案是：{selected_species}")
