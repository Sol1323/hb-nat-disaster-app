"use strict";


// -------------------------EDIT BUTTON TOGGLE SCRIPT---------------------------
$("#edit-user-form-button").click(function(){
        $("#user-edit-form").toggle();
});


$(".edit-contact-button").click(function(){
  const id = $(this).attr("id");
        $("#contact-edit-form-"+ id).toggle();
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
// FIXME: Does not append with edit button
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

$('#user-edit-form').on('submit', (evt) => {
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
  console.log(user_id);
  // TODO: Add logic to show updated user's info withouth refreshing page
  //Q: How to refresh the user's info in the page withouth appending
  $.post('/users/'+ user_id, formInputs, (user) => {
    // $('#show-user-info').each(function(){
    //   console.log(this);
      alert("its working");
    // });
  });
});
