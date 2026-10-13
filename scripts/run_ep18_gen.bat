@echo off
rem 第18集《暖阳》全集视频生成 runner：先 R2V（32 有角色镜）后 T2V（22 无角色镜），串行避免显存争抢。
chcp 65001 >nul
cd /d D:\Users\Administrator\code\super_intelligence_2035_short_drama
echo ==================== EP18 R2V START %date% %time% ====================
D:\Python310\python.exe -u scripts\gen_ep18_h3_r2v.py --wait --skip-existing
echo ==================== EP18 R2V END   %date% %time% ====================
echo ==================== EP18 T2V START %date% %time% ====================
D:\Python310\python.exe -u scripts\gen_ep18_h3_t2v.py --wait --skip-existing
echo ==================== EP18 T2V END   %date% %time% ====================
echo ====EP18_GEN_ALL_DONE====
