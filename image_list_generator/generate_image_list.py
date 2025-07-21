import requests
import json

GITHUB_API_IMAGES_URL = "https://api.github.com/repos/KellyLee0825/animal-app/contents/images"
headers = {}

def get_folder_contents(url):
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise Exception(f"API 請求失敗，狀態碼: {res.status_code}")
    return res.json()

def gather_images(url, parent_folder=""):
    items = get_folder_contents(url)
    images = []
    for item in items:
        if item['type'] == 'file' and item['name'].lower().endswith(('.jpg', '.jpeg', '.png')):
            images.append({
                "species": parent_folder,
                "url": item['download_url']
            })
        elif item['type'] == 'dir':
            images += gather_images(item['url'], item['name'])
    return images

try:
    all_images = gather_images(GITHUB_API_IMAGES_URL)
    with open('image_list.json', 'w', encoding='utf-8') as f:
        json.dump(all_images, f, ensure_ascii=False, indent=2)
    print(f"總共找到 {len(all_images)} 張圖片，清單已儲存到 image_list.json")
except Exception as e:
    print("執行發生錯誤:", e)

input("按 Enter 結束")
