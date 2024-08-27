document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#postForm').addEventListener('submit', postForm);
    document.querySelector('#allPosts').addEventListener('click', showPost);

    // By default, load all posts
    showPost();
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

function showPost() {
    fetch('/allPosts')
    .then(response => response.json())
    .then(array => {
        array.forEach(element => {
            // Create element to store post
            const container = document.createElement('div');
            container.className = 'singlePost';

            //Append information to post
            const user = document.createElement('div');
            const body = document.createElement('div');
            const timestamp = document.createElement('div');
            user.innerHTML = `${element.user}`;
            body.innerHTML = `${element.body}`;   
            timestamp.innerHTML = `${element.timestamp}`;

            // Append to bottom of posts
            container.append(user, body, timestamp);
            document.querySelector('#posts').append(container);
        });
        
    })
}