import json
import urllib.parse
from fileinput import filename

import  overall_team_statistics_graphs
import data_animation
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from flask import url_for

@app.route('/')
def index():
    return 'index'

@app.route('/charts')
def get_charts():
    # string = data_still_grafs.top_20_win_percentage()
    # fig = data_still_grafs.create_a_bar_graph(data_x=[1, 2, 3, 4, 5], data_y=[0, 1, 2, 3, 4], title='Test', x_label='X', y_label='Y')
    # string = data_still_grafs.export_bar_graph(fig)
    figures = overall_team_statistics_graphs.get_all_still_graphs()
    figures.append(data_animation.get_all_animations())
    list_of_figures_dicts = [obj.to_dict() for obj in figures]

    return json.dumps(list_of_figures_dicts)

@app.route('/animation')
def get_animation():
    string = data_animation.send_animation_as_base64()
    image = 'data:image/gif;base64,' + urllib.parse.quote(string)
    filename = 'world_cup_goals_over_time.gif'
    return jsonify({'image': image, 'filename': filename})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)