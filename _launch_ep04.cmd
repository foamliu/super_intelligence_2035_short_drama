@echo off
REM 第04集《棋子》一键后台生成（固化 · 顺序：场景图 → R2V → T2V）
REM 用法: 在项目根目录执行  _launch_ep04.cmd
REM 日志: _gen_ep04_all.log（stdout）/ _gen_ep04_all.err.log（stderr）
cd /d D:\Users\Administrator\code\super_intelligence_2035_short_drama

echo [%date% %time%] ==== START SCENES (15 imgs) ==== >> _gen_ep04_all.log
py -3.10 -u scripts\gen_ep04_scenes.py --wait >> _gen_ep04_all.log 2>> _gen_ep04_all.err.log
echo [%date% %time%] ==== SCENES DONE (exit=%errorlevel%) ==== >> _gen_ep04_all.log

echo [%date% %time%] ==== START R2V (21 shots) ==== >> _gen_ep04_all.log
py -3.10 -u scripts\gen_ep04_h3_r2v.py --skip-existing --wait >> _gen_ep04_all.log 2>> _gen_ep04_all.err.log
echo [%date% %time%] ==== R2V DONE (exit=%errorlevel%) ==== >> _gen_ep04_all.log

echo [%date% %time%] ==== START T2V (34 shots) ==== >> _gen_ep04_all.log
py -3.10 -u scripts\gen_ep04_h3_t2v.py --skip-existing --wait >> _gen_ep04_all.log 2>> _gen_ep04_all.err.log
echo [%date% %time%] ==== T2V DONE (exit=%errorlevel%) ==== >> _gen_ep04_all.log

echo [%date% %time%] ==== ALL DONE ==== >> _gen_ep04_all.log
