@echo off
title Klaiz Designs - Local Store Server
echo ============================================
echo   KLAIZ DESIGNS - Starting Local Server
echo ============================================
echo.
echo Starting server at http://localhost:3000
echo.
echo  STORE:  http://localhost:3000/index.html
echo  SHOP:   http://localhost:3000/collection.html
echo  ADMIN:  http://localhost:3000/admin/products.html
echo.
echo DO NOT close this window while using the site.
echo Press Ctrl+C to stop the server.
echo.

:: Kill any existing server on port 3000
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING" 2^>nul') do taskkill /F /PID %%a >nul 2>&1

:: Start server and open browser
start http://localhost:3000/index.html
python -m http.server 3000
