document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  // Adding event listerers to each button, 
  // The argument inside each functions is the id of the event ...
  // ... that the event listener is being added to
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  // Add the necessary event listeners for the static html pages
  // -----------------------------------------------------------
  
  // Backend code for "Compose"
  // --------------------------------------------------------------


  // Test fetch request method GET, request current user objvect
  // document.querySelector('#check-user').onclick = function() {
  //   console.log('check user button ok!');

  //   fetch('/check')
  //   .then(response => response.json())
  //   .then(check_user => {
  //     if (check_user.message) {
  //       console.log('User exists! All good!');
  //       console.log(check_user.email);

  //     } else if (check_user.error) {
  //       console.log('User does not exist. Not good.');
  //     }});
  //   };

  // // Test fetch request method POST. Post passed in data
  // document.querySelector('#check-post').onclick = function() {  
    
  //   console.log('check post button pressed');

  //   fetch('/check', { // fetch, .then, and .then need to be closed in their own respective parentheses
  //     method: "POST",
  //     headers: {
  //       'Content-Type': 'application/json'  // Indicates that the request body contains JSON data
  //     },
  //     body: JSON.stringify({ // 'body' has to be called body
  //       foo: 'foo',
  //       bar: 'bar',
  //       baz: 'baz'
  //     })
  //   })
  //   .then(response => response.json())
  //   .then(check_post => {
  //     if (check_post.good) {
  //       console.log(check_post.good.message);
  //       console.log(check_post.good.foo);
  //       console.log(check_post.good.bar);
  //       console.log(check_post.good.baz);
  //     } else if (check_post.bad) {
  //       console.log(check_post.bad);
  //     }
  //   });
  // };

  // Create an email to be sent with user inputd data from compose tab when form is submitted
  document.querySelector('#compose-form').onsubmit = function() {
    console.log('Form submission attempted');

    // turn all user input fields into const to be manipulated further
    sender = document.querySelector('#compose-sender').value;
    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value

    // turn user input data into a list
    const form_data = [
      sender,recipients,subject,body
    ];

    // interate over user data to ensure that no fields are empty. If empty return false and end submission early
    for (const field of form_data) {
      if (field === '') {
        console.log("field was empty. Exit early");
        return false;
      }
      console.log('no fields were blank all good!');
    }

    // do fetch web request and post the data to .compose view via /email url route
    fetch('/emails', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        sender: sender,
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      if (result.message) {
        console.log(result.message);
      } else if (result.error) {
        console.log(result.error);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
    return false;
  };


  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() { // when this function is called it should only be used to manipulate the html using javascript, not post, request, pull data etc

  // Show compose view and hide other views
  document.querySelector('#compose-view').style.display = 'block'; // Compose Form = Show // reveal and format the div where the content and forms for making an email would show up
  document.querySelector('#emails-view').style.display = 'none'; // Mailbox Name = Hide // hide the div where emails would show up
  document.querySelector('#single-email-view').style.display = 'none'; // Single Email = Hide
  document.querySelector('#mailbox-view').style.display = 'none'; // Mailbox = Hide

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

 }


function load_mailbox(mailbox) { // when this function is called it should only be used to manipulate the html using javascript, not post, request, pull data etc
  
  // Show the mailbox and hide the compose view
  document.querySelector('#emails-view').style.display = 'block'; // Mailbox Name = Show // reveal the div where emails will be loaded and displayed in
  document.querySelector('#mailbox-view').style.display = 'block'; // Mailbox = Show
  document.querySelector('#compose-view').style.display = 'none'; // Compose Form = Hide // hide the forms and content used to compose emails
  document.querySelector('#single-email-view').style.display = 'none'; // Single Email = Hide
  
  // Display the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`; // string argument from add event listner

  // Log which mailbox is currently being accessed
  console.log(`mailbox is = ${mailbox}`);

  // Clear current Mailbox
  document.querySelector('#mailbox-view').innerHTML = '';

  
  // Load, populate, and display current mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(inbox => {
    inbox.forEach(function(email) {
      
      // Turn html element 'mailbox-view' into variable
      inbox = document.querySelector('#mailbox-view');

      // Create a div element
      const email_prototype = document.createElement('div');
      email_prototype.className = 'border border-dark mb-3 p-3 d-flex justify-content-between align-items-center email'; 

      // Create child div's to be appended to email_prototype, populate email_prototype
      const id = document.createElement('span');
      id.innerHTML = `id = ${email.id}`;
      email_prototype.appendChild(id);

      const sender = document.createElement('span');
      sender.innerHTML = `From: ${email.sender}`;
      email_prototype.appendChild(sender);
      
      const recipient = document.createElement('span');
      recipient.innerHTML = `To: ${email.recipients}`;
      email_prototype.appendChild(recipient);

      // Add event listner for div when clicked = call load_email function
      email_prototype.onclick = function() {
        load_email(email);
      }

      // Append populated email_prototype to mailbox view
      inbox.append(email_prototype);
    });
  });


  // setTimeout(() => {
  //   console.log('Fubiyo');
  //   document.querySelector('#test-view').append('fubiyo');
  // }, 2000);

  // setTimeout(() => {
  //   console.log('Blank');
  //   document.querySelector('#test-view').innerHTML = '';
  // }, 4000);

  // setTimeout(() => {
  //   console.log('Angelica');
  //   document.querySelector('#test-view').append('email view = angelica');
  // }, 6000);

  

  // inbox, sent, archive, check for full '===' equivalency matches
  // --------------------------------------------------------------
  
  // if mailbox loaded is the inbox
  // if (mailbox === 'inbox') {
  //   console.log(`mailbox is = ${mailbox}`);

  //   fetch(`/emails/${mailbox}`)
  //   .then(response => response.json())
  //   .then(inbox => {
  //     inbox.forEach(function(email) {
        
  //       // Turn html element 'mailbox-view' into variable
  //       inbox = document.querySelector('#mailbox-view');

  //       // Create a div element
  //       const email_prototype = document.createElement('div');
  //       email_prototype.className = 'border border-dark mb-3 p-3 d-flex justify-content-between align-items-center email'; 

  //       // Create child div's to be appended to email_prototype, populate email_prototype
  //       const id = document.createElement('span');
  //       id.innerHTML = `id = ${email.id}`;
  //       email_prototype.appendChild(id);

  //       const sender = document.createElement('span');
  //       sender.innerHTML = `From: ${email.sender}`;
  //       email_prototype.appendChild(sender);
        
  //       const recipient = document.createElement('span');
  //       recipient.innerHTML = `To: ${email.recipients}`;
  //       email_prototype.appendChild(recipient);

  //       // Add event listner for div when clicked = call load_email function
  //       email_prototype.onclick = function() {
  //         load_email(email);
  //       }

  //       // Append populated email_prototype to mailbox view
  //       inbox.append(email_prototype);
  //     });
  //   });


  // } else if (mailbox === 'archive') {
  //   console.log(`mailbox = ${mailbox}`);


  // } else if (mailbox === 'sent') {
  //   console.log(`mailbox is = ${mailbox}`);

  //   fetch(`/emails/${mailbox}`)
  //   .then(response => response.json())
  //   .then(inbox => {
  //     inbox.forEach(function(email) {
        
  //       // Turn html element 'mailbox-view' into variable
  //       inbox = document.querySelector('#mailbox-view');

  //       // Create a div element
  //       const email_prototype = document.createElement('div');
  //       email_prototype.className = 'border border-dark mb-3 p-3 d-flex justify-content-between align-items-center email'; 

  //       // Create child div's to be appended to email_prototype, populate email_prototype
  //       const id = document.createElement('span');
  //       id.innerHTML = `id = ${email.id}`;
  //       email_prototype.appendChild(id);

  //       const sender = document.createElement('span');
  //       sender.innerHTML = `From: ${email.sender}`;
  //       email_prototype.appendChild(sender);
        
  //       const recipient = document.createElement('span');
  //       recipient.innerHTML = `To: ${email.recipients}`;
  //       email_prototype.appendChild(recipient);

  //       // Add event listner for div when clicked = call load_email function
  //       email_prototype.onclick = function() {
  //         load_email(email);
  //       }

  //       // Append populated email_prototype to mailbox view
  //       inbox.append(email_prototype);
  //     });
  //   });

  // }

};

function load_email(email) {

  // Show and hide the proper mailboxes
  document.querySelector('#emails-view').style.display = 'block'; // Mailbox Name = Show // reveal the div where emails will be loaded and displayed in
  document.querySelector('#single-email-view').style.display = 'block'; // Single Email = Show
  document.querySelector('#mailbox-view').style.display = 'none'; // Mailbox = Hide
  document.querySelector('#compose-view').style.display = 'none'; // Compose Form = Hide // hide the forms and content used to compose emails


  //single email sender,timestamp,subject,body
  
  // Append all data to respective html elements to be displayed
  document.querySelector('#single-email-sender').innerHTML = email.sender;
  document.querySelector('#single-email-timestamp').innerHTML = email.timestamp;
  document.querySelector('#single-email-subject').innerHTML = email.subject;
  document.querySelector('#single-email-body').innerHTML = email.body;

  if (email.archived === false) {
    console.log('email is archived');
  }
 
};


