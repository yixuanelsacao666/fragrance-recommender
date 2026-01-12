from flask import Flask, render_template, request, url_for
import sqlite3
import pandas as pd
import re
import os
from datetime import datetime

app = Flask(__name__)

# 数据库文件
DB_FILE = "fragrance_Internal.db"

# 图片文件夹路径（放在 static 里）
IMAGE_FOLDER = 'fragrance_internal_fig'  # 相对于 static/


# 连接数据库并读取为 DataFrame
def load_fragrances():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM fragrance", conn)  # 表名叫 fragrance
    conn.close()
    df['parsed_notes'] = df['sig_note'].apply(parse_notes)
    return df


def parse_notes(sig_note):
    if pd.isna(sig_note):
        return []
    notes = []
    matches = re.findall(r'(\w+|\w+\s\w+)\((\d+)%\)', sig_note)
    for note, percent in matches:
        notes.append((note.strip(), int(percent)))
    return notes


# Personality and scent mappings
personality_mapping = {
    'Confident 自信': {'attributes': ['男香', '中性香'], 'frag_types': ['木质东方调', '辛辣木质调', '芳香木质调', '黑胡椒']},
    'Elegent 优雅': {'attributes': ['女香', '中性香'], 'frag_types': ['花香调', '绿叶花香调', '花香东方调', '馥奇东方调', '馥奇调', '木质花香调', '芳香柑橘调']},
    'Sports 运动': {'attributes': ['男香', '中性香'], 'frag_types': ['辛辣芳香调', '芳香调', '果香花香调']},
    'Romantic 浪漫': {'attributes': ['女香', '中性香'], 'frag_types': ['花香调', '绿叶花香调', '玫瑰', '花香西普调', '花香东方调', '木质花香调']},
    'Humble 低调': {'attributes': ['中性香'], 'frag_types': ['木质调', '芳香调', '芳香柑橘调', '洋甘菊', '水生花香调']},
}

scent_categories = {
    'Citrus 柑橘': ['葡萄柚', '橘子', '香柠檬', '柠檬', '日本柚子', '橙子'],
    'Floral 花香': ['薰衣草', '茉莉', '玫瑰', '紫罗兰', '晚香玉', '风信子', '铃兰', '紫丁香', '牡丹'],
    'Woody 木质': ['雪松', '檀香木', '愈创木', '广藿香', '木质香', '干燥木头'],
    'Spicy 辛辣': ['肉桂', '胡椒', '粉红胡椒', '肉豆蔻'],
    'Sweet 甜香': ['香草', '零陵香豆', '琥珀', '安息香脂'],
    'Fruity 果香': ['梨', '桃子', '菠萝', '荔枝', '树莓', '曼多拉'],
}


# 根据香水名匹配图片
def find_image_for_perfume(name):
    static_path = os.path.join(app.static_folder, IMAGE_FOLDER)
    for img_file in os.listdir(static_path):
        if name in img_file:
            return os.path.join(IMAGE_FOLDER, img_file)  # 返回相对 static 路径
    return None


def recommend_fragrances(scent_prefs, personality, gender=None):
    df = load_fragrances()
    recommendations = []

    target_notes = []
    for scent in scent_prefs:
        target_notes.extend(scent_categories.get(scent, [scent]))

    target_attributes = personality_mapping.get(personality, {}).get('attributes', [])
    target_frag_types = personality_mapping.get(personality, {}).get('frag_types', [])

    for _, row in df.iterrows():
        score = 0
        matched_notes = []
        parsed_notes = row['parsed_notes']

        for note, percent in parsed_notes:
            if note in target_notes:
                score += percent
                matched_notes.append(note)

        if row['attribute'] in target_attributes:
            score += 20
        if row['frag_type'] in target_frag_types:
            score += 20

        if gender and row['attribute'] != gender and row['attribute'] != '中性香':
            continue

        if score > 0:
            itemcomment1 = str(row['itemcomment1']) if pd.notna(row['itemcomment1']) else "暂无评论"
            image_path = find_image_for_perfume(row['name'])
            recommendations.append({
                'brand': row['brand'],
                'name': row['name'],
                'frag_type': row['frag_type'],
                'sig_note': row['sig_note'],
                'attribute': row['attribute'],
                'itemcomment1': itemcomment1,
                'matched_notes': matched_notes,
                'score': score,
                'image_path': image_path
            })

    recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)[:5]
    return recommendations


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        scent_prefs = request.form.getlist('scent_prefs')
        personality = request.form.get('personality')
        gender = request.form.get('gender')

        if not scent_prefs or not personality:
            return render_template('index.html', error="请至少选择一种香味和一种性格特征")

        recommendations = recommend_fragrances(scent_prefs, personality, gender)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return render_template('results.html',
                               recommendations=recommendations,
                               timestamp=timestamp)

    return render_template('index.html',
                           scent_options=scent_categories.keys(),
                           personality_options=personality_mapping.keys())


if __name__ == '__main__':
    app.run(debug=True)
