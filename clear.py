import redis
import argparse

def delete_all_sessions(host, port, password):
    redis_client = redis.StrictRedis(host=host, port=port, password=password, db=0)  # Redis 호스트 및 포트 설정
    keys = redis_client.flushdb()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Delete all Redis session values.')
    parser.add_argument('-RedisHost', type=str, required=True, help='Redis server host')
    parser.add_argument('-RedisPort', type=int, default=6379, help='Redis server port (default: 6379)')
    parser.add_argument('-RedisAuth', type=str, default=None, help='Redis server Password')

    args = parser.parse_args()
    delete_all_sessions(args.RedisHost, args.RedisPort, args.RedisAuth)
