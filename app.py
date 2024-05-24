# 导入必要的库
from flask import Flask, render_template, request, jsonify, session
import pymysql
import random

# 创建 Flask 应用实例
app = Flask(__name__)

# 为 Flask 会话设置一个密钥
app.secret_key = 'wordlearning'

# 函数用于建立数据库连接
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123456",  
        database="wordlearning"
    )

# 函数用于关闭数据库连接
def close_db(connection):
    if connection:
        connection.close()

# 主页路由
@app.route('/')
def index():
    """
    主页路由

    当用户访问网站主页时，返回单词学习的 HTML 页面。
    """
    return render_template('word_learning.html')
@app.route('/help')
def help_page():
    return render_template('Help.html')
# 启动学习流程的路由
@app.route('/start_learning', methods=['POST'])
def start_learning():
    db = connect_db()
    cursor = db.cursor()
    user_id = session.get('user_id', '2252086')  # 用实际的用户标识替换
    cursor.execute("SELECT Wordname FROM Words LIMIT 1")
    word = cursor.fetchone()
    cursor.execute("SELECT Familiarity FROM WordProgress WHERE Wordname = %s AND user_id = %s", (word, user_id))
    Fa = cursor.fetchone()
    cursor.execute("SELECT Expression FROM Expressions WHERE Wordname = %s", (word,))
    correct_definition = cursor.fetchone()
    # 获取其他错误释义
    cursor.execute("SELECT Expression FROM Expressions WHERE Wordname != %s ORDER BY RAND() LIMIT 2", (word,))
    wrong_definitions = cursor.fetchall()
    options = [correct_definition[0], wrong_definitions[0][0], wrong_definitions[1][0]]
    random.shuffle(options)
    close_db(db)
    if word:
        return jsonify({
            'word': word[0],
            'familiarity': Fa[0],
            'definitions': options,
            'correct_definition': correct_definition[0]
        })
    else:
        return jsonify({'error': '未找到单词'}), 404

@app.route('/wrongword_db', methods=['POST'])
def wrongword_db():
    db = connect_db()
    cursor = db.cursor()
    user_id = session.get('user_id', '2252086')  # 用实际的用户标识替换
    cursor.execute("SELECT Wordname FROM WordProgress WHERE (Familiarity = 0 OR Familiarity = 1) AND user_ID = %s LIMIT 1", (user_id,))
    word = cursor.fetchone()
    if not word:
        close_db(db)
        return jsonify({'error': '恭喜，目前暂无错题！'})
    cursor.execute("SELECT Familiarity FROM WordProgress WHERE Wordname = %s AND user_id = %s", (word, user_id))
    Fa = cursor.fetchone()
    cursor.execute("SELECT Expression FROM Expressions WHERE Wordname = %s", (word,))
    correct_definition = cursor.fetchone()
    # 获取其他错误释义
    cursor.execute("SELECT Expression FROM Expressions WHERE Wordname != %s ORDER BY RAND() LIMIT 2", (word,))
    wrong_definitions = cursor.fetchall()
    options = [correct_definition[0], wrong_definitions[0][0], wrong_definitions[1][0]]
    random.shuffle(options)
    close_db(db)
    if word:
        return jsonify({
            'word': word[0],
            'familiarity': Fa[0],
            'definitions': options,
            'correct_definition': correct_definition[0]
        })
    else:
        return jsonify({'error': '未找到单词'}), 404

# 获取下一个要学习的单词的路由
@app.route('/next_word', methods=['POST'])
def next_word():
    nowword = request.json.get('word')
    db = connect_db()
    cursor = db.cursor()
    user_id = session.get('user_id', '2252086')
    current_word=nowword
    cursor.execute("SELECT Wordname FROM Words ORDER BY Wordname")
    all_words = cursor.fetchall()
    all_words = [word[0] for word in all_words]

    if not all_words:
        close_db(db)
        return jsonify({'error': '未找到单词'}), 404

    if current_word is None:
        next_word = all_words[0]
    else:
        try:
            current_index = all_words.index(current_word)
            next_index = (current_index + 1) % len(all_words)
            next_word = all_words[next_index]
        except ValueError:
            next_word = all_words[0]

    session['current_word'] = next_word

    cursor.execute("SELECT PT FROM Words WHERE Wordname = %s", (next_word,))
    pt = cursor.fetchone()
    cursor.execute("SELECT Expression, ES FROM Expressions WHERE Wordname = %s", (next_word,))
    expressions = cursor.fetchall()
    cursor.execute("SELECT Familiarity FROM WordProgress WHERE Wordname = %s AND user_id = %s", (next_word, user_id))
    Fa = cursor.fetchone()

    # 获取正确释义
    cursor.execute("SELECT Expression FROM Expressions WHERE Wordname = %s", (next_word,))
    correct_definition = cursor.fetchone()

    # 获取其他错误释义
    cursor.execute("SELECT Expression FROM Expressions WHERE Wordname != %s ORDER BY RAND() LIMIT 2", (next_word,))
    wrong_definitions = cursor.fetchall()

    options = [correct_definition[0], wrong_definitions[0][0], wrong_definitions[1][0]]
    random.shuffle(options)

    close_db(db)
    if pt and expressions:
        return jsonify({
            'word': next_word,
            'PT': pt[0],
            'familiarity': Fa[0],
            'definitions': options,
            'correct_definition': correct_definition[0],
            'expressions': [{'expression': exp[0], 'es': exp[1]} for exp in expressions]
        })
    else:
        return jsonify({'error': '单词详情加载失败'}), 404
    
