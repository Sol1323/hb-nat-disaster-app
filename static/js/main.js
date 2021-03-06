"use strict";

$(".edit-contact-button").click(function(){
  const id = $(this).attr("id");
        $("#contact-edit-form-"+ id).toggle();
});

// -------------------------ADD EARTHQUAKE SETTING SCRIPT---------------------------

// $('#earthquake-form').on('submit', (evt) => {
//   evt.preventDefault();
//
//   const settingCode = $('.setting_code').val();
//   const formInputs = {
//     'magnitude': $('.earth-mag').val();
//   };
//
//   $.post('/settings/'+ settingCode, formInputs, (setting) => {
//     $('#mag-user-value').text(`${setting.user_value}`);
//   });
// });
// -------------------------ADD CONTACT SCRIPT---------------------------


$('#add-contact-form').on('submit', (evt) => {
  evt.preventDefault();

  const formInputs = {
    'name': $('.contact-name').val(),
    'type': $('.phone-type').val(),
    'phone': $('.contact-phone').val()
  };
// FIXME: Does not append when is the first contact that you are going to add into your list of contacts
// FIXME: Does not append with edit button
  $.post('/contacts', formInputs, (contact) => {
    console.log(contact)
    $('.user-contacts').append(`
                              <h3 class="g-font-size-18--xs g-margin-b-10--xs"><a href="/contacts/${contact.contact_id}"> ${contact.name}</a></h3>
                              <li class="g-font-size-18--sm">${contact.phone[0].type}: ${contact.phone[0].phone}</li>
                              <button type="button" class="edit-contact-button s-btn--xs s-btn--primary-bg g-radius--50 g-padding-x-50--xs" id="${contact.contact_id }">Edit</button>
                              `
                              );
    $('#add-contact-form').each(function(){
      this.reset();
    });
  });
});


// -------------------------UPDATE USER SCRIPT---------------------------
$("#edit-user-form-button").click(function(){
        $("#user-edit-form").toggle();
});


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
