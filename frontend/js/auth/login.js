/**
 * Login Page JavaScript
 * Handles login form submission and validation
 */

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    const errorMessage = document.getElementById('errorMessage');
    const passwordToggles = document.querySelectorAll('.password-toggle');

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

    // Form submission
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = loginForm.querySelector('.auth-submit');
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;

        // Hide previous errors
        loginError.classList.remove('show');

        // Basic validation
        if (!email || !password) {
            showError('Please fill in all fields');
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
            const response = await window.API.login({ email, password, remember });

            if (response.success) {
                // Store auth token
                if (remember) {
                    localStorage.setItem('authToken', response.token);
                    localStorage.setItem('user', JSON.stringify(response.user));
                } else {
                    sessionStorage.setItem('authToken', response.token);
                    sessionStorage.setItem('user', JSON.stringify(response.user));
                }

                // Redirect to dashboard
                window.location.href = '../dashboard/dashboard.html';
            } else {
                showError(response.message || 'Login failed');
            }
        } catch (error) {
            console.error('Login error:', error);
            showError('An error occurred. Please try again.');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });

    // Helper functions
    function showError(message) {
        errorMessage.textContent = message;
        loginError.classList.add('show');
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Social login handlers
    const socialBtns = document.querySelectorAll('.social-btn');
    socialBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const provider = btn.textContent.includes('Google') ? 'google' : 'github';
            console.log(`Initiating ${provider} login...`);
            // TODO: Implement OAuth flow
            alert(`${provider.charAt(0).toUpperCase() + provider.slice(1)} login coming soon!`);
        });
    });
});
