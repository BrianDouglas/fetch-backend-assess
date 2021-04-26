myObj = [{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" },
{ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" },
{ "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" },
{ "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" },
{ "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }]

spendObj = {points: 5000}

function add_records(){
    fetch('/add', {
        headers: { 'Content-Type': 'application/json'},
        method: 'POST',
        body: JSON.stringify(myObj)
    })
}

function spend_points(){
    fetch('/spend', {
        headers: { 'Content-Type': 'application/json'},
        method: 'POST',
        body: JSON.stringify(spendObj)
    }).then(
        response => response.json()).then(
            data => console.log(data))
}