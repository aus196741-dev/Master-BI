@echo off
echo ==============================
echo  Master BI - Actualizando...
echo ==============================
echo.
echo [1/2] Extrayendo datos del Excel...
python "C:\Users\ausisima\Desktop\DIRECCION DE PRODUCTO\Master BI por region\extraer_datos.py"
if errorlevel 1 ( echo ERROR en extraccion de datos & pause & exit /b 1 )
echo.
echo [2/2] Generando dashboard...
python "C:\Users\ausisima\Desktop\DIRECCION DE PRODUCTO\Master BI por region\Master BI.py"
if errorlevel 1 ( echo ERROR generando dashboard & pause & exit /b 1 )
echo.
echo ==============================
echo  Dashboard listo!
echo ==============================
pause
