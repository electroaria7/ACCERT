@echo off
echo Installing Flask dependencies...
pip install -r requirements.txt

echo.
echo Starting ACCERT Output Processor Server...
echo.
echo Access the application at: http://localhost:5000
echo Upload page: http://localhost:5000
echo Table display: http://localhost:5000/table_display.html
echo.
echo Press Ctrl+C to stop the server
echo.

python server.py 