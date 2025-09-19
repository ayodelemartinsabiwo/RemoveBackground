; filepath: installer_config.iss
[Setup]
AppName=Background Remover (Free)
AppVersion=1.0
AppPublisher=Palmer Enterprises
AppPublisherURL=mailto:palmarenterprise@gmail.com
AppSupportURL=mailto:palmarenterprise@gmail.com
AppUpdatesURL=mailto:palmarenterprise@gmail.com
AppCopyright=Copyright (C) 2025 Palmer Enterprises
AppContact=palmarenterprise@gmail.com
AppComments=Free AI-Powered Background Remover by Palmer Enterprises
UninstallDisplayName=Background Remover (Free) by Palmer Enterprises
DefaultDirName={autopf}\BackgroundRemover
DefaultGroupName=Background Remover
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=BackgroundRemover_Setup
SetupIconFile=assets\icon.ico
WizardImageFile=assets\splash.bmp
Compression=lzma
SolidCompression=yes
WizardStyle=modern
LicenseFile=LICENSE.txt
InfoBeforeFile=
InfoAfterFile=USER_GUIDE.txt
VersionInfoVersion=1.0.0.0
VersionInfoCompany=Palmar Tech
VersionInfoDescription=Background Remover Setup
VersionInfoCopyright=Copyright (C) 2025 Palmar Tech
VersionInfoProductName=Background Remover
VersionInfoProductVersion=1.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\BackgroundRemover.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "USER_GUIDE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "fix_windows_defender.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "open_installation_folder.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\context_menu.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "install-context-menu.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "uninstall-context-menu.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\WINDOWS_DEFENDER_FIX.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Background Remover"; Filename: "{app}\BackgroundRemover.exe"
Name: "{group}\User Guide"; Filename: "{app}\USER_GUIDE.txt"
Name: "{group}\Fix Windows Defender"; Filename: "{app}\fix_windows_defender.bat"; IconFilename: "{sys}\shell32.dll"; IconIndex: 78
Name: "{group}\Open Installation Folder"; Filename: "{app}"; IconFilename: "{sys}\shell32.dll"; IconIndex: 3
Name: "{group}\{cm:UninstallProgram,Background Remover}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Background Remover"; Filename: "{app}\BackgroundRemover.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\install-context-menu.bat"; Flags: runhidden
Filename: "{app}\BackgroundRemover.exe"; Description: "{cm:LaunchProgram,Background Remover}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{app}\uninstall-context-menu.bat"; Flags: runhidden

[Code]
var
  RedBullButton: TNewButton;
  ContactButton: TNewButton;

procedure RedBullButtonOnClick(Sender: TObject);
var
  SupportMsg: string;
begin
  SupportMsg := 'Thank you for considering support!' + #13#10 + #13#10 +
                'Buy us a Red Bull!' + #13#10 + #13#10 +
                'Bank Details:' + #13#10 +
                'Account Name: PALMER ENTERPRISES' + #13#10 +
                'Bank: Zenith Bank' + #13#10 +
                'Account Number: 1017441664' + #13#10 + #13#10 +
                'Your support helps keep this software free for everyone!';
  MsgBox(SupportMsg, mbInformation, MB_OK);
end;

procedure ContactButtonOnClick(Sender: TObject);
var
  ErrorCode: Integer;
  ContactMsg: string;
begin
  ContactMsg := 'Contact Palmer Enterprises:' + #13#10 + #13#10 +
                'Email: palmarenterprise@gmail.com' + #13#10 + #13#10 +
                'Subject: Background Remover Contact' + #13#10 +
                'Message: Hi Palmer Enterprises team!' + #13#10 + #13#10 +
                'You can copy this email address and contact us directly.';

  // Try to open default email client, but show contact info if it fails
  if not ShellExec('open', 'mailto:palmarenterprise@gmail.com?subject=Background%20Remover%20Contact&body=Hi%20Palmer%20Enterprises%20team!', '', '', SW_SHOWNORMAL, ewNoWait, ErrorCode) then
    MsgBox(ContactMsg, mbInformation, MB_OK);
end;

procedure InitializeWizard();
begin
  // Create Red Bull Support Button - 72 pixels below Next/Cancel buttons
  RedBullButton := TNewButton.Create(WizardForm);
  RedBullButton.Parent := WizardForm;
  RedBullButton.Left := 20;
  RedBullButton.Top := WizardForm.NextButton.Top + 72;  // 72 pixels below
  RedBullButton.Width := 130;
  RedBullButton.Height := WizardForm.NextButton.Height;  // Same height as Next button
  RedBullButton.Caption := 'Buy us a Red Bull';
  RedBullButton.OnClick := @RedBullButtonOnClick;

  // Create Contact Button - 72 pixels below Next/Cancel buttons
  ContactButton := TNewButton.Create(WizardForm);
  ContactButton.Parent := WizardForm;
  ContactButton.Left := 160;
  ContactButton.Top := WizardForm.NextButton.Top + 72;  // 72 pixels below
  ContactButton.Width := 110;
  ContactButton.Height := WizardForm.NextButton.Height;  // Same height as Next button
  ContactButton.Caption := '@ Contact Us';
  ContactButton.OnClick := @ContactButtonOnClick;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
end;
