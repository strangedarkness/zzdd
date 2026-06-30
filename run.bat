@echo off

cd /d "C:\Users\stran\OneDrive\文档\Projects\zzdd"

call .venv\Scripts\activate

python -m uvicorn main:app --reload

pause