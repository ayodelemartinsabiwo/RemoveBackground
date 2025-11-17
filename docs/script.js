// ==================== //
// Global Variables for Form
// ==================== //

let userLocation = null;
let detectedCurrency = 'USD';

// Currency mapping based on country codes
const currencyMapping = {
    'US': 'USD', 'CA': 'CAD', 'GB': 'GBP', 'AU': 'AUD', 'NZ': 'AUD',
    'JP': 'JPY', 'CN': 'CNY', 'IN': 'INR', 'NG': 'NGN', 'ZA': 'ZAR',
    'KE': 'KES', 'GH': 'GHS', 'DE': 'EUR', 'FR': 'EUR', 'ES': 'EUR',
    'IT': 'EUR', 'NL': 'EUR', 'BE': 'EUR', 'AT': 'EUR', 'PT': 'EUR',
    'IE': 'EUR', 'FI': 'EUR', 'GR': 'EUR', 'PL': 'EUR', 'SE': 'EUR'
};

// Download URL
const DOWNLOAD_URL = 'https://github.com/ayodelemartinsabiwo/RemoveBackground/releases/download/v1.0.0/BackgroundRemover_Setup.exe';

// ==================== //
// Mobile Menu Toggle
// ==================== //

const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
    });
}

// ==================== //
// Form Modal Elements
// ==================== //

const modal = document.getElementById('formModal');
const downloadBtn = document.getElementById('downloadBtn');
const downloadBtnMain = document.getElementById('downloadBtnMain');
const closeBtn = document.querySelector('.close');
const userForm = document.getElementById('userForm');
const detectLocationBtn = document.getElementById('detectLocationBtn');
const willingToPayRadios = document.querySelectorAll('input[name="willingToPay"]');
const amountGroup = document.getElementById('amountGroup');
const amountInput = document.getElementById('amount');
const amountRange = document.getElementById('amountRange');
const rangeValue = document.getElementById('rangeValue');
const currencySelect = document.getElementById('currency');
const successMessage = document.getElementById('successMessage');

// ==================== //
// Initialize on Load
// ==================== //

document.addEventListener('DOMContentLoaded', () => {
    console.log('Palmar Tech Background Remover Website Loaded');

    initializeFormEventListeners();
    tryAutoDetectLocation();

    // Add visual feedback for tip cards
    const tipCardsLoad = document.querySelectorAll('.tip-card');
    tipCardsLoad.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Example: Log page views (you can integrate analytics here)
    if (typeof gtag !== 'undefined') {
        gtag('event', 'page_view', {
            page_title: document.title,
            page_location: window.location.href,
            page_path: window.location.pathname
        });
    }
});

// ==================== //
// Form Event Listeners
// ==================== //

function initializeFormEventListeners() {
    // Download buttons open modal
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            modal.style.display = 'block';
        });
    }

    if (downloadBtnMain) {
        downloadBtnMain.addEventListener('click', () => {
            modal.style.display = 'block';
        });
    }

    // Close button closes modal
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    // Click outside modal to close
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Detect location button
    if (detectLocationBtn) {
        detectLocationBtn.addEventListener('click', detectLocation);
    }

    // Willing to pay radio buttons
    willingToPayRadios.forEach(radio => {
        radio.addEventListener('change', handleWillingToPayChange);
    });

    // Amount range slider
    if (amountRange) {
        amountRange.addEventListener('input', (e) => {
            const value = e.target.value;
            rangeValue.textContent = value;
            amountInput.value = value;
        });
    }

    // Amount input field
    if (amountInput) {
        amountInput.addEventListener('input', (e) => {
            const value = Math.min(Math.max(e.target.value, 0), 100);
            amountRange.value = value;
            rangeValue.textContent = value;
        });
    }

    // Form submission
    if (userForm) {
        userForm.addEventListener('submit', handleFormSubmit);
    }
}

// ==================== //
// Location Detection
// ==================== //

