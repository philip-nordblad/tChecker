var PinPad = (function() {
    let pin = '';
    const MAX_PIN_LENGTH = 4;

    function updateDisplay() {
        const display = document.getElementById('pin-display');
        if (display) display.innerText = '•'.repeat(pin.length);
    }

    function getCSRFToken() {
        const csrfInput = document.querySelector('[name=csrf_token]');
        return csrfInput ? csrfInput.value : '';
    }

    return {
        press(num) {
            if (pin.length < MAX_PIN_LENGTH) {
                pin += num;
                updateDisplay();

                if (pin.length === MAX_PIN_LENGTH) {
                    setTimeout(() => this.submitPin(), 300);
                }
            }
        },

        reset() {
            pin = '';
            updateDisplay();
        },

        undo() {
            pin = pin.slice(0,-1)
            updateDisplay();
        },

        getCurrentPin() {
            return pin;
        },

        async submitPin() {
            if (pin.length !== MAX_PIN_LENGTH) {
                alert('Please enter a complete 4-digit PIN');
                return;
            }

            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ pin: pin })
                });

                // First check if we got any response at all
                if (!response) {
                    throw new Error('No response from server');
                }

                // Handle non-JSON responses
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    const text = await response.text();
                    throw new Error(`Expected JSON but got: ${text.substring(0, 100)}`);
                }

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.message || 'Login failed');
                }

                if (data.success) {
                    window.location.href = data.redirect || '/';
                } else {
                    alert(data.message || 'Invalid PIN');
                    this.reset();
                }
            } catch (error) {
                console.error('Error:', error);
                alert(error.message || 'An error occurred. Please try again.');
                this.reset();
            }
        }
    };
})();