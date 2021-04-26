from datetime import datetime
import json

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

''' data to keep track of '''
transactions = []
totals = {}
needs_sorted = False

''' helper functions '''
def update_totals(payer, points):
    if payer in totals:
        totals[payer] += points
    else:
        totals[payer] = points
    # 'We want no payer's points to go negative.'
    if totals[payer] < 0:
        totals[payer] = 0

def check_for_sort():
    global needs_sorted
    if needs_sorted or (len(transactions) > 1 and transactions[-1]['timestamp'] < transactions[-2]['timestamp']):
        needs_sorted = True
    else:
        needs_sorted = False

def add_transaction(record):
    transactions.append(record)
    check_for_sort()
    update_totals(record['payer'], record['points'])

def sort_transactions():
    global transactions
    transactions = sorted(transactions, key= lambda i: i['timestamp'])
    global needs_sorted
    needs_sorted = False

def update_spend_log(payer, points, log):
    if payer in log:
        log[payer] -= points
    else:
        log[payer] = 0 - points
    return log

def get_points_total_balance():
    total_points = 0
    for payer in totals:
        total_points += totals[payer]
    return total_points

''' ROUTES '''
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=['POST'])
def add():
    ''' 
        accepts data as json or form submission 
        data received via form submission will have timestamp added by server 
    '''
    data = request.get_json()
    if data:
        if type(data) != list:
            data = [data]
        for record in data:
            add_transaction(record)
    else:
        # get the relevant data from the request
        payer = request.form["payer"]
        points = int(request.form["points"])
        time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        # create a record and add it to the list
        record = {"payer": payer, "points": points, "timestamp": time}
        add_transaction(record)
    print(transactions)
    return "OK", 200

@app.route("/spend", methods=['POST'])
def spend():
    data = request.get_json()
    points_to_spend = data['points']
    points_available = get_points_total_balance()
    
    if points_available < points_to_spend:
        return jsonify({"ERROR": "Not enough points. You need {} more points to complete this transaction".format(points_to_spend - points_available)})

    if needs_sorted:
        sort_transactions()

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
    spend_receipt = []
    for key in spend_log:
        spend_receipt.append({'payer': key, 'points': spend_log[key]})
    return jsonify(spend_receipt)


@app.route("/balance", methods=['GET'])
def balance():
    return totals, 200

if __name__ == "__main__":
    app.run(debug=True)