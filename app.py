from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import pymysql,base64,os,hashlib,random,json,time
from datetime import datetime
import os,string,traceback
from sqlalchemy import or_
from flask import send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '123'
@app.route('/getUserStarredArticles')
def get_user_starred_articles():
    connection = pymysql.connect(
    host="localhost",
    user="root",
    password="jyd",
    database="web_program"
    )
    user_id = session.get('user_id')
    if user_id:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT articles.title, articles.category, articles.id
            FROM articles
            INNER JOIN star_article ON articles.id = star_article.article_id
            WHERE star_article.user_id = %s
        """, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        articles = []
        for row in result:
            article = {
                'title': row[0],
                'category': row[1],
                'article_id': row[2]
            }
            articles.append(article)
        print(articles)
        return jsonify(articles)
    else:
        return jsonify({'error': 'User_id not found in session'})
@app.route('/checkUserStarred', methods=['POST','GET'])
def check_user_starred():
    connection = pymysql.connect(
    host="localhost",
    user="root",
    password="jyd",
    database="web_program"
    )
    user_id = session.get('user_id')
    article_id = session.get('article_id')
    # 在这里查询数据库，检查用户是否已经收藏了文章
    # 假设数据库中有名为 user_article 的表，存储了用户收藏的文章信息
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM star_article WHERE user_id = %s AND article_id = %s", (user_id, article_id))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return jsonify({'starred': True})
    else:
        return jsonify({'starred': False})
@app.route('/checkUserThumbed', methods=['POST','GET'])
def check_user_thumbed():
    connection = pymysql.connect(
    host="localhost",
    user="root",
    password="jyd",
    database="web_program"
    )
    user_id = session.get('user_id')
    article_id = session.get('article_id')
    # 在这里查询数据库，检查用户是否已经收藏了文章
    # 假设数据库中有名为 user_article 的表，存储了用户收藏的文章信息
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM thumb_article WHERE user_id = %s AND article_id = %s", (user_id, article_id))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return jsonify({'thumbed': True})
    else:
        return jsonify({'thumbed': False})
@app.route('/addThumbArticle', methods=['POST'])
def add_thumb_article():
    connection = pymysql.connect(
    host="localhost",
    user="root",
    password="jyd",
    database="web_program"
)
    user_id = session.get('user_id')
    article_id = session.get('article_id')
    try:
        with connection.cursor() as cursor:
            # 执行插入语句
            sql = "INSERT INTO thumb_article (user_id, article_id) VALUES (%s, %s)"
            cursor.execute(sql, (user_id, article_id))
        # 提交事务
        connection.commit()
        return jsonify({'message': 'Thumb article added successfully!'})
    except Exception as e:
        # 发生错误时回滚
        connection.rollback()
        return jsonify({'error': 'Error adding thumb article: ' + str(e)})

@app.route('/deleteThumbArticle', methods=['POST'])
def delete_thumb_article():
    connection = pymysql.connect(
    host="localhost",
    user="root",
    password="jyd",
    database="web_program"
)
    user_id = session.get('user_id')
    article_id = session.get('article_id')
    try:
        with connection.cursor() as cursor:
            # 执行删除语句
            sql = "DELETE FROM thumb_article WHERE user_id = %s AND article_id = %s"
            cursor.execute(sql, (user_id, article_id))
        # 提交事务
        connection.commit()
        return jsonify({'message': 'Thumb article deleted successfully!'})
    except Exception as e:
        # 发生错误时回滚
        connection.rollback()
        return jsonify({'error': 'Error deleting thumb article: ' + str(e)})
@app.route('/addStarArticle', methods=['POST'])
def add_star_article():
    connection = pymysql.connect(
    host="localhost",
    user="root",
    password="jyd",
    database="web_program"
)
    user_id = session.get('user_id')
    article_id = session.get('article_id')
    try:
        with connection.cursor() as cursor:
            # 执行插入语句
            sql = "INSERT INTO star_article (user_id, article_id) VALUES (%s, %s)"
            cursor.execute(sql, (user_id, article_id))
        # 提交事务
        connection.commit()
        return jsonify({'message': 'Star article added successfully!'})
    except Exception as e:
        # 发生错误时回滚
        connection.rollback()
        return jsonify({'error': 'Error adding star article: ' + str(e)})

@app.route('/deleteStarArticle', methods=['POST'])
def delete_star_article():
    connection = pymysql.connect(
    host="localhost",
    user="root",
    password="jyd",
    database="web_program"
)
    user_id = session.get('user_id')
    article_id = session.get('article_id')
    try:
        with connection.cursor() as cursor:
            # 执行删除语句
            sql = "DELETE FROM star_article WHERE user_id = %s AND article_id = %s"
            cursor.execute(sql, (user_id, article_id))
        # 提交事务
        connection.commit()
        return jsonify({'message': 'Star article deleted successfully!'})
    except Exception as e:
        # 发生错误时回滚
        connection.rollback()
        return jsonify({'error': 'Error deleting star article: ' + str(e)})
@app.route("/myFavourite", methods=['GET', 'POST'])
def myFavouritee():
    return render_template("myFavourite.html")
@app.route('/articlesDetail.html', methods=['GET'])
def show_article_detail():
    book_id = request.args.get('id')
    session['article_id']=book_id
    # 根据 book_id 获取相应的书籍详情
    # 然后渲染 articlesDetail.html 模板并返回
    return render_template('articlesDetail.html', book_id=book_id)
@app.route("/readingWelcome", methods=['GET', 'POST'])
def readingWelcome():
    return render_template("readingWelcome.html")
@app.route("/moreArticles", methods=['GET', 'POST'])
def moreArticles():
    return render_template("moreArticles.html")
@app.route("/articlesAdd", methods=['GET', 'POST'])
def rarticlesAdd():
    return render_template("articlesAdd.html")
# 记录操作日志(两个区块链函数)
# operation_type 操作类型 post_hash 文章哈希 comment_hash 评论哈希，不是评论操作为空
def record_operation(operation_name, operation_type, post_hash, comment_hash):
    tx_hash = session['contract'].functions.recordOperation(operation_type, post_hash, comment_hash).transact({
        'from': operation_name #这里是操作者
    })
    receipt = session['web3'].eth.wait_for_transaction_receipt(tx_hash)
    # print("Operation recorded:", receipt)

# 查看操作日志
def get_operations():
    count = session['contract'].caller().getOperationsCount()
    operations = []
    for i in range(count):
        operation = session['contract'].caller().getOperation(i)
        operations.append({
            'operator': operation[0],
            'operation_type': operation[1],
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(operation[2])),
            'post_hash': operation[3],
            'comment_hash': operation[4]
        })
    return operations

# 登录界面
# 功能：输入密码和用户名，实现home页跳转；还未注册，则可跳转到注册页
@app.route('/login', methods=['GET', 'POST'])
def login():
    """#区块链相关内容，登录界面执行一次即可
    # 连接到本地以太坊节点
    ganache_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    # 检查连接是否成功
    if web3.is_connected():
        print("Connected to Ethereum node")
    else:
        print("Failed to connect to Ethereum node")

    # 设置默认账户
    default_account = web3.eth.accounts[0]
    web3.eth.defaultAccount = default_account

    # 获取已部署合约的 ABI 和地址
    with open('build/contracts/OperationLog.json') as f:
        contract_data = json.load(f)

    abi = contract_data['abi']
    bytecode = contract_data['bytecode']
    Example = web3.eth.contract(abi=abi, bytecode=bytecode)
    hash = Example.constructor().transact({
        'from': default_account
    })
    tx_receipt = web3.eth.wait_for_transaction_receipt(hash)

    # contract_address = contract_data['networks']['5777']['address']
    # contract = web3.eth.contract(address=contract_address, abi=abi)
    contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    session['web3']=web3
    session['contract']=contract
    #区块链初始化结束"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="jyd",
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
                cursor.close()
                connection.close()
                return jsonify({'message': '登录成功'})
            else:
                # 验证失败，返回登录页面并显示错误信息
                error = "用户名或密码错误"
                cursor.close()
                connection.close()
                return jsonify({'error': error}) 
        else:
            # 用户不存在，返回登录页面并显示错误信息
            error = "用户名或密码错误"
            cursor.close()
            connection.close()
            return jsonify({'error': error}) 

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
            password="jyd",
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
        password="jyd",
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
        password="jyd",
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
        password="jyd",
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
        password="jyd",
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
        password="jyd",  
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
@app.route('/person')
def person_init():
    if session.get('username') is None:
        return redirect(url_for('login'))
    return render_template('person.html')

