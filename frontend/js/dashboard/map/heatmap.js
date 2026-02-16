/**
 * Heatmap Module
 * Handles heatmap visualization for mobility data
 */

const Heatmap = {
    map: null,
    heatLayer: null,
    data: [],

    /**
     * Default configuration
     */
    config: {
        radius: 25,
        blur: 15,
        maxZoom: 17,
        max: 1.0,
        minOpacity: 0.3,
        gradient: {
            0.0: '#0a0a0f',
            0.2: '#1a1a24',
            0.4: '#00ccff',
            0.6: '#00ffaa',
            0.8: '#ffb74d',
            1.0: '#ff5252'
        }
    },

    /**
     * Initialize heatmap on an existing map
     * @param {Object} map - Leaflet map instance
     * @param {Object} options - Heatmap configuration
     */
    init(map, options = {}) {
        this.map = map;
        this.config = { ...this.config, ...options };

        // Check if heatmap plugin is loaded
        if (typeof L.heatLayer === 'undefined') {
            this.loadHeatmapPlugin(() => this.createHeatLayer());
        } else {
            this.createHeatLayer();
        }
    },

    /**
     * Load Leaflet.heat plugin dynamically
     */
    loadHeatmapPlugin(callback) {
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js';
        script.onload = callback;
        document.head.appendChild(script);
    },

    /**
     * Create the heat layer
     */
    createHeatLayer() {
        if (!this.map) return;

        // Generate sample data if none provided
        if (this.data.length === 0) {
            this.data = this.generateSampleData();
        }

        this.heatLayer = L.heatLayer(this.data, {
            radius: this.config.radius,
            blur: this.config.blur,
            maxZoom: this.config.maxZoom,
            max: this.config.max,
            minOpacity: this.config.minOpacity,
            gradient: this.config.gradient
        }).addTo(this.map);
    },

    /**
     * Generate sample heatmap data
     */
    generateSampleData() {
        const data = [];
        const center = this.map.getCenter();
        
        // Generate clusters of activity
        const clusters = [
            { lat: center.lat + 0.02, lng: center.lng - 0.01, intensity: 0.9, spread: 0.015 },
            { lat: center.lat - 0.01, lng: center.lng + 0.02, intensity: 0.8, spread: 0.012 },
            { lat: center.lat + 0.015, lng: center.lng + 0.015, intensity: 0.7, spread: 0.01 },
            { lat: center.lat - 0.02, lng: center.lng - 0.015, intensity: 0.6, spread: 0.008 },
            { lat: center.lat, lng: center.lng, intensity: 1.0, spread: 0.02 }
        ];

        clusters.forEach(cluster => {
            // Generate points around each cluster
            const numPoints = Math.floor(50 * cluster.intensity);
            
            for (let i = 0; i < numPoints; i++) {
                const lat = cluster.lat + (Math.random() - 0.5) * cluster.spread * 2;
                const lng = cluster.lng + (Math.random() - 0.5) * cluster.spread * 2;
                const intensity = cluster.intensity * (0.5 + Math.random() * 0.5);
                
                data.push([lat, lng, intensity]);
            }
        });

        return data;
    },

    /**
     * Set heatmap data
     * @param {Array} data - Array of [lat, lng, intensity] points
     */
    setData(data) {
        this.data = data;
        
        if (this.heatLayer) {
            this.heatLayer.setLatLngs(data);
        }
    },

    /**
     * Add points to existing heatmap
     * @param {Array} points - Array of [lat, lng, intensity] points
     */
    addPoints(points) {
        this.data = this.data.concat(points);
        
        if (this.heatLayer) {
            this.heatLayer.setLatLngs(this.data);
        }
    },

    /**
     * Clear all heatmap data
     */
    clearData() {
        this.data = [];
        
        if (this.heatLayer) {
            this.heatLayer.setLatLngs([]);
        }
    },

    /**
     * Update heatmap configuration
     */
    setOptions(options) {
        this.config = { ...this.config, ...options };
        
        if (this.heatLayer) {
            this.heatLayer.setOptions(this.config);
        }
    },

    /**
     * Set radius
     */
    setRadius(radius) {
        this.config.radius = radius;
        this.setOptions({ radius });
    },

    /**
     * Set blur amount
     */
    setBlur(blur) {
        this.config.blur = blur;
        this.setOptions({ blur });
    },

    /**
     * Set maximum intensity
     */
    setMax(max) {
        this.config.max = max;
        this.setOptions({ max });
    },

    /**
     * Set custom gradient
     */
    setGradient(gradient) {
        this.config.gradient = gradient;
        this.setOptions({ gradient });
    },

    /**
     * Show heatmap
     */
    show() {
        if (this.heatLayer && this.map) {
            this.heatLayer.addTo(this.map);
        }
    },

    /**
     * Hide heatmap
     */
    hide() {
        if (this.heatLayer && this.map) {
            this.map.removeLayer(this.heatLayer);
        }
    },

    /**
     * Toggle heatmap visibility
     */
    toggle() {
        if (!this.heatLayer || !this.map) return;

        if (this.map.hasLayer(this.heatLayer)) {
            this.hide();
        } else {
            this.show();
        }
    },

    /**
     * Load heatmap data from API
     */
    async loadData(filters = {}) {
        try {
            const response = await window.API.getHeatmapData(filters);
            
            if (response.success && response.data) {
                this.setData(response.data);
            }
        } catch (error) {
            console.error('Failed to load heatmap data:', error);
        }
    },

    /**
     * Export heatmap data as GeoJSON
     */
    exportAsGeoJSON() {
        return {
            type: 'FeatureCollection',
            features: this.data.map(point => ({
                type: 'Feature',
                geometry: {
                    type: 'Point',
                    coordinates: [point[1], point[0]] // GeoJSON uses [lng, lat]
                },
                properties: {
                    intensity: point[2]
                }
            }))
        };
    },

    /**
     * Generate heatmap from trip data
     * @param {Array} trips - Array of trip objects with origin/destination
     */
    generateFromTrips(trips) {
        const data = [];

        trips.forEach(trip => {
            // Add origin points
            if (trip.origin) {
                data.push([trip.origin.lat, trip.origin.lng, 0.5]);
            }
            
            // Add destination points (weighted higher)
            if (trip.destination) {
                data.push([trip.destination.lat, trip.destination.lng, 0.8]);
            }
        });

        this.setData(data);
    },

    /**
     * Create a time-animated heatmap
     * @param {Array} timeData - Array of { time, points } objects
     * @param {number} interval - Animation interval in ms
     */
    animateOverTime(timeData, interval = 1000) {
        let currentIndex = 0;

        const animate = () => {
            if (currentIndex >= timeData.length) {
                currentIndex = 0;
            }

            this.setData(timeData[currentIndex].points);
            currentIndex++;

            setTimeout(animate, interval);
        };

        animate();
    },

    /**
     * Destroy heatmap
     */
    destroy() {
        if (this.heatLayer && this.map) {
            this.map.removeLayer(this.heatLayer);
        }
        this.heatLayer = null;
        this.data = [];
    }
};

// Make Heatmap available globally
window.Heatmap = Heatmap;
