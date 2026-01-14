/**
 * Main JavaScript file for User Registration and Login System
 * Contains common functions and utilities used across the application
 */

// Utility Functions
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const toggleBtn = document.querySelector('.mobile-menu-toggle i');
    
    if (navMenu.style.display === 'flex') {
        navMenu.style.display = 'none';
        toggleBtn.classList.remove('fa-times');
        toggleBtn.classList.add('fa-bars');
    } else {
        navMenu.style.display = 'flex';
        navMenu.style.position = 'absolute';
        navMenu.style.top = '100%';
        navMenu.style.left = '0';
        navMenu.style.right = '0';
        navMenu.style.backgroundColor = 'white';
        navMenu.style.flexDirection = 'column';
        navMenu.style.padding = '1rem';
        navMenu.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        
        toggleBtn.classList.remove('fa-bars');
        toggleBtn.classList.add('fa-times');
    }
}

function toggleDropdown() {
    const dropdown = document.getElementById('userDropdown');
    const toggle = document.querySelector('.dropdown-toggle i:last-child');
    
    if (dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
        toggle.style.transform = 'rotate(0deg)';
    } else {
        dropdown.style.display = 'block';
        toggle.style.transform = 'rotate(180deg)';
    }
}

function closeFlashMessage(button) {
    const flashMessage = button.closest('.flash-message');
    flashMessage.style.animation = 'slideOutRight 0.3s ease-out';
    setTimeout(() => {
        flashMessage.remove();
    }, 300);
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('userDropdown');
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    
    if (dropdown && dropdownToggle && 
        !dropdownToggle.contains(event.target) && 
        !dropdown.contains(event.target)) {
        dropdown.style.display = 'none';
        const toggle = dropdownToggle.querySelector('i:last-child');
        if (toggle) {
            toggle.style.transform = 'rotate(0deg)';
        }
    }
});

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((message, index) => {
        setTimeout(() => {
            if (message.parentElement) {
                message.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => {
                    if (message.parentElement) {
                        message.remove();
                    }
                }, 300);
            }
        }, 5000 + (index * 500)); // Stagger the removal
    });
});

// Form validation utilities
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

function validatePassword(password) {
    return password.length >= 8 && 
           /[A-Z]/.test(password) && 
           /[a-z]/.test(password) && 
           /\d/.test(password);
}

function validateUsername(username) {
    return username.length >= 3 && 
           username.length <= 20 && 
           /^[a-zA-Z0-9_]+$/.test(username);
}

// Loading state utilities
function showLoadingState(button, originalText) {
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
}

function hideLoadingState(button, originalText) {
    button.disabled = false;
    button.innerHTML = originalText;
}

// API utilities
async function makeRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, finalOptions);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Session management
function checkSessionValidity() {
    return makeRequest('/auth/check-session');
}

function updateLastActivity() {
    return makeRequest('/auth/update-activity', { method: 'POST' });
}

// Local storage utilities
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('Failed to save to localStorage:', error);
        return false;
    }
}

function getFromLocalStorage(key) {
    try {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : null;
    } catch (error) {
        console.error('Failed to get from localStorage:', error);
        return null;
    }
}

function removeFromLocalStorage(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (error) {
        console.error('Failed to remove from localStorage:', error);
        return false;
    }
}

// Theme management
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    saveToLocalStorage('theme', theme);
}

function getTheme() {
    return getFromLocalStorage('theme') || 'light';
}

function initTheme() {
    const theme = getTheme();
    setTheme(theme);
}

// Accessibility utilities
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// Keyboard navigation
function handleEscapeKey(callback) {
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            callback();
        }
    });
}

// Form utilities
function serializeForm(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

function resetForm(form) {
    form.reset();
    
    // Clear validation feedback
    const feedbackElements = form.querySelectorAll('.validation-feedback');
    feedbackElements.forEach(element => {
        element.textContent = '';
        element.className = 'validation-feedback';
    });
    
    // Clear password strength indicators
    const strengthBars = form.querySelectorAll('.password-strength');
    strengthBars.forEach(bar => {
        bar.className = 'password-strength';
    });
}

// Modal utilities
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // Focus first input in modal
        const firstInput = modal.querySelector('input, button, select, textarea');
        if (firstInput) {
            firstInput.focus();
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function setupModalClose(modalId) {
    // Close on X button click
    const closeBtn = document.querySelector(`#${modalId} .modal-close`);
    if (closeBtn) {
        closeBtn.addEventListener('click', () => closeModal(modalId));
    }
    
    // Close on outside click
    window.addEventListener('click', function(event) {
        const modal = document.getElementById(modalId);
        if (event.target === modal) {
            closeModal(modalId);
        }
    });
    
    // Close on Escape key
    handleEscapeKey(() => closeModal(modalId));
}

// Animation utilities
function animateElement(element, animationClass, duration = 300) {
    element.classList.add(animationClass);
    
    setTimeout(() => {
        element.classList.remove(animationClass);
    }, duration);
}

// Error handling
function handleApiError(error, defaultMessage = 'An error occurred') {
    console.error('API Error:', error);
    
    const message = error.message || defaultMessage;
    
    // Show error message to user
    const errorDiv = document.createElement('div');
    errorDiv.className = 'flash-message flash-error';
    errorDiv.innerHTML = `
        <div class="message-content">
            <i class="fas fa-exclamation-circle"></i>
            <span>${message}</span>
            <button class="message-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    const flashContainer = document.querySelector('.flash-messages') || 
                          document.querySelector('.main-content');
    
    if (flashContainer) {
        flashContainer.insertBefore(errorDiv, flashContainer.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentElement) {
                errorDiv.remove();
            }
        }, 5000);
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initTheme();
    
    // Setup mobile menu
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    if (mobileToggle) {
        mobileToggle.addEventListener('click', toggleMobileMenu);
    }
    
    // Setup dropdown
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    if (dropdownToggle) {
        dropdownToggle.addEventListener('click', toggleDropdown);
    }
    
    // Check session validity periodically
    if (document.body.classList.contains('authenticated')) {
        setInterval(checkSessionValidity, 60000); // Check every minute
        setInterval(updateLastActivity, 300000); // Update activity every 5 minutes
    }
});

// Export utilities for use in other files
window.AppUtils = {
    toggleMobileMenu,
    toggleDropdown,
    closeFlashMessage,
    validateEmail,
    validatePassword,
    validateUsername,
    showLoadingState,
    hideLoadingState,
    makeRequest,
    checkSessionValidity,
    updateLastActivity,
    saveToLocalStorage,
    getFromLocalStorage,
    removeFromLocalStorage,
    setTheme,
    getTheme,
    initTheme,
    announceToScreenReader,
    handleEscapeKey,
    serializeForm,
    resetForm,
    openModal,
    closeModal,
    setupModalClose,
    animateElement,
    handleApiError
};
