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
        // Close other open items
        const isActive = item.classList.contains('active');

        faqItems.forEach(otherItem => {
            if (otherItem !== item) {
                otherItem.classList.remove('active');
            }
        });

        // Toggle current item
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

        // Don't prevent default for # only links (used for onclick handlers)
        if (href === '#') {
            return;
        }

        e.preventDefault();

        const target = document.querySelector(href);
        if (target) {
            const navHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = target.offsetTop - navHeight - 20;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });

            // Close mobile menu if open
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

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
    } else {
        navbar.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)';
    }

    lastScroll = currentScroll;
});

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

// Observe elements that should animate on scroll
document.querySelectorAll('.feature-card, .step, .doc-card, .unique-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ==================== //
// Download Button Handler
// ==================== //

function handleDownload() {
    // This is a placeholder for when you have the actual download file
    alert('To set up the download:\n\n' +
          '1. Build the installer: pyinstaller build_optimized.spec && iscc installer_config.iss\n' +
          '2. Upload the installer to a hosting service (GitHub Releases, etc.)\n' +
          '3. Update this button with the download URL');
}

// ==================== //
// Hero Demo Cards - Enhanced Hover Effect
// ==================== //

const demoCards = document.querySelectorAll('.demo-card-enhanced');

demoCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        // Add a subtle scale animation
        card.style.transition = 'all 0.3s ease';
    });
});

// ==================== //
// Stats Counter Animation
// ==================== //

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// ==================== //
// Copy to Clipboard
// ==================== //

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success message
        console.log('Copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// ==================== //
// Initialize on Load
// ==================== //

document.addEventListener('DOMContentLoaded', () => {
    console.log('Palmar Tech Background Remover Website Loaded');

    // Add any initialization code here

    // Example: Log page views (you can integrate analytics here)
    if (typeof gtag !== 'undefined') {
        gtag('event', 'page_view', {
            page_title: document.title,
            page_location: window.location.href,
            page_path: window.location.pathname
        });
    }

    // Add visual feedback for tip cards
    const tipCardsLoad = document.querySelectorAll('.tip-card');
    tipCardsLoad.forEach((card, index) => {
        // Stagger the appearance of tip cards
        card.style.animationDelay = `${index * 0.1}s`;
    });
});

// ==================== //
// Performance Monitoring
// ==================== //

// Log page load time
window.addEventListener('load', () => {
    const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
    console.log(`Page loaded in ${loadTime}ms`);
});

// ==================== //
// Feature Detection
// ==================== //

// Check for required browser features
const hasRequiredFeatures = () => {
    return 'IntersectionObserver' in window &&
           'requestAnimationFrame' in window &&
           'classList' in document.documentElement;
};

if (!hasRequiredFeatures()) {
    console.warn('Some features may not work in this browser');
}

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
    // Close FAQ items on Escape
    if (e.key === 'Escape') {
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
    // Expand all FAQ items before printing
    faqItems.forEach(item => {
        item.classList.add('active');
    });
});

window.addEventListener('afterprint', () => {
    // Collapse all FAQ items after printing
    faqItems.forEach(item => {
        item.classList.remove('active');
    });
});

// ==================== //
// Share Functionality
// ==================== //

function shareWebsite() {
    if (navigator.share) {
        navigator.share({
            title: 'Palmar Tech Background Remover - AI-Powered Background Removal',
            text: 'Check out this awesome background remover for Windows!',
            url: window.location.href
        }).then(() => {
            console.log('Shared successfully');
        }).catch((error) => {
            console.log('Error sharing:', error);
        });
    } else {
        // Fallback: copy URL to clipboard
        copyToClipboard(window.location.href);
        alert('Website URL copied to clipboard!');
    }
}

// ==================== //
// Theme Toggle (Future Feature)
// ==================== //

function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Load saved theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.body.setAttribute('data-theme', savedTheme);
}

// ==================== //
// Unique Card Animations
// ==================== //

// Add progressive reveal for unique feature cards
const uniqueCards = document.querySelectorAll('.unique-card');
uniqueCards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.15}s`;
});

// ==================== //
// Mobile Detection
// ==================== //

const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

if (isMobile) {
    // Add mobile-specific enhancements
    document.body.classList.add('mobile-device');

    // On mobile, tap to flip cards
    tipCards.forEach(card => {
        card.addEventListener('touchstart', (e) => {
            e.preventDefault();
            card.classList.toggle('flipped');
        });
    });
}
