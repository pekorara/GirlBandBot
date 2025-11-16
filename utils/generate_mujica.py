import asyncio

import aiohttp
import os
import json
from pathlib import Path
from config import GOOGLE_DRIVE_API_KEY, MUJICA_FOLDER_URL

""" 獲取資料夾 ID """
def get_folder_id(folder_url: str) -> str:
    try:
        return folder_url.split('/folders/')[1].split('?')[0]
    except Exception as e:
        raise ValueError(f"提取資料夾失敗: {str(e)}")

"""讀取 Google Drive 資料夾中的文件列表 """
async def list_folder_files(folder_id: str, api_key: str) -> list:
    query = f"'{folder_id}'+in+parents"
    fields = "files(id,name,mimeType),nextPageToken"
    page_size = 100
    
    all_files = []
    page_token = None
    
    try:
        async with aiohttp.ClientSession() as session:
            while True:
                api_url = f"https://www.googleapis.com/drive/v3/files?q={query}&fields={fields}&pageSize={page_size}&key={api_key}"

                if page_token:
                    api_url += f"&pageToken={page_token}"
                
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        files = data.get('files', [])
                        all_files.extend(files)
                        
                        page_token = data.get('nextPageToken')
                        if not page_token:
                            break
                        
                        print(f"已讀取 {len(all_files)} 個文件，繼續讀取下一頁...")
                    else:
                        error_text = await response.text()
                        raise ValueError(f"無法讀取資料夾 (狀態碼: {response.status})\n{error_text}")
        
        print(f"總共讀取 {len(all_files)} 個文件")
        return all_files
        
    except Exception as e:
        raise ValueError(f"讀取資料夾失敗: {str(e)}")

""" 產生有名稱跟ID的陣列 """
async def generate_list(folder_id: str, api_key: str = None) -> list:

    files = await list_folder_files(folder_id, api_key)
    
    result = []
    for file in files:
        mime_type = file.get('mimeType', '')
        file_id = file.get('id', '')
        file_name = file.get('name', '')
        
        if 'image' in mime_type and file_id:
            name_without_ext = os.path.splitext(file_name)[0]
            result.append({
                "alt": name_without_ext,
                "id": file_id
            })
    
    return result

"""保存為 json """
async def save_list_to_file(json_name:str):
    try:
        print("正在讀取 Google Drive 資料夾...")
        
        # 提取資料夾 ID
        folder_id = get_folder_id(MUJICA_FOLDER_URL)
        
        # 生成 list
        result = await generate_list(folder_id, GOOGLE_DRIVE_API_KEY)
        
        # 確保輸出資料夾存在
        out_dir = Path("../static") / "data"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{json_name}.json"

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"成功生成 {out_path}，包含 {len(result)} 張圖片")
        
    except Exception as e:
        print(f"生成 static/data/{json_name}.json 失敗: {str(e)}")


