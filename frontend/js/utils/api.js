/**
 * API Module
 * Centralized API calls to the backend
 */

const API = {
    // Base URL - connected to Flask backend
    baseURL: 'http://localhost:5000/api',
    
    // Use mock auth for demonstration (real data from backend)
    useMock: true,

    /**
     * Generic fetch wrapper with error handling
     */
    async request(endpoint, options = {}) {
        if (this.useMock) {
            return this.mockRequest(endpoint, options);
        }

        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        // Add auth token if available
        const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    /**
     * Mock request handler for development
     */
    async mockRequest(endpoint, options = {}) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 400));

        const body = options.body ? JSON.parse(options.body) : {};

        // Mock responses based on endpoint
        switch (endpoint) {
            case '/auth/login':
                return this.mockLogin(body);
            case '/auth/signup':
                return this.mockSignup(body);
            case '/auth/forgot-password':
                return this.mockForgotPassword(body);
            case '/auth/verify-code':
                return this.mockVerifyCode(body);
            case '/auth/reset-password':
                return this.mockResetPassword(body);
            case '/auth/resend-code':
                return this.mockResendCode(body);
            case '/mobility/stats':
                return MockData.getStats();
            case '/mobility/trips':
                return MockData.getTrips(body);
            case '/mobility/zones':
                return MockData.getZones();
            default:
                return { success: true, data: {} };
        }
    },

    // Mock auth responses
    mockLogin(body) {
        const { email, password } = body;
        
        // Demo credentials
        if (email === 'demo@urbanmobility.com' && password === 'demo1234') {
            return {
                success: true,
                token: 'mock-jwt-token-' + Date.now(),
                user: {
                    id: '1',
                    name: 'Demo User',
                    email: email,
                    avatar: null
                }
            };
        }

        // Allow any valid-looking credentials for demo
        if (email && password && password.length >= 6) {
            return {
                success: true,
                token: 'mock-jwt-token-' + Date.now(),
                user: {
                    id: '1',
                    name: email.split('@')[0],
                    email: email,
                    avatar: null
                }
            };
        }

        return {
            success: false,
            message: 'Invalid email or password'
        };
    },

    mockSignup(body) {
        const { email, fullName, password } = body;

        if (email && fullName && password) {
            return {
                success: true,
                message: 'Verification code sent to your email'
            };
        }

        return {
            success: false,
            message: 'Please provide all required information'
        };
    },

    mockForgotPassword(body) {
        const { email } = body;

        if (email) {
            return {
                success: true,
                message: 'Verification code sent to your email'
            };
        }

        return {
            success: false,
            message: 'Email not found'
        };
    },

    mockVerifyCode(body) {
        const { code } = body;

        // Accept any 6-digit code or specific test codes
        if (code === '123456' || code.length === 6) {
            return {
                success: true,
                token: 'verification-token-' + Date.now()
            };
        }

        return {
            success: false,
            message: 'Invalid verification code'
        };
    },

    mockResetPassword(body) {
        const { token, password } = body;

        if (token && password && password.length >= 8) {
            return {
                success: true,
                message: 'Password reset successfully'
            };
        }

        return {
            success: false,
            message: 'Failed to reset password'
        };
    },

    mockResendCode(body) {
        return {
            success: true,
            message: 'New verification code sent'
        };
    },

    // Auth API methods
    async login(credentials) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    },

    async signup(userData) {
        return this.request('/auth/signup', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },

    async forgotPassword(data) {
        return this.request('/auth/forgot-password', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    async verifyCode(data) {
        return this.request('/auth/verify-code', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    async resetPassword(data) {
        return this.request('/auth/reset-password', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    async resendCode(data) {
        return this.request('/auth/resend-code', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    // Mobility Data API methods
    async getStats() {
        return this.request('/mobility/stats');
    },

    async getTrips(filters = {}) {
        return this.request('/mobility/trips', {
            method: 'POST',
            body: JSON.stringify(filters)
        });
    },

    async getZones() {
        return this.request('/mobility/zones');
    },

    async getZoneDetails(zoneId) {
        return this.request(`/mobility/zones/${zoneId}`);
    },

    async getTripVolume(period = '7d') {
        return this.request(`/mobility/trip-volume?period=${period}`);
    },

    async getHeatmapData() {
        return this.request('/mobility/heatmap');
    },

    // User API methods
    async getProfile() {
        return this.request('/user/profile');
    },

    async updateProfile(data) {
        return this.request('/user/profile', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    async logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        sessionStorage.removeItem('authToken');
        sessionStorage.removeItem('user');
        return { success: true };
    }
};

// Make API available globally
window.API = API;
