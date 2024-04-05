// static/script.js
function generateAI() {
    var objective = document.getElementById('objective').value;
    var llm_choice = document.getElementById('llm').value;
    // Using Fetch API to post the objective and get the Python code
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'objective=' + encodeURIComponent(objective) + '&llm_choice=' + encodeURIComponent(llm_choice)
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('code').innerText = data;
    });
}

function download() {
    var text = document.getElementById('code').innerText;
    var blob = new Blob([text], { type: 'text/plain' });
    var anchor = document.createElement('a');
    anchor.download = 'generated_code.py';
    console.log(text)
    anchor.href = window.URL.createObjectURL(blob);
    anchor.target = '_blank';
    anchor.style.display = 'none';
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
}