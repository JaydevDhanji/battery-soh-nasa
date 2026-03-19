@echo off
setlocal

echo ===============================
echo 1) Build SoH table
echo ===============================
python src\data\make_soh_table.py
if errorlevel 1 goto :fail

echo ===============================
echo 2) Plot SoH curves
echo ===============================
python src\data\plot_soh_curves.py
if errorlevel 1 goto :fail

echo ===============================
echo 3) Train XGB SoH model
echo ===============================
python src\models\train_xgb_soh.py
if errorlevel 1 goto :fail

echo ===============================
echo 4) GroupKFold CV
echo ===============================
python src\models\cv_xgb_soh.py
if errorlevel 1 goto :fail

echo ===============================
echo 5) Calibrated uncertainty (group bootstrap)
echo ===============================
python src\models\ensemble_uncertainity_grpbootstrap.py
if errorlevel 1 goto :fail

echo ===============================
echo 6) Make results panel
echo ===============================
python src\models\results.py
if errorlevel 1 goto :fail

echo ===============================
echo DONE. Check the reports\ folder.
echo ===============================
goto :eof

:fail
echo.
echo ERROR: One step failed. Scroll up for the error message.
exit /b 1