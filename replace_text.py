import os
import re # 匯入正規表示式模組

# --- 設定 ---
target_directory = 'docs/wiki'             # 要處理的資料夾名稱
index_file_path = 'docs/index.md'          # 要更新連結的 index.md 檔案路徑
string_to_find = '/wiki/'                  # 要尋找的字串
string_to_replace = '/ar-omega/wiki/'      # 要替換成的新字串
# --- 結束設定 ---

# --- 第一階段：掃描 wiki 資料夾，替換字串並建立「權威清單」 ---

# 檢查目標資料夾是否存在
if not os.path.isdir(target_directory):
    print(f"錯誤：找不到資料夾 '{target_directory}'")
    exit()

print(f"--- 第一階段：開始處理資料夾 '{target_directory}' ---")

# 建立一個集合(set)來儲存所有實際存在的 .md 檔案名稱 (不含副檔名)
# 使用集合可以快速查找，且自動處理重複
existing_wiki_pages = set()

# 遍歷資料夾中的所有檔案
for filename in os.listdir(target_directory):
    if filename.endswith('.md'):
        file_path = os.path.join(target_directory, filename)
        
        try:
            # 讀取檔案
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 檢查並替換內容
            if string_to_find in content:
                new_content = content.replace(string_to_find, string_to_replace)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"已處理（內容已替換）：{filename}")
            else:
                print(f"跳過（內容不需變更）：{filename}")

            # 將確認存在的檔案名稱（不含 .md）加入權威清單
            page_name = os.path.splitext(filename)[0]
            existing_wiki_pages.add(page_name)

        except Exception as e:
            print(f"處理檔案 {filename} 時發生錯誤：{e}")

print(f"\n'{target_directory}' 資料夾處理完成，共找到 {len(existing_wiki_pages)} 個有效頁面。")
print("-" * 40)


# --- 第二階段：清理 index.md 中的過時連結 ---

print(f"--- 第二階段：開始清理 '{index_file_path}' 的過時連結 ---")

# 檢查 index.md 是否存在
if not os.path.isfile(index_file_path):
    print(f"錯誤：找不到索引檔案 '{index_file_path}'")
    exit()

try:
    with open(index_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []
    stale_links_removed_count = 0
    # 定義用來匹配 wiki 連結的正規表示式
    # 它會捕捉 [連結文字](.../檔案名稱) 中的 "檔案名稱" 部分
    link_pattern = re.compile(r'\[.*?\]\(' + re.escape(string_to_replace) + r'([^)]+)\)')

    for line in lines:
        match = link_pattern.search(line)
        if match:
            # 如果這行有 wiki 連結，就檢查它是否有效
            linked_page_name = match.group(1) # 取得連結指向的檔案名稱
            if linked_page_name in existing_wiki_pages:
                cleaned_lines.append(line) # 連結有效，保留此行
            else:
                # 連結無效 (檔案已不存在)，捨棄此行
                print(f"  - 已移除過時連結：{line.strip()}")
                stale_links_removed_count += 1
        else:
            # 如果這行沒有 wiki 連結，直接保留
            cleaned_lines.append(line)
    
    if stale_links_removed_count > 0:
        # 如果有移除連結，才需要寫回檔案
        with open(index_file_path, 'w', encoding='utf-8') as file:
            file.writelines(cleaned_lines)
        print(f"\n清理完成，共移除了 {stale_links_removed_count} 個過時連結。")
    else:
        print("索引檔案中沒有需要移除的過時連結。")

except Exception as e:
    print(f"清理索引檔案 '{index_file_path}' 時發生錯誤：{e}")

print("-" * 40)


# --- 第三階段：在 index.md 中新增遺漏的連結 ---

print(f"--- 第三階段：開始新增遺漏連結至 '{index_file_path}' ---")

try:
    # 重新讀取可能已被清理過的 index.md 內容
    with open(index_file_path, 'r', encoding='utf-8') as file:
        index_content = file.read()

    links_to_add = []
    for page_name in sorted(list(existing_wiki_pages)): # 排序以確保每次新增順序一致
        # 產生標準的 Markdown 連結格式
        markdown_link = f"[{page_name}]({string_to_replace}{page_name})"
        # 檢查連結是否已存在於檔案內容中
        if markdown_link not in index_content:
            links_to_add.append(markdown_link)

    if links_to_add:
        print(f"發現 {len(links_to_add)} 個新連結，將新增至檔案末尾：")
        
        with open(index_file_path, 'a', encoding='utf-8') as file:
            # 確保檔案末尾是新的一行
            if not index_content.endswith('\n\n') and index_content.strip() != '':
                file.write('\n') # 如果結尾不是空的，加一個換行
            
            for link in links_to_add:
                file.write(link + '\n')
                print(f"  - 已新增：{link}")
        
        print(f"\n成功更新 '{index_file_path}'！")
    else:
        print(f"'{index_file_path}' 內容已是最新，無需新增連結。")

except Exception as e:
    print(f"新增連結至 '{index_file_path}' 時發生錯誤：{e}")

print("\n\n=== 全部處理完成！ ===")