@app.route('/myblogs',methods=['GET','POST'])
def myblogs():
    # 连接本地的数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="jyd",
        database="web_program"
    )
    # 建立游标，用于后续的mysql操纵
    cursor = connection.cursor()
    if request.method == 'GET':
        query = "SELECT blogid, title, blogger, time FROM blogs WHERE blogger = %s ORDER BY time DESC"
        cursor.execute(query,session['username'])
        result = cursor.fetchall()
        return jsonify({'myblogs':result}),201
    # 关闭数据库连接
    cursor.close()
    connection.close()
    return render_template('person.html')

#论坛的帖子详情页，显示该帖子的时间，内容，评论等信息，以及上传评论功能
@app.route('/blog_info')
def blog_info_init():
    if session.get('username') is None:
        return redirect(url_for('login'))
    return render_template('blog_info.html')

@app.route('/bloginfo',methods=['GET','POST'])
def blogcomments():
    now=datetime.now()
    # 连接本地的数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="jyd",
        database="web_program"
    )
    if request.method=='GET':
        blog_id = request.args.get('blog_id')
        # 建立游标，用于后续的mysql操纵
        cursor = connection.cursor()
        query = "SELECT blogger,title,content,blogimage FROM blogs WHERE blogid = %s"
        cursor.execute(query, blog_id)
        result=cursor.fetchone()
        if not result[3]:
            blog={'blogger':result[0],'title':result[1],'content':result[2]}
        else:
            blog={'blogger':result[0],'title':result[1],'content':result[2],'image':base64.b64encode(result[3]).decode('utf-8')}
        query = "SELECT commenter,content FROM comments WHERE blogid = %s"
        cursor.execute(query, blog_id)
        comments=cursor.fetchall()
        # 关闭数据库连接
        cursor.close()
        connection.close()
        return jsonify({'blog':blog,'comments':comments})
    elif request.method=='POST':
        # 获取请求体中的数据（JSON 格式）  
        data = request.get_json()  
        # 从 JSON 数据中提取所需的字段  
        blog_id = data.get('blog_id')  
        content = data.get('comment')
        # 建立游标，用于后续的mysql操纵
        cursor = connection.cursor()
        query = "INSERT INTO comments (content,commenter,blogid,time) VALUES (%s, %s,%s,%s)"
        cursor.execute(query, (content,session['username'],blog_id,now))
        # 提交事务
        connection.commit()
        query = "SELECT commenter,content FROM comments WHERE blogid = %s"
        cursor.execute(query, blog_id)
        comments=cursor.fetchall()
        query = "SELECT content FROM blogs WHERE blogid = %s"
        cursor.execute(query, blog_id)
        blog_content=cursor.fetchone()
        comment_id=cursor.lastrowid
        # 关闭数据库连接
        cursor.close()
        connection.close()
        # 记录上传操作
        print(blog_id)
        hashed_blog=hashlib.sha256((str(blog_id)+"&"+blog_content[0]).encode()).hexdigest()
        hashed_comment = hashlib.sha256((str(comment_id)+"&"+content).encode()).hexdigest()
        #record_operation(session['username'], "upload", hashed_blog, hashed_comment)
        return jsonify({'comments':comments})
    return render_template('blog_info.html')

