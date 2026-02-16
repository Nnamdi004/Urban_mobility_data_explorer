/**
 * Line Chart Module
 * Reusable line chart component using Chart.js
 */

const LineChart = {
    /**
     * Default options for line charts
     */
    defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false
        },
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
                displayColors: true,
                usePointStyle: true
            }
        },
        scales: {
            y: {
                beginAtZero: false,
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
                    padding: 10,
                    maxRotation: 0
                }
            }
        },
        elements: {
            point: {
                radius: 4,
                hoverRadius: 6,
                hitRadius: 10
            },
            line: {
                tension: 0.4,
                borderWidth: 2
            }
        }
    },

    /**
     * Default colors for line charts
     */
    colors: {
        primary: {
            border: '#00ffaa',
            background: 'rgba(0, 255, 170, 0.1)',
            point: '#00ffaa'
        },
        secondary: {
            border: '#00ccff',
            background: 'rgba(0, 204, 255, 0.1)',
            point: '#00ccff'
        },
        muted: {
            border: '#606070',
            background: 'rgba(96, 96, 112, 0.1)',
            point: '#606070'
        }
    },

    /**
     * Create a new line chart
     * @param {string|HTMLCanvasElement} canvas - Canvas element or selector
     * @param {Object} data - Chart data { labels: [], datasets: [] }
     * @param {Object} options - Custom options to override defaults
     * @returns {Chart} Chart.js instance
     */
    create(canvas, data, options = {}) {
        const ctx = typeof canvas === 'string' ? document.getElementById(canvas) : canvas;
        if (!ctx) {
            console.error('LineChart: Canvas element not found');
            return null;
        }

        // Apply default styling to datasets
        if (data.datasets) {
            data.datasets.forEach((dataset, index) => {
                const colorSet = index === 0 ? this.colors.primary : 
                                 index === 1 ? this.colors.secondary : this.colors.muted;
                
                dataset.borderColor = dataset.borderColor || colorSet.border;
                dataset.backgroundColor = dataset.backgroundColor || colorSet.background;
                dataset.pointBackgroundColor = dataset.pointBackgroundColor || colorSet.point;
                dataset.fill = dataset.fill !== undefined ? dataset.fill : true;
            });
        }

        const config = {
            type: 'line',
            data: data,
            options: this.mergeOptions(options)
        };

        return new Chart(ctx, config);
    },

    /**
     * Create an area chart (line with fill)
     */
    createArea(canvas, data, options = {}) {
        if (data.datasets) {
            data.datasets.forEach(dataset => {
                dataset.fill = true;
            });
        }

        return this.create(canvas, data, options);
    },

    /**
     * Create a multi-line comparison chart
     */
    createComparison(canvas, data, options = {}) {
        const comparisonOptions = {
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#a0a0b0',
                        usePointStyle: true,
                        padding: 20
                    }
                }
            },
            ...options
        };

        // Style secondary lines as dashed
        if (data.datasets && data.datasets.length > 1) {
            data.datasets.slice(1).forEach(dataset => {
                if (!dataset.borderDash) {
                    dataset.borderDash = [5, 5];
                }
                if (dataset.fill === undefined) {
                    dataset.fill = false;
                }
            });
        }

        return this.create(canvas, data, comparisonOptions);
    },

    /**
     * Create a real-time updating chart
     */
    createRealTime(canvas, data, options = {}) {
        const chart = this.create(canvas, data, options);
        
        // Add method to push new data
        chart.pushData = (label, values) => {
            chart.data.labels.push(label);
            values.forEach((value, index) => {
                if (chart.data.datasets[index]) {
                    chart.data.datasets[index].data.push(value);
                }
            });

            // Keep maximum 20 points visible
            const maxPoints = options.maxPoints || 20;
            if (chart.data.labels.length > maxPoints) {
                chart.data.labels.shift();
                chart.data.datasets.forEach(dataset => {
                    dataset.data.shift();
                });
            }

            chart.update('none');
        };

        return chart;
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
            },
            elements: {
                ...this.defaultOptions.elements,
                ...(customOptions.elements || {})
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
                    chart.data.datasets[index].data = dataset.data;
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

// Make LineChart available globally
window.LineChart = LineChart;
