@echo off
python -c "import selenium"
if ERRORLEVEL 1 (pip check selenium & pip install selenium)

python -c "import webdriver_manager"
if ERRORLEVEL 1 (pip check webdriver-manager & pip install webdriver-manager)

python -c "import HtmlTestRunner"
if ERRORLEVEL 1 (pip check html-testRunner & pip install html-testRunner)

if ERRORLEVEL 0 (echo Done) else (echo Some errors, please check)

