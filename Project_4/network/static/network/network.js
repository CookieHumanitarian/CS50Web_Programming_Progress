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

        // Show edit and attach the event listener to the edit form
        document.querySelectorAll('.editButton').forEach(button => {
            button.addEventListener('click', function() {
                const postId = this.dataset.id;
                const postElement = document.querySelector(`.post[data-id="${postId}"]`);
                editButton(postElement);
    
                // Attach submit listener to the edit form when it's shown
                const editForm = postElement.querySelector('.editForm');
                if (editForm) {
                    editForm.addEventListener('submit', function(event) {
                        event.preventDefault();
                        const formBody = editForm.querySelector('.formBody').value;
                        editFormFunction(formBody, postId, postElement);
                    });
                }
            });
        });
    })



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

function editFormFunction(formBody, postID, postElement) {
    fetch('/editView', {
        method: 'POST',
        body: JSON.stringify({
            body: formBody,
            postID: postID
        })
    })
    .then(response => response.json())
    .then(result => {
        postElement.querySelector('.postBody').style.display = 'block';
        postElement.querySelector('.postEdit').style.display = 'none';
        
        const newBody = postElement.querySelector('.postBody');
        newBody.innerHTML = ''; 
        newBody.innerHTML = formBody; 

        
        alert(JSON.stringify(result.message))
    })
}
