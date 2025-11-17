# Google Sheets Integration Setup Guide

This guide will help you set up automatic form submission data collection to Google Sheets using Google Apps Script (100% free).

## Step 1: Open Your Google Sheet

1. Go to your Google Sheet: https://docs.google.com/spreadsheets/d/14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g/edit
2. Make sure you're logged in with the account that owns this sheet (or has edit access)

## Step 2: Create the Apps Script

1. In your Google Sheet, click **Extensions** → **Apps Script**
2. Delete any code in the editor
3. Copy and paste the code from `google-apps-script.js` file (see below)
4. Click the **Save** icon (💾) or press `Ctrl+S` / `Cmd+S`
5. Name your project: "Background Remover Form Handler"

## Step 3: Deploy as Web App

1. Click **Deploy** → **New deployment**
2. Click the gear icon (⚙️) next to "Select type"
3. Choose **Web app**
4. Configure the deployment:
   - **Description**: "Form submission handler v1"
   - **Execute as**: Me (your email)
   - **Who has access**: Anyone
5. Click **Deploy**
6. **Authorize access**:
   - Click "Authorize access"
   - Choose your Google account
   - Click "Advanced" → "Go to Background Remover Form Handler (unsafe)"
   - Click "Allow"
7. **Copy the Web App URL** - it will look like:
   ```
   https://script.google.com/macros/s/AKfycby.../exec
   ```
8. **IMPORTANT**: Keep this URL safe! You'll need it in the next step.

## Step 4: Update Your Website Code

1. Open `docs/script.js` in your project
2. Find the line (around line 21):
   ```javascript
   const GOOGLE_APPS_SCRIPT_URL = 'YOUR_DEPLOYMENT_URL_HERE';
   ```
3. Replace `'YOUR_DEPLOYMENT_URL_HERE'` with your actual Web App URL from Step 3
4. Save the file
5. Commit and push to GitHub:
   ```bash
   git add docs/script.js
   git commit -m "Add Google Apps Script URL for form submissions"
   git push
   ```

## Step 5: Test the Integration

1. Go to your GitHub Pages website
2. Fill out and submit the form
3. Check your Google Sheet - a new row should appear with the submission data!

## Troubleshooting

**If data is not appearing in the sheet:**

1. Check browser console (F12) for errors
2. Verify the Apps Script URL is correct in `script.js`
3. Make sure the Apps Script deployment is set to "Anyone" for access
4. Check the Apps Script logs:
   - Go to Apps Script editor
   - Click **Executions** (left sidebar)
   - Look for any error messages

**If you see CORS errors:**

- Make sure you deployed as a Web App (not as an API executable)
- Make sure "Who has access" is set to "Anyone"

## Sheet Structure

The Apps Script will create these columns automatically:
- Timestamp
- Name
- Email
- Age Range
- Location
- Profession
- Willing to Pay
- Amount
- Currency
- Detected Country
- Detected Country Code

## Updating the Apps Script

If you need to make changes:

1. Edit the code in Apps Script editor
2. Click **Deploy** → **Manage deployments**
3. Click the pencil icon (✏️) to edit
4. Change the version to "New version"
5. Click **Deploy**
6. The URL stays the same, no need to update `script.js`

## Security Note

This setup is safe because:
- The Apps Script runs under your Google account
- Only you can modify the script
- The script only writes to your specific Google Sheet
- No sensitive credentials are exposed in the frontend code
