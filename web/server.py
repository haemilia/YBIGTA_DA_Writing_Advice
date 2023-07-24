import os
from flask_cors import CORS
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)


@app.route('/react_to_flask', methods=['POST'])
def react_to_flask():
    data = request.get_json()
    category = data['category']
    text = data['text']
    #-------------------------------------------------------
    #여기에 맞춤법 맞추는 코드가 들어가야함 근데 적용이 안됨
    modifiedText = f'category is {category}. text is {text}.'
    #-------------------------------------------------------
    return jsonify({'modifiedText': modifiedText})


if __name__ == '__main__':
    app.run(port="5000",  debug=True)