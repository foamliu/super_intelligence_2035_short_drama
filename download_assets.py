import urllib.request
import os
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = 'ASSETS/12_身体'
dirs = [
    f'{base}/CHARACTERS/赵淑芬',
    f'{base}/CHARACTERS/小暖',
    f'{base}/CHARACTERS/女儿',
    f'{base}/BACKGROUNDS',
    f'{base}/PROPS',
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

urls = {
    'CHARACTERS/赵淑芬/01_正面定妆.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/021784422541181b686cf77507a74aa4905f351832e6617c6b17f_0.jpeg',
    'CHARACTERS/赵淑芬/02_侧面坐姿.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/02178442255826879be1521b480472bd1aa7097703cfa201578a6_0.jpeg',
    'CHARACTERS/赵淑芬/03_手部特写.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/02178442257476342e276d595e9cfc376ad966d4ec2124649e46a_0.jpeg',
    'CHARACTERS/赵淑芬/04_近景表情.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/021784422598921ffa368fe9ac51d90198cd5026e9cf3e33cf5b4_0.jpeg',
    'CHARACTERS/小暖/01_正面全身.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/02178442262466485c9a7acb047d6dabbfa02bbf3a2b67b92fda9_0.jpeg',
    'CHARACTERS/小暖/02_侧面全身.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/021784422659110fdfd2e3c33d5b6eddad55ac385080e72a19fdd_0.jpeg',
    'CHARACTERS/小暖/03_机械臂特写.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/02178442268288764d8a6219dbbdb6281842e0590025e9211213a_0.jpeg',
    'CHARACTERS/小暖/04_指示灯特写.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/02178442269968516105250997c3183a3687369088432ad81e6c6_0.jpeg',
    'CHARACTERS/小暖/05_辫子滑触线.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/02178442272479116105250997c3183a3687369088432adf39a1f_0.jpeg',
    'BACKGROUNDS/01_卧室_晨光.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/021784422741746d619db30bd0c9858e230a26bb1693525e3210a_0.jpeg',
    'BACKGROUNDS/02_客厅_白天.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/02178442277543137079cdcc08b35ab782b1fd6e8da4cf0909c9f_0.jpeg',
    'BACKGROUNDS/03_餐厅.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/021784422793110d323cdad39964ab14a5fcc08ad1c3650c0da04_0.jpeg',
    'BACKGROUNDS/04_浴室.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/021784422808660b060a07fba38d5479db0751ac158bec591681d_0.jpeg',
    'BACKGROUNDS/05_客厅_傍晚.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/0217844228291289dea1a5de2f6b6146a54635f535da4d3839885_0.jpeg',
    'PROPS/01_天花板轨道.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/02178442284915942e276d595e9cfc376ad966d4ec21246cffadd_0.jpeg',
    'PROPS/02_进度数字界面.png': 'https://ark-content-generation-v2-cn-beijing.tos-cn-beijing.volces.com/doubao-seedream-4-5/021784422876629d619db30bd0c9858e230a26bb169352561fe31_0.jpeg',
}

for rel_path, url in urls.items():
    filepath = os.path.join(base, rel_path)
    print(f"Downloading {rel_path}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, context=ctx, timeout=30)
        data = resp.read()
        with open(filepath, "wb") as f:
            f.write(data)
        print(f"  OK: {len(data)} bytes -> {filepath}")
    except Exception as e:
        print(f"  FAIL: {e}")

print("All done!")