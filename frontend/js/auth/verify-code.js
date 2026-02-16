/**
 * Verify Code Page JavaScript
 * Handles verification code input and validation
 */

document.addEventListener('DOMContentLoaded', () => {
    const verifyForm = document.getElementById('verifyForm');
    const verifyError = document.getElementById('verifyError');
    const errorMessage = document.getElementById('errorMessage');
    const codeInputs = document.querySelectorAll('.code-input');
    const userEmailEl = document.getElementById('userEmail');
    const resendBtn = document.getElementById('resendBtn');
    const resendTimer = document.getElementById('resendTimer');
    const countdownEl = document.getElementById('countdown');

    // Get email from session storage
    const email = sessionStorage.getItem('resetEmail') || sessionStorage.getItem('signupEmail') || 'your email';
    userEmailEl.textContent = email;

    // Get type from URL params
    const urlParams = new URLSearchParams(window.location.search);
    const isReset = urlParams.get('type') === 'reset';

    // Auto-focus and auto-advance code inputs
    codeInputs.forEach((input, index) => {
        // Auto-focus first input
        if (index === 0) input.focus();

        input.addEventListener('input', (e) => {
            const value = e.target.value;
            
            // Only allow numbers
            if (!/^\d*$/.test(value)) {
                e.target.value = '';
                return;
            }

            // Add filled class
            if (value) {
                input.classList.add('filled');
            } else {
                input.classList.remove('filled');
            }

            // Auto-advance to next input
            if (value && index < codeInputs.length - 1) {
                codeInputs[index + 1].focus();
            }

            // Auto-submit when all fields are filled
            if (value && index === codeInputs.length - 1) {
                const allFilled = Array.from(codeInputs).every(input => input.value);
                if (allFilled) {
                    verifyForm.dispatchEvent(new Event('submit'));
                }
            }
        });

        input.addEventListener('keydown', (e) => {
            // Handle backspace
            if (e.key === 'Backspace' && !input.value && index > 0) {
                codeInputs[index - 1].focus();
            }

            // Handle paste
            if (e.key === 'v' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                navigator.clipboard.readText().then(text => {
                    const digits = text.replace(/\D/g, '').slice(0, 6);
                    digits.split('').forEach((digit, i) => {
                        if (codeInputs[i]) {
                            codeInputs[i].value = digit;
                            codeInputs[i].classList.add('filled');
                        }
                    });
                    if (digits.length === 6) {
                        verifyForm.dispatchEvent(new Event('submit'));
                    }
                });
            }
        });

        // Select all on focus
        input.addEventListener('focus', () => {
            input.select();
        });
    });

    // Form submission
    verifyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = verifyForm.querySelector('.auth-submit');
        const code = Array.from(codeInputs).map(input => input.value).join('');

        // Hide previous errors
        verifyError.classList.remove('show');

        // Validation
        if (code.length !== 6) {
            showError('Please enter the complete 6-digit code');
            return;
        }

        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        try {
            // Call API (using mock for now)
            const response = await window.API.verifyCode({ email, code });

            if (response.success) {
                // Store verification token
                sessionStorage.setItem('verificationToken', response.token);

                if (isReset) {
                    // Redirect to reset password
                    window.location.href = 'reset-password.html';
                } else {
                    // Redirect to success page
                    window.location.href = 'success.html?type=verify';
                }
            } else {
                showError(response.message || 'Invalid verification code');
                // Clear inputs
                codeInputs.forEach(input => {
                    input.value = '';
                    input.classList.remove('filled');
                });
                codeInputs[0].focus();
            }
        } catch (error) {
            console.error('Verify error:', error);
            showError('An error occurred. Please try again.');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });

    // Resend code functionality
    let countdown = 0;

    resendBtn.addEventListener('click', async () => {
        if (countdown > 0) return;

        resendBtn.disabled = true;

        try {
            const response = await window.API.resendCode({ email });

            if (response.success) {
                // Start countdown
                countdown = 60;
                resendBtn.parentElement.style.display = 'none';
                resendTimer.style.display = 'block';

                const timer = setInterval(() => {
                    countdown--;
                    countdownEl.textContent = countdown;

                    if (countdown <= 0) {
                        clearInterval(timer);
                        resendBtn.parentElement.style.display = 'block';
                        resendTimer.style.display = 'none';
                        resendBtn.disabled = false;
                    }
                }, 1000);
            } else {
                showError('Failed to resend code. Please try again.');
                resendBtn.disabled = false;
            }
        } catch (error) {
            console.error('Resend error:', error);
            showError('An error occurred. Please try again.');
            resendBtn.disabled = false;
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        verifyError.classList.add('show');
    }
});
