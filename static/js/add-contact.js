"use strict";


$('.contact-form').on('submit', (evt) => {
  evt.preventDefault();

  const formInputs = {
    'name': $('.contact-name').val(),
    'type': $('.phone-type').val(),
    'phone': $('.contact-phone').val()
  };

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
