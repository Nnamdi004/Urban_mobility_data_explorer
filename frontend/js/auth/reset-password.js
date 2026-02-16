/**
 * Reset Password Page JavaScript
 * Handles new password creation
 */

document.addEventListener('DOMContentLoaded', () => {
    const resetForm = document.getElementById('resetForm');
    const resetError = document.getElementById('resetError');
    const errorMessage = document.getElementById('errorMessage');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const passwordToggles = document.querySelectorAll('.password-toggle');
    const strengthBars = document.querySelectorAll('.strength-bar');
    const strengthText = document.getElementById('strengthText');

    // Check for verification token
    const verificationToken = sessionStorage.getItem('verificationToken');
    if (!verificationToken) {
        // Redirect to forgot password if no token
        window.location.href = 'forgot-password.html';
        return;
    }

    // Password visibility toggle
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const wrapper = toggle.closest('.password-wrapper');
            const input = wrapper.querySelector('.form-input');
            const eyeOpen = toggle.querySelector('.eye-open');
            const eyeClosed = toggle.querySelector('.eye-closed');

            if (input.type === 'password') {
                input.type = 'text';
                eyeOpen.style.display = 'none';
                eyeClosed.style.display = 'block';
            } else {
                input.type = 'password';
                eyeOpen.style.display = 'block';
                eyeClosed.style.display = 'none';
            }
        });
    });

    // Password strength checker
    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        const strength = calculatePasswordStrength(password);
        updateStrengthIndicator(strength);
    });

    function calculatePasswordStrength(password) {
        let score = 0;
        
        if (password.length === 0) return { score: 0, text: 'Password strength' };
        if (password.length >= 8) score++;
        if (password.length >= 12) score++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
        if (/\d/.test(password)) score++;
        if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;

        if (score <= 1) return { score: 1, text: 'Weak' };
        if (score <= 2) return { score: 2, text: 'Fair' };
        if (score <= 3) return { score: 3, text: 'Good' };
        return { score: 4, text: 'Strong' };
    }

    function updateStrengthIndicator(strength) {
        const classes = ['', 'weak', 'weak', 'medium', 'strong'];
        
        strengthBars.forEach((bar, index) => {
            bar.className = 'strength-bar';
            if (index < strength.score) {
                bar.classList.add(classes[strength.score]);
            }
        });

        strengthText.textContent = strength.text;
    }

    // Form submission
    resetForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = resetForm.querySelector('.auth-submit');
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // Hide previous errors
        resetError.classList.remove('show');

        // Validation
        if (!password || !confirmPassword) {
            showError('Please fill in all fields');
            return;
        }

        if (password.length < 8) {
            showError('Password must be at least 8 characters');
            return;
        }

        if (password !== confirmPassword) {
            showError('Passwords do not match');
            return;
        }

        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        try {
            // Call API (using mock for now)
            const response = await window.API.resetPassword({ 
                token: verificationToken, 
                password 
            });

            if (response.success) {
                // Clear session storage
                sessionStorage.removeItem('verificationToken');
                sessionStorage.removeItem('resetEmail');

                // Redirect to success page
                window.location.href = 'success.html';
            } else {
                showError(response.message || 'Failed to reset password');
            }
        } catch (error) {
            console.error('Reset password error:', error);
            showError('An error occurred. Please try again.');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        resetError.classList.add('show');
    }
});