#论坛的帖子发布页，上传帖子标题与内容还有时间
@app.route('/upload',methods=['GET','POST'])
def uploadinit():
    if session.get('username') is None:
        return redirect(url_for('login'))
    return render_template('upload.html')

@app.route('/uploadblog',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        print(title)
        now=datetime.now()
        # 连接本地的数据库
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="jyd",
            database="web_program"
        )
        # 建立游标，用于后续的mysql操纵
        cursor = connection.cursor()
        # 将帖子信息导入到数据库
        if request.files.get('blogimage'):
            image_file=request.files['blogimage']
            image=image_file.read()
            query = "INSERT INTO blogs (title, content,blogger,time,blogimage) VALUES (%s, %s,%s,%s,%s)"
            cursor.execute(query, (title, content,session['username'],now,image))
        else:
            query = "INSERT INTO blogs (title, content,blogger,time) VALUES (%s, %s,%s,%s)"
            cursor.execute(query, (title, content,session['username'],now))
        # 提交事务
        connection.commit()
        blog_id=cursor.lastrowid
        # 关闭数据库连接
        cursor.close()
        connection.close()
        # 记录上传操作
        hashed_blog = hashlib.sha256((str(blog_id)+"&"+title+content).encode()).hexdigest()
        #record_operation(session['username'], "upload", hashed_blog, "")
        # 发布成功
        return jsonify({'success': True, 'message': '发布成功'}) ,200
    return render_template('upload.html')

