python make_exe.py py2exe
move /Y dist\*.exe .
rd /s /q .\dist
rd /s /q .\build
del /s /q *.pyc
