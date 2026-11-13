import os
import sys
import builtins

# ── 全域檔案 handle，由 setup_output() 開啟 ──────────────────────────────────
_tree_file = None


def dual_print(*args, **kwargs):
    """
    取代內建 print：
      - 螢幕：cp950 safe（encode errors='ignore'，字元無法顯示時靜默略過）
      - 檔案：UTF-8 完整寫入
    """
    text = ' '.join(str(a) for a in args)
    end  = kwargs.get('end', '\n')

    # --- 螢幕輸出 ---
    try:
        sys.stdout.write(text + end)
        sys.stdout.flush()
    except UnicodeEncodeError:
        safe = text.encode('cp950', errors='ignore').decode('cp950')
        sys.stdout.write(safe + end)
        sys.stdout.flush()

    # --- 檔案輸出（UTF-8）---
    if _tree_file and not _tree_file.closed:
        _tree_file.write(text + end)


def setup_output(filepath='tree.txt'):
    """開啟輸出檔案並以 dual_print 覆蓋內建 print。
    若 filepath 被占用（PermissionError），自動 fallback 到 tree_output.txt。
    """
    global _tree_file
    try:
        _tree_file = open(filepath, 'w', encoding='utf-8')
    except PermissionError:
        fallback = 'tree_output.txt'
        sys.stdout.write(f'[WARN] {filepath} 被占用，改用 {fallback}\n')
        sys.stdout.flush()
        _tree_file = open(fallback, 'w', encoding='utf-8')
        filepath = fallback  # 讓 teardown_output 顯示正確檔名
    builtins.print = dual_print
    return filepath


def teardown_output(filepath='tree.txt'):
    """關閉輸出檔案並還原內建 print。"""
    global _tree_file
    if _tree_file and not _tree_file.closed:
        _tree_file.close()
    builtins.print = builtins.__dict__.get('_original_print', dual_print)
    # 螢幕提示（直接用 sys.stdout 避免循環）
    sys.stdout.write(f'\n已輸出到 {filepath}\n')
    sys.stdout.flush()


# ── 核心功能（邏輯不變，移除 emoji）────────────────────────────────────────────

def list_files_tree(startpath):
    if not os.path.exists(startpath):
        print(f"[ERROR] 找不到路徑 '{startpath}'，請檢查是否輸入正確。")
        return

    print(f"\n正在讀取目錄結構: {startpath}")
    print("=" * 50)

    for root, dirs, files in os.walk(startpath):
        # 計算目錄深度以決定縮排
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)

        # 取得當前資料夾名稱
        folder_name = os.path.basename(root)
        if not folder_name:  # 處理路徑末尾斜線的情況
            folder_name = os.path.basename(os.path.dirname(root))

        print(f'{indent}[DIR]  {folder_name}/')

        # 顯示該目錄下的檔案
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{sub_indent}[FILE] {f}')


# ── 程式進入點 ────────────────────────────────────────────────────────────────

def main():
    OUTPUT_FILE = 'tree.txt'

    # 啟用雙輸出（同時寫螢幕 + tree.txt，若被占用自動 fallback）
    actual_file = setup_output(OUTPUT_FILE)

    try:
        print("=== Rossi's Directory Analyzer ===")
        user_path = input("請輸入或貼上資料夾路徑 (例如 E:\\xxx\\yyy): ").strip()

        # 移除使用者貼上路徑時可能帶有的雙引號
        clean_path = user_path.replace('"', '')

        list_files_tree(clean_path)
    finally:
        teardown_output(actual_file)


if __name__ == "__main__":
    main()
