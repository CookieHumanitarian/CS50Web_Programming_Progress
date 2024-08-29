document.addEventListener('DOMContentLoaded', function() {

    //Only attach event listener to post form if user is logged in
    const form = document.querySelector('#postForm');
    if (form) {
        form.addEventListener('submit', postForm);
    }
});

function postForm(event) {
    event.preventDefault();
    
    // Make a new post
    fetch('/newPost', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#postBody').value
        })
        })
        .then(response => response.json())
        .then(result => {
            alert(JSON.stringify(result.message));
            });

    // Clear value
    document.querySelector('#postBody').value = '';
}