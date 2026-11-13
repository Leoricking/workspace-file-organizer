# Workspace File Organizer

兩支 Python 工具，分別用來匯出目錄結構，以及依檔名關鍵字和副檔名整理工作檔案。兩支腳本皆使用 Python 3 標準函式庫。

| 腳本 | 用途 |
| --- | --- |
| `find_directory_tree.py` | 遞迴列出資料夾與檔案名稱，並將目錄樹輸出為 UTF-8 文字檔。 |
| `workspace_manager.py` | 對指定根目錄下各個第一層子資料夾內的直屬檔案進行分類與搬移。 |

## 匯出目錄樹

在專案資料夾的 Windows PowerShell 執行以下指令，接著輸入要掃描的路徑，例如 `E:\工作`。

```powershell
python .\find_directory_tree.py
```

程式會在終端機顯示掃描結果，並在目前工作目錄寫入 `tree.txt`。每次執行會重新寫入輸出。若 `tree.txt` 無法以寫入模式開啟且回報權限錯誤，程式會改寫 `tree_output.txt`。輸出包含檔名和資料夾名稱，分享前請先檢查內容。

## 依規則整理檔案

1. 開啟 `workspace_manager.py`，將檔尾的 `target_path` 改為要整理的根目錄。程式會掃描根目錄下的第一層子資料夾，逐一處理每個子資料夾中的直屬檔案。
2. 視需要調整 `my_protected_projects`。第一層子資料夾名稱只要包含清單中的任一字串，就會跳過。比對區分大小寫。
3. 先用測試副本執行。現有版本會直接搬移檔案，沒有預覽或復原功能。

```powershell
python .\workspace_manager.py
```

分類順序為截圖檔名關鍵字、HR／行政檔名關鍵字、最後依副檔名判斷。目的地位於檔案所屬的第一層子資料夾內，例如 `Screenshots/`、`Personal_HR/`、`Code_Scripts/` 或 `Media_Videos/`。未符合規則的檔案會移入 `Others/`。目的地有同名檔案時，程式會在檔名加上數字尾碼。截圖類檔案會另加來源資料夾衍生的前綴。

## 後續規劃

規劃加入搬移前預覽，並依人工確認的範例學習主題分類，例如將蝶式陸上練習影片歸入 `游泳/蝶式/`，將手機運鏡教學歸入 `拍攝技巧/運鏡/`。現有版本依檔名關鍵字及副檔名判斷。

目錄掃描結果、`Split_Results/`、專案壓縮檔和本機截圖可留在本機。
