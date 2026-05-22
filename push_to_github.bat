@echo off
echo ==========================================
echo    CyberLocator Auto GitHub Pusher
echo ==========================================
echo.
echo Bhai, ye script tumhara code sidha GitHub par push kar degi.
echo.

:: Initialize Git
git init
git add .
git commit -m "Initial commit of CyberLocator v2.0"
git branch -M main

:: Push to GitHub using GitHub CLI (gh)
echo Repository create kar raha hu...
gh repo create CyberLocator --public --source=. --remote=origin --push

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] gh command fail ho gaya!
    echo Lagta hai GitHub pe login nahi hai ya repo pehle se exist karti hai.
    echo Agar login nahi hai toh cmd me likho: gh auth login
    echo.
    echo Agar repo pehle se hai, toh manual push use karo:
    git remote add origin https://github.com/RaveendraK1/CyberLocator.git
    git push -u origin main
) else (
    echo.
    echo [SUCCESS] Code successfully GitHub par push ho gaya hai! 🎉
    echo Link: https://github.com/RaveendraK1/CyberLocator
)

echo.
pause
