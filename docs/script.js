// ==================== //
// Global Variables for Form
// ==================== //

let userLocation = null;
let detectedCurrency = 'USD';
let currentPhase = 1;
let navigatedBack = false; // Track if user navigated back
let autoAdvanceEnabled = true; // Control auto-advance behavior
let phase1CompleteTimer = null; // Debounce timer for phase 1
let phase2CompleteTimer = null; // Debounce timer for phase 2
let userInteractedWithDropdown = false; // Track if user is actively using dropdown

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

// Google Apps Script URL for form submissions
// IMPORTANT: Replace this with your actual deployment URL after setting up Google Apps Script
// See GOOGLE_SHEETS_SETUP.md for detailed instructions
const GOOGLE_APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyn056eNTDU5ONCP5xZK_Rt4lMfsMP4Hpor4YCHcj2Iv9nqkULjh_D6MUlCjbhvm0irvA/exec';

// Form phase titles and descriptions
const phaseContent = {
    1: {
        title: "Help us improve!",
        description: "Share a few details to help us serve you better"
    },
    2: {
        title: "Tell Us About Yourself",
        description: "We'd love to know what you do"
    },
    3: {
        title: "Almost Done!",
        description: "Help us understand your needs"
    }
};

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
const finalSubmitBtn = document.getElementById('finalSubmitBtn');

// ==================== //
// Initialize on Load
// ==================== //

document.addEventListener('DOMContentLoaded', () => {
    console.log('Palmar Tech Background Remover Website Loaded');

    initializeFormEventListeners();

    // Try to detect location immediately on page load
    setTimeout(() => {
        tryAutoDetectLocation();
    }, 100); // Small delay to ensure DOM is fully ready

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
    // Download button in download section opens modal
    if (downloadBtnMain) {
        downloadBtnMain.addEventListener('click', () => {
            modal.style.display = 'block';
            resetForm();
            // Ensure location is detected when modal opens (retry if not already detected)
            setTimeout(() => {
                if (!userLocation || !document.getElementById('location')?.value) {
                    console.log('Location not yet detected, retrying...');
                    tryAutoDetectLocation();
                }
            }, 100);
        });
    }

    // Close button closes modal
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
            resetForm();
        });
    }

    // Click outside modal to close
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
            resetForm();
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
            checkPhase3Complete();
        });
    }

    // Amount input field
    if (amountInput) {
        amountInput.addEventListener('input', (e) => {
            const value = Math.min(Math.max(e.target.value, 0), 100);
            amountRange.value = value;
            rangeValue.textContent = value;
            checkPhase3Complete();
        });
    }

    // Form submission
    if (userForm) {
        userForm.addEventListener('submit', handleFormSubmit);
    }

    // Back navigation
    const backLinks = document.querySelectorAll('.back-link');
    backLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetPhase = parseInt(link.getAttribute('data-back-to'));
            goToPhase(targetPhase, true); // Pass true for back navigation
        });
    });

    // Phase 1 field listeners
    document.getElementById('name')?.addEventListener('input', checkPhase1Complete);
    document.getElementById('email')?.addEventListener('input', checkPhase1Complete);

    // Age dropdown - handle keyboard navigation and mouse selection
    const ageDropdown = document.getElementById('ageRange');
    if (ageDropdown) {
        // Track when user opens the dropdown
        ageDropdown.addEventListener('focus', () => {
            userInteractedWithDropdown = true;
        });

        // When user makes a selection, auto-advance immediately
        ageDropdown.addEventListener('change', () => {
            userInteractedWithDropdown = false; // User has made selection
            // Small delay to allow for smooth transition
            setTimeout(() => {
                checkPhase1Complete();
            }, 400);
        });

        // Track when user is done with dropdown (backup for blur without change)
        ageDropdown.addEventListener('blur', () => {
            setTimeout(() => {
                userInteractedWithDropdown = false;
                checkPhase1Complete();
            }, 300);
        });
    }

    // Phase 2 field listeners
    document.getElementById('profession')?.addEventListener('input', checkPhase2Complete);
    document.getElementById('location')?.addEventListener('input', checkPhase2Complete);

    // Next button listeners
    document.getElementById('nextBtn1')?.addEventListener('click', (e) => {
        e.preventDefault();
        // Keep manual navigation mode active
        goToPhase(2, false, true); // Pass true as third parameter for manual navigation
    });

    document.getElementById('nextBtn2')?.addEventListener('click', (e) => {
        e.preventDefault();
        // Keep manual navigation mode active
        goToPhase(3, false, true); // Pass true as third parameter for manual navigation
    });
}

// ==================== //
// Multi-Phase Logic
// ==================== //

