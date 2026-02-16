/**
 * Forgot Password Page JavaScript
 * Handles password reset request
 */

document.addEventListener('DOMContentLoaded', () => {
    const forgotForm = document.getElementById('forgotForm');
    const forgotError = document.getElementById('forgotError');
    const forgotSuccess = document.getElementById('forgotSuccess');
    const errorMessage = document.getElementById('errorMessage');

    forgotForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = forgotForm.querySelector('.auth-submit');
        const email = document.getElementById('email').value.trim();

        // Hide previous messages
        forgotError.classList.remove('show');
        forgotSuccess.classList.remove('show');

        // Validation
        if (!email) {
            showError('Please enter your email address');
            return;
        }

        if (!isValidEmail(email)) {
            showError('Please enter a valid email address');
            return;
        }

        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        try {
            // Call API (using mock for now)
            const response = await window.API.forgotPassword({ email });

            if (response.success) {
                // Store email for verification page
                sessionStorage.setItem('resetEmail', email);
                
                // Show success message
                forgotSuccess.classList.add('show');

                // Redirect to verification after a short delay
                setTimeout(() => {
                    window.location.href = 'verify-code.html?type=reset';
                }, 2000);
            } else {
                showError(response.message || 'Failed to send verification code');
            }
        } catch (error) {
            console.error('Forgot password error:', error);
            showError('An error occurred. Please try again.');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        forgotError.classList.add('show');
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
});
