# 🔐 Code Signing Guide - Removing "Unknown Publisher"

## 🚨 **Current Status: "Unknown Publisher"**

The Windows User Account Control (UAC) shows "Unknown Publisher" because the executable is not digitally signed with a code signing certificate.

## 🎯 **Solutions to Remove "Unknown Publisher":**

### **Option 1: Get a Code Signing Certificate (RECOMMENDED)**

#### **Commercial Certificate Providers:**
- **DigiCert**: $474/year (most trusted)
- **Sectigo**: $474/year (good reputation)
- **GlobalSign**: $599/year (enterprise grade)
- **SSL.com**: $399/year (budget option)

#### **Requirements for Certificate:**
- Valid business registration
- Business phone number (verified)
- Business address (verified)
- EV certificates require additional validation

#### **Signing Process:**
```powershell
# After getting certificate (.pfx file):
signtool sign /f "certificate.pfx" /p "password" /t http://timestamp.digicert.com "BackgroundRemover.exe"
```

### **Option 2: Self-Signed Certificate (Development Only)**

⚠️ **Warning**: Self-signed certificates still show security warnings but can be used for internal distribution.

```powershell
# Create self-signed certificate
New-SelfSignedCertificate -DnsName "Palmar Tech" -Type CodeSigning -CertStoreLocation cert:\CurrentUser\My

# Sign the executable
Set-AuthenticodeSignature -FilePath "BackgroundRemover.exe" -Certificate $cert
```

### **Option 3: SmartScreen Reputation Building**

- **Distribute unsigned version** to build Windows SmartScreen reputation
- **After many downloads** from trusted sources, warnings may reduce
- **Takes months/years** of distribution history
- **Not reliable** for immediate professional deployment

## 🏢 **For Palmar Tech - Recommended Action:**

### **Professional Distribution:**
1. **Purchase EV Code Signing Certificate** from DigiCert or Sectigo
2. **Register Palmar Tech** as verified business entity
3. **Sign all executables** before distribution
4. **Include timestamp** to ensure signature validity beyond certificate expiration

### **Cost-Benefit Analysis:**
- **Certificate Cost**: ~$474/year
- **Professional Credibility**: ✅ High
- **User Trust**: ✅ No security warnings
- **Windows Compatibility**: ✅ Perfect
- **SmartScreen Issues**: ✅ Resolved

## 🛠️ **Current Installer Improvements Applied:**

✅ **Enhanced Publisher Information**:
- AppPublisher=Palmar Tech
- AppContact=support@palmartech.com
- AppComments=AI-Powered Background Remover by Palmar Tech
- UninstallDisplayName=Background Remover by Palmar Tech

✅ **Professional License Agreement**:
- Custom EULA for Palmar Tech
- Proper copyright notices
- AI processing disclaimers
- Privacy statements

## 📋 **Next Steps:**

1. **Immediate**: Use current signed installer with improved metadata
2. **Short-term**: Consider self-signed certificate for internal testing
3. **Long-term**: Purchase commercial code signing certificate for public release

**Note**: Even with a certificate, first-time installs may show SmartScreen warnings until reputation is established.
