document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#postForm').addEventListener('submit', postForm);

});

function postForm(event) {
    event.preventDefault();

    // Send email
    fetch('/newPost', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#postBody').value
        })
        })
        .then(response => response.json())
        .then(result => {
            alert(JSON.stringify(result.message))
            });
}
