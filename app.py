from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import pymysql,base64,os,hashlib,random

app = Flask(__name__)
app.secret_key = '123'

# 登录界面
# 功能：输入密码和用户名，实现home页跳转；还未注册，则可跳转到注册页
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="密码",
            database="web_program"
        )
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            # 获取数据库中存储的哈希密码
            hashed_password = result[2]
            # 对用户输入的密码进行哈希处理
            input_hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if hashed_password == input_hashed_password:
                # 验证通过，跳转到home页
                session["username"] = username
                session["user_id"]=result[0]
                return jsonify({'message': '登录成功'})
            else:
                # 验证失败，返回登录页面并显示错误信息
                error = "用户名或密码错误"
                return jsonify({'error': error}) 
        else:
            # 用户不存在，返回登录页面并显示错误信息
            error = "用户名或密码错误"
            return jsonify({'error': error}) 

        cursor.close()
        connection.close()

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # 清空会话中的用户名信息
    session.pop('user_id', None)
    return '退出登录成功'
# 注册界面
# 功能：输入用户的用户名、邮箱、密码和确认密码，对用户名是否存在、密码和确认密码是否匹配进行检查
# 若均正确，则跳转到登录界面，否则报错，并停留在该界面
@app.route("/register", methods=['GET', 'POST'])
def register():
    # 用户开始输入了
    if request.method == 'POST':
        # 用户输入用户名、邮箱、密码和确认密码
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        # 连接数据库
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="密码",
            database="web_program"
        )
        # 建立游标，用于后续的mysql操纵
        cursor = connection.cursor()
        # 检查用户名是否已存在
        query = "SELECT * FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        # 已存在，则报错并跳转回signin界面
        if result:
            error = "用户名已存在"
            return jsonify({'error': error}) 
        # 将用户名和密码导入到数据库
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        # 提交事务
        connection.commit()
        # 获取新用户的ID
        user_id = cursor.lastrowid
        
        # 从words表中获取所有的Wordname，并将新用户的ID与每个单词的名称和熟练度0一起插入到wordprogress表中
        query = "INSERT INTO wordprogress (user_id, Wordname, Familiarity) SELECT %s, Wordname, 0 FROM words"
        cursor.execute(query, (user_id,))
        # 提交事务
        connection.commit()
        # 关闭数据库连接
        cursor.close()
        connection.close()
        # 注册成功，跳转到登录页面
        return jsonify({'message': '注册成功'})
    return render_template("register.html")

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")
@app.route("/personal_web/<username>")
def personal_web(username):
    return render_template("person.html")

# 功能：从数据库中取得用户名为username的用户的信息，如果用户没有设置头像、个人信息，则有默认值
def execute_user_info(username):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="密码",
        database="web_program"
    )
    # 建立游标，用于后续的mysql操纵
    cursor = connection.cursor()
    cursor.execute("SELECT id,username, sex, signature,image,background FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        if user:
            if user[4] is not None and user[5] is not None:
                # image不为null时，进行base64编码
                user_info_dict = {'id':user[0],'username': user[1], 'sex': user[2], 'signature': user[3],
                                  'image': base64.b64encode(user[4]).decode('utf-8'),'background':base64.b64encode(user[5]).decode('utf-8')}
            elif user[5] is not None:
                # image为null时，设置默认头像
                with open('static/user.jpg', 'rb') as f:
                    default_image = f.read()
                user_info_dict = {'id':user[0],'username': user[1], 'sex': user[2], 'signature': user[3],
                                  'image': base64.b64encode(default_image).decode('utf-8'),'background':base64.b64encode(user[5]).decode('utf-8')}
            elif user[4] is not None:
                # image为null时，设置默认头像
                with open('static/bg.jpg', 'rb') as f:
                    default_image = f.read()
                user_info_dict = {'id':user[0],'username': user[1], 'sex': user[2], 'signature': user[3],
                                  'image': base64.b64encode(user[4]).decode('utf-8'),'background':base64.b64encode(default_image).decode('utf-8')}
            else:
                with open('static/user.jpg', 'rb') as f:
                    default_image_1 = f.read()
                with open('static/bg.jpg', 'rb') as f:
                    default_image_2 = f.read()
                user_info_dict = {'id':user[0],'username': user[1], 'sex': user[2], 'signature': user[3],
                                  'image': base64.b64encode(default_image_1).decode('utf-8'),'background':base64.b64encode(default_image_2).decode('utf-8')}
        return user_info_dict
    else:
        return None
# 存放用户名为username的用户的信息的网页
@app.route('/user_info/<username>', methods=['GET'])
def get_user_info(username):
    user_info_dict = execute_user_info(username)
    if user_info_dict:
        return jsonify(user_info_dict)
    else:
        return jsonify({"error": "没找到用户"}, 404)
# 接收更新用户个人主页信息的网页
@app.route('/update_data', methods=['POST'])
def update_data():
    # 连接到MySQL数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="密码",
        database="web_program"
    )
    cursor = connection.cursor()
    # 获取前端发送的数据
    data = request.get_json()
    # 接收对应的数据并保存到数据库
    username=data['username']
    sex = data['sex']
    signature = data['signature']
    # 执行更新操作
    query = "UPDATE users SET sex = %s, signature = %s WHERE username = %s"
    values = ( sex, signature,username)
    cursor.execute(query, values)
    connection.commit()
    # 关闭数据库连接
    cursor.close()
    connection.close()
    return '数据保存成功！'
