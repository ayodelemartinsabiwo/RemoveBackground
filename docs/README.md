# Background Remover Website

A professional landing page for the Background Remover application with an integrated user feedback form that collects data and automatically populates a Google Sheets spreadsheet.

## Features

- **Professional Landing Page**: Showcases the Background Remover application with features, benefits, and download options
- **Interactive Form**: Pops up when users click "Download for Windows"
- **Smart Location Detection**: Automatically detects user location using IP geolocation
- **Currency Auto-Selection**: Automatically selects currency based on detected location
- **Data Collection**: Saves form responses to both CSV and Google Sheets
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

## Form Fields

The form collects the following information:
- Name (required)
- Email (required)
- Age Range (required)
- Location (required, with auto-detect option)
- Profession (required)
- Willing to pay for the product? (required)
- If willing, how much? (with currency selection and range slider)

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- npm (comes with Node.js)
- A Google Cloud Platform account (for Google Sheets integration)

### Installation

1. **Navigate to the website directory:**
   ```bash
   cd website
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

### Google Sheets Integration Setup

To enable automatic data population to Google Sheets, follow these steps:

#### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

#### 2. Create a Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - Name: `background-remover-form`
   - Description: `Service account for form data collection`
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"

#### 3. Generate Service Account Key

1. Click on the created service account
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON" format
5. Download the key file
6. Rename it to `credentials.json`
7. Move it to the `website` folder

#### 4. Share Google Sheet with Service Account

1. Open the downloaded `credentials.json` file
2. Copy the `client_email` value (looks like: `something@project-id.iam.gserviceaccount.com`)
3. Open your Google Sheet: [https://docs.google.com/spreadsheets/d/14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g/edit](https://docs.google.com/spreadsheets/d/14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g/edit)
4. Click "Share" button
5. Paste the service account email
6. Give it "Editor" permissions
7. Click "Send"

### Running the Server

#### Development Mode (with auto-reload):
```bash
npm run dev
```

#### Production Mode:
```bash
npm start
```

The server will start at `http://localhost:3000`

## File Structure

```
website/
├── index.html          # Main landing page
├── styles.css          # Styling and responsive design
├── script.js           # Frontend JavaScript (form logic, location detection)
├── server.js           # Backend server (Express.js)
├── package.json        # Node.js dependencies
├── credentials.json    # Google Sheets credentials (not in git)
├── form_submissions.csv # Local CSV backup (auto-generated)
└── README.md          # This file
```

## Data Storage

The application stores data in two places:

### 1. Local CSV File
- File: `form_submissions.csv`
- Location: `website/form_submissions.csv`
- Format: Comma-separated values with headers
- Purpose: Local backup and easy data export

### 2. Google Sheets
- Spreadsheet ID: `14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g`
- URL: [View Spreadsheet](https://docs.google.com/spreadsheets/d/14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g/edit?usp=sharing)
- Updates: Real-time when form is submitted
- Purpose: Easy sharing and collaboration

## API Endpoints

### POST `/api/submit-form`
Submits form data and saves to CSV and Google Sheets.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "ageRange": "25-34",
  "location": "New York, United States",
  "profession": "Graphic Designer",
  "willingToPay": "Yes",
  "amount": "25",
  "currency": "USD"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Form data saved successfully",
  "savedToCSV": true,
  "savedToSheets": true
}
```

### GET `/api/submissions`
Retrieves all form submissions from CSV.

**Response:**
```json
{
  "submissions": [...]
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "OK",
  "googleSheetsConfigured": true
}
```

## Location Detection

The application uses IP geolocation to automatically detect user location:

1. **Primary API**: [ipapi.co](https://ipapi.co/)
2. **Fallback API**: [ipify.org](https://www.ipify.org/)
3. **Manual Entry**: Users can also enter location manually

## Currency Mapping

The application automatically selects currency based on detected country:

| Country/Region | Currency |
|---------------|----------|
| United States | USD ($) |
| Canada | CAD ($) |
| United Kingdom | GBP (£) |
| European Union | EUR (€) |
| Japan | JPY (¥) |
| China | CNY (¥) |
| India | INR (₹) |
| Nigeria | NGN (₦) |
| South Africa | ZAR (R) |
| Kenya | KES (KSh) |
| Ghana | GHS (₵) |
| Australia/New Zealand | AUD ($) |

## Security Notes

⚠️ **Important Security Considerations:**

1. **credentials.json**: Never commit this file to git. It contains sensitive credentials.
2. **Email Sending**: To actually send emails to `palmartech18@gmail.com`, you'll need to implement email functionality using services like SendGrid, Mailgun, or Nodemailer.
3. **Rate Limiting**: In production, add rate limiting to prevent abuse.
4. **CORS**: Configure CORS properly for production deployment.
5. **Input Validation**: Server-side validation is implemented, but consider adding more robust validation.

## Deployment

### Deploy to Heroku

1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create app: `heroku create background-remover-website`
4. Set environment variables:
   ```bash
   heroku config:set NODE_ENV=production
   ```
5. Add credentials as config var or use Heroku's file system
6. Deploy: `git push heroku main`

### Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel`
4. Add credentials in Vercel dashboard

### Deploy to AWS/DigitalOcean

1. Set up a Linux server
2. Install Node.js and npm
3. Clone repository
4. Run `npm install`
5. Use PM2 to manage the process:
   ```bash
   npm install -g pm2
   pm2 start server.js --name background-remover
   pm2 save
   pm2 startup
   ```

## Email Notifications

To send email notifications when form is submitted:

1. Install nodemailer: `npm install nodemailer`
2. Add email configuration to server.js
3. Send email in the `/api/submit-form` endpoint

Example code:
```javascript
const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'your-email@gmail.com',
    pass: 'your-app-password'
  }
});

// In the form submission handler
const mailOptions = {
  from: 'your-email@gmail.com',
  to: 'palmartech18@gmail.com',
  subject: 'New Background Remover Form Submission',
  text: `New submission from ${formData.name} (${formData.email})`
};

await transporter.sendMail(mailOptions);
```

## Troubleshooting

### Google Sheets not updating

1. Check that `credentials.json` is in the website folder
2. Verify the service account email has Editor access to the sheet
3. Check server logs for error messages
4. Verify the Spreadsheet ID is correct

### Location detection not working

1. Check browser console for errors
2. Verify internet connection
3. Some ad blockers may block geolocation APIs
4. Users can still enter location manually

### Form not submitting

1. Check if server is running
2. Check browser console for errors
3. Verify CORS settings
4. Check network tab in browser dev tools

## Support

For issues and questions, please check:
1. Server console logs
2. Browser console (F12)
3. CSV file for saved data
4. Google Sheets for synced data

## License

This project is part of the Background Remover application.