function tryAutoDetectLocation() {
    fetch('https://ipapi.co/json/')
        .then(response => response.json())
        .then(data => {
            if (data.country_code) {
                const location = `${data.city || data.region || ''}, ${data.country_name || data.country_code}`;
                const locationInput = document.getElementById('location');
                if (locationInput) {
                    locationInput.value = location.trim();
                }
                userLocation = data;

                const currency = currencyMapping[data.country_code] || 'USD';
                detectedCurrency = currency;
                if (currencySelect) {
                    currencySelect.value = currency;
                }
            }
        })
        .catch(error => {
            console.log('Auto-detection failed, user can manually detect or enter location');
        });
}

function detectLocation() {
    detectLocationBtn.disabled = true;
    detectLocationBtn.textContent = '📍 Detecting...';

    fetch('https://ipapi.co/json/')
        .then(response => response.json())
        .then(data => {
            if (data.country_code) {
                const location = `${data.city || data.region || ''}, ${data.country_name || data.country_code}`;
                document.getElementById('location').value = location.trim();
                userLocation = data;

                const currency = currencyMapping[data.country_code] || 'USD';
                detectedCurrency = currency;
                currencySelect.value = currency;

                detectLocationBtn.textContent = '✓ Location Detected';
                setTimeout(() => {
                    detectLocationBtn.textContent = '📍 Auto-detect';
                    detectLocationBtn.disabled = false;
                }, 2000);
            }
        })
        .catch(error => {
            fetch('https://api.ipify.org?format=json')
                .then(response => response.json())
                .then(ipData => {
                    alert('Unable to auto-detect location. Please enter manually.');
                    detectLocationBtn.textContent = '📍 Auto-detect';
                    detectLocationBtn.disabled = false;
                })
                .catch(() => {
                    alert('Location detection failed. Please enter your location manually.');
                    detectLocationBtn.textContent = '📍 Auto-detect';
                    detectLocationBtn.disabled = false;
                });
        });
}

function handleWillingToPayChange(e) {
    const value = e.target.value;
    if (value === 'Yes' || value === 'Maybe') {
        amountGroup.style.display = 'block';
        amountInput.required = true;
    } else {
        amountGroup.style.display = 'none';
        amountInput.required = false;
        amountInput.value = '';
        amountRange.value = 0;
        rangeValue.textContent = '0';
    }
}

// ==================== //
// Form Submission
// ==================== //

async function handleFormSubmit(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        ageRange: document.getElementById('ageRange').value,
        location: document.getElementById('location').value,
        profession: document.getElementById('profession').value,
        willingToPay: document.querySelector('input[name="willingToPay"]:checked').value,
        currency: currencySelect.value,
        amount: amountInput.value || '0',
        timestamp: new Date().toISOString(),
        detectedCountry: userLocation ? userLocation.country_name : 'Not detected',
        detectedCountryCode: userLocation ? userLocation.country_code : 'N/A'
    };

    try {
        // Send data to backend (if server is running)
        const response = await fetch('/api/submit-form', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            console.log('Form data saved successfully');
        }
    } catch (error) {
        console.log('Backend not available, storing locally');
        storeDataLocally(formData);
    }

    // Close modal
    modal.style.display = 'none';

    // Show success message
    successMessage.style.display = 'block';

    // Reset form
    userForm.reset();
    amountGroup.style.display = 'none';

    // Hide success message after 3 seconds and start download
    setTimeout(() => {
        successMessage.style.display = 'none';
        initiateDownload();
    }, 3000);
}

function storeDataLocally(data) {
    const existingData = JSON.parse(localStorage.getItem('formSubmissions') || '[]');
    existingData.push(data);
    localStorage.setItem('formSubmissions', JSON.stringify(existingData));
    console.log('Form data stored locally:', data);
}

function initiateDownload() {
    // Create a temporary link to trigger download
    const link = document.createElement('a');
    link.href = DOWNLOAD_URL;
    link.download = 'BackgroundRemover_Setup.exe';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ==================== //
// Flip Card Functionality for Pro Tips
// ==================== //

const tipCards = document.querySelectorAll('.tip-card');

tipCards.forEach(card => {
    card.addEventListener('click', () => {
        card.classList.toggle('flipped');
    });
});

// ==================== //
// FAQ Accordion
// ==================== //

const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');

    question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');

        faqItems.forEach(otherItem => {
            if (otherItem !== item) {
                otherItem.classList.remove('active');
            }
        });

        if (isActive) {
            item.classList.remove('active');
        } else {
            item.classList.add('active');
        }
    });
});

