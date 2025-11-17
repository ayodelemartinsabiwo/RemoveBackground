/**
 * Google Apps Script for Background Remover Form Submissions
 *
 * This script receives form data from the website and writes it to Google Sheets.
 * Deploy this as a Web App to get an endpoint URL.
 *
 * Instructions:
 * 1. Open your Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Paste this code
 * 4. Deploy as Web App (Execute as: Me, Access: Anyone)
 * 5. Copy the deployment URL and add it to script.js
 */

// Your Google Sheet ID (the part in the URL between /d/ and /edit)
const SHEET_ID = '14Tr3whY3PSV_ljcCasV2LuwpMtIfU5fyvusPbFDtL2g';
const SHEET_NAME = 'Form Submissions'; // Name of the sheet tab

/**
 * Handle POST requests from the form
 */
function doPost(e) {
  try {
    // Parse the incoming JSON data
    const data = JSON.parse(e.postData.contents);

    // Get the spreadsheet
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    let sheet = spreadsheet.getSheetByName(SHEET_NAME);

    // Create the sheet if it doesn't exist
    if (!sheet) {
      sheet = spreadsheet.insertSheet(SHEET_NAME);

      // Add headers
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
        'Detected Country Code'
      ];
      sheet.appendRow(headers);

      // Format header row
      const headerRange = sheet.getRange(1, 1, 1, headers.length);
      headerRange.setFontWeight('bold');
      headerRange.setBackground('#ff6b35');
      headerRange.setFontColor('#ffffff');

      // Freeze header row
      sheet.setFrozenRows(1);
    }

    // Prepare the row data
    const rowData = [
      new Date(), // Timestamp
      data.name || '',
      data.email || '',
      data.ageRange || '',
      data.location || '',
      data.profession || '',
      data.willingToPay || '',
      data.amount || '0',
      data.currency || 'USD',
      data.detectedCountry || 'Not detected',
      data.detectedCountryCode || 'N/A'
    ];

    // Append the data to the sheet
    sheet.appendRow(rowData);

    // Auto-resize columns for better readability
    sheet.autoResizeColumns(1, rowData.length);

    // Log success
    Logger.log('Form submission saved: ' + data.email);

    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        'result': 'success',
        'message': 'Data saved successfully',
        'timestamp': new Date().toISOString()
      }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    // Log error
    Logger.log('Error: ' + error.toString());

    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        'result': 'error',
        'message': error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Handle GET requests (optional - for testing)
 */
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({
      'result': 'success',
      'message': 'Background Remover Form Handler is running!',
      'instructions': 'Send POST requests with form data to this endpoint.',
      'timestamp': new Date().toISOString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Test function to verify the script works
 * Run this from the Apps Script editor to test
 */
function testFormSubmission() {
  const testData = {
    name: 'Test User',
    email: 'test@example.com',
    ageRange: '25-34',
    location: 'Lagos, Nigeria',
    profession: 'Software Developer',
    willingToPay: 'Yes',
    amount: '10',
    currency: 'NGN',
    detectedCountry: 'Nigeria',
    detectedCountryCode: 'NG'
  };

  const testEvent = {
    postData: {
      contents: JSON.stringify(testData)
    }
  };

  const response = doPost(testEvent);
  Logger.log('Test response: ' + response.getContent());
}
