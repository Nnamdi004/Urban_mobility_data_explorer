/**
 * Dashboard Main JavaScript
 * Handles dashboard functionality, charts, and interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize dashboard components
    initSidebar();
    initMobileMenu();
    initCharts();
    initMaps();
    initHeatmap();
    initCorrelationMatrix();
    initInteractions();
});

/**
 * Sidebar toggle functionality
 */
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            // Store preference
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });

        // Restore preference
        if (localStorage.getItem('sidebarCollapsed') === 'true') {
            sidebar.classList.add('collapsed');
        }
    }
}

/**
 * Mobile menu functionality
 */
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.getElementById('sidebar');

    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 900) {
                if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                    sidebar.classList.remove('open');
                }
            }
        });
    }
}

/**
 * Initialize all charts
 */
function initCharts() {
    // Check if Chart.js is loaded, if not load it dynamically
    if (typeof Chart === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = () => {
            setupCharts();
        };
        document.head.appendChild(script);
    } else {
        setupCharts();
    }
}

/**
 * Setup all chart instances
 */
function setupCharts() {
    // Get current theme
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    
    // Set default Chart.js options based on theme
    Chart.defaults.color = isDark ? '#b0b0b0' : '#444444';
    Chart.defaults.borderColor = isDark ? '#222222' : '#dddddd';
    Chart.defaults.font.family = 'Inter, sans-serif';

    // Trip Volume Line Chart
    const tripVolumeChart = document.getElementById('tripVolumeChart');
    if (tripVolumeChart) {
        const tripData = MockData.getTrips({ period: '7d' });
        new Chart(tripVolumeChart, {
            type: 'line',
            data: {
                labels: tripData.data.labels,
                datasets: [{
                    label: 'Trips',
                    data: tripData.data.datasets[0].data,
                    borderColor: '#FFD600',
                    backgroundColor: 'rgba(255, 214, 0, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#FFD600'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: { color: 'rgba(100, 100, 100, 0.2)' }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });

        // Handle filter changes
        const lineChartFilter = document.getElementById('lineChartFilter');
        if (lineChartFilter) {
            lineChartFilter.addEventListener('change', (e) => {
                const newData = MockData.getTrips({ period: e.target.value });
                // Update chart data
                tripVolumeChart.__chart__.data.labels = newData.data.labels;
                tripVolumeChart.__chart__.data.datasets[0].data = newData.data.datasets[0].data;
                tripVolumeChart.__chart__.update();
            });
        }
    }

    // Zone Bar Chart
    const zoneBarChart = document.getElementById('zoneBarChart');
    if (zoneBarChart) {
        const zoneData = MockData.getZoneBarData();
        new Chart(zoneBarChart, {
            type: 'bar',
            data: {
                labels: zoneData.labels,
                datasets: [{
                    label: 'Trips',
                    data: zoneData.data,
                    backgroundColor: [
                        '#FFD600',
                        '#ffffff',
                        '#888888',
                        '#FFD600',
                        '#ffffff',
                        '#666666'
                    ],
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(100, 100, 100, 0.2)' }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    }

    // Scatter Plot
    const scatterChart = document.getElementById('scatterChart');
    if (scatterChart) {
        const scatterData = MockData.getScatterData();
        new Chart(scatterChart, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Trips',
                    data: scatterData,
                    backgroundColor: 'rgba(255, 214, 0, 0.6)',
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Distance (km)' },
                        grid: { color: 'rgba(100, 100, 100, 0.2)' }
                    },
                    y: {
                        title: { display: true, text: 'Duration (min)' },
                        grid: { color: 'rgba(100, 100, 100, 0.2)' }
                    }
                }
            }
        });
    }

    // Weekly Comparison Chart (Overview page)
    const weeklyComparisonChart = document.getElementById('weeklyComparisonChart');
    if (weeklyComparisonChart) {
        const comparisonData = MockData.getComparisonData();
        new Chart(weeklyComparisonChart, {
            type: 'bar',
            data: {
                labels: comparisonData.labels,
                datasets: [
                    {
                        label: 'This Week',
                        data: comparisonData.datasets[0].data,
                        backgroundColor: '#FFD600',
                        borderRadius: 4
                    },
                    {
                        label: 'Last Week',
                        data: comparisonData.datasets[1].data,
                        backgroundColor: '#666666',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(100, 100, 100, 0.2)' }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    }

    // Transport Type Doughnut Chart (Overview page)
    const transportTypeChart = document.getElementById('transportTypeChart');
    if (transportTypeChart) {
        const transportData = MockData.getTransportTypes();
        new Chart(transportTypeChart, {
            type: 'doughnut',
            data: {
                labels: transportData.labels,
                datasets: [{
                    data: transportData.data,
                    backgroundColor: [
                        '#FFD600',
                        '#ffffff',
                        '#888888',
                        '#444444',
                        '#222222'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    }

    // Prediction Chart (Insights page)
    const predictionChart = document.getElementById('predictionChart');
    if (predictionChart) {
        const predictionData = MockData.getPredictionData();
        new Chart(predictionChart, {
            type: 'line',
            data: {
                labels: predictionData.labels,
                datasets: [
                    {
                        label: 'Predicted',
                        data: predictionData.datasets[0].data,
                        borderColor: '#FFD600',
                        backgroundColor: 'rgba(255, 214, 0, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Historical Avg',
                        data: predictionData.datasets[1].data,
                        borderColor: '#888888',
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: { color: 'rgba(100, 100, 100, 0.2)' }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    }
}

/**
 * Initialize map placeholder
 */
function initMaps() {
    const mapContainer = document.getElementById('mapContainer');
    if (!mapContainer) return;

    // Map view toggle buttons
    const mapBtns = document.querySelectorAll('.map-btn');
    mapBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            mapBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const view = btn.dataset.view;
            console.log(`Switching to ${view} view`);
            // TODO: Implement actual map switching when map library is integrated
        });
    });
}

/**
 * Initialize hourly heatmap
 */
function initHeatmap() {
    const heatmapGrid = document.getElementById('hourlyHeatmap');
    if (!heatmapGrid) return;

    const hourlyData = MockData.getHourlyData();
    
    // Generate heatmap cells
    heatmapGrid.innerHTML = '';
    
    for (let hour = 0; hour < 24; hour++) {
        const hourData = hourlyData.filter(d => d.hour === hour);
        const avgValue = hourData.reduce((sum, d) => sum + d.value, 0) / hourData.length;
        
        const cell = document.createElement('div');
        cell.className = 'heatmap-cell';
        cell.style.backgroundColor = `rgba(255, 214, 0, ${avgValue})`;
        cell.title = `${hour}:00 - Activity: ${Math.round(avgValue * 100)}%`;
        
        heatmapGrid.appendChild(cell);
    }

    // Chart tabs
    const chartTabs = document.querySelectorAll('.chart-tab');
    chartTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            chartTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Regenerate heatmap with different data type
            const type = tab.dataset.type;
            console.log(`Switching heatmap to ${type}`);
            // Regenerate with slight variation
            initHeatmap();
        });
    });
}

/**
 * Initialize correlation matrix
 */
function initCorrelationMatrix() {
    const correlationMatrix = document.getElementById('correlationMatrix');
    if (!correlationMatrix) return;

    const { variables, matrix } = MockData.getCorrelationMatrix();
    
    correlationMatrix.innerHTML = '';
    
    matrix.forEach(cell => {
        const cellEl = document.createElement('div');
        cellEl.className = 'correlation-cell';
        
        // Color based on correlation value
        const absValue = Math.abs(cell.value);
        let color;
        if (cell.value > 0) {
            color = `rgba(0, 255, 170, ${absValue})`;
        } else {
            color = `rgba(255, 82, 82, ${absValue})`;
        }
        
        cellEl.style.backgroundColor = color;
        cellEl.textContent = cell.value.toFixed(2);
        cellEl.title = `${cell.y} vs ${cell.x}: ${cell.value}`;
        
        correlationMatrix.appendChild(cellEl);
    });
}

/**
 * Initialize interactive elements
 */
function initInteractions() {
    // Export button
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            alert('Export functionality coming soon!');
        });
    }

    // Refresh insights button
    const refreshInsights = document.getElementById('refreshInsights');
    if (refreshInsights) {
        refreshInsights.addEventListener('click', () => {
            refreshInsights.classList.add('loading');
            setTimeout(() => {
                refreshInsights.classList.remove('loading');
                // Reinitialize charts with new data
                initCharts();
                initHeatmap();
                initCorrelationMatrix();
            }, 1000);
        });
    }

    // Date range picker
    const dateRange = document.getElementById('dateRange');
    if (dateRange) {
        dateRange.addEventListener('change', (e) => {
            console.log(`Date range changed to: ${e.target.value}`);
            // Refresh data with new date range
        });
    }

    // Activity list load more (if exists)
    const viewAllLink = document.querySelector('.view-all-link');
    if (viewAllLink) {
        viewAllLink.addEventListener('click', (e) => {
            e.preventDefault();
            console.log('View all activity clicked');
        });
    }

    // Recommendation action buttons
    const recommendationBtns = document.querySelectorAll('.recommendation-card .btn');
    recommendationBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.textContent.trim();
            const card = btn.closest('.recommendation-card');
            const title = card.querySelector('.recommendation-title').textContent;
            console.log(`${action} clicked for: ${title}`);
            
            if (action === 'Implement') {
                btn.textContent = 'Implementing...';
                btn.disabled = true;
                setTimeout(() => {
                    btn.textContent = 'Implemented';
                    btn.classList.remove('btn-primary');
                    btn.classList.add('btn-ghost');
                }, 1500);
            }
        });
    });

    // Anomaly investigate buttons
    const anomalyBtns = document.querySelectorAll('.anomaly-item .btn');
    anomalyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const item = btn.closest('.anomaly-item');
            const text = item.querySelector('.anomaly-text').textContent;
            alert(`Investigating: ${text}`);
        });
    });
}
