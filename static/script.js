// Global variables
let energyBitrateChart = null;
let bitratePieChart = null;
let currentAnalysisData = null;

// DOM Elements
const audioFileSelect = document.getElementById('audioFile');
const bandwidthSlider = document.getElementById('bandwidthSlider');
const bandwidthValue = document.getElementById('bandwidthValue');
const frameWiseToggle = document.getElementById('frameWiseToggle');
const frameOptions = document.querySelector('.frame-options');
const analyzeBtn = document.getElementById('analyzeBtn');
const encodeBtn = document.getElementById('encodeBtn');
const statusBar = document.getElementById('statusBar');
const loadingSpinner = document.getElementById('loadingSpinner');
const scenariosContainer = document.getElementById('scenariosContainer');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadScenarios();
    setupEventListeners();
});

function setupEventListeners() {
    bandwidthSlider.addEventListener('input', updateBandwidthDisplay);
    frameWiseToggle.addEventListener('change', toggleFrameOptions);
    analyzeBtn.addEventListener('click', analyzeAudio);
    encodeBtn.addEventListener('click', encodeAudio);
}

function updateBandwidthDisplay() {
    bandwidthValue.textContent = bandwidthSlider.value;
}

function toggleFrameOptions() {
    frameOptions.style.display = frameWiseToggle.checked ? 'block' : 'none';
}

function updateStatus(message) {
    statusBar.textContent = message;
}

function showLoading(show) {
    loadingSpinner.style.display = show ? 'flex' : 'none';
}

// Load scenarios from API
async function loadScenarios() {
    try {
        const response = await fetch('/api/scenarios');
        const scenarios = await response.json();
        
        scenariosContainer.innerHTML = '';
        scenarios.forEach(scenario => {
            const btn = document.createElement('button');
            btn.className = 'scenario-btn';
            btn.innerHTML = `<strong>${scenario.name}</strong><small>${scenario.bandwidth} Mbps</small><p style="font-size: 0.8em; margin-top: 3px;">${scenario.description}</p>`;
            btn.addEventListener('click', () => {
                bandwidthSlider.value = scenario.bandwidth;
                updateBandwidthDisplay();
            });
            scenariosContainer.appendChild(btn);
        });
    } catch (error) {
        console.error('Error loading scenarios:', error);
        updateStatus('Error loading scenarios');
    }
}

// Analyze audio
async function analyzeAudio() {
    const filename = audioFileSelect.value;
    if (!filename) {
        alert('Please select an audio file');
        return;
    }

    showLoading(true);
    updateStatus('Analyzing audio...');

    try {
        const bandwidth = parseFloat(bandwidthSlider.value);
        const useFramewise = frameWiseToggle.checked;

        let endpoint = '/api/analyze';
        let payload = {
            filename: filename,
            bandwidth: bandwidth
        };

        if (useFramewise) {
            endpoint = '/api/framewise-adaptive';
            payload.frame_size = parseInt(document.getElementById('frameSize').value);
            payload.hop_size = parseInt(document.getElementById('hopSize').value);
        }

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        currentAnalysisData = data;
        displayAnalysisResults(data, useFramewise);
        updateStatus(`✓ Analysis complete for ${filename}`);

    } catch (error) {
        console.error('Error:', error);
        alert('Error analyzing audio: ' + error.message);
        updateStatus('Error analyzing audio');
    } finally {
        showLoading(false);
    }
}

// Display analysis results
function displayAnalysisResults(data, isFramewise) {
    // Update statistics
    const statsContainer = document.getElementById('statsContainer');
    
    if (isFramewise) {
        statsContainer.innerHTML = `
            <div class="stat-item">
                <span class="stat-label">Filename</span>
                <span class="stat-value">${data.filename}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Total Frames</span>
                <span class="stat-value">${data.total_frames}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Average Bitrate</span>
                <span class="stat-value">${data.average_bitrate.toFixed(2)} kbps</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Bitrate Range</span>
                <span class="stat-value">${data.bitrate_stats.min.toFixed(1)}-${data.bitrate_stats.max.toFixed(1)} kbps</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Bandwidth Level</span>
                <span class="stat-value">${data.bandwidth_level}</span>
            </div>
        `;

        // Update charts for frame-wise data
        updateEnergyBitrateChart(data);
        updateBitratePieChart(data);
    } else {
        const stats = data.energy_stats;
        statsContainer.innerHTML = `
            <div class="stat-item">
                <span class="stat-label">Filename</span>
                <span class="stat-value">${data.filename}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Energy Level</span>
                <span class="stat-value">${data.energy_level}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Mean Energy</span>
                <span class="stat-value">${stats.mean.toFixed(6)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Max Energy</span>
                <span class="stat-value">${stats.max.toFixed(6)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Selected Bitrate</span>
                <span class="stat-value">${data.selected_bitrate} kbps</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Bandwidth Level</span>
                <span class="stat-value">${data.bandwidth_level}</span>
            </div>
        `;

        // Update charts
        updateEnergyBitrateChart(data);
        updateBitratePieChart(data);
    }
}

