@echo off
REM 第03集《种子》一键后台生成（固化 · 顺序：场景图 → R2V → T2V）
REM 用法: 在项目根目录执行  _launch_ep03.cmd
REM 日志: _gen_ep03_all.log（stdout）/ _gen_ep03_all.err.log（stderr）
cd /d D:\Users\Administrator\code\super_intelligence_2035_short_drama

echo [%date% %time%] ==== START SCENES ==== >> _gen_ep03_all.log
python -u scripts\gen_ep03_scenes.py --wait >> _gen_ep03_all.log 2>> _gen_ep03_all.err.log
echo [%date% %time%] ==== SCENES DONE (exit=%errorlevel%) ==== >> _gen_ep03_all.log

echo [%date% %time%] ==== START R2V (38 shots) ==== >> _gen_ep03_all.log
python -u scripts\gen_ep03_h3_r2v.py --skip-existing --wait >> _gen_ep03_all.log 2>> _gen_ep03_all.err.log
echo [%date% %time%] ==== R2V DONE (exit=%errorlevel%) ==== >> _gen_ep03_all.log

echo [%date% %time%] ==== START T2V (14 shots) ==== >> _gen_ep03_all.log
python -u scripts\gen_ep03_h3_t2v.py --skip-existing --wait >> _gen_ep03_all.log 2>> _gen_ep03_all.err.log
echo [%date% %time%] ==== T2V DONE (exit=%errorlevel%) ==== >> _gen_ep03_all.log

echo [%date% %time%] ==== ALL DONE ==== >> _gen_ep03_all.log
