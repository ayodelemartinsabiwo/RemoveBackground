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
Name: "{group}\{cm:UninstallProgram,Background Remover}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Background Remover"; Filename: "{app}\BackgroundRemover.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
; Install context menu only if user selected the option
Filename: "{app}\install-context-menu-simple.bat"; Parameters: "silent"; WorkingDir: "{app}"; Flags: runhidden waituntilterminated; Tasks: contextmenu
Filename: "{app}\BackgroundRemover.exe"; Description: "{cm:LaunchProgram,Background Remover}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Remove context menu during uninstall
Filename: "{app}\uninstall-context-menu-simple.bat"; Parameters: "silent"; Flags: runhidden waituntilterminated

[UninstallDelete]
; Force removal of dynamically created files and folders
Type: filesandordirs; Name: "{app}\models"
Type: filesandordirs; Name: "{app}\_internal\models_compressed"
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"
; Remove any leftover configuration or cache files
Type: filesandordirs; Name: "{localappdata}\BackgroundRemover"

[Code]
var
  RedBullButton: TNewButton;
  ContactButton: TNewButton;
  ButtonsCreated: Boolean;

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

  if not ShellExec('open', 'mailto:palmarenterprise@gmail.com?subject=Background%20Remover%20Contact&body=Hi%20Palmer%20Enterprises%20team!', '', '', SW_SHOWNORMAL, ewNoWait, ErrorCode) then
    MsgBox(ContactMsg, mbInformation, MB_OK);
end;

procedure UpdateButtonPositions;
begin
  if not ButtonsCreated then
    Exit;

  try
    // Position buttons at the same level as standard buttons, but on the left side
    if Assigned(RedBullButton) then
    begin
      RedBullButton.Left := 8;
      RedBullButton.Top := WizardForm.CancelButton.Top;
      RedBullButton.Visible := True;
      RedBullButton.BringToFront;
    end;

    if Assigned(ContactButton) then
    begin
      ContactButton.Left := RedBullButton.Left + RedBullButton.Width + 8;
      ContactButton.Top := WizardForm.CancelButton.Top;
      ContactButton.Visible := True;
      ContactButton.BringToFront;
    end;
  except
    // Ignore positioning errors
  end;
end;

procedure CreateCustomButtons;
begin
  if ButtonsCreated then
    Exit;

  try
    // Create Red Bull Support Button
    RedBullButton := TNewButton.Create(WizardForm);
    RedBullButton.Parent := WizardForm;
    RedBullButton.Caption := 'Buy us a Red Bull';
    RedBullButton.Width := 130;
    RedBullButton.Height := 25;
    RedBullButton.OnClick := @RedBullButtonOnClick;
    RedBullButton.Visible := True;
    RedBullButton.Enabled := True;

    // Create Contact Button
    ContactButton := TNewButton.Create(WizardForm);
    ContactButton.Parent := WizardForm;
    ContactButton.Caption := 'Contact Us';
    ContactButton.Width := 100;
    ContactButton.Height := 25;
    ContactButton.OnClick := @ContactButtonOnClick;
    ContactButton.Visible := True;
    ContactButton.Enabled := True;

    ButtonsCreated := True;

    // Position buttons immediately after creation
    UpdateButtonPositions;

  except
    // If button creation fails, continue without buttons
    ButtonsCreated := False;
  end;
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  // Create buttons if not already created
  if not ButtonsCreated then
    CreateCustomButtons;

  // Always ensure buttons are visible and positioned on every page
  if ButtonsCreated then
  begin
    UpdateButtonPositions;

    // Force visibility and bring to front
    if Assigned(RedBullButton) then
    begin
      RedBullButton.Visible := True;
      RedBullButton.Enabled := True;
      RedBullButton.BringToFront;
    end;
    if Assigned(ContactButton) then
    begin
      ContactButton.Visible := True;
      ContactButton.Enabled := True;
      ContactButton.BringToFront;
    end;
  end;
end;

// Handle window resize events
procedure MainFormOnResize(Sender: TObject);
begin
  if ButtonsCreated then
    UpdateButtonPositions;
end;





procedure InitializeWizard;
begin
  ButtonsCreated := False;
  CreateCustomButtons;

  // Hook resize event
  WizardForm.OnResize := @MainFormOnResize;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
end;

// Custom uninstall cleanup
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ResultCode: Integer;
  AppDir: string;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    AppDir := ExpandConstant('{app}');

    // Force removal of any remaining directories that might have been missed
    try
      // Remove models directory if it still exists
      if DirExists(AppDir + '\models') then
        DelTree(AppDir + '\models', True, True, True);

      // Remove any remaining _internal subdirectories
      if DirExists(AppDir + '\_internal') then
        DelTree(AppDir + '\_internal', True, True, True);

      // Try to remove the main app directory if it's empty
      RemoveDir(AppDir);
    except
      // Ignore errors - some files might be in use
    end;

    // Ensure context menu is completely removed
    Exec('reg', 'delete "HKCU\Software\Classes\*\shell\RemoveBackground" /f', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    Exec('reg', 'delete "HKLM\SOFTWARE\Classes\*\shell\RemoveBackground" /f', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

    // Final registry cleanup without dangerous scripts
    Exec('reg', 'delete "HKCU\Software\Classes\*\shell\RemoveBackground" /f', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    Exec('reg', 'delete "HKLM\SOFTWARE\Classes\*\shell\RemoveBackground" /f', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
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
