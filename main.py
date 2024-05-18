from flask import Flask, render_template, request
from utils import repo_avg_pull, events, plot

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def plot_event_default():
    graph_json = plot(event_dict=None, offset_value=0)
    return render_template('index.html', graphJSON=graph_json)


@app.route('/data_event', methods=['POST', 'GET'])
def event():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        offset = request.form["Offset"]
        event_dict = events(offset=int(offset))
        if isinstance(event_dict, dict):
            interested_events_dict = dict()
            interested_events = ["WatchEvent", "PullRequestEvent", "IssuesEvent"]
            for (key, value) in event_dict.items():
                if key in interested_events:
                    interested_events_dict[key] = value
            graph_json = plot(event_dict=event_dict, offset_value=int(offset))
            render = render_template('event_data.html', graphJSON=graph_json, event_dict=interested_events_dict)
        else:
            render = f"please enter offset below {event_dict} minutes"
        return render


@app.route('/data', methods=['POST', 'GET'])
def pull_requests():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return repo_avg_pull(username=form_data["Username"], repo=form_data["Repository"])


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/event_form')
def event_form():
    return render_template('events.html')
