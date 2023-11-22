@echo off

if exist data.db (
    if exist data.db.bak (
        del data.db.bak
    )
    ren data.db data.db.bak
)
