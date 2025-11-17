# Quick Setup Guide for Background Remover Website

This guide will help you set up the website in 10 minutes.

## Option 1: Quick Start (CSV Only - No Google Sheets)

If you want to get started quickly without Google Sheets integration:

1. **Install Node.js** (if not already installed):
   - Download from [nodejs.org](https://nodejs.org/)
   - Install and verify: `node --version`

2. **Open terminal in the website folder:**
   ```bash
   cd website
   ```

3. **Install dependencies:**
   ```bash
   npm install
   ```

4. **Start the server:**
   ```bash
   npm start
   ```

5. **Open browser:**
   - Go to `http://localhost:3000`
   - Form data will be saved to `form_submissions.csv`

✅ **You're done!** The website is running and collecting data in CSV format.

---

## Option 2: Full Setup (with Google Sheets Integration)

Follow these steps to enable automatic Google Sheets population:

### Step 1: Create Google Cloud Project (5 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "New Project"
3. Name it: `background-remover-form`
4. Click "Create"

### Step 2: Enable Google Sheets API (2 minutes)

1. In the Google Cloud Console, go to **"APIs & Services"** > **"Library"**
2. Search for **"Google Sheets API"**
3. Click on it and click **"Enable"**

### Step 3: Create Service Account (3 minutes)

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** > **"Service Account"**
3. Fill in:
   - **Name:** `form-collector`
   - **Description:** `Collects form data`
4. Click **"Create and Continue"**
5. Skip the optional steps
6. Click **"Done"**

### Step 4: Download Credentials (1 minute)

1. In the Credentials page, find your service account
2. Click on it
3. Go to the **"Keys"** tab
4. Click **"Add Key"** > **"Create new key"**
5. Choose **"JSON"**
6. Click **"Create"**
7. The file will download automatically
8. **Rename it to `credentials.json`**
9. **Move it to the `website` folder**

### Step 5: Share Google Sheet (2 minutes)

1. Open the `credentials.json` file you just downloaded
2. Find and copy the `client_email` (looks like: `form-collector@project-123456.iam.gserviceaccount.com`)
3. Open the Google Sheet:
   - URL: https://docs.google.com/spreadsheets/d/14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g/edit
4. Click the **"Share"** button (top right)
5. Paste the service account email
6. Set permission to **"Editor"**
7. **Uncheck "Notify people"**
8. Click **"Share"** or **"Send"**

### Step 6: Run the Server (1 minute)

1. Open terminal in the website folder:
   ```bash
   cd website
   ```

2. Install dependencies (if not done already):
   ```bash
   npm install
   ```

3. Start the server:
   ```bash
   npm start
   ```

4. You should see:
   ```
   ✅ Google Sheets API initialized successfully
   ✅ Spreadsheet headers initialized
   🚀 Server running at: http://localhost:3000
   ```

### Step 7: Test It! (1 minute)

1. Open browser: `http://localhost:3000`
2. Click **"Download for Windows"**
3. Fill out the form
4. Submit
5. Check the Google Sheet - your data should appear!

---

## Troubleshooting

### "Google Sheets credentials not found"

- Make sure `credentials.json` is in the `website` folder
- Make sure the file is named exactly `credentials.json` (not `credentials.json.txt`)

### "Error 403: Permission denied"

- Make sure you shared the Google Sheet with the service account email
- Make sure the service account has "Editor" permissions

### "Cannot find module 'googleapis'"

- Run `npm install` in the website folder

### Form submits but no data in Google Sheets

- Check the server console for error messages
- Verify the Spreadsheet ID in `server.js` matches your sheet
- Try refreshing the Google Sheet

### Port 3000 already in use

- Either close the app using port 3000, or
- Change the port in `server.js`: `const PORT = 3001;`

---

## Testing Without Running the Server

If you just want to view the website design without the backend:

1. Open `index.html` directly in a browser
2. Click around and test the form
3. Data won't be saved (no server running)
4. Good for design preview only

---

## Using a Different Google Sheet

If you want to use a different Google Sheet:

1. Create a new Google Sheet
2. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```
3. Open `server.js`
4. Find this line:
   ```javascript
   const SPREADSHEET_ID = '14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g';
   ```
5. Replace with your Sheet ID:
   ```javascript
   const SPREADSHEET_ID = 'YOUR_SHEET_ID_HERE';
   ```
6. Share the new sheet with your service account email
7. Restart the server

---

## Keeping Server Running 24/7

### Using PM2 (Recommended for Linux/Mac)

```bash
# Install PM2
npm install -g pm2

# Start server with PM2
pm2 start server.js --name background-remover

# Make it start on boot
pm2 startup
pm2 save
```

### Using forever (Alternative)

```bash
# Install forever
npm install -g forever

# Start server
forever start server.js
```

### Using Windows Service

For Windows, you can use [node-windows](https://www.npmjs.com/package/node-windows) to create a Windows service.

---

## Next Steps

1. **Add a real download file**: Update the download link in `script.js`
2. **Deploy to production**: Use Heroku, Vercel, or your own server
3. **Add analytics**: Track page views and form submissions
4. **Customize design**: Edit `styles.css` to match your brand
5. **Add email notifications**: Get notified when someone submits the form

---

## Need Help?

- Check the main `README.md` for detailed documentation
- Check server console logs for errors
- Check browser console (F12) for client-side errors
- Verify all files are in the correct location

Good luck! 🚀