// ==================== //
// Smooth Scroll
// ==================== //

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');

        if (href === '#') {
            return;
        }

        e.preventDefault();

        const target = document.querySelector(href);
        if (target) {
            const navbar = document.querySelector('.navbar');
            const navHeight = navbar ? navbar.offsetHeight : 0;
            const targetPosition = target.offsetTop - navHeight - 20;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });

            if (navLinks && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                if (mobileMenuToggle) {
                    mobileMenuToggle.classList.remove('active');
                }
            }
        }
    });
});

// ==================== //
// Navbar Background on Scroll
// ==================== //

let lastScroll = 0;
const navbar = document.querySelector('.navbar');

if (navbar) {
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
        } else {
            navbar.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)';
        }

        lastScroll = currentScroll;
    });
}

// ==================== //
// Scroll Animations
// ==================== //

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .step, .doc-card, .unique-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ==================== //
// Hero Demo Cards - Enhanced Hover Effect
// ==================== //

const demoCards = document.querySelectorAll('.demo-card-enhanced');

demoCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transition = 'all 0.3s ease';
    });
});

// ==================== //
// Unique Card Animations
// ==================== //

const uniqueCards = document.querySelectorAll('.unique-card');
uniqueCards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.15}s`;
});

// ==================== //
// Easter Egg
// ==================== //

let clickCount = 0;
const logoIcon = document.querySelector('.logo-icon');

if (logoIcon) {
    logoIcon.addEventListener('click', () => {
        clickCount++;
        if (clickCount === 5) {
            alert('🎨 Made with precision by Palmar Tech! Thanks for exploring!');
            clickCount = 0;
        }
    });
}

// ==================== //
// Keyboard Navigation
// ==================== //

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close modal
        if (modal && modal.style.display === 'block') {
            modal.style.display = 'none';
        }

        // Close FAQ items
        faqItems.forEach(item => {
            item.classList.remove('active');
        });

        // Unflip all tip cards
        tipCards.forEach(card => {
            card.classList.remove('flipped');
        });
    }
});

// ==================== //
// Print Styles Handler
// ==================== //

window.addEventListener('beforeprint', () => {
    faqItems.forEach(item => {
        item.classList.add('active');
    });
});

window.addEventListener('afterprint', () => {
    faqItems.forEach(item => {
        item.classList.remove('active');
    });
});

// ==================== //
// Mobile Detection
// ==================== //

const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

if (isMobile) {
    document.body.classList.add('mobile-device');

    tipCards.forEach(card => {
        card.addEventListener('touchstart', (e) => {
            e.preventDefault();
            card.classList.toggle('flipped');
        });
    });
}

// ==================== //
// Performance Monitoring
// ==================== //

window.addEventListener('load', () => {
    const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
    console.log(`Page loaded in ${loadTime}ms`);
});

// ==================== //
// Export form data as CSV (for admin/testing purposes)
// ==================== //

function exportFormDataAsCSV() {
    const data = JSON.parse(localStorage.getItem('formSubmissions') || '[]');
    if (data.length === 0) {
        alert('No data to export');
        return;
    }

    const headers = ['Timestamp', 'Name', 'Email', 'Age Range', 'Location', 'Profession', 'Willing to Pay', 'Amount', 'Currency', 'Detected Country'];
    const csvRows = [headers.join(',')];

    data.forEach(row => {
        const values = [
            row.timestamp,
            row.name,
            row.email,
            row.ageRange,
            row.location,
            row.profession,
            row.willingToPay,
            row.amount,
            row.currency,
            row.detectedCountry
        ];
        csvRows.push(values.map(v => `"${v}"`).join(','));
    });

    const csvContent = csvRows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'form_submissions.csv';
    link.click();
    window.URL.revokeObjectURL(url);
}

// Add console command for admins to export data
console.log('%c Admin Commands', 'color: #ff6b35; font-size: 16px; font-weight: bold;');
console.log('To export form data as CSV, run: exportFormDataAsCSV()');
