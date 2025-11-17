const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');
const { google } = require('googleapis');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// CSV file path
const CSV_FILE = path.join(__dirname, 'form_submissions.csv');

// Google Sheets configuration
const SCOPES = ['https://www.googleapis.com/auth/spreadsheets'];
const SPREADSHEET_ID = '14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g';

// Initialize Google Sheets API
let sheetsClient = null;

async function initializeGoogleSheets() {
    try {
        // Check if credentials file exists
        const credentialsPath = path.join(__dirname, 'credentials.json');
        try {
            await fs.access(credentialsPath);
        } catch {
            console.log('⚠️  Google Sheets credentials not found. Data will only be saved to CSV.');
            console.log('   To enable Google Sheets integration, add credentials.json to the website folder.');
            return;
        }

        const credentials = JSON.parse(await fs.readFile(credentialsPath, 'utf8'));

        // Use service account authentication
        const auth = new google.auth.GoogleAuth({
            credentials: credentials,
            scopes: SCOPES,
        });

        const authClient = await auth.getClient();
        sheetsClient = google.sheets({ version: 'v4', auth: authClient });

        console.log('✅ Google Sheets API initialized successfully');

        // Initialize spreadsheet with headers if needed
        await initializeSpreadsheet();
    } catch (error) {
        console.error('❌ Error initializing Google Sheets:', error.message);
        console.log('   Data will be saved to CSV only.');
    }
}

async function initializeSpreadsheet() {
    if (!sheetsClient) return;

    try {
        // Check if the sheet has headers
        const response = await sheetsClient.spreadsheets.values.get({
            spreadsheetId: SPREADSHEET_ID,
            range: 'Sheet1!A1:K1',
        });

        // If no headers, add them
        if (!response.data.values || response.data.values.length === 0) {
            const headers = [
                'Timestamp',
                'Name',
                'Email',
                'Age Range',
                'Location',
                'Profession',
                'Willing to Pay',
                'Amount',
                'Currency',
                'Detected Country',
                'Country Code'
            ];

            await sheetsClient.spreadsheets.values.update({
                spreadsheetId: SPREADSHEET_ID,
                range: 'Sheet1!A1:K1',
                valueInputOption: 'RAW',
                resource: {
                    values: [headers],
                },
            });

            console.log('✅ Spreadsheet headers initialized');
        }
    } catch (error) {
        console.error('Error initializing spreadsheet:', error.message);
    }
}

// Initialize CSV file
async function initializeCSV() {
    try {
        await fs.access(CSV_FILE);
    } catch {
        // File doesn't exist, create it with headers
        const headers = 'Timestamp,Name,Email,Age Range,Location,Profession,Willing to Pay,Amount,Currency,Detected Country,Country Code\n';
        await fs.writeFile(CSV_FILE, headers, 'utf8');
        console.log('✅ CSV file initialized');
    }
}

// Save data to CSV
async function saveToCSV(data) {
    try {
        const row = [
            data.timestamp,
            data.name,
            data.email,
            data.ageRange,
            data.location,
            data.profession,
            data.willingToPay,
            data.amount,
            data.currency,
            data.detectedCountry,
            data.detectedCountryCode
        ];

        // Escape CSV values (wrap in quotes and escape existing quotes)
        const escapedRow = row.map(value => {
            const stringValue = String(value);
            if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
                return `"${stringValue.replace(/"/g, '""')}"`;
            }
            return stringValue;
        });

        const csvLine = escapedRow.join(',') + '\n';
        await fs.appendFile(CSV_FILE, csvLine, 'utf8');

        console.log('✅ Data saved to CSV');
        return true;
    } catch (error) {
        console.error('Error saving to CSV:', error);
        return false;
    }
}

// Save data to Google Sheets
async function saveToGoogleSheets(data) {
    if (!sheetsClient) {
        console.log('⚠️  Google Sheets not configured, skipping...');
        return false;
    }

    try {
        const row = [
            data.timestamp,
            data.name,
            data.email,
            data.ageRange,
            data.location,
            data.profession,
            data.willingToPay,
            data.amount,
            data.currency,
            data.detectedCountry,
            data.detectedCountryCode
        ];

        await sheetsClient.spreadsheets.values.append({
            spreadsheetId: SPREADSHEET_ID,
            range: 'Sheet1!A:K',
            valueInputOption: 'RAW',
            insertDataOption: 'INSERT_ROWS',
            resource: {
                values: [row],
            },
        });

        console.log('✅ Data saved to Google Sheets');
        return true;
    } catch (error) {
        console.error('Error saving to Google Sheets:', error.message);
        return false;
    }
}

// API endpoint to handle form submissions
app.post('/api/submit-form', async (req, res) => {
    try {
        const formData = req.body;

        // Validate required fields
        if (!formData.name || !formData.email || !formData.ageRange ||
            !formData.location || !formData.profession || !formData.willingToPay) {
            return res.status(400).json({ error: 'Missing required fields' });
        }

        // Add server timestamp
        formData.timestamp = new Date().toISOString();

        // Save to CSV
        const csvSaved = await saveToCSV(formData);

        // Save to Google Sheets
        const sheetsSaved = await saveToGoogleSheets(formData);

        console.log(`📝 Form submission received from ${formData.name} (${formData.email})`);

        res.json({
            success: true,
            message: 'Form data saved successfully',
            savedToCSV: csvSaved,
            savedToSheets: sheetsSaved
        });
    } catch (error) {
        console.error('Error processing form submission:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// API endpoint to get all submissions (admin only - add authentication in production)
app.get('/api/submissions', async (req, res) => {
    try {
        const csvContent = await fs.readFile(CSV_FILE, 'utf8');
        const lines = csvContent.split('\n');
        const headers = lines[0].split(',');

        const submissions = lines.slice(1)
            .filter(line => line.trim())
            .map(line => {
                const values = line.split(',');
                const submission = {};
                headers.forEach((header, index) => {
                    submission[header] = values[index];
                });
                return submission;
            });

        res.json({ submissions });
    } catch (error) {
        console.error('Error reading submissions:', error);
        res.status(500).json({ error: 'Error reading submissions' });
    }
});

// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'OK',
        googleSheetsConfigured: sheetsClient !== null
    });
});

// Initialize and start server
async function startServer() {
    await initializeCSV();
    await initializeGoogleSheets();

    app.listen(PORT, () => {
        console.log('='.repeat(60));
        console.log('🚀 Background Remover Website Server');
        console.log('='.repeat(60));
        console.log(`📍 Server running at: http://localhost:${PORT}`);
        console.log(`📊 CSV file location: ${CSV_FILE}`);
        console.log(`📈 Google Sheets ID: ${SPREADSHEET_ID}`);
        console.log(`🔗 Google Sheets URL: https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}`);
        console.log('='.repeat(60));
        console.log('');
        console.log('✨ Ready to accept form submissions!');
        console.log('');
    });
}

startServer();
