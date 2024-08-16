document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';

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

        // Click to enter mail
        mail.addEventListener('click', () => {
          view_mail(element.id)
        });

         // Change color of mail for read/unread emails
        if (element.read == false){
          mail.style.backgroundColor = "white";
        }
        else {
          mail.style.backgroundColor = "gray";
        }
        document.querySelector('#emails-view').append(mail);
      });
  })
}

function view_mail(id) {
  // Show the mail and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';

   // Fetch individual mail
   fetch(`/emails/${id}`)
   .then(response => response.json()) 
   .then(response => {
    document.querySelector('#mail_from').innerHTML = `From: ${response.sender}`;
    document.querySelector('#mail_to').innerHTML = `To: ${response.recipients}`;
    document.querySelector('#mail_subject').innerHTML = `Subject: ${response.subject}`;
    document.querySelector('#mail_timestamp').innerHTML = `Timestamp: ${response.timestamp}`;
    document.querySelector('#mail_body').innerHTML = `Body: ${response.body}`;

    //Change read to true
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    //Archive or unarchive mail
    const archive = document.querySelector('#archive_mail')
    if (response.archived == true){
      archive.innerHTML = "Unarchive";
      archive.onclick = () => archive_mail(id, true);
    }
    else {
      archive.innerHTML = "Archive";
      archive.onclick = () => archive_mail(id, false);;
    }
   });

   // Reply mail
   document.querySelector('#reply').onclick = () => reply_mail(id);
}

function archive_mail(id, archived) {
   //Change archive
   if (archived){
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
  }
  else {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  }
  load_mailbox('inbox');
}

function reply_mail(id) {
   // Show compose view and hide other views
   document.querySelector('#emails-view').style.display = 'none';
   document.querySelector('#compose-view').style.display = 'block';
   document.querySelector('#mail-view').style.display = 'none';
 
  // Fetch individual mail
  fetch(`/emails/${id}`)
  .then(response => response.json()) 
  .then(response => {
  
  // Pre-fill out composition fields
  document.querySelector('#compose-recipients').value = response.sender;
  document.querySelector('#compose-subject').value = `Re: ${response.subject}`;
  document.querySelector('#compose-body').value = `On ${response.timestamp} ${response.sender} wrote: ${response.body}`;
  });  
}