#论坛首页，实现搜索功能和所有人的帖子展示
@app.route('/base')
def baseinit():
    if session.get('username') is None:
        return redirect(url_for('login'))
    return render_template('base.html')

@app.route('/allblogs',methods=['GET','POST'])
def all_blogs():
    # 连接本地的数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="jyd",
        database="web_program"
    )
    # 建立游标，用于后续的mysql操纵
    cursor = connection.cursor()
    if request.method == 'GET':
        query = "SELECT blogid, title, blogger, time FROM blogs ORDER BY time DESC"
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
        query = "SELECT blogid,title,blogger,time FROM blogs WHERE title LIKE %s"
        # 使用%作为通配符来匹配任意字符  
        cursor.execute(query, ('%{}%'.format(search_word),))
        result = cursor.fetchall()
        # 关闭数据库连接
        cursor.close()
        connection.close()
        return jsonify({'allblogs':result})
    return render_template('base.html')

# 允许所有域名跨域-解决同源策略问题
CORS(app, resources={r"/*": {"origins": "*"}})
# mysql://username:password@hostname:port/database_name
# 配置数据库访问 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{username}:{password}@{hostname}:{port}/{database_name}'.format(
    username='root',
    password='jyd',
    hostname='localhost',
    port=3306,
    database_name='web_program')
# 配置文件上传路径
app.config['UPLOAD_FOLDER'] = '/media/uploads'
# 配置访问秘钥
app.config['SECRET_KEY'] = '123'
# 创建数据库连接对象
db = SQLAlchemy(app)
# 设置静态文件目录
app.media_folder = 'media/uploads'
def all_params_present(**kwargs):
    """参数非空校验-所有参数都不为None或者空字符串，返回 True,否则返回 False"""
    print(kwargs.items())
    # 所有不符合要求的参数名
    keys: list = []
    for item in kwargs.items():
        if item[1] in [None, '']:
            keys.append(item[0])
    return not bool(len(keys)), keys
def array_sorted_by_order_ids(data_list, order_ids, prop='id'):
    """按顺序id排序的数组"""
    try:
        # 判断是否为数组
        if not isinstance(order_ids, list):
            order_ids = []
        # 使用字典来存储ID到索引的映射
        id_to_index = {item: index for index, item in enumerate(order_ids)}
        if len(order_ids) == 0:
            id_to_index = {item[prop]: index for index, item in enumerate(data_list)}
        # 根据指定的ID顺序重排列表
        return [item for _, item in sorted(enumerate(data_list), key=lambda x: id_to_index.get(x[1][prop]))]
    except Exception as e:
        print('sorted Exception', e)
        return data_list
