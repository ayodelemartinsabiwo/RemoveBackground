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
UninstallDisplayIcon={app}\BackgroundRemover.exe
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
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "contextmenu"; Description: "Context Menu (Right Click)"; GroupDescription: "Integration"; Flags: checkedonce

[Files]
; Include the entire BackgroundRemover folder structure (exe + _internal folder with models)
Source: "dist\BackgroundRemover\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "USER_GUIDE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "fix_windows_defender.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "open_installation_folder.bat"; DestDir: "{app}"; Flags: ignoreversion
; Simple and reliable context menu scripts
Source: "install-context-menu-simple.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "uninstall-context-menu-simple.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "test_context_menu_manually.bat"; DestDir: "{app}"; Flags: ignoreversion
; Remove old context menu files
;Source: "src\context_menu.py"; DestDir: "{app}"; Flags: ignoreversion
;Source: "install-context-menu.bat"; DestDir: "{app}"; Flags: ignoreversion
;Source: "docs\WINDOWS_DEFENDER_FIX.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Background Remover"; Filename: "{app}\BackgroundRemover.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\User Guide"; Filename: "{app}\USER_GUIDE.txt"
Name: "{group}\Fix Windows Defender"; Filename: "{app}\fix_windows_defender.bat"; IconFilename: "{sys}\shell32.dll"; IconIndex: 1
Name: "{group}\Open Installation Folder"; Filename: "{app}"; IconFilename: "{sys}\shell32.dll"; IconIndex: 3
Name: "{group}\Install Context Menu"; Filename: "{app}\install-context-menu-simple.bat"; IconFilename: "{sys}\shell32.dll"; IconIndex: 1
Name: "{group}\Test Context Menu"; Filename: "{app}\test_context_menu_manually.bat"; IconFilename: "{sys}\shell32.dll"; IconIndex: 1
Name: "{group}\{cm:UninstallProgram,Background Remover}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Background Remover"; Filename: "{app}\BackgroundRemover.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
; Install context menu only if user selected the option
Filename: "{app}\install-context-menu-simple.bat"; Parameters: "silent"; WorkingDir: "{app}"; Flags: runhidden waituntilterminated; Tasks: contextmenu
Filename: "{app}\BackgroundRemover.exe"; Description: "{cm:LaunchProgram,Background Remover}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Remove context menu during uninstall
Filename: "{app}\uninstall-context-menu.bat"; Parameters: "silent"; Flags: runhidden waituntilterminated

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

// Custom page to show context menu installation status
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  StatusMsg: string;
  RetryCount: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Check if context menu was installed successfully
    if WizardIsTaskSelected('contextmenu') then
    begin
      // Wait a bit and retry verification up to 3 times
      RetryCount := 0;
      ResultCode := 1; // Start with failure

      while (RetryCount < 3) and (ResultCode <> 0) do
      begin
        Sleep(500); // Wait 500ms
        if Exec('reg', 'query "HKCU\Software\Classes\*\shell\RemoveBackground"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
        begin
          if ResultCode = 0 then
            Break; // Success, exit loop
        end;
        RetryCount := RetryCount + 1;
      end;

      if ResultCode = 0 then
      begin
        StatusMsg := 'Context menu installed successfully!' + #13#10 + #13#10 +
                    'Right-click any image file to see "Remove Background" option.';
      end else
      begin
        StatusMsg := 'Context menu installation may have failed.' + #13#10 + #13#10 +
                    'You can manually install it later using:' + #13#10 +
                    'Start Menu -> Background Remover -> Install Context Menu';
      end;

      // Only show message if not running silently
      if not WizardSilent then
        MsgBox(StatusMsg, mbInformation, MB_OK);
    end;
  end;
end;

[UninstallRun]
; Remove context menu during uninstall
Filename: "{app}\uninstall-context-menu-simple.bat"; Parameters: "silent"; WorkingDir: "{app}"; Flags: runhidden waituntilterminated