# 接收用户更新头像的请求，并且将该数据保存到数据库中
@app.route("/uploadimage", methods=["POST"])
def uploadimage():
    # 连接到MySQL数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="密码",
        database="web_program"
    )
    username = request.form.get('username')
    image_file = request.files['image']
    cursor = connection.cursor()
    query = "UPDATE users SET image= %s WHERE username = %s"
    values = (image_file.read(), username)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return '数据保存成功！'
# 接收用户更新背景的请求，并且将该数据保存到数据库中
@app.route("/uploadbgimage", methods=["POST"])
def upload_bg_image():
    # 连接到MySQL数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="密码",
        database="web_program"
    )
    username = request.form.get('username')
    image_file = request.files['image']
    cursor = connection.cursor()
    query = "UPDATE users SET background= %s WHERE username = %s"
    values = (image_file.read(), username)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return '数据保存成功！'

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="密码",  
        database="web_program"
    )

# 函数用于关闭数据库连接
def close_db(connection):
    if connection:
        connection.close()

# 主页路由
@app.route('/word_learning')
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
    user_id = session.get('user_id')  # 用实际的用户标识替换
    print(user_id)
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
    user_id = session.get('user_id')  # 用实际的用户标识替换
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
    user_id = session.get('user_id')
    print(user_id)
    current_word=nowword
    print(current_word)
    cursor.execute("SELECT Wordname FROM Words ORDER BY Wordname")
    all_words = cursor.fetchall()
    all_words = [word[0] for word in all_words]
    print(all_words)
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
    print(next_word)
    cursor.execute("SELECT PT FROM Words WHERE Wordname = %s", (next_word,))
    pt = cursor.fetchone()
    cursor.execute("SELECT Expression, ES FROM Expressions WHERE Wordname = %s", (next_word,))
    expressions = cursor.fetchall()
    cursor.execute("SELECT Familiarity FROM WordProgress WHERE Wordname = %s AND user_id = %s", (next_word, user_id))
    Fa = cursor.fetchone()
    print(Fa)
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
    user_id = session.get('user_id')
    current_word=nowword
    cursor.execute("SELECT Wordname FROM WordProgress WHERE (Familiarity = 0 OR Familiarity = 1) AND user_id = %s ORDER BY Wordname", (user_id,))
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
    user_id = session.get('user_id')

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
    user_id = session.get('user_id')  # 用实际的用户标识替换
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

# 跳转到词书选择页
@app.route('/word_book_choose')
def word_book_choose():
    return render_template('word_book_choose.html')

