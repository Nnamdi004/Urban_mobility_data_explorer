/**
 * Mock Data Module
 * Provides fake data while the backend isn't ready
 */

const MockData = {
    /**
     * Generate random number within range
     */
    random(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },

    /**
     * Generate random float within range
     */
    randomFloat(min, max, decimals = 2) {
        return parseFloat((Math.random() * (max - min) + min).toFixed(decimals));
    },

    /**
     * Get dashboard statistics
     */
    getStats() {
        return {
            success: true,
            data: {
                totalTrips: this.random(100000, 150000),
                avgDuration: this.random(18, 35),
                activeZones: this.random(40, 55),
                peakHour: ['7 AM', '8 AM', '9 AM', '5 PM', '6 PM'][this.random(0, 4)],
                changes: {
                    trips: this.randomFloat(-5, 15),
                    duration: this.randomFloat(-8, 8),
                    zones: this.random(-3, 8),
                }
            }
        };
    },

    /**
     * Get trip data for charts
     */
    getTrips(filters = {}) {
        const period = filters.period || '7d';
        const days = period === '7d' ? 7 : period === '30d' ? 30 : 90;
        
        const data = [];
        const labels = [];
        const now = new Date();

        for (let i = days - 1; i >= 0; i--) {
            const date = new Date(now);
            date.setDate(date.getDate() - i);
            
            labels.push(date.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric' 
            }));
            
            // Generate realistic daily trip volumes
            const baseVolume = 15000;
            const dayOfWeek = date.getDay();
            const weekendFactor = (dayOfWeek === 0 || dayOfWeek === 6) ? 0.6 : 1;
            const variance = this.random(-2000, 2000);
            
            data.push(Math.floor(baseVolume * weekendFactor + variance));
        }

        return {
            success: true,
            data: {
                labels,
                datasets: [{ data }]
            }
        };
    },

    /**
     * Get zone data
     */
    getZones() {
        const zones = [
            { id: 1, name: 'Downtown Core', trips: this.random(20000, 30000), score: 94 },
            { id: 2, name: 'Business District', trips: this.random(15000, 25000), score: 89 },
            { id: 3, name: 'Tech Hub', trips: this.random(12000, 20000), score: 85 },
            { id: 4, name: 'University Area', trips: this.random(10000, 18000), score: 82 },
            { id: 5, name: 'Shopping Center', trips: this.random(8000, 15000), score: 78 },
            { id: 6, name: 'Residential North', trips: this.random(5000, 12000), score: 75 },
            { id: 7, name: 'Industrial Zone', trips: this.random(4000, 10000), score: 70 },
            { id: 8, name: 'Airport Area', trips: this.random(6000, 14000), score: 72 },
            { id: 9, name: 'Harbor District', trips: this.random(3000, 8000), score: 68 },
            { id: 10, name: 'Suburban South', trips: this.random(2000, 6000), score: 65 }
        ];

        return {
            success: true,
            data: zones.sort((a, b) => b.trips - a.trips)
        };
    },

    /**
     * Get zone bar chart data
     */
    getZoneBarData() {
        return {
            labels: ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6'],
            data: [
                this.random(15000, 25000),
                this.random(12000, 20000),
                this.random(10000, 18000),
                this.random(8000, 15000),
                this.random(6000, 12000),
                this.random(4000, 10000)
            ]
        };
    },

    /**
     * Get scatter plot data for duration vs distance
     */
    getScatterData() {
        const data = [];
        for (let i = 0; i < 50; i++) {
            data.push({
                x: this.randomFloat(1, 20),  // Distance in km
                y: this.randomFloat(5, 60)    // Duration in minutes
            });
        }
        return data;
    },

    /**
     * Get hourly activity data for heatmap
     */
    getHourlyData() {
        const data = [];
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        
        for (let day = 0; day < 7; day++) {
            for (let hour = 0; hour < 24; hour++) {
                // Generate realistic patterns
                let intensity = 0.2;
                
                // Rush hours (weekdays)
                if (day < 5) {
                    if ((hour >= 7 && hour <= 9) || (hour >= 17 && hour <= 19)) {
                        intensity = this.randomFloat(0.7, 1.0);
                    } else if (hour >= 10 && hour <= 16) {
                        intensity = this.randomFloat(0.4, 0.6);
                    } else if (hour >= 6 && hour <= 22) {
                        intensity = this.randomFloat(0.2, 0.4);
                    }
                } else {
                    // Weekends - different pattern
                    if (hour >= 10 && hour <= 20) {
                        intensity = this.randomFloat(0.3, 0.6);
                    }
                }
                
                data.push({
                    day: days[day],
                    hour,
                    value: intensity
                });
            }
        }
        
        return data;
    },

    /**
     * Get comparison data for overview page
     */
    getComparisonData() {
        const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        const thisWeek = labels.map(() => this.random(12000, 22000));
        const lastWeek = labels.map(() => this.random(11000, 20000));

        return {
            labels,
            datasets: [
                { label: 'This Week', data: thisWeek },
                { label: 'Last Week', data: lastWeek }
            ]
        };
    },

    /**
     * Get transport type distribution
     */
    getTransportTypes() {
        return {
            labels: ['Car', 'Public Transit', 'Bicycle', 'Walking', 'Rideshare'],
            data: [45, 28, 12, 10, 5]
        };
    },

    /**
     * Get prediction data for insights page
     */
    getPredictionData() {
        const labels = [];
        const predicted = [];
        const historical = [];
        const now = new Date();

        // Generate 24 hour predictions
        for (let i = 0; i < 24; i++) {
            const hour = (now.getHours() + i) % 24;
            labels.push(`${hour}:00`);
            
            // Base patterns
            let base = 5000;
            if ((hour >= 7 && hour <= 9) || (hour >= 17 && hour <= 19)) {
                base = 18000;
            } else if (hour >= 10 && hour <= 16) {
                base = 12000;
            } else if (hour >= 6 || hour <= 22) {
                base = 8000;
            }

            predicted.push(base + this.random(-1000, 1000));
            historical.push(base + this.random(-2000, 2000));
        }

        return {
            labels,
            datasets: [
                { label: 'Predicted', data: predicted },
                { label: 'Historical Avg', data: historical }
            ]
        };
    },

    /**
     * Get correlation matrix data
     */
    getCorrelationMatrix() {
        const variables = ['Trips', 'Duration', 'Distance', 'Weather', 'Events'];
        const matrix = [];

        for (let i = 0; i < variables.length; i++) {
            for (let j = 0; j < variables.length; j++) {
                let value;
                if (i === j) {
                    value = 1;
                } else if (Math.abs(i - j) === 1) {
                    value = this.randomFloat(0.5, 0.9);
                } else {
                    value = this.randomFloat(-0.3, 0.7);
                }
                
                matrix.push({
                    x: variables[j],
                    y: variables[i],
                    value: parseFloat(value.toFixed(2))
                });
            }
        }

        return {
            variables,
            matrix
        };
    },

    /**
     * Get recent activity
     */
    getRecentActivity() {
        const activities = [
            { type: 'zone', text: 'New zone Downtown Core added', time: '2 minutes ago' },
            { type: 'data', text: 'Data updated for North District', time: '15 minutes ago' },
            { type: 'alert', text: 'Peak congestion alert in Zone 12', time: '1 hour ago' },
            { type: 'zone', text: 'Zone 5 boundary updated', time: '2 hours ago' },
            { type: 'data', text: 'Weekly report generated', time: '3 hours ago' }
        ];

        return activities;
    }
};

// Make MockData available globally
window.MockData = MockData;
