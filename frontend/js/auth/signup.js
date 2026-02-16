/**
 * Signup Page JavaScript
 * Handles signup form submission, validation, and password strength
 */

document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const signupError = document.getElementById('signupError');
    const errorMessage = document.getElementById('errorMessage');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const passwordToggles = document.querySelectorAll('.password-toggle');
    const strengthBars = document.querySelectorAll('.strength-bar');
    const strengthText = document.getElementById('strengthText');

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
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = signupForm.querySelector('.auth-submit');
        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const terms = document.getElementById('terms').checked;

        // Hide previous errors
        signupError.classList.remove('show');

        // Validation
        if (!fullName || !email || !password || !confirmPassword) {
            showError('Please fill in all fields');
            return;
        }

        if (!isValidEmail(email)) {
            showError('Please enter a valid email address');
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

        if (!terms) {
            showError('Please accept the Terms of Service');
            return;
        }

        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        try {
            // Call API (using mock for now)
            const response = await window.API.signup({ fullName, email, password });

            if (response.success) {
                // Store email for verification page
                sessionStorage.setItem('signupEmail', email);
                
                // Redirect to verification or success
                window.location.href = 'verify-code.html';
            } else {
                showError(response.message || 'Signup failed');
            }
        } catch (error) {
            console.error('Signup error:', error);
            showError('An error occurred. Please try again.');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });

    // Helper functions
    function showError(message) {
        errorMessage.textContent = message;
        signupError.classList.add('show');
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Social signup handlers
    const socialBtns = document.querySelectorAll('.social-btn');
    socialBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const provider = btn.textContent.includes('Google') ? 'google' : 'github';
            console.log(`Initiating ${provider} signup...`);
            alert(`${provider.charAt(0).toUpperCase() + provider.slice(1)} signup coming soon!`);
        });
    });
});
