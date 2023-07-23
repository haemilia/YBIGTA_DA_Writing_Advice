import csv
from flask import Flask, request, jsonify
from konlpy.tag import Kkma

app = Flask(__name__)

@app.route('/api/send_data', methods=['POST'])
def receive_data_from_react():
    data = request.get_json()  # JSON 데이터 받아오기
    title = data.get('title', '')
    content = data.get('content', '')

    # title과 content를 합쳐서 full_text 변수 생성 --- 그냥 내가 임의로 이렇게 한거임
    full_text = f"{title} {content}"

    # Kkma 형태소 분석
    kkma = Kkma()
    pos_tags = kkma.pos(full_text)

    # 기존의 pos_tagging.csv 파일에 데이터를 추가 ---- 이것도 나중에 해인이 코드 받아서 수정해야 할듯
    with open('pos_tagging.csv', 'a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['word', 'tag']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        for word, tag in pos_tags:
            writer.writerow({'word': word, 'tag': tag})

    # POS tagging 결과를 React로 보내기 위해 리스트 형태로 변환
    pos_tags_list = [{'word': word, 'tag': tag} for word, tag in pos_tags]

    return jsonify({'pos_tags': pos_tags_list})

if __name__ == '__main__':
    app.run(debug=True)
