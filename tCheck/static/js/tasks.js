function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.button-basic.task-button');

    buttons.forEach(function(button) {
        // Save original button text for restoration if needed
        button.dataset.originalText = button.textContent;

        button.addEventListener('click', function() {
            const itemId = button.getAttribute('data-item-id');
            console.log('Item ID:', itemId); // Debugging line
            const itemInput = document.getElementById(`item-${itemId}-input`);
            const value = itemInput ? itemInput.value : '';

            // Ensure the itemId is not null or undefined
            if (!itemId) {
                console.error('Item ID is not defined');
                return;
            }

            // Disable and mark completed visually
            button.disabled = true;
            button.textContent = 'Completed';
            button.classList.add('completed');

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
            .then(response => response.json().then(data => ({
                statusCode: response.status,
                ok: response.ok,
                body: data
            })))
            .then(({ ok, body }) => {
                if (ok) {
                    alert(body.message);
                    // Button stays disabled and text stays "Completed"
                } else {
                    alert('Error: ' + body.message);
                    // Re-enable and restore button text so user can try again
                    button.disabled = false;
                    button.textContent = button.dataset.originalText;
                    button.classList.remove('completed');
                }
            })
            .catch(err => {
                console.error('Network or parsing error:', err);
                alert('Network error, please try again.');
                // Re-enable and restore button text
                button.disabled = false;
                button.textContent = button.dataset.originalText;
                button.classList.remove('completed');
            });
        });
    });
});
