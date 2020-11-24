import re

from flask import Flask, request, json

import setting
from user import User

app = Flask(__name__)
#  <Config {'ENV': 'development', 'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SECRET_KEY': None, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=31), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'session', 'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(seconds=43200), 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'JSON_AS_ASCII': True, 'JSON_SORT_KEYS': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'JSONIFY_MIMETYPE': 'application/json', 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093}>
print(app.config)
# ①读取配置文件
app.config.from_object(setting)


# app.config['ENV'] = 'development'  # 配置环境


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test')
def test():
    return 'test'


#                ②app.route 装饰器
#     def route(self, rule, **options):
#         def decorator(f):
#             endpoint = options.pop("endpoint", None)
#             self.add_url_rule(rule, endpoint, f, **options)
#             return f
#         return decorator
# =======等于========
def testSame():
    return 'xxxx'


app.add_url_rule('/add', view_func=testSame)

data = {'sz': '苏州', 'xz': '徐州'}


# 获取get和post的数据
# <key>就是默认的str
# <int:key> key的type是int
# float、path、uuid


@app.route('/get/getCity/<key>')
def getCity(key):
    return data.get(key)


# 重定向
# /get/ 既可以匹配/get/ 也可以/get

# response
# str content-type=application:text/html;charset=utf-8
# dict content-type=application:json;charset=utf-8
# turple 元组 返回是(内容，状态码)
@app.route('/get/getTruple')
def getTruple():
    return "Truple", 200


@app.route('/get/getUser')
def getUser():
    user = User("ww", 15)
    return user


# endpoint
# request
# app.py和模板的结合使用
# render_template 可以读取html文件变成字符串返回给前端
users = []


@app.route('/add/addUser', methods=['GET', 'POST'])
def addUser():
    # request.args get请求 获取dict类型
    # request.form post请求 form格式
    # request.form post请求 form格式
    if request.method == 'GET':
        name = request.args.get('name')
        age = request.args.get('age')
        users.append({"name": name, "age": age, "method": request.method})
    elif request.method == 'POST':
        print(request.content_type)
        s = str(request.content_type)
        if request.content_type == 'application:json':
            # raw 格式 application:json
            name = request.form['name']
            age = request.form['age']
            users.append({"name": name, "age": age, "method": request.method})
        elif re.search(r'(multipart/form-data).*', s) is not None:
            # form表单
            name = request.form.get('name')
            age = request.form.get('age')
            users.append({"name": name, "age": age, "method": request.method})
    return json.dumps(users)


# def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
# debug：none 代码不会热部署  true 热部署
if __name__ == '__main__':
    app.run(port=8000)
