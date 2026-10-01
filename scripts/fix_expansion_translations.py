import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def to_ncr(text):
    return ''.join(f'&#{ord(c)};' if ord(c) > 127 else c for c in text)

def from_ncr(text):
    return re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)

# Mapping of text replacements (decoded text)
REPLACEMENTS = [
    # 1. 邊界擴張 (User's specific issue: city culture expansion)
    ('邊界擴充套件了!', '邊界擴張了!'),
    ('邊界擴充套件了！', '邊界擴張了！'),
    
    # 2. 領土、邊界與城市文化擴張 (Border & territory expansion)
    ('早期擴充套件城市的文化邊界', '早期擴張城市的文化邊界'),
    ('早期擴充套件城市邊界', '早期擴張城市邊界'),
    ('早期是擴充套件文明邊界的有效方法', '早期是擴張文明邊界的有效方法'),
    ('快速擴充套件文明邊界', '快速擴張文明邊界'),
    ('擴充套件文化邊界', '擴張文化邊界'),
    ('邊界通常立即擴充套件到', '邊界通常立即擴張到'),
    ('其邊界將向外擴充套件', '其邊界將向外擴張'),
    ('通常位於能擴充套件國界', '通常位於能擴張國界'),
    ('城市範圍隨之擴充套件', '城市範圍隨之擴大'),
    ('可能擴充套件到原屬城市範圍', '可能擴張到原屬城市範圍'),
    ('視野將擴充套件到', '視野將拓展到'),
    ('國家的不斷擴充套件', '國家的不斷擴張'),
    ('向北擴充套件', '向北擴張'),
    ('大擴充套件成為可能', '大幅擴張成為可能'),
    ('統治領域擴充套件到', '統治領域擴張到'),
    ('領土擴充套件到', '領土擴張到'),
    ('野心擴充套件他的疆土', '野心擴張他的疆土'),
    ('帝國擴充套件至歐洲', '帝國擴張至歐洲'),
    ('大大擴充套件的馬其頓', '大幅擴張的馬其頓'),
    ('城市的擴充套件', '城市的擴張'),
    
    # 3. 企業/商業拓展 (Corporation & Business spread)
    ('擴充套件公司業務', '拓展公司業務'),
    ('擴充套件業務', '拓展業務'),
    ('業務已擴充套件到', '業務已拓展到'),
    ('業務擴充套件到該城市', '業務拓展到該城市'),
    ('擴充套件相應公司的業務', '拓展相應公司的業務'),
    ('缺乏進一步擴充套件業務', '缺乏進一步拓展業務'),
    ('迅速擴充套件自己的業務', '迅速拓展自己的業務'),
    ('擴充套件%F2_RelIcon業務', '拓展%F2_RelIcon業務'),
    ('公司業務每擴充套件到', '公司業務每拓展到'),
    ('公司業務擴充套件至該城市', '公司業務拓展至該城市'),
    
    # 4. 領域、學術與介面擴展/延伸 (Scope, academic & interface expansion)
    ('商路將擴充套件到', '商路將拓展到'),
    ('文化擴充套件到了這片聖地', '文化擴展到了這片聖地'),
    ('很快地就擴充套件到古典藝術', '很快地就擴展到古典藝術'),
    ('一直擴充套件到北美西南部', '一直延伸到北美西南部'),
    ('水路不斷擴充套件', '水路不斷擴展'),
    ('控制力擴充套件到廣闊的地區', '控制力擴展到廣闊的地區'),
    ('將文明遊戲擴充套件到', '將文明遊戲擴展到'),
    ('應用範圍的擴充套件', '應用範圍的擴展'),
    ('用途就擴充套件到', '用途就擴展到'),
    ('介面進行了擴充套件', '介面進行了擴展'),
    ('有極大的擴充套件', '有極大的擴充'),
    
    # 5. OpenCC 過度轉換修復：內存在誤轉為記憶體在 (Bug from 内存 -> 記憶體)
    ('記憶體在', '內存在'),
    
    # 6. OpenCC 過度轉換修復：法律程序誤轉為法律程式 (Bug from 程序 -> 程式)
    ('法律正當程式', '法律正當程序'),
    ('正當程式條款', '正當程序條款'),

    # 7. 台灣用語優化：網絡 -> 網路
    ('帝國網絡', '帝國網路'),
    ('交通網絡', '交通網路'),
]

def apply_fixes():
    target_dirs = [
        os.path.join(ROOT, 'src'),
        os.path.join(ROOT, 'patch', 'PatchFiles'),
    ]

    ncr_pairs = [(to_ncr(old), to_ncr(new)) for old, new in REPLACEMENTS]

    total_files_modified = 0
    total_replacements = 0

    for base_dir in target_dirs:
        for root, dirs, files in os.walk(base_dir):
            for f in files:
                if f.endswith('.xml'):
                    p = os.path.join(root, f)
                    with open(p, 'r', encoding='ascii') as fp:
                        content = fp.read()

                    new_content = content
                    file_rep_count = 0
                    for old_ncr, new_ncr in ncr_pairs:
                        if old_ncr in new_content:
                            count = new_content.count(old_ncr)
                            new_content = new_content.replace(old_ncr, new_ncr)
                            file_rep_count += count

                    if file_rep_count > 0:
                        with open(p, 'w', encoding='ascii', newline='\r\n') as fp:
                            fp.write(new_content)
                        rel = os.path.relpath(p, ROOT)
                        print(f"[FIXED] {rel} ({file_rep_count} replacements)")
                        total_files_modified += 1
                        total_replacements += file_rep_count

    print(f"\nDone! Modified {total_files_modified} files with {total_replacements} replacements.")

if __name__ == '__main__':
    apply_fixes()
