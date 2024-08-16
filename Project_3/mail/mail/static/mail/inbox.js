document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email)

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show appropriate mail
  show_mail(mailbox);
}

function send_email(event) {
  event.preventDefault();
  
  // Send email
  fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Check for errors
        if (result.error){
          alert(JSON.stringify(result['error']))
        }
        else {
          alert(JSON.stringify(result['message']))
          load_mailbox('inbox')
        }
    });
  }

function show_mail(mailbox) {
  // Fetch inbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json()) 
  .then(array => {

      // Loop through each email 
      array.forEach(element => {
        //Attach heading of mail
        const mail = document.createElement('div');
        mail.innerHTML = `${element.sender} Subject: ${element.subject} Time: ${element.timestamp}`;
        document.querySelector('.container').append(mail);

         // Change color of mail for read/unread emails
         if (!element.read){
          mail.style.backgroundColor = "#D3D3D3";
        }
        else {
          mail.style.backgroundColor = "white";
        }
      });
    console.log(array)
  })
}