class Articles(db.Model):
    """文章模型"""
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    cover = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(255), nullable=False)
    paragraphs_sort = db.Column(db.String(255), nullable=True)
    paragraphs_list = db.relationship('Paragraphs', backref='article', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return '<Articles %r>' % self.title

    # 列表
    def to_format(self):
        return {
            "id": self.id,
            "category": self.category,
            "coverUrl": request.host_url.rstrip('/') + self.cover if self.cover else None,
            "cover": self.cover,
            "title": self.title,
            "intro": self.intro,
            "createdAt": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    # 详情
    def to_format_info(self):
        order_ids = [] if self.paragraphs_sort is None else [int(i) for i in self.paragraphs_sort.split(',')]
        data_list = [i.to_format() for i in self.paragraphs_list]
        return {
            "id": self.id,
            "category": self.category,
            "coverUrl": request.host_url.rstrip('/') + self.cover if self.cover else None,
            "cover": self.cover,
            "title": self.title,
            "intro": self.intro,
            "paragraphsList": array_sorted_by_order_ids(data_list, order_ids),
            "createdAt": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Paragraphs(db.Model):
    """段落模型"""
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'))
    content_en = db.Column(db.Text, nullable=False)
    content_zh = db.Column(db.Text, nullable=False)
    word_en = db.Column(db.String(50), nullable=False)
    word_zh = db.Column(db.String(50), nullable=False)
    word_sample_en = db.Column(db.String(200), nullable=False)
    word_sample_zh = db.Column(db.String(200), nullable=False)
    picture = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Paragraphs %r>' % self.word_en

    # 列表
    def to_format(self):
        return {
            "id": self.id,
            "articleId": self.article_id,
            "contentEn": self.content_en,
            "contentZh": self.content_zh,
            "wordEn": self.word_en,
            "wordZh": self.word_zh,
            "wordSampleEn": self.word_sample_en,
            "wordSampleZh": self.word_sample_zh,
            "pictureUrl": request.host_url.rstrip('/') + self.picture if self.picture else None,
            "picture": self.picture,
        }

@app.route('/media/uploads/<path:filename>')
def send_static(filename):
    """开放媒体文件的访问"""
    return send_from_directory(app.media_folder, filename)


@app.route('/upload/image', methods=['POST','GET'])
def upload_image():
    """上传图片"""
    try:
        if 'file' not in request.files:
            return jsonify({
                "code": 400,
                "data": None,
                'msg': '找不到文件块'
            })

        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({
                "code": 400,
                "data": None,
                'msg': '未选择文件'
            })

        # 这里可以加文件类型判断逻辑
        # 生成随机字符串，防止图片名字重复
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        # 文件后缀名
        file_extension = file.filename.split(".")[-1] if '.' in file.filename else ''
        # 图片名称, 给图片重命名, 为了图片名称的唯一性
        filename = ran_str + '.' + file_extension
        basedir = os.path.abspath(os.path.dirname(__file__))  # 定义一个根目录 用于保存图片
        # 保存文件夹
        save_folder = basedir + app.config['UPLOAD_FOLDER']
        # 如果不存在该目录，则创建
        os.makedirs(save_folder, exist_ok=True)
        save_path = save_folder + '/' + filename
        file.save(save_path)
        image_path = "{public_path}/{filename}".format(
                    public_path=app.config["UPLOAD_FOLDER"],
                    filename=filename)
        image_url = request.host_url.rstrip('/') + image_path
        print(image_url)
        print(image_path)
        return jsonify({
            "code": 200,
            "data": {
                "imageUrl": image_url,
                "imagePath": image_path
            },
            "msg": "ok"
        })
    except Exception:
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "data": None,
            "msg": "系统错误"
        })


@app.route('/articles', methods=['GET'])
def get_articles_list():
    """获取文章列表"""
    try:
        keyword = request.args.get('keyword')
        category = request.args.get('category')
        # 构建一个查询来获取所有文章
        data = Articles.query.order_by(Articles.id.desc())
        if keyword:
            data = data.filter(
                or_(Articles.title.like('%{}%'.format(keyword)),
                    Articles.intro.like('%{}%'.format(keyword)))
            )
        if category:
            data = data.filter_by(category=category)
        data.all()
        return jsonify({
            "code": 200,
            "data": [article.to_format() for article in data],
            "msg": "ok"
        })
    except Exception:
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "data": None,
            "msg": "系统错误"
        })


