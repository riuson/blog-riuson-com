Title: Обновление PATH пользователя из командной строки
Tags: Git

Обновление пользовательской переменной окружения PATH из командной строки.
<!-- more -->

### Git Bash:

```
setlocal ENABLEEXTENSIONS
set KEY_NAME="HKEY_CURRENT_USER\Environment"
set VALUE_NAME="PATH"

FOR /F "usebackq skip=2 tokens=1,2*" %%A IN (`REG QUERY %KEY_NAME% /v %VALUE_NAME% 2^>nul`) DO (
    set ValueName=%%A
    set ValueType=%%B
    set User_Path=%%C
)

if defined ValueName (
    @echo User_Path = %User_Path%
) else (
    @echo %KEY_NAME%\%VALUE_NAME% not found.
)

If NOT "%User_Path%"=="%User_Path:Git=%" (
    echo Already added
) else (
    echo Adding
	setx PATH "%User_Path%;c:\Tools\Git64\bin"
)

echo %PATH%
```

### PowerShell

```
function DisplayPath {
  $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
  Write-Host ("Current path: " + $userPath)
}

function EnsurePathAdded {
  param([System.String] $requiredPath)
  
  $userPath = [Environment]::GetEnvironmentVariable("Path", "User")

  if ($userPath.Contains($requiredPath)) {
    Write-Host ("Exists: " + $requiredPath)
  } else {
    $userPathNew = $userPath + ";" + $requiredPath
    [Environment]::SetEnvironmentVariable("Path", $userPathNew, "User")

    $userPathUpdated = [Environment]::GetEnvironmentVariable("Path", "User")

    if ($userPathUpdated.Contains($requiredPath)) {
      Write-Host ("Added: " + $requiredPath)
    } else {
      Write-Host ("Failed to add path: " + $requiredPath)
    }
  }
}

DisplayPath
EnsurePathAdded -requiredPath "c:\Work\Tools\Git64\bin"
DisplayPath
```

Опциональный запуск через bat:
```
@echo off
set dir=%cd%
PowerShell.exe -ExecutionPolicy bypass %dir%\update-path.ps1
```
