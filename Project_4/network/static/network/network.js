document.addEventListener('DOMContentLoaded', function() {

    //Only attach event listener to post form if user is logged in
    const form = document.querySelector('#postForm');
    if (form) {
        form.addEventListener('submit', postForm);
    }

    // Follow/unfollow button
    const following = document.querySelector('#following');
    if (following) {
        following.addEventListener('click', followingView);
    }

    // Editing post
    document.querySelectorAll('.editButton').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.id;
            const postElement = document.querySelector(`.post[data-id="${postId}"]`);
            editButton(postElement);
        });
    });

    //Editing Post
    document.querySelector('#editForm').addEventListener('click', editForm);
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

function editButton(postElement) {
    postElement.querySelector('.postBody').style.display = 'none';
    postElement.querySelector('.postEdit').style.display = 'block';
}