#Create REST API

from flask import Flask, jsonify, request
import simple_data_tool
import plotly.graph_objects as go

app = Flask(__name__)
sdt = None

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        data = "Welcome to SF Coding Competition 2023!"
        return jsonify({'data':data})
    
@app.route('/home/display_data')
def display_data():
    #Display most spoken languages by agents in the state with the most and least disasters
    state_with_least_disasters = sdt.get_state_with_least_disasters()
    state_with_most_disasters = sdt.get_state_with_most_disasters()

    #Data for a variety of states
    dp1 = sdt.get_num_disasters_for_state(state_with_least_disasters)
    dp2 = sdt.get_num_disasters_for_state(state_with_most_disasters)
    dp3 = sdt.get_num_disasters_for_state('Alaska')
    dp4 = sdt.get_num_disasters_for_state('Oklahoma')
    dp5 = sdt.get_num_disasters_for_state('Texas')
    dp6 = sdt.get_num_disasters_for_state('Florida')
    dp7 = sdt.get_num_disasters_for_state('California')
    dp8 = sdt.get_num_disasters_for_state('New York')
    fig = go.Figure(data=[go.Bar(x=[state_with_least_disasters,'Alaska','Oklahoma','Texas','Florida','California','New York'], y=[dp1,dp2,dp3,dp4,dp5,dp6,dp7,dp8])])
    fig.show()
    return jsonify({'data': fig})

if __name__ == "__main__":
    #Initialize unit test class to get data
    sdt = simple_data_tool.SimpleDataTool()
    app.run(debug=True)
