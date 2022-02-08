function searchMail() {
    var email_from = document.getElementById("searchId").value;
    var raw = JSON.stringify({"email": email_from});

    var requestOptions = {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: raw
    };
    fetch("http://127.0.0.1:8081/mail-bounce", requestOptions)
    .then(response => response.json())
    .then(result => {
        var records = result.records;
        var content = "";
        records.forEach(element => {
            content += `${JSON.stringify(element, null, 4)}`;
        });
        document.getElementById("result").innerHTML = content;
    })
    .catch(error => console.log('error', error));
}