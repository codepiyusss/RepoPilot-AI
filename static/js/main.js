
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeSmoothScroll();
});


function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Update active nav link based on current page
    navLinks.forEach(link => {
        if (link.getAttribute('href') === window.location.pathname) {
            link.style.color = 'var(--accent-primary)';
        }
    });
}

function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Validate GitHub repository URL
 * @param {string} url - The repository URL to validate
 * @returns {boolean} - if valid Display True, false otherwise
 */

function isValidGitHubUrl(url) {
    const githubUrlPattern = /^(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_.-]+\/?$/i;
    return githubUrlPattern.test(url);
}

/**
 * Parse repository URL to extract owner and repo
 * @param {string} url - The repository URL
 * @returns {object} - Object with owner and repo properties
 */
function parseRepoUrl(url) {
    try {
        
        let cleanUrl = url.trim();
        if (!cleanUrl.startsWith('http')) {
            cleanUrl = 'https://' + cleanUrl;
        }
        
        const urlObj = new URL(cleanUrl);
        const pathParts = urlObj.pathname.split('/').filter(part => part.length > 0);
        
        if (pathParts.length >= 2) {
            return {
                owner: pathParts[0],
                repo: pathParts[1].replace('.git', '')
            };
        }
    } catch (error) {
        console.error('Error parsing URL:', error);
    }
    
    return null;
}

function observeElements() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease-out';
        observer.observe(card);
    });
}


if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', observeElements);
} else {
    observeElements();
}

/**
 * Utility function to show notification messages
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, error, info)
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles dynamically if not already in CSS
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        background-color: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        z-index: 9999;
        animation: slideInDown 0.3s ease-out;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideInDown 0.3s ease-out reverse';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Handle form submissions
 */
function setupFormHandlers() {
    // This is a placeholder for future form handling
    // Will be expanded when backend API is ready
}

setupFormHandlers();

/**
 * Utility: Debounce function for optimized event handling
 * @param {function} func - The function to debounce
 * @param {number} wait - The wait time in milliseconds
 * @returns {function} - The debounced function
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
 * Utility: Throttle function for optimized event handling
 * @param {function} func - The function to throttle
 * @param {number} limit - The limit time in milliseconds
 * @returns {function} - The throttled function
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}


console.log('RepoPilot AI - GitHub Repository Analyzer');
console.log('Version: 1.0.0 (Foundation Release)');
console.log('Ready for development');