#论坛的个人主页，显示该用户所有帖子的信息
@app.route('/person',methods=['GET'])
def person():
    user_info_dict = execute_user_info(session["username"])
    # 连接本地的数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="密码",
        database="web_program"
    )
    # 建立游标，用于后续的mysql操纵
    cursor = connection.cursor()
    query="SELECT title FROM blogs WHERE userid=%s"
    cursor.execute(query, (user_info_dict['id'],))
    result = cursor.fetchall()
    # 关闭数据库连接
    cursor.close()
    connection.close()
    return jsonify({'titles':result})

#论坛的帖子详情页，显示该帖子的时间，内容，评论等信息，以及上传评论功能
@app.route('/blog_info')
def blog_info():
    return render_template('blog_info.html')

@app.route('/bloginfo',methods=['GET','POST'])
def blogcomments():
    if session.get('username') is None:
        return jsonify({'success': False, 'message': '未登录'}),401
    blog_id = request.args.get('blog_id')
    # 连接本地的数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="密码",
        database="web_program"
    )
    if request.method=='GET':
        # 建立游标，用于后续的mysql操纵
        cursor = connection.cursor()
        query = "SELECT blogger,title,content,blogimage FROM blogs WHERE blogid = %s"
        cursor.execute(query, blog_id)
        result=cursor.fetchall()
        blog=(result[0][0],result[0][1],result[0][2],base64.b64encode(result[0][3]).decode('utf-8'))
        query = "SELECT commenter,content FROM comments WHERE blogid = %s"
        cursor.execute(query, blog_id)
        comments=cursor.fetchall()
        # 关闭数据库连接
        cursor.close()
        connection.close()
        return jsonify({'blog':blog,'comments':comments})
        
    return render_template('blog_info.html')

#论坛的帖子发布页，上传帖子标题与内容还有时间
@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        if session.get('username') is None:
            return jsonify({'success': False, 'message': '未登录'}),401
        user_info_dict = execute_user_info(session["username"])
        title=request.form['title']
        content=request.form['content']
        now=datetime.now()
        # 连接本地的数据库
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="密码",
            database="web_program"
        )
        # 建立游标，用于后续的mysql操纵
        cursor = connection.cursor()
        # 将帖子信息导入到数据库
        if request.files.get('blogimage'):
            image_file=request.files['blogimage']
            image=image_file.read()
            query = "INSERT INTO blogs (title, content,userid,time,blogimage) VALUES (%s, %s,%s,%s,%s)"
            cursor.execute(query, (title, content,user_info_dict['id'],now,image))
        else:
            query = "INSERT INTO blogs (title, content,userid,time) VALUES (%s, %s,%s,%s)"
            cursor.execute(query, (title, content,user_info_dict['id'],now))
        # 提交事务
        connection.commit()
        # 关闭数据库连接
        cursor.close()
        connection.close()
        # 发布成功
        return jsonify({'success': True, 'message': '发布成功'}) ,200
    return render_template('upload.html')

#论坛首页，实现搜索功能和所有人的帖子展示
@app.route('/base')
def baseinit():
    return render_template('base.html')

@app.route('/allblogs',methods=['GET','POST'])
def all_blogs():
    if session.get('username') is None:
        return jsonify({'success': False, 'message': '未登录'}),401
    # 连接本地的数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="密码",
        database="web_program"
    )
    # 建立游标，用于后续的mysql操纵
    cursor = connection.cursor()
    if request.method == 'GET':
        query="SELECT blogs.blogid,blogs.title,users.username,blogs.time FROM blogs natural join users"
        cursor.execute(query)
        result = cursor.fetchall()
        # 关闭数据库连接
        cursor.close()
        connection.close()
        return jsonify({'allblogs':result})
    elif request.method == 'POST':
        data = request.get_json()
        search_word = data.get('keyword')
        # 在标题中搜索包含关键词的帖子  
        query = "SELECT blogs.blogid,blogs.title,users.username,blogs.time FROM blogs natural join users WHERE blogs.title LIKE %s"
        # 使用%作为通配符来匹配任意字符  
        cursor.execute(query, ('%{}%'.format(search_word),))
        result = cursor.fetchall()
        # 关闭数据库连接
        cursor.close()
        connection.close()
        return jsonify({'allblogs':result})
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)