@app.route('/articles/page', methods=['GET'])
def get_articles_list_page():
    """获取文章列表"""
    try:
        page_number = request.args.get('pageNumber', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        keyword = request.args.get('keyword')
        category = request.args.get('category')
        # 构建一个查询来获取所有文章
        data = Articles.query.order_by(Articles.id.desc())
        if keyword:
            data = data.filter(
                or_(Articles.title.like('%{}%'.format(keyword)),
                    Articles.intro.like('%{}%'.format(keyword)))
            )
        if category:
            data = data.filter_by(category=category)
        # 开始分页
        query_set = data.paginate(page=page_number, per_page=page_size)
        return jsonify({
            "code": 200,
            "data": {
                "data": [article.to_format() for article in query_set.items],
                "pageNumber": page_number,
                "pageSize": page_size,
                "pages": query_set.pages,
                "total": query_set.total
            },
            "msg": "ok"
        })
    except Exception:
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "data": None,
            "msg": "系统错误"
        })


@app.route('/articles/<int:article_id>', methods=['GET'])
def get_articles_info(article_id):
    """获取文章详情"""
    try:
        if article_id is None:
            return jsonify({
                "code": 400,
                "data": None,
                "msg": "ID参数错误"
            })
        # 构建一个查询来获取所有文章
        data = Articles.query.filter_by(id=article_id).first()
        if data is None:
            return jsonify({
                "code": 400,
                "data": None,
                "msg": "未找到相关记录"
            })
        return jsonify({
            "code": 200,
            "data": data.to_format_info(),
            "msg": "ok"
        })
    except Exception:
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "data": None,
            "msg": "系统错误"
        })


@app.route('/articles/edit/<int:article_id>', methods=['POST'])
def edit_articles(article_id):
    """编辑文章"""
    try:
        if article_id is None:
            return jsonify({
                "code": 400,
                "data": None,
                "msg": "ID参数错误"
            })
        # 构建一个查询来获取所有文章
        article = Articles.query.filter_by(id=article_id).first()
        if article is None:
            return jsonify({
                "code": 400,
                "data": None,
                "msg": "未找到相关记录"
            })
        # 提交的数据
        post_data = request.get_json()
        category = post_data.get('category')
        cover = post_data.get('cover')
        title = post_data.get('title')
        intro = post_data.get('intro')
        paragraphs_list = post_data.get('paragraphsList', [])
        v_result, err_keys = all_params_present(category=category, title=title, intro=intro)
        if not v_result:
            return jsonify({
                "code": 400,
                "data": None,
                "msg": "参数非空校验未通过，以下参数不能为空: {}".format(', '.join(err_keys))
            })
        # 更新文章
        article.category = category
        article.cover = cover
        article.title = title
        article.intro = intro
        # 原段落排序
        old_paragraphs_sort: list = article.paragraphs_sort.split(',')
        # 新段落排序
        paragraphs_sort = []
        for i in paragraphs_list:
            if i.get('id') is None:
                paragraph = Paragraphs(
                    article_id=article.id,
                    content_en=i['contentEn'],
                    content_zh=i['contentZh'],
                    word_en=i['wordEn'],
                    word_zh=i['wordZh'],
                    word_sample_en=i['wordSampleEn'],
                    word_sample_zh=i['wordSampleZh'],
                    picture=i['picture'])
                db.session.add(paragraph)
                # 提交事务
                db.session.commit()
                # 确保添加的是字符串类型的ID
                paragraphs_sort.append(str(paragraph.id))
            else:
                paragraph = Paragraphs.query.filter_by(id=i['id']).first()
                if paragraph is None:
                    continue
                # 更新段落
                paragraph.article_id = article.id
                paragraph.content_en = i['contentEn']
                paragraph.content_zh = i['contentZh']
                paragraph.word_en = i['wordEn']
                paragraph.word_zh = i['wordZh']
                paragraph.word_sample_en = i['wordSampleEn']
                paragraph.word_sample_zh = i['wordSampleZh']
                paragraph.picture = i['picture']
                # 提交事务
                db.session.commit()
                # 确保添加的是字符串类型的ID
                paragraphs_sort.append(str(i['id']))
        # 开始事务
        db.session.begin()
        # 删除段落
        for pid in old_paragraphs_sort:
            if pid not in paragraphs_sort:
                # 删除满足条件的段落，返回值是已删除记录的条数，int类型
                Paragraphs.query.filter_by(id=pid).delete()
                # 提交事务
                db.session.commit()
        # 更新段落排序
        article.paragraphs_sort = ','.join(paragraphs_sort)
        # 提交事务
        db.session.commit()

        return jsonify({
            "code": 200,
            "data": None,
            "msg": "ok"
        })
    except Exception:
        traceback.print_exc()
        # 回滚事务
        db.session.rollback()
        return jsonify({
            "code": 500,
            "data": None,
            "msg": "系统错误"
        })
    finally:
        # 确保在程序结束时关闭Session
        db.session.close()


