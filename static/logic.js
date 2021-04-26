// THESE DEFAULT OBJECTS WILL BE LOADED WHEN THE INDEX PAGE LOADS. FEEL FREE TO OVERWRITE THEM VIA THE DEVELOPER CONSOLE IF YOU WANT TO TRY DIFFERENT INPUTS

// An example transactions objects that can be sent to the add route
transactions = [{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" },
{ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" },
{ "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" },
{ "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" },
{ "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }]

// An example spend object that can be sent to the spend route
spendObj = {points: 5000}

//THESE FUNCTIONS ARE AVAILABLE TO CALL FROM THE INDEX PAGE VIA THE DEVELOPER CONSOLE.

// Posts the above transactions to the add route. Current list of transactions should be logged to the terminal
function add_records(){
    fetch('/add', {
        headers: { 'Content-Type': 'application/json'},
        method: 'POST',
        body: JSON.stringify(transactions)
    })
}

// Posts the spendObj to the spend route. Will print a receipt of the transaction to the developer console.
function spend_points(){
    fetch('/spend', {
        headers: { 'Content-Type': 'application/json'},
        method: 'POST',
        body: JSON.stringify(spendObj)
    }).then(
        response => response.json()).then(
            data => console.log(data))
}