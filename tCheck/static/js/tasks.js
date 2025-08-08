
function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}



document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.button-basic.task-button');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {



            const itemId = button.getAttribute('data-item-id');
            console.log('Item ID:', itemId); // Debugging line
            const itemInput = document.getElementById(`item-${itemId}-input`);
            const value = itemInput ? itemInput.value : '';


            // Need toensure the itemId is not null or undefined
            if (!itemId) {
                console.error('Item ID is not defined');
                return;
            }

            // Only send itemInput if it's not empty
            const payload = { item_id: itemId };
            if (value && value.trim() !== '') {
                payload.item_input = value;
            }

            fetch('/tasks/complete_item', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify(payload)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Server responded with status ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert('Item marked as completed!');
                } else {
                    alert('Error: ' + data.error);
                }
            });
        });
    });
});