function goToPhase(phaseNumber, isBackNavigation = false, isManualNext = false) {
    // Hide all phases
    document.querySelectorAll('.form-phase').forEach(phase => {
        phase.classList.remove('active');
    });

    // Show target phase
    const targetPhase = document.querySelector(`[data-phase="${phaseNumber}"]`);
    if (targetPhase) {
        targetPhase.classList.add('active');
    }

    // Update progress indicator
    document.querySelectorAll('.progress-step').forEach(step => {
        const stepNum = parseInt(step.getAttribute('data-step'));
        step.classList.remove('active', 'completed');

        if (stepNum === phaseNumber) {
            step.classList.add('active');
        } else if (stepNum < phaseNumber) {
            step.classList.add('completed');
        }
    });

    // Update title and description
    const formTitle = document.getElementById('formTitle');
    const formDescription = document.getElementById('formDescription');

    if (formTitle && formDescription && phaseContent[phaseNumber]) {
        formTitle.textContent = phaseContent[phaseNumber].title;
        formDescription.textContent = phaseContent[phaseNumber].description;
    }

    currentPhase = phaseNumber;

    // Handle back navigation - disable auto-advance and show next buttons
    if (isBackNavigation) {
        navigatedBack = true;
        autoAdvanceEnabled = false;
        showNextButtonForPhase(phaseNumber);
    } else if (isManualNext) {
        // User clicked next button - stay in manual mode and show next button for current phase
        navigatedBack = true;
        autoAdvanceEnabled = false;
        // Show next button for the current phase if it's not phase 3
        if (phaseNumber < 3) {
            showNextButtonForPhase(phaseNumber);
        }
    } else {
        // Normal auto-advance - hide all next buttons
        document.querySelectorAll('.next-link').forEach(btn => {
            btn.style.display = 'none';
        });
    }
}

function showNextButtonForPhase(phaseNumber) {
    const nextBtn = document.getElementById(`nextBtn${phaseNumber}`);
    if (nextBtn) {
        nextBtn.style.display = 'inline-block';
    }
}

function checkPhase1Complete() {
    const name = document.getElementById('name')?.value.trim();
    const email = document.getElementById('email')?.value.trim();
    const ageRange = document.getElementById('ageRange')?.value;

    const isValid = name && email && ageRange &&
                   document.getElementById('email')?.checkValidity();

    // Clear any existing timer
    if (phase1CompleteTimer) {
        clearTimeout(phase1CompleteTimer);
    }

    // Only auto-advance if enabled and user hasn't navigated back
    if (isValid && autoAdvanceEnabled && !navigatedBack && !userInteractedWithDropdown) {
        // Add longer delay to allow user to finish interacting with dropdown
        phase1CompleteTimer = setTimeout(() => {
            goToPhase(2);
        }, 1000); // Increased from 500ms to 1000ms
    }

    // Show next button if user navigated back and form is complete
    if (isValid && navigatedBack) {
        showNextButtonForPhase(1);
    }
}

function checkPhase2Complete() {
    const profession = document.getElementById('profession')?.value.trim();
    const location = document.getElementById('location')?.value.trim();

    const isValid = profession && location;

    // Clear any existing timer
    if (phase2CompleteTimer) {
        clearTimeout(phase2CompleteTimer);
    }

    // Only auto-advance if enabled and user hasn't navigated back
    if (isValid && autoAdvanceEnabled && !navigatedBack) {
        // Add delay to allow user to finish typing and review
        phase2CompleteTimer = setTimeout(() => {
            goToPhase(3);
        }, 2500); // Longer delay to let user see what they typed
    }

    // Show next button if user navigated back and form is complete
    if (isValid && navigatedBack) {
        showNextButtonForPhase(2);
    }
}

function checkPhase3Complete() {
    const willingToPay = document.querySelector('input[name="willingToPay"]:checked');

    if (!willingToPay) {
        finalSubmitBtn.disabled = true;
        return;
    }

    // If Yes or Maybe is selected, check if amount is filled
    if (willingToPay.value === 'Yes' || willingToPay.value === 'Maybe') {
        const amount = amountInput?.value;
        finalSubmitBtn.disabled = !amount || parseFloat(amount) <= 0;
    } else {
        // If No is selected, enable submit button
        finalSubmitBtn.disabled = false;
    }
}

function resetForm() {
    currentPhase = 1;
    navigatedBack = false;
    autoAdvanceEnabled = true;
    userInteractedWithDropdown = false;

    // Clear any pending timers
    if (phase1CompleteTimer) clearTimeout(phase1CompleteTimer);
    if (phase2CompleteTimer) clearTimeout(phase2CompleteTimer);

    goToPhase(1);
    userForm?.reset();
    amountGroup.style.display = 'none';
    finalSubmitBtn.disabled = true;
    // Hide all next buttons
    document.querySelectorAll('.next-link').forEach(btn => {
        btn.style.display = 'none';
    });
}

// ==================== //
// Location Detection
// ==================== //

