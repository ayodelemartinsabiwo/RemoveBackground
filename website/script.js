// Global variables
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

// DOM Elements
const modal = document.getElementById('formModal');
const downloadBtn = document.getElementById('downloadBtn');
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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    tryAutoDetectLocation();
});

function initializeEventListeners() {
    // Download button opens modal
    downloadBtn.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    // Close button closes modal
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Click outside modal to close
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Detect location button
    detectLocationBtn.addEventListener('click', detectLocation);

    // Willing to pay radio buttons
    willingToPayRadios.forEach(radio => {
        radio.addEventListener('change', handleWillingToPayChange);
    });

    // Amount range slider
    amountRange.addEventListener('input', (e) => {
        const value = e.target.value;
        rangeValue.textContent = value;
        amountInput.value = value;
    });

    // Amount input field
    amountInput.addEventListener('input', (e) => {
        const value = Math.min(Math.max(e.target.value, 0), 100);
        amountRange.value = value;
        rangeValue.textContent = value;
    });

    // Form submission
    userForm.addEventListener('submit', handleFormSubmit);
}

function tryAutoDetectLocation() {
    // Try to detect location automatically on page load
    fetch('https://ipapi.co/json/')
        .then(response => response.json())
        .then(data => {
            if (data.country_code) {
                const location = `${data.city || data.region || ''}, ${data.country_name || data.country_code}`;
                document.getElementById('location').value = location.trim();
                userLocation = data;

                // Set currency based on country
                const currency = currencyMapping[data.country_code] || 'USD';
                detectedCurrency = currency;
                currencySelect.value = currency;
            }
        })
        .catch(error => {
            console.log('Auto-detection failed, user can manually detect or enter location');
        });
}

function detectLocation() {
    detectLocationBtn.disabled = true;
    detectLocationBtn.textContent = '📍 Detecting...';

    // Try multiple geolocation APIs for reliability
    fetch('https://ipapi.co/json/')
        .then(response => response.json())
        .then(data => {
            if (data.country_code) {
                const location = `${data.city || data.region || ''}, ${data.country_name || data.country_code}`;
                document.getElementById('location').value = location.trim();
                userLocation = data;

                // Set currency based on country
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
            // Fallback to another API
            fetch('https://api.ipify.org?format=json')
                .then(response => response.json())
                .then(ipData => {
                    // At least we got the IP, show a message
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

async function handleFormSubmit(e) {
    e.preventDefault();

    // Collect form data
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
        // Send data to backend
        const response = await fetch('/api/submit-form', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
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
        } else {
            throw new Error('Failed to submit form');
        }
    } catch (error) {
        console.error('Error submitting form:', error);

        // Fallback: Store data locally and still allow download
        storeDataLocally(formData);

        alert('Thank you! Your response has been recorded. Download will begin shortly.');
        modal.style.display = 'none';

        setTimeout(() => {
            initiateDownload();
        }, 1000);
    }
}

function storeDataLocally(data) {
    // Store in localStorage as backup
    const existingData = JSON.parse(localStorage.getItem('formSubmissions') || '[]');
    existingData.push(data);
    localStorage.setItem('formSubmissions', JSON.stringify(existingData));

    // Also create a downloadable CSV
    console.log('Form data stored locally:', data);
}

function initiateDownload() {
    // Create a temporary link to trigger download
    // In production, this would point to the actual installer file
    const link = document.createElement('a');
    link.href = '#'; // Replace with actual download link
    link.download = 'BackgroundRemover_Setup.exe';

    // For demonstration, show an alert
    alert('Download would start here!\n\nIn production, this would download:\nBackgroundRemover_Setup.exe (~100MB)\n\nFor now, the form data has been collected successfully.');

    // Uncomment the following line when you have an actual file to download
    // link.click();
}

// Export form data as CSV (for admin/testing purposes)
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
console.log('Admin: To export form data as CSV, run: exportFormDataAsCSV()');
