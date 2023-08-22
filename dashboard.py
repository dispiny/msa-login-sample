# dashboard_service.py
from flask import Flask, request, jsonify
import redis
import argparse

app = Flask(__name__)

@app.route('/healthcheck')
def healthcheck():
    return {"code": 200, "msg": {"body": "this server is healthy", "status": "up"}}

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # 세션 확인 로직
    session_id = request.cookies.get('session_id')
    if session_id:
        username = redis_client.get(session_id)
        if username:
            return jsonify({'message': f'Welcome to the dashboard, {username.decode("utf-8")}!'})
    
    return jsonify({'message': 'Unauthorized'})

if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description='Delete all Redis session values.')
    parser.add_argument('-RedisHost', type=str, required=True, help='Redis server host')
    parser.add_argument('-RedisPort', type=int, default=6379, help='Redis server port (default: 6379)')
    parser.add_argument('-RedisAuth', type=str, default=None, help='Redis server Password')

    args = parser.parse_args()

    redis_client = redis.StrictRedis(host=args.RedisHost, port=args.RedisPort, password=args.RedisAuth, db=0)
    
    app.run(host='0.0.0.0', port=8081)
