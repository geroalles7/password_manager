[Setup]
AppId={{E8D1A7F1-3A9C-4C1D-9F88-1C5B3F2A7B01}
AppName=Password Manager
AppVersion=1.0
AppPublisher=Alles Geronimo
AppCopyright=© 2026 Alles Geronimo. Todos los derechos reservados.
DefaultDirName={autopf}\Password Manager
DefaultGroupName=Password Manager
OutputDir=Output
OutputBaseFilename=PasswordManagerSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\main.exe

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Password Manager"; Filename: "{app}\main.exe"
Name: "{commondesktop}\Password Manager"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "Ejecutar Password Manager"; Flags: nowait postinstall skipifsilent