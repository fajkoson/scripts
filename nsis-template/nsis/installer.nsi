
!include "FileFunc.nsh"
!include "LogicLib.nsh"

OutFile "..\out\bin\package.exe"
InstallDir "$PROGRAMFILES\MyApp"
Page directory
Page instfiles

RequestExecutionLevel admin

Section "Main"

; === Use temp location inside install folder for signature
SetOutPath "$INSTDIR\.temp"
File /oname=$INSTDIR\.temp\payload.sig "..\out\source\payload.sig"

; === Copy external payload.tar to install directory
SetOutPath "$INSTDIR"
File /r "..\extra\*"
CopyFiles "$EXEDIR\payload.tar" "$INSTDIR\payload.tar"

DetailPrint "Verifying integrity..."

; === Create temporary verify.bat to compute the hash
FileOpen $0 "$INSTDIR\verify.bat" w
FileWrite $0 'certutil -hashfile "$INSTDIR\payload.tar" SHA256 > "$INSTDIR\hash.txt"$\r$\n'
FileClose $0
ExecWait '"$INSTDIR\verify.bat"'

; === Read computed hash (line 2 of hash.txt)
FileOpen $1 "$INSTDIR\hash.txt" r
FileRead $1 $0      ; Skip line 1
FileRead $1 $1      ; Line 2: actual hash
FileClose $1
StrCpy $1 $1 64     ; Trim

; === Read expected signature from embedded payload.sig
FileOpen $2 "$INSTDIR\.temp\payload.sig" r
FileRead $2 $3
FileClose $2
StrCpy $3 $3 64     ; Trim

DetailPrint "Computed: $1"
DetailPrint "Expected: $3"

${If} $1 == $3
    DetailPrint "Signature valid."

    ; === Extract payload.tar using Windows built-in tar.exe
    ExecWait 'tar -xf "$INSTDIR\payload.tar" -C "$INSTDIR"'

    DetailPrint "Extraction completed."

    ; Final cleanup
    Delete "$INSTDIR\payload.tar"
    Delete "$INSTDIR\verify.bat"
    Delete "$INSTDIR\hash.txt"
    RMDir /r "$INSTDIR\.temp"

${Else}
    MessageBox MB_ICONSTOP "ERROR: Invalid TAR signature. Installation aborted."

    ; Cleanup on failure
    Delete "$INSTDIR\payload.tar"
    Delete "$INSTDIR\verify.bat"
    Delete "$INSTDIR\hash.txt"
    RMDir /r "$INSTDIR\.temp"
    Abort
${EndIf}

SectionEnd
