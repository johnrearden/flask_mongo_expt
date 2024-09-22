from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from utils.duration_filter import millis_to_duration

import os
if os.path.exists('env.py'):
    import env

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.jinja_env.filters['duration'] = millis_to_duration
mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    routes = mongo.db.runs.distinct('route')
    print(routes)
    return render_template("index.html", routes=routes)


@app.route('/runs_by_route/<route>')
def runs_by_route(route):

    # Get sorting queries from the request. Results will be sorted in date
    # order ascending by default. Sorting by total_time will only be done
    # if explicitly requested in the query, and will override sorting by date
    # in this case.
    total_time_ordering = request.args.get('total_time_ordering')
    date_ordering = request.args.get('date_ordering', 1)
    if total_time_ordering:
        sort_flag = -1 if total_time_ordering == 'desc' else 1
        sort_dict = {"total_time": sort_flag}
    else:
        sort_flag = -1 if date_ordering == 'desc' else 1
        sort_dict = {"date": sort_flag}
        total_time_ordering = 'asc' # default if not present in query

    routes = mongo.db.runs.distinct('route')
    cursor = mongo.db.runs.find({'route': route}).sort(sort_dict)

    runs = list(cursor)
    run_list = []  # The list of all runs
    split_count = []

    for run in runs:
        run_map = {}  # The key/value pairs for this run
        split_list = [run[key] for key in run if key.startswith('split')]
        split_count.append(len(split_list))
        run_map['splits'] = split_list
        run_map['total_time'] = run['total_time']
        run_map['date'] = run['date']
        run_map['min_mile'] = run['min_mile']
        run_list.append(run_map)

    # Tell the template what the next ordering queries should be if the
    # sort icons are toggled, so that it can add them to the request
    next_total_time_order = "desc" if total_time_ordering == "asc" else "asc"
    next_date_order = "desc" if date_ordering == "asc" else "asc"

    return render_template(
        "runs.html",
        run_list=run_list,
        routes=routes,
        current_route=route,
        split_count=max(split_count),
        next_total_time_order=next_total_time_order,
        next_date_order=next_date_order,
    )
    

@app.route('/add_new_run/<route>', methods=['GET', 'POST'])
def add_new_run(route):
    routes = mongo.db.runs.distinct('route')
    return render_template(
        "add_new_run.html", routes=routes, current_route=route,
    )


if __name__ == '__main__':
    app.run(debug=True)