@app.route('/articles/add', methods=['POST'])
def add_articles():
    """新增文章"""
    try:
        # 提交的数据
        post_data = request.get_json()
        category = post_data.get('category')
        cover = post_data.get('cover')
        title = post_data.get('title')
        intro = post_data.get('intro')
        v_result, err_keys = all_params_present(category=category, title=title, intro=intro)
        if not v_result:
            return jsonify({
                "code": 400,
                "data": None,
                "msg": "参数非空校验未通过，以下参数不能为空: {}".format(', '.join(err_keys))
            })
        paragraphs_list = post_data.get('paragraphsList', [])
        # 开始事务
        db.session.begin()
        article = Articles(category=category, cover=cover, title=title, intro=intro)
        db.session.add(article)
        # 提交事务
        db.session.commit()
        if len(paragraphs_list):
            paragraphs_sort = []
            paragraphs_models = []
            # 创建文章段落
            for i in paragraphs_list:
                paragraph = Paragraphs(
                    article_id=article.id,
                    content_en=i['contentEn'],
                    content_zh=i['contentZh'],
                    word_en=i['wordEn'],
                    word_zh=i['wordZh'],
                    word_sample_en=i['wordSampleEn'],
                    word_sample_zh=i['wordSampleZh'],
                    picture=i['picture'])
                paragraphs_models.append(paragraph)
            db.session.add_all(paragraphs_models)
            # 提交事务
            db.session.commit()
            # 获取文章段落排序
            for i in paragraphs_models:
                # 确保添加的是字符串类型的ID
                paragraphs_sort.append(str(i.id))

            # 更新段落排序
            article.paragraphs_sort = ','.join(paragraphs_sort)
            # 提交事务
            db.session.commit()

        return jsonify({
            "code": 200,
            "data": {
                "articleId": article.id
            },
            "msg": "ok"
        })
    except Exception as e:
        print('Exception', e)
        # 回滚事务
        db.session.rollback()
        return jsonify({
            "code": 500,
            "data": None,
            "msg": "系统错误"
        })
    finally:
        # 确保在程序结束时关闭Session
        db.session.close()


@app.route('/articles/del/<int:article_id>', methods=['DELETE'])
def del_articles(article_id):
    """删除文章"""
    try:
        if article_id is None:
            return jsonify({
                "code": 400,
                "data": None,
                "msg": "ID参数错误"
            })
        # 删除满足条件的文章，返回值是已删除记录的条数，int类型
        article = Articles.query.filter_by(id=article_id).delete()
        if article == 0:
            return jsonify({
                "code": 400,
                "data": None,
                "msg": "未找到相关记录"
            })
        # 删除满足条件的段落，返回值是已删除记录的条数，int类型
        Paragraphs.query.filter_by(article_id=article_id).delete()
        # 提交事务
        db.session.commit()
        return jsonify({
            "code": 200,
            "data": None,
            "msg": "ok"
        })
    except Exception:
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "data": None,
            "msg": "系统错误"
        })
    finally:
        # 确保在程序结束时关闭Session
        db.session.close()

if __name__ == '__main__':
    app.run(debug=True)