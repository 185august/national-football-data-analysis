import urllib.parse
from flask import Flask, jsonify
import  data_still_grafs
import data_animation
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from flask import url_for

@app.route('/')
def index():
    return 'index'

@app.route('/image')
def get_image():
    string = data_still_grafs.top_20_win_percentage()
    image = 'data:image/png;base64,' + urllib.parse.quote(string)
    filename = 'top_20_win_percentage.png'
    return jsonify({'image': image, 'filename': filename})

@app.route('/animation')
def get_animation():
    string = data_animation.send_animation_as_base64()
    image = 'data:image/gif;base64,' + urllib.parse.quote(string)
    filename = 'world_cup_goals_over_time.gif'
    return jsonify({'image': image, 'filename': filename})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)