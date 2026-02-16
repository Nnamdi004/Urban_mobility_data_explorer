/**
 * Bar Chart Module
 * Reusable bar chart component using Chart.js
 */

const BarChart = {
    /**
     * Default options for bar charts
     */
    defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: '#1a1a24',
                borderColor: '#2a2a3a',
                borderWidth: 1,
                titleColor: '#f0f0f5',
                bodyColor: '#a0a0b0',
                padding: 12,
                cornerRadius: 8,
                displayColors: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: { 
                    color: '#1a1a24',
                    drawBorder: false
                },
                ticks: {
                    color: '#606070',
                    padding: 10
                }
            },
            x: {
                grid: { display: false },
                ticks: {
                    color: '#606070',
                    padding: 10
                }
            }
        }
    },

    /**
     * Default colors for bar charts
     */
    colors: [
        'rgba(0, 255, 170, 0.8)',
        'rgba(0, 204, 255, 0.8)',
        'rgba(167, 139, 250, 0.8)',
        'rgba(255, 183, 77, 0.8)',
        'rgba(255, 82, 82, 0.8)',
        'rgba(0, 255, 170, 0.5)',
        'rgba(0, 204, 255, 0.5)'
    ],

    /**
     * Create a new bar chart
     * @param {string|HTMLCanvasElement} canvas - Canvas element or selector
     * @param {Object} data - Chart data { labels: [], datasets: [] }
     * @param {Object} options - Custom options to override defaults
     * @returns {Chart} Chart.js instance
     */
    create(canvas, data, options = {}) {
        const ctx = typeof canvas === 'string' ? document.getElementById(canvas) : canvas;
        if (!ctx) {
            console.error('BarChart: Canvas element not found');
            return null;
        }

        // Apply colors if not provided
        if (data.datasets && data.datasets[0] && !data.datasets[0].backgroundColor) {
            data.datasets[0].backgroundColor = this.colors.slice(0, data.labels?.length || this.colors.length);
        }

        // Add border radius to bars
        if (data.datasets) {
            data.datasets.forEach(dataset => {
                if (!dataset.borderRadius) {
                    dataset.borderRadius = 4;
                }
            });
        }

        const config = {
            type: 'bar',
            data: data,
            options: this.mergeOptions(options)
        };

        return new Chart(ctx, config);
    },

    /**
     * Create a horizontal bar chart
     */
    createHorizontal(canvas, data, options = {}) {
        const horizontalOptions = {
            indexAxis: 'y',
            ...options
        };

        return this.create(canvas, data, horizontalOptions);
    },

    /**
     * Create a stacked bar chart
     */
    createStacked(canvas, data, options = {}) {
        const stackedOptions = {
            scales: {
                x: { stacked: true },
                y: { stacked: true }
            },
            ...options
        };

        return this.create(canvas, data, stackedOptions);
    },

    /**
     * Merge custom options with defaults
     */
    mergeOptions(customOptions) {
        return {
            ...this.defaultOptions,
            ...customOptions,
            plugins: {
                ...this.defaultOptions.plugins,
                ...(customOptions.plugins || {})
            },
            scales: {
                ...this.defaultOptions.scales,
                ...(customOptions.scales || {})
            }
        };
    },

    /**
     * Update chart data
     */
    update(chart, newData, animate = true) {
        if (!chart) return;

        if (newData.labels) {
            chart.data.labels = newData.labels;
        }

        if (newData.datasets) {
            newData.datasets.forEach((dataset, index) => {
                if (chart.data.datasets[index]) {
                    Object.assign(chart.data.datasets[index], dataset);
                }
            });
        }

        chart.update(animate ? 'default' : 'none');
    },

    /**
     * Destroy chart instance
     */
    destroy(chart) {
        if (chart) {
            chart.destroy();
        }
    }
};

// Make BarChart available globally
window.BarChart = BarChart;
