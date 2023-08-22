# login_service.py
from flask import Flask, request, jsonify, redirect, url_for, make_response, render_template
import redis
import argparse
import uuid

app = Flask(__name__)

# 미리 생성한 계정 정보
user_info = {
    'root': 'P@ssword',
    'skills': 'SK11s125#',
}

@app.route('/healthcheck')
def healthcheck():
    return {"code": 200, "msg": {"body": "this server is healthy", "status": "up"}}

@app.route('/login', methods=['GET'])
def login_page():
    # 세션 ID를 쿠키에서 가져오기
    session_id = request.cookies.get('session_id')
    if session_id and redis_client.exists(session_id):
        # 이미 로그인되어 있으면 대시보드로 리다이렉
        # return redirect('http://127.0.0.1:8081/dashboard')
        return redirect(request.host_url + 'dashboard')
    else:
        # 로그인 페이지를 렌더링
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # 로그인 처리 로직
    username = request.form.get('username')
    password = request.form.get('password')

    if username in user_info and user_info[username] == password:
        # 로그인 성공 시 세션 정보를 Redis에 저장
        session_id = 'session_' + str(uuid.uuid4())
        redis_client.set(session_id, username)
        
        # 쿠키에 세션 정보 저장 및 대시보드로 리다이렉트
        # print(request.host_url + 'dashboard')
        response = make_response(redirect(request.host_url + 'dashboard'))
        # response = make_response(redirect('http://127.0.0.1:8081/dashboard'))
        response.set_cookie('session_id', session_id)
        return response
    else:
        return jsonify({'message': 'Login failed'})

@app.route('/logout', methods=['POST'])
def logout():
    # 로그아웃 처리 로직
    session_id = request.cookies.get('session_id')
    if session_id:
        redis_client.delete(session_id)
        
        # 쿠키에서 세션 정보 제거 및 로그인 페이지로 리다이렉트
        response = make_response(redirect(request.host_url + 'logout'))
        response.delete_cookie('session_id')
        return response
    else:
        return jsonify({'message': 'Logout failed'})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete all Redis session values.')
    parser.add_argument('-RedisHost', type=str, required=True, help='Redis server host')
    parser.add_argument('-RedisAuth', type=str, default=None, help='Redis server Password')
    parser.add_argument('-RedisPort', type=int, default=6379, help='Redis server port (default: 6379)')

    args = parser.parse_args()

    redis_client = redis.StrictRedis(host=args.RedisHost, port=args.RedisPort, password=args.RedisAuth, db=0)

    app.run(host='0.0.0.0', port=8080)
