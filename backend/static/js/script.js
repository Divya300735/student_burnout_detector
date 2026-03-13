// Academic Burnout Detection System - Client-side JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('Academic Burnout Detection System loaded');
    
    // Initialize tooltips or other UI enhancements if needed
    initializeUI();
});

/**
 * Initialize UI components
 */
function initializeUI() {
    // Add any UI initialization code here
    console.log('UI initialized');
}

/**
 * Format a number to a fixed decimal place
 */
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

/**
 * Get risk category label with styling
 */
function getRiskCategoryLabel(score) {
    if (score < 4) {
        return {
            category: 'Low Risk',
            color: '#90EE90',
            textColor: '#000'
        };
    } else if (score < 7) {
        return {
            category: 'Moderate Risk',
            color: '#FFD700',
            textColor: '#000'
        };
    } else {
        return {
            category: 'High Risk',
            color: '#FF6B6B',
            textColor: '#fff'
        };
    }
}

/**
 * Fetch and display data from API
 */
async function fetchData(endpoint) {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

/**
 * Display error message to user
 */
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <div style="background-color: #f8d7da; color: #721c24; padding: 12px; border-radius: 5px; margin: 10px 0; border: 1px solid #f5c6cb;">
            <strong>Error:</strong> ${message}
        </div>
    `;
    return errorDiv;
}

/**
 * Display success message to user
 */
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <div style="background-color: #d4edda; color: #155724; padding: 12px; border-radius: 5px; margin: 10px 0; border: 1px solid #c3e6cb;">
            <strong>Success:</strong> ${message}
        </div>
    `;
    return successDiv;
}

/**
 * Validate form inputs
 */
function validateInputs(data) {
    const validations = {
        'sleep_hours': { min: 0, max: 12, name: 'Sleep Hours' },
        'study_hours': { min: 0, max: 12, name: 'Study Hours' },
        'screen_time': { min: 0, max: 14, name: 'Screen Time' },
        'stress_level': { min: 0, max: 10, name: 'Stress Level' },
        'physical_activity': { min: 0, max: 10, name: 'Physical Activity' },
        'assignment_load': { min: 0, max: 10, name: 'Assignment Load' }
    };

    for (const [key, rules] of Object.entries(validations)) {
        const value = data[key];
        if (isNaN(value) || value < rules.min || value > rules.max) {
            return {
                valid: false,
                message: `${rules.name} must be between ${rules.min} and ${rules.max}`
            };
        }
    }

    return { valid: true };
}

/**
 * Calculate burnout score with custom formula
 */
function calculateBurnoutScoreLocal(data) {
    // This mirrors the backend calculation
    let burnout = (
        0.35 * data.stress_level +
        0.25 * data.screen_time +
        0.20 * data.study_hours -
        0.30 * data.sleep_hours -
        0.05 * data.physical_activity +
        0.05 * data.assignment_load
    );

    // Normalize to 0-10 scale
    const min_raw = -4;
    const max_raw = 8;

    if (max_raw > min_raw) {
        burnout = 10 * (burnout - min_raw) / (max_raw - min_raw);
    } else {
        burnout = 5;
    }

    // Clamp to 0-10
    return Math.max(0, Math.min(10, burnout));
}

/**
 * Smooth scroll to element
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Format time display
 */
function formatTime(hours) {
    if (hours < 1) {
        return `${Math.round(hours * 60)} minutes`;
    }
    return `${hours} hour${hours !== 1 ? 's' : ''}`;
}

/**
 * Create a chart container dynamically
 */
function createChartContainer(title, imagePath) {
    const container = document.createElement('div');
    container.className = 'graph-card';
    container.innerHTML = `
        <img src="${imagePath}" alt="${title}">
        <p>${title}</p>
    `;
    return container;
}

/**
 * Initialize chart animation on scroll
 */
function observeCharts() {
    const charts = document.querySelectorAll('.graph-card img');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.parentElement.style.animation = 'fadeIn 0.5s ease-in';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    charts.forEach(chart => observer.observe(chart));
}

/**
 * Generate statistical summary
 */
function generateStatisticsSummary(stats) {
    const summary = [];
    
    for (const [variable, values] of Object.entries(stats)) {
        summary.push({
            variable: variable.replace(/_/g, ' ').toUpperCase(),
            mean: parseFloat(values.mean).toFixed(2),
            median: parseFloat(values.median).toFixed(2),
            std_dev: parseFloat(values.std_dev).toFixed(2)
        });
    }

    return summary;
}

/**
 * Export data as CSV
 */
function exportAsCSV(data, filename = 'data.csv') {
    let csv = [];
    
    // Add headers
    if (Array.isArray(data) && data.length > 0) {
        csv.push(Object.keys(data[0]).join(','));
        
        // Add rows
        data.forEach(row => {
            csv.push(Object.values(row).join(','));
        });
    }

    // Create and download
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

/**
 * Parse query parameters from URL
 */
function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    const result = {};
    for (const [key, value] of params) {
        result[key] = value;
    }
    return result;
}

/**
 * Debounce function for form inputs
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Add CSS animation for fade in effect
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

console.log('Script initialized successfully');
