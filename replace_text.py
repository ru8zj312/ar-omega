import os

# --- 設定 ---
target_directory = 'docs/wiki'             # 要處理的資料夾名稱
string_to_find = '/wiki/'            # 要尋找的字串
string_to_replace = '/ar-omega/wiki/' # 要替換成的新字串
# --- 結束設定 ---

# 檢查目標資料夾是否存在
if not os.path.isdir(target_directory):
    print(f"錯誤：找不到資料夾 '{target_directory}'")
    exit()

print(f"開始處理資料夾 '{target_directory}' 中的 .md 檔案...")

# 遍歷資料夾中的所有檔案
for filename in os.listdir(target_directory):
    # 檢查檔案是否以 .md 結尾
    if filename.endswith('.md'):
        # 組合完整的檔案路徑
        file_path = os.path.join(target_directory, filename)
        
        try:
            # --- 讀取檔案 ---
            # 使用 'with' 可以確保檔案在使用後會自動關閉
            # 使用 encoding='utf-8' 來處理中文字或特殊字元，這是個好習慣
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # --- 檢查並替換內容 ---
            # 如果內容有變化，才需要寫入，這樣更有效率
            if string_to_find in content:
                new_content = content.replace(string_to_find, string_to_replace)

                # --- 寫回檔案 ---
                # 使用 'w' 模式會覆蓋整個檔案
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                
                print(f"已處理：{filename}")
            else:
                print(f"跳過（內容不需變更）：{filename}")

        except Exception as e:
            print(f"處理檔案 {filename} 時發生錯誤：{e}")

print("\n處理完成！")