// Update energy-bitrate chart
function updateEnergyBitrateChart(data) {
    const ctx = document.getElementById('energyBitrateChart').getContext('2d');
    
    const energies = data.frame_energies || [];
    const bitrates = data.framewise_bitrates || [];
    const labels = Array.from({length: energies.length}, (_, i) => i);

    if (energyBitrateChart) {
        energyBitrateChart.destroy();
    }

    energyBitrateChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Frame Energy',
                    data: energies,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    yAxisID: 'y',
                    tension: 0.3
                },
                {
                    label: 'Adaptive Bitrate (kbps)',
                    data: bitrates,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    yAxisID: 'y1',
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Energy'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Bitrate (kbps)'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            }
        }
    });
}

// Update bitrate pie chart
function updateBitratePieChart(data) {
    const ctx = document.getElementById('bitratePieChart').getContext('2d');
    
    let energyLevels = data.framewise_energy_levels || [];
    
    // Count energy levels
    const counts = {
        'high_energy': energyLevels.filter(e => e === 'high_energy').length,
        'medium_energy': energyLevels.filter(e => e === 'medium_energy').length,
        'low_energy': energyLevels.filter(e => e === 'low_energy').length
    };

    if (bitratePieChart) {
        bitratePieChart.destroy();
    }

    bitratePieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['High Energy', 'Medium Energy', 'Low Energy'],
            datasets: [{
                data: [counts['high_energy'], counts['medium_energy'], counts['low_energy']],
                backgroundColor: [
                    '#ef4444',
                    '#f59e0b',
                    '#3b82f6'
                ],
                borderColor: '#1e293b',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Encode audio
async function encodeAudio() {
    const filename = audioFileSelect.value;
    if (!filename) {
        alert('Please select an audio file');
        return;
    }

    showLoading(true);
    updateStatus('Encoding audio...');

    try {
        const bandwidth = parseFloat(bandwidthSlider.value);
        const useFramewise = frameWiseToggle.checked;

        const response = await fetch('/api/encode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                filename: filename,
                bandwidth: bandwidth,
                use_framewise: useFramewise
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayEncodingResults(data);
        updateStatus('✓ Encoding complete');

    } catch (error) {
        console.error('Error:', error);
        alert('Error encoding audio: ' + error.message);
        updateStatus('Error encoding audio');
    } finally {
        showLoading(false);
    }
}

// Display encoding results
function displayEncodingResults(data) {
    const resultsSection = document.querySelector('.results-section');
    const resultsContainer = document.getElementById('resultsContainer');
    const metrics = data.metrics;

    resultsContainer.innerHTML = `
        <div class="result-item">
            <span class="result-label">Output File</span>
            <span class="result-value">${data.output_filename}</span>
        </div>
        <div class="result-item">
            <span class="result-label">Bandwidth</span>
            <span class="result-value">${data.bandwidth_mbps} Mbps</span>
        </div>
        <div class="result-item">
            <span class="result-label">Selected Bitrate</span>
            <span class="result-value">${data.selected_bitrate} kbps</span>
        </div>
        <div class="result-item">
            <span class="result-label">Energy Level</span>
            <span class="result-value">${data.energy_level}</span>
        </div>
    `;

    // Display metrics
    const metricsContainer = document.getElementById('metricsContainer');
    metricsContainer.innerHTML = `
        <div class="metric-item">
            <div class="metric-label">SNR (dB)</div>
            <div class="metric-value">${metrics.snr_db.toFixed(2)}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">MSE</div>
            <div class="metric-value">${metrics.mse.toExponential(2)}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Compression Ratio</div>
            <div class="metric-value">${metrics.compression_ratio.toFixed(2)}x</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Duration (s)</div>
            <div class="metric-value">${metrics.duration.toFixed(2)}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Original Size</div>
            <div class="metric-value">${(metrics.original_bits / 1048576).toFixed(2)} MB</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Compressed Size</div>
            <div class="metric-value">${(metrics.compressed_bits / 1048576).toFixed(2)} MB</div>
        </div>
    `;

    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
