document.addEventListener('DOMContentLoaded', function() {
    // Select all buttons with both classes
    const buttons = document.querySelectorAll('.button-basic.task-button');
    buttons.forEach(function(button) {
        button.addEventListener('click', function(event) {
        // You can access the parent list item or data attributes here
        alert('Button clicked!'); // Replace with your logic
        });
    });
    });