@app.route('/nextwrongword', methods=['POST'])
def nextwrongword():
    nowword = request.json.get('word')
    db = connect_db()
    cursor = db.cursor()
    user_id = session.get('user_id', '2252086')
    current_word=nowword
    cursor.execute("SELECT Wordname FROM WordProgress WHERE (Familiarity = 0 OR Familiarity = 1) AND user_ID = %s ORDER BY Wordname", (user_id,))
    all_words = cursor.fetchall()
    all_words = [word[0] for word in all_words]

    if not all_words:
        close_db(db)
        return jsonify({'error': '恭喜，目前暂无错题！'})

    if current_word is None:
        next_word = all_words[0]
    else:
        try:
            current_index = all_words.index(current_word)
            next_index = (current_index + 1) % len(all_words)
            next_word = all_words[next_index]
        except ValueError:
            next_word = all_words[0]

    session['current_word'] = next_word

    cursor.execute("SELECT PT FROM Words WHERE Wordname = %s", (next_word,))
    pt = cursor.fetchone()
    cursor.execute("SELECT Expression, ES FROM Expressions WHERE Wordname = %s", (next_word,))
    expressions = cursor.fetchall()
    cursor.execute("SELECT Familiarity FROM WordProgress WHERE Wordname = %s AND user_id = %s", (next_word, user_id))
    Fa = cursor.fetchone()

    # 获取正确释义
    cursor.execute("SELECT Expression FROM Expressions WHERE Wordname = %s", (next_word,))
    correct_definition = cursor.fetchone()

    # 获取其他错误释义
    cursor.execute("SELECT Expression FROM Expressions WHERE Wordname != %s ORDER BY RAND() LIMIT 2", (next_word,))
    wrong_definitions = cursor.fetchall()

    options = [correct_definition[0], wrong_definitions[0][0], wrong_definitions[1][0]]
    random.shuffle(options)

    close_db(db)
    if pt and expressions:
        return jsonify({
            'word': next_word,
            'PT': pt[0],
            'familiarity': Fa[0],
            'definitions': options,
            'correct_definition': correct_definition[0],
            'expressions': [{'expression': exp[0], 'es': exp[1]} for exp in expressions]
        })
    else:
        return jsonify({'error': '单词详情加载失败'}), 404


# 更新用户对单词的熟悉度的路由
@app.route('/update_familiarity', methods=['POST'])
def update_familiarity():
    data = request.get_json()
    word = data.get('word')
    correct_definition = data.get('correct_definition')
    selected_definition = data.get('selected_definition')

    if word is None or correct_definition is None or selected_definition is None:
        return jsonify({'error': '缺少参数'}), 400

    db = connect_db()
    cursor = db.cursor()
    user_id = session.get('user_id', '2252086')

    if selected_definition == correct_definition:
        cursor.execute("UPDATE WordProgress SET Familiarity = LEAST(Familiarity + 1, 2) WHERE user_id = %s AND Wordname = %s", (user_id, word))
    else:
        cursor.execute("UPDATE WordProgress SET Familiarity = GREATEST(Familiarity - 1, 0) WHERE user_id = %s AND Wordname = %s", (user_id, word))
    cursor.execute("SELECT Familiarity FROM WordProgress WHERE Wordname = %s AND user_id = %s", (word, user_id))
    Fa = cursor.fetchone()

    db.commit()
    close_db(db)
    return jsonify({
            'word' : word,
            'familiarity':Fa[0]
        })
    
# 搜索单词的路由
# 修改搜索单词的路由
@app.route('/search_word', methods=['POST'])
def search_word():
    data = request.get_json()
    search_word = data.get('word')

    if not search_word:
        return jsonify({'error': '缺少搜索词'}), 400

    db = connect_db()
    cursor = db.cursor()
    user_id = session.get('user_id', '2252086')  # 用实际的用户标识替换
    cursor.execute("SELECT w.Wordname, IFNULL(wp.Familiarity, 0) FROM Words w LEFT JOIN WordProgress wp ON w.Wordname = wp.Wordname AND wp.user_id = %s WHERE w.Wordname = %s",
                   (user_id, search_word))
    result = cursor.fetchone()
    close_db(db)

    if result:
        word_name = result[0]
        familiarity = result[1]
        return jsonify({'word': word_name, 'familiarity': familiarity})
    else:
        return jsonify({'error': '单词不存在'}), 404


# 获取单词详细信息的路由
@app.route('/get_word_details', methods=['GET'])
def get_word_details():
    """
    获取单词详细信息的路由

    当用户请求获取单词的详细信息时，从数据库中查找并返回单词的表达和例句。

    如果缺少单词参数，返回 JSON 响应包含错误信息和 400 状态码。
    如果找到单词详细信息，返回 JSON 响应包含表达和例句。
    如果未找到单词详细信息，返回 JSON 响应包含错误信息和 404 状态码。
    """
    word = request.args.get('word')

    if not word:
        return jsonify({'error': '缺少单词参数'}), 400

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT Expression, ES,ES_c FROM Expressions WHERE Wordname = %s", (word,))
    word_details = cursor.fetchone()
    cursor.execute("SELECT PT FROM Words WHERE Wordname = %s",(word,))
    word_PT = cursor.fetchone()
    close_db(db)

    if word_details:
        return jsonify({'PT': word_PT[0],'expression': word_details[0], 'example_sentence': word_details[1], 'example_sentence_c': word_details[2]})
    else:
        return jsonify({'error': '未找到单词详细信息'}), 404

if __name__ == '__main__':
    app.run(debug=True)