import time
from datetime import datetime
import json

from flask import Flask, redirect, url_for, render_template, request, jsonify

app = Flask(__name__)

transactions = []
totals = {}
needs_sorted = False

def update_totals(payer, points):
    if payer in totals:
        totals[payer] += points
    else:
        totals[payer] = points
    
    if totals[payer] < 0:
        totals[payer] = 0

def sort_transactions():
    global transactions
    transactions = sorted(transactions, key= lambda i: i['timestamp'])

def update_spend_log(payer, points, log):
    if payer in log:
        log[payer] -= points
    else:
        log[payer] = 0 - points
    return log


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=['POST'])
def add():
    data = request.get_json()
    if data:
        if type(data) != list:
            data = [data]
        for record in data:
            transactions.append(record)
            update_totals(record['payer'], record['points'])
    else:
        # get the relevant data from the request
        payer = request.form["payer"]
        points = int(request.form["points"])
        time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        # create a record and add it to the list
        record = {"payer": payer, "points": points, "timestamp": time}
        transactions.append(record)
        update_totals(record['payer'], record['points'])
    # flag to sort
    global needs_sorted
    needs_sorted = True

    print(transactions)
    return "OK", 200

@app.route("/spend", methods=['POST'])
def spend():
    if request.method == 'POST':
        if needs_sorted:
            sort_transactions()

        data = request.get_json()
        points_to_spend = data['points']
        spend_log = {}

        # loop over records until all points are spent.
        for record in transactions:
            if points_to_spend == 0:
                break
            if record['points'] == 0:
                # we could remove zeroed out records from the transactions list if required.
                # for now, keeping them for posterity
                pass
            elif record['points'] <= points_to_spend:
                spend_log = update_spend_log(record['payer'], record['points'], spend_log)
                update_totals(record['payer'], 0 - record['points'])
                points_to_spend -= record['points']
                record['points'] = 0
            else:
                spend_log = update_spend_log(record['payer'], points_to_spend, spend_log)
                update_totals(record['payer'], 0 - points_to_spend)
                record['points'] -= points_to_spend
                points_to_spend = 0

        # format for return
        return_list = []
        for key in spend_log:
            return_list.append({'payer': key, 'points': spend_log[key]})
        return jsonify(return_list)


@app.route("/balance", methods=['GET'])
def balance():
    return totals, 200

if __name__ == "__main__":
    app.run(debug=True)