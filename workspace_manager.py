import os
import shutil
import hashlib
from datetime import datetime

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def organize_workspace(base_path, protected_list):
    # 擴充分類字典，加入 HR 與行政類別
    file_map = {
        'Code_Scripts': ['.c', '.cpp', '.py', '.js', '.sh', '.v', '.h', '.cs', '.html', '.makefile'],
        'Docs_Technical': ['.pdf', '.md'], # 專門放技術規格書
        'Personal_HR': ['.doc', '.docx', '.ppt', '.pptx', '.txt', '.rtf'], # 錄取通知、合約、規章
        'Data_Validation': ['.xls', '.xlsx', '.csv', '.log', '.bin', '.json'],
        'Media_Videos': ['.mp4', '.mov', '.avi'],
        'Archives': ['.zip', '.7z', '.tar', '.gz']
    }

    # 關鍵字分類邏輯 (優先於副檔名)
    hr_keywords = ['錄取', '通知', '薪資', '薪資單', '體檢', '補助', '合約', '新人', '考績', '分紅', '福利', 'welfare', 'offer']

    if not os.path.exists(base_path):
        print(f"Error: 路徑 {base_path} 不存在")
        return

    all_hashes = {}
    folders = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    for folder in folders:
        if any(p in folder for p in protected_list):
            print(f"跳過受保護目錄: {folder}")
            continue

        folder_path = os.path.join(base_path, folder)
        print(f"正在整理: {folder}")
        
        # 抓取公司名作為前綴
        company_prefix = folder.split('.')[-1].strip()

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            if os.path.isfile(item_path):
                f_hash = get_file_hash(item_path)
                if f_hash:
                    all_hashes.setdefault(f_hash, []).append(item_path)

                file_name_lower = item.lower()
                ext = os.path.splitext(file_name_lower)[1]
                target_sub = "Others"
                new_name = item

                # 1. 優先處理「截圖與照片」
                if any(x in file_name_lower for x in ["screenshot", "img_", "capture", "microsoftteams-image"]):
                    target_sub = "Screenshots"
                    new_name = f"{company_prefix}_SS_{item}"
                
                # 2. 處理「個人 HR 與行政文件」 (根據關鍵字)
                elif any(key in file_name_lower for key in hr_keywords):
                    target_sub = "Personal_HR"
                
                # 3. 根據副檔名進行一般分類
                else:
                    for sub, exts in file_map.items():
                        if ext in exts:
                            target_sub = sub
                            break

                # 執行搬移
                target_dir = os.path.join(folder_path, target_sub)
                os.makedirs(target_dir, exist_ok=True)
                
                try:
                    dst_path = os.path.join(target_dir, new_name)
                    # 避免同名覆蓋
                    if os.path.exists(dst_path):
                        count = 1
                        name_part, ext_part = os.path.splitext(new_name)
                        while os.path.exists(dst_path):
                            dst_path = os.path.join(target_dir, f"{name_part}_{count}{ext_part}")
                            count += 1
                    shutil.move(item_path, dst_path)
                except Exception as e:
                    print(f"移動失敗 {item}: {e}")

    # 生成報告... (省略同前)

# --- 設定區 ---
target_path = r"E:\工作" 
my_protected_projects = ["Gaudi 2", "Gaudi 3", "Aura", "HLS Downloader", "Claude Code"]

organize_workspace(target_path, my_protected_projects)