function tryAutoDetectLocation() {
    console.log('Attempting to auto-detect location...');

    fetch('https://ipapi.co/json/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Location API response:', data);

            if (data.error) {
                console.warn('Location API error:', data.error, data.reason);
                return;
            }

            if (data.country_code) {
                const location = `${data.city || data.region || ''}, ${data.country_name || data.country_code}`;
                const locationInput = document.getElementById('location');
                if (locationInput) {
                    locationInput.value = location.trim();
                    console.log('Location set to:', location.trim());
                } else {
                    console.warn('Location input field not found');
                }

                userLocation = data;

                const currency = currencyMapping[data.country_code] || 'USD';
                detectedCurrency = currency;
                const currencySelect = document.getElementById('currency');
                if (currencySelect) {
                    currencySelect.value = currency;
                    console.log('Currency set to:', currency);
                } else {
                    console.warn('Currency select field not found');
                }
            } else {
                console.warn('No country_code in API response');
            }
        })
        .catch(error => {
            console.error('Auto-detection failed:', error);
            console.log('User can manually detect or enter location');
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
    checkPhase3Complete();
}

// ==================== //
// Form Submission
// ==================== //

function handleFormSubmit(e) {
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

    // Send data to Google Sheets via Apps Script (non-blocking)
    // Check if Google Apps Script URL is configured
    if (GOOGLE_APPS_SCRIPT_URL && GOOGLE_APPS_SCRIPT_URL !== 'YOUR_DEPLOYMENT_URL_HERE') {
        console.log('Sending form data to Google Sheets...');

        // Fire and forget - don't wait for response
        fetch(GOOGLE_APPS_SCRIPT_URL, {
            method: 'POST',
            mode: 'no-cors', // Important for Apps Script
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        }).then(() => {
            console.log('Form data sent to Google Sheets successfully');
        }).catch(error => {
            console.error('Error sending to Google Sheets:', error);
            console.log('Storing data locally as fallback...');
            storeDataLocally(formData);
        });
    } else {
        console.warn('Google Apps Script URL not configured. See GOOGLE_SHEETS_SETUP.md for setup instructions.');
        console.log('Storing data locally as fallback...');
        storeDataLocally(formData);
    }

    // Close modal
    modal.style.display = 'none';

    // Extract first name from full name
    const fullName = formData.name;
    const firstName = fullName.split(' ')[0];

    // Update success message with user's first name
    const successMessageElement = document.getElementById('successMessage');
    const successTitle = successMessageElement.querySelector('h3');
    if (successTitle) {
        successTitle.textContent = `Thank You, ${firstName}!`;
    }

    // Show success message
    successMessage.style.display = 'block';

    // Reset form
    resetForm();

    // Hide success message after 5 seconds and start download
    setTimeout(() => {
        successMessage.style.display = 'none';
        initiateDownload();
    }, 5000);
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

    // Log for debugging
    console.log('Download initiated:', DOWNLOAD_URL);
}

// ==================== //
// Flip Card Functionality for Pro Tips
// ==================== //

const tipCards = document.querySelectorAll('.tip-card');

// Desktop: use click
tipCards.forEach(card => {
    // Track if this is a desktop device (will be overridden for mobile below)
    if (!(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))) {
        card.addEventListener('click', () => {
            card.classList.toggle('flipped');
        });
    }
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
            resetForm();
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
// Mobile Detection & Improved Touch Handling
// ==================== //

const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

if (isMobile) {
    document.body.classList.add('mobile-device');

    // Improved tap detection for flip cards - prevents accidental flips during scrolling
    tipCards.forEach(card => {
        let touchStartX = 0;
        let touchStartY = 0;
        let touchStartTime = 0;
        let isTouching = false;

        card.addEventListener('touchstart', (e) => {
            // Don't prevent default - allow scrolling
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
            touchStartTime = Date.now();
            isTouching = true;
        }, { passive: true });

        card.addEventListener('touchmove', (e) => {
            // If user moves finger more than 10px, it's a scroll, not a tap
            const touchMoveX = e.touches[0].clientX;
            const touchMoveY = e.touches[0].clientY;
            const moveDistance = Math.sqrt(
                Math.pow(touchMoveX - touchStartX, 2) +
                Math.pow(touchMoveY - touchStartY, 2)
            );

            if (moveDistance > 10) {
                isTouching = false; // Cancel the tap
            }
        }, { passive: true });

        card.addEventListener('touchend', (e) => {
            const touchDuration = Date.now() - touchStartTime;

            // Only flip if:
            // 1. Touch was brief (< 300ms)
            // 2. No significant movement occurred (isTouching still true)
            if (isTouching && touchDuration < 300) {
                e.preventDefault(); // Prevent ghost click
                card.classList.toggle('flipped');
            }

            isTouching = false;
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
