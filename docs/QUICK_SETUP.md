# 🚀 Quick Setup Guide - Google Sheets Integration

## What You're Setting Up

This connects your GitHub Pages website form to automatically populate your Google Sheet when users submit data. No server needed!

---

## ⚡ 5-Minute Setup

### Step 1️⃣: Open Apps Script

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g/edit
2. Click: **Extensions** → **Apps Script**

### Step 2️⃣: Paste the Code

1. Delete any existing code in the editor
2. Open the file: `google-apps-script.js` from your project
3. Copy ALL the code
4. Paste it into the Apps Script editor
5. Click **Save** (💾)
6. Name it: "Background Remover Form Handler"

### Step 3️⃣: Deploy

1. Click **Deploy** → **New deployment**
2. Click ⚙️ next to "Select type"
3. Choose **Web app**
4. Settings:
   - **Execute as**: Me
   - **Who has access**: Anyone
5. Click **Deploy**
6. Click **Authorize access** → Choose your account
7. Click **Advanced** → **Go to ... (unsafe)**
8. Click **Allow**

### Step 4️⃣: Copy Your URL

You'll see a URL like:
```
https://script.google.com/macros/s/AKfycby...LONG_ID.../exec
```

**Copy this entire URL!** ✂️

### Step 5️⃣: Update Your Code

1. Open `docs/script.js` in your project
2. Find line 26:
   ```javascript
   const GOOGLE_APPS_SCRIPT_URL = 'YOUR_DEPLOYMENT_URL_HERE';
   ```
3. Replace `'YOUR_DEPLOYMENT_URL_HERE'` with your copied URL:
   ```javascript
   const GOOGLE_APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycby...your-url.../exec';
   ```
4. Save the file

### Step 6️⃣: Push to GitHub

```bash
git add docs/script.js
git commit -m "Configure Google Sheets integration"
git push
```

### Step 7️⃣: Test It! 🎉

1. Wait 1-2 minutes for GitHub Pages to update
2. Visit your website
3. Fill out and submit the form
4. Check your Google Sheet - new data should appear!

---

## ✅ Success Checklist

- [ ] Apps Script code pasted and saved
- [ ] Web app deployed with "Anyone" access
- [ ] Deployment URL copied
- [ ] URL added to `script.js`
- [ ] Changes pushed to GitHub
- [ ] Test submission successful
- [ ] Data appears in Google Sheet

---

## 🐛 Troubleshooting

**Data not appearing?**
- Open browser console (F12) - check for errors
- Verify the URL in `script.js` is correct (should end with `/exec`)
- Make sure deployment access is set to "Anyone"
- Wait 5 minutes and try again (sometimes there's a delay)

**Still not working?**
- Go to Apps Script → **Executions** (left sidebar)
- Check if there are any failed executions
- Look at the error message

**Need to update the script?**
- Edit code in Apps Script editor
- Click **Deploy** → **Manage deployments**
- Click ✏️ (pencil icon)
- Version: "New version"
- Click **Deploy**
- URL stays the same - no need to update `script.js`

---

## 📊 Your Data

All form submissions will appear in a new tab called **"Form Submissions"** with these columns:

| Column | Example |
|--------|---------|
| Timestamp | 2025-11-17 14:30:00 |
| Name | John Doe |
| Email | john@example.com |
| Age Range | 25-34 |
| Location | Lagos, Nigeria |
| Profession | Graphic Designer |
| Willing to Pay | Yes |
| Amount | 10 |
| Currency | NGN |
| Detected Country | Nigeria |
| Detected Country Code | NG |

---

## 🔒 Security

✅ **This is secure because:**
- Script runs under your Google account
- Only you can modify the script
- No credentials exposed in frontend code
- Data goes directly to your sheet

---

## 💡 Pro Tips

1. **Share the sheet** with team members (they don't need Apps Script access)
2. **Create a dashboard** using Google Sheets charts
3. **Set up notifications**: Tools → Notification rules
4. **Export data**: File → Download → CSV

---

## 📝 Notes

- The form will still work even if Google Sheets is down (data saved locally)
- Check localStorage in browser to recover offline submissions
- Run `exportFormDataAsCSV()` in console to export local data

---

Need more help? Check `GOOGLE_SHEETS_SETUP.md` for detailed instructions.
