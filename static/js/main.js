"use strict";


// -------------------------EDIT BUTTON TOGGLE SCRIPT---------------------------
$(".editFormButton").click(function(){
        $(".edit-form").toggle();
});


// -------------------------ADD CONTACT SCRIPT---------------------------
$('.contact-form').on('submit', (evt) => {
  evt.preventDefault();

  const formInputs = {
    'name': $('.contact-name').val(),
    'type': $('.phone-type').val(),
    'phone': $('.contact-phone').val()
  };
// FIXME: Does not append when is the first contact that you are going to add into your list of contacts
  $.post('/contacts', formInputs, (contact) => {
    $('.user-contacts').append(`
                              <a href="/contacts/${contact.contact_id}"> ${contact.name} </a>
                              <li>${contact.type}: ${contact.phone}</li>`
                              );
    $('.contact-form').each(function(){
      this.reset();
    });
  });
});


// -------------------------UPDATE USER SCRIPT---------------------------

$('.user-edit-form').on('submit', (evt) => {
  evt.preventDefault();

  const user_id = $('.user-id').val();

  const formInputs = {
    'name': $('.user-name').val(),
    'email': $('.user-email').val(),
    'age': $('.user-age').val(),
    'residency_address': $('.user-address').val(),
    'zipcode': $('.user-zipcode').val(),
    'allergies': $('.user-allergies').val(),
    'medications': $('.user-medications').val(),
    'phone': $('.user-phone').val()
  };

  $.post('/users/'+ user_id, formInputs, (contact) => {
    alert("this is working!!");
  });
});
