/**
 * Scatter Plot Module
 * Reusable scatter plot component using Chart.js
 */

const ScatterPlot = {
    /**
     * Default options for scatter plots
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
                displayColors: false,
                callbacks: {
                    label: function(context) {
                        return `X: ${context.parsed.x.toFixed(2)}, Y: ${context.parsed.y.toFixed(2)}`;
                    }
                }
            }
        },
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                grid: { 
                    color: '#1a1a24',
                    drawBorder: false
                },
                ticks: {
                    color: '#606070',
                    padding: 10
                }
            },
            y: {
                grid: { 
                    color: '#1a1a24',
                    drawBorder: false
                },
                ticks: {
                    color: '#606070',
                    padding: 10
                }
            }
        },
        elements: {
            point: {
                radius: 6,
                hoverRadius: 8,
                hitRadius: 12
            }
        }
    },

    /**
     * Default colors for scatter plots
     */
    colors: [
        'rgba(0, 204, 255, 0.6)',
        'rgba(0, 255, 170, 0.6)',
        'rgba(167, 139, 250, 0.6)',
        'rgba(255, 183, 77, 0.6)',
        'rgba(255, 82, 82, 0.6)'
    ],

    /**
     * Create a new scatter plot
     * @param {string|HTMLCanvasElement} canvas - Canvas element or selector
     * @param {Object} data - Chart data { datasets: [{ data: [{x, y}] }] }
     * @param {Object} options - Custom options to override defaults
     * @returns {Chart} Chart.js instance
     */
    create(canvas, data, options = {}) {
        const ctx = typeof canvas === 'string' ? document.getElementById(canvas) : canvas;
        if (!ctx) {
            console.error('ScatterPlot: Canvas element not found');
            return null;
        }

        // Apply colors if not provided
        if (data.datasets) {
            data.datasets.forEach((dataset, index) => {
                if (!dataset.backgroundColor) {
                    dataset.backgroundColor = this.colors[index % this.colors.length];
                }
                if (!dataset.borderColor) {
                    dataset.borderColor = dataset.backgroundColor.replace('0.6', '1');
                }
            });
        }

        const config = {
            type: 'scatter',
            data: data,
            options: this.mergeOptions(options)
        };

        return new Chart(ctx, config);
    },

    /**
     * Create a bubble chart (scatter with variable point sizes)
     */
    createBubble(canvas, data, options = {}) {
        const ctx = typeof canvas === 'string' ? document.getElementById(canvas) : canvas;
        if (!ctx) {
            console.error('ScatterPlot: Canvas element not found');
            return null;
        }

        // Apply colors if not provided
        if (data.datasets) {
            data.datasets.forEach((dataset, index) => {
                if (!dataset.backgroundColor) {
                    dataset.backgroundColor = this.colors[index % this.colors.length];
                }
            });
        }

        const config = {
            type: 'bubble',
            data: data,
            options: this.mergeOptions(options)
        };

        return new Chart(ctx, config);
    },

    /**
     * Create a scatter plot with regression line
     */
    createWithRegression(canvas, data, options = {}) {
        // Calculate regression line
        const points = data.datasets[0].data;
        const regression = this.calculateLinearRegression(points);

        // Add regression line as separate dataset
        const minX = Math.min(...points.map(p => p.x));
        const maxX = Math.max(...points.map(p => p.x));

        data.datasets.push({
            type: 'line',
            label: 'Trend',
            data: [
                { x: minX, y: regression.predict(minX) },
                { x: maxX, y: regression.predict(maxX) }
            ],
            borderColor: 'rgba(255, 183, 77, 0.8)',
            borderWidth: 2,
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false
        });

        return this.create(canvas, data, options);
    },

    /**
     * Calculate linear regression for a set of points
     */
    calculateLinearRegression(points) {
        const n = points.length;
        let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;

        points.forEach(point => {
            sumX += point.x;
            sumY += point.y;
            sumXY += point.x * point.y;
            sumX2 += point.x * point.x;
        });

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;

        return {
            slope,
            intercept,
            predict: (x) => slope * x + intercept
        };
    },

    /**
     * Create a clustered scatter plot with different colors per cluster
     */
    createClustered(canvas, clusteredData, options = {}) {
        // clusteredData format: { clusters: [{ label, data: [{x, y}] }] }
        const data = {
            datasets: clusteredData.clusters.map((cluster, index) => ({
                label: cluster.label,
                data: cluster.data,
                backgroundColor: this.colors[index % this.colors.length]
            }))
        };

        const clusteredOptions = {
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

        return this.create(canvas, data, clusteredOptions);
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
                x: {
                    ...this.defaultOptions.scales.x,
                    ...(customOptions.scales?.x || {})
                },
                y: {
                    ...this.defaultOptions.scales.y,
                    ...(customOptions.scales?.y || {})
                }
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
     * Add new points to scatter plot
     */
    addPoints(chart, datasetIndex, points) {
        if (!chart || !chart.data.datasets[datasetIndex]) return;

        const dataset = chart.data.datasets[datasetIndex];
        if (Array.isArray(points)) {
            dataset.data.push(...points);
        } else {
            dataset.data.push(points);
        }

        chart.update();
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

// Make ScatterPlot available globally
window.ScatterPlot = ScatterPlot;
