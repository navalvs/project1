// // reorder_level.js

// function makeEditable(element, pk) {
//     var value = element.textContent;
//     var input = document.createElement('input');
//     input.type = 'number';
//     input.value = value;
//     input.onblur = function() {
//         element.textContent = input.value;
//         // Save the edited value in local storage
//         localStorage.setItem('reorder_level_' + pk, input.value);
//         element.parentNode.removeChild(input);
//     };
//     element.textContent = '';
//     element.appendChild(input);
//     input.focus();
// }

// // Retrieve and set the edited value from local storage on page load
// document.addEventListener('DOMContentLoaded', function() {
//     var editableElements = document.getElementsByClassName('editable');
//     for (var i = 0; i < editableElements.length; i++) {
//         var pk = editableElements[i].getAttribute('data-pk');
//         var savedValue = localStorage.getItem('reorder_level_' + pk);
//         if (savedValue) {
//             editableElements[i].textContent = savedValue;
//         }
//     }
// });

