function postRequest(route, input_date, callback) {
    fetch(route, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN,
        },
        body: JSON.stringify(input_date)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        }
        else {
            return callback(data);
        }
    })
}

function getRequest(route, callback) {
    fetch(route, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        }
        else {
            return callback(data);
        }
    })
}

export { postRequest, getRequest };
