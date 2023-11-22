@echo off
call backup_db.bat
python csv2db.py
python reset_crud_history.py
python reset_chat.py