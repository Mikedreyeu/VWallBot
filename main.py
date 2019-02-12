import os
from flask import Flask, request, jsonify
from VWB import bot
from VWB import tools


app = Flask(__name__)


@app.route('/')
def index():
    return 'Get out of my room'


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        update = request.get_json()
        tools.log_json(update, 'updates.log')
        bot.handle_update(update)
        return jsonify(update)
    return 'hi'


@app.route('/auth', methods=['GET'])
def auth():
    return 'Yay'


@app.route('/start', methods=['POST', 'GET'])  # :)
def start():
    bot.start_bot()
    return 'Yay'


if __name__ == '__main__':
    tools.init_tokens('VWB/tokens.txt')
    os.mkdir('VWB/logs')
    try:
        bot.start_bot()
    except Exception as e:
        tools.log_err(e, 'errors.log')
