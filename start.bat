@echo off

@rem ------------Flask------------
pip list | findstr /C:"Flask" >nul 2>&1
if not %errorlevel% == 0 (
    echo Installing Flask
    pip install Flask
) 

@rem ------------jinja2------------
pip list | findstr /C:"jinja2" >nul 2>&1
if not %errorlevel% == 0 (
    echo Installing jinja2
    pip install jinja2
) 

@rem ------------unicodecsv------------
pip list | findstr /C:"unicodecsv" >nul 2>&1
if not %errorlevel% == 0 (
    echo Installing unicodecsv
    pip install unicodecsv
) 

@rem ------------waitress------------
pip list | findstr /C:"waitress" >nul 2>&1
if not %errorlevel% == 0 (
    echo Installing waitress
    pip install waitress
) 

call csv2db.bat

@REM rem ------------SQLAlchemy------------
@REM pip list | findstr /C:"SQLAlchemy" >nul 2>&1
@REM if not %errorlevel% == 0 (
@REM     echo Installing SQLAlchemy
@REM     pip install SQLAlchemy
@REM ) 

@REM rem ------------flask-sqlalchemy------------
@REM pip list | findstr /C:"flask-sqlalchemy" >nul 2>&1
@REM if not %errorlevel% == 0 (
@REM     echo Installing flask-sqlalchemy
@REM     pip install flask-sqlalchemy
@REM ) 

@REM rem ------------psycopg2------------
@REM pip list | findstr /C:"psycopg2" >nul 2>&1
@REM if not %errorlevel% == 0 (
@REM     echo Installing psycopg2
@REM     pip install psycopg2
@REM ) 

@REM rem ------------Flask-Migrate------------
@REM pip list | findstr /C:"Flask-Migrate" >nul 2>&1
@REM if not %errorlevel% == 0 (
@REM     echo Installing Flask-Migrate
@REM     pip install Flask-Migrate
@REM ) 

python main.py