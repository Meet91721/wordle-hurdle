import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def correctness(target, guess):
    green = []
    yellow = []
    gray = []
    considered = []
    for index, (i, j) in enumerate(zip(target, guess)):
        if i == j:
            green.append(index)
            considered.append(index)
    for index, (i, j) in enumerate(zip(target, guess)):
        if index not in green and j in target:
            for target_i, target_c in enumerate(target):
                if target_c == guess[index] and target_i not in considered:
                    considered.append(target_i)
                    yellow.append(index)
                    break
    for index in range(len(target)):
        if index not in green and index not in yellow:
            gray.append(index)
    res = [0 for i in range(5)]
    for i in green:
        res[i] = 2
    for i in yellow:
        res[i] = 1
    for i in gray:
        res[i] = 3
    return res

@app.route('/check', methods=['GET'])
def check_word():
    target = request.args.get('target')
    guess = request.args.get('guess') 
    res = correctness(target, guess)
    return jsonify({
        'response': res
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
