import json
import wget

if __name__ == '__main__':
    user2audio = []
    with open('data/user2audio.json', encoding='utf8') as f:
        user2audio = json.loads(f.read())
    for item in user2audio:
        print(wget.download('http://'+item['audio_src'], out='data/'))
        break