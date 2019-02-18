"use strict";

 // TODO: add way to refresh contact list in a user's profile and clear form
$('.contact-form').on('submit', (evt) => {
  evt.preventDefault();

  const formInputs = {
    'name': $('.contact-name').val(),
    'type': $('.phone-type').val(),
    'phone': $('.contact-phone').val()
  };

  $.post('/add-contact', formInputs, (results) => {
    alert(results);
  });
});
