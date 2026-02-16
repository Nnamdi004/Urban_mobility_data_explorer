/**
 * Zone Map Module
 * Handles zone visualization on maps
 */

const ZoneMap = {
    map: null,
    zones: [],
    markers: [],
    selectedZone: null,

    /**
     * Default map configuration
     */
    config: {
        center: [40.7128, -74.0060], // Default: New York City
        zoom: 12,
        style: 'dark',
        colors: {
            high: '#00ffaa',
            medium: '#00ccff',
            low: '#606070',
            selected: '#ff5252'
        }
    },

    /**
     * Initialize the map
     * @param {string} containerId - ID of the container element
     * @param {Object} options - Map configuration options
     */
    init(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('ZoneMap: Container not found');
            return null;
        }

        this.config = { ...this.config, ...options };

        // Check if Leaflet is available
        if (typeof L === 'undefined') {
            this.showPlaceholder(container);
            this.loadLeaflet(() => this.createMap(container));
            return;
        }

        this.createMap(container);
    },

    /**
     * Show placeholder while map loads
     */
    showPlaceholder(container) {
        container.innerHTML = `
            <div class="map-placeholder">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20M2 12h20"/>
                </svg>
                <p>Loading map...</p>
            </div>
        `;
    },

    /**
     * Load Leaflet library dynamically
     */
    loadLeaflet(callback) {
        // Load CSS
        const css = document.createElement('link');
        css.rel = 'stylesheet';
        css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
        document.head.appendChild(css);

        // Load JS
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
        script.onload = callback;
        document.head.appendChild(script);
    },

    /**
     * Create the map instance
     */
    createMap(container) {
        container.innerHTML = '';

        this.map = L.map(container, {
            center: this.config.center,
            zoom: this.config.zoom,
            zoomControl: true,
            attributionControl: false
        });

        // Add dark-themed tile layer
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            maxZoom: 19
        }).addTo(this.map);

        // Add attribution
        L.control.attribution({
            prefix: false
        }).addAttribution('© <a href="https://carto.com/">CARTO</a>').addTo(this.map);

        // Load sample zones
        this.loadSampleZones();
    },

    /**
     * Load sample zone data
     */
    loadSampleZones() {
        // Sample zones for demonstration
        const sampleZones = [
            { id: 1, name: 'Downtown Core', lat: 40.7580, lng: -73.9855, activity: 0.95, trips: 25000 },
            { id: 2, name: 'Business District', lat: 40.7484, lng: -73.9857, activity: 0.88, trips: 20000 },
            { id: 3, name: 'Tech Hub', lat: 40.7282, lng: -73.7949, activity: 0.82, trips: 18000 },
            { id: 4, name: 'University Area', lat: 40.8075, lng: -73.9626, activity: 0.75, trips: 15000 },
            { id: 5, name: 'Shopping Center', lat: 40.7549, lng: -73.9840, activity: 0.70, trips: 12000 },
            { id: 6, name: 'Residential North', lat: 40.8448, lng: -73.8648, activity: 0.55, trips: 8000 },
            { id: 7, name: 'Industrial Zone', lat: 40.6501, lng: -74.0088, activity: 0.45, trips: 5000 },
            { id: 8, name: 'Airport Area', lat: 40.6413, lng: -73.7781, activity: 0.60, trips: 10000 }
        ];

        this.addZones(sampleZones);
    },

    /**
     * Add zones to the map
     * @param {Array} zones - Array of zone objects
     */
    addZones(zones) {
        this.zones = zones;

        zones.forEach(zone => {
            const marker = this.createZoneMarker(zone);
            this.markers.push(marker);
        });
    },

    /**
     * Create a zone marker
     */
    createZoneMarker(zone) {
        const color = this.getActivityColor(zone.activity);
        const size = 20 + (zone.activity * 30);

        const icon = L.divIcon({
            className: 'zone-marker',
            html: `
                <div class="zone-marker-inner" style="
                    width: ${size}px;
                    height: ${size}px;
                    background: ${color};
                    border-radius: 50%;
                    opacity: 0.8;
                    box-shadow: 0 0 15px ${color};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 10px;
                    font-weight: bold;
                    color: #0a0a0f;
                ">
                    ${zone.id}
                </div>
            `,
            iconSize: [size, size],
            iconAnchor: [size / 2, size / 2]
        });

        const marker = L.marker([zone.lat, zone.lng], { icon })
            .addTo(this.map)
            .bindPopup(this.createPopupContent(zone));

        marker.on('click', () => this.onZoneClick(zone));

        return marker;
    },

    /**
     * Create popup content for a zone
     */
    createPopupContent(zone) {
        return `
            <div class="zone-popup">
                <h4 style="margin: 0 0 8px 0; color: #f0f0f5;">${zone.name}</h4>
                <div style="color: #a0a0b0; font-size: 13px;">
                    <p style="margin: 4px 0;">Trips: <strong style="color: #00ffaa;">${zone.trips.toLocaleString()}</strong></p>
                    <p style="margin: 4px 0;">Activity: <strong style="color: #00ccff;">${Math.round(zone.activity * 100)}%</strong></p>
                </div>
            </div>
        `;
    },

    /**
     * Get color based on activity level
     */
    getActivityColor(activity) {
        if (activity >= 0.7) return this.config.colors.high;
        if (activity >= 0.4) return this.config.colors.medium;
        return this.config.colors.low;
    },

    /**
     * Handle zone click event
     */
    onZoneClick(zone) {
        this.selectedZone = zone;
        
        // Dispatch custom event
        const event = new CustomEvent('zoneSelected', { detail: zone });
        document.dispatchEvent(event);

        console.log('Zone selected:', zone);
    },

    /**
     * Focus on a specific zone
     */
    focusZone(zoneId) {
        const zone = this.zones.find(z => z.id === zoneId);
        if (zone && this.map) {
            this.map.setView([zone.lat, zone.lng], 14);
        }
    },

    /**
     * Update zone data
     */
    updateZone(zoneId, data) {
        const index = this.zones.findIndex(z => z.id === zoneId);
        if (index !== -1) {
            this.zones[index] = { ...this.zones[index], ...data };
            // Refresh marker
            if (this.markers[index]) {
                this.markers[index].remove();
                this.markers[index] = this.createZoneMarker(this.zones[index]);
            }
        }
    },

    /**
     * Clear all zones from map
     */
    clearZones() {
        this.markers.forEach(marker => marker.remove());
        this.markers = [];
        this.zones = [];
    },

    /**
     * Get map bounds
     */
    getBounds() {
        return this.map ? this.map.getBounds() : null;
    },

    /**
     * Destroy map instance
     */
    destroy() {
        if (this.map) {
            this.map.remove();
            this.map = null;
        }
        this.zones = [];
        this.markers = [];
    }
};

// Make ZoneMap available globally
window.ZoneMap = ZoneMap;
