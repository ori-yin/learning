%隐藏cmd窗口%
@echo off
if "%1"=="h" goto begin
start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
cd /d C:\Users\HCKJ\Documents
jupyter notebook


@echo off
chcp 65001 >nul
explorer "microsoft-edge:http://127.0.0.1:8889"
jupyter notebook --port=8889 --no-browser
