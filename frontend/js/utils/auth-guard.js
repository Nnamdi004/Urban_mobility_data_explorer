/**
 * Auth Guard Module
 * Handles authentication state and route protection
 */

const AuthGuard = {
    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
        return !!token;
    },

    /**
     * Get current user
     */
    getUser() {
        const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
        if (userStr) {
            try {
                return JSON.parse(userStr);
            } catch (e) {
                return null;
            }
        }
        return null;
    },

    /**
     * Get auth token
     */
    getToken() {
        return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    },

    /**
     * Redirect to login if not authenticated
     */
    requireAuth() {
        if (!this.isAuthenticated()) {
            // Store intended destination
            sessionStorage.setItem('redirectAfterLogin', window.location.href);
            window.location.href = '../auth/login.html';
            return false;
        }
        return true;
    },

    /**
     * Redirect to dashboard if already authenticated
     */
    redirectIfAuthenticated() {
        if (this.isAuthenticated()) {
            window.location.href = '../dashboard/dashboard.html';
            return true;
        }
        return false;
    },

    /**
     * Logout user
     */
    logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        sessionStorage.removeItem('authToken');
        sessionStorage.removeItem('user');
        window.location.href = '../auth/login.html';
    },

    /**
     * Update user info in storage
     */
    updateUser(user) {
        const storage = localStorage.getItem('authToken') ? localStorage : sessionStorage;
        storage.setItem('user', JSON.stringify(user));
    },

    /**
     * Initialize auth guard on protected pages
     */
    init() {
        // Check authentication on protected pages (dashboard)
        const isDashboardPage = window.location.pathname.includes('/dashboard/');
        
        if (isDashboardPage) {
            if (!this.requireAuth()) {
                return;
            }

            // Update UI with user info
            this.updateUIWithUser();

            // Setup logout handler
            this.setupLogoutHandler();
        }

        // Redirect from auth pages if already logged in
        const isAuthPage = window.location.pathname.includes('/auth/');
        const isLoginOrSignup = window.location.pathname.includes('login.html') || 
                                window.location.pathname.includes('signup.html');
        
        if (isAuthPage && isLoginOrSignup) {
            this.redirectIfAuthenticated();
        }
    },

    /**
     * Update UI elements with user information
     */
    updateUIWithUser() {
        const user = this.getUser();
        if (!user) return;

        // Update user name elements
        const userNameEls = document.querySelectorAll('#userName, .user-name');
        userNameEls.forEach(el => {
            el.textContent = user.name || user.email.split('@')[0];
        });

        // Update user email elements
        const userEmailEls = document.querySelectorAll('#userEmail, .user-email');
        userEmailEls.forEach(el => {
            el.textContent = user.email;
        });

        // Update user avatar
        const userAvatarEls = document.querySelectorAll('.user-avatar');
        userAvatarEls.forEach(el => {
            if (user.avatar) {
                el.innerHTML = `<img src="${user.avatar}" alt="${user.name}">`;
            } else {
                // Show initials
                const initials = (user.name || user.email)
                    .split(' ')
                    .map(n => n[0])
                    .join('')
                    .toUpperCase()
                    .slice(0, 2);
                el.textContent = initials;
            }
        });
    },

    /**
     * Setup logout button handler
     */
    setupLogoutHandler() {
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        }
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    AuthGuard.init();
});

// Make AuthGuard available globally
window.AuthGuard = AuthGuard;
