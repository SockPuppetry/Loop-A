import sys
import os
import string
from datetime import datetime
import subprocess
import random
import urllib.parse as url

COOKIE_FILE = "cookie"


class SwitchPrinter:
    def __init__(self, out=None, enabled=True):
        self.out = out
        self.enabled = enabled

    def __call__(self, *args, **kwargs):
        if not self.enabled:
            return
        print(*args, file=self.out)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


oprint = SwitchPrinter(sys.stdout)
dprint = SwitchPrinter(sys.stderr)
nullfile = open(os.devnull, "w")


strings = string.ascii_letters + string.digits
# Create variables
z_name = ''.join(random.choices(strings, k=random.randint(8, 17)))
z_reason = ''.join(random.choices(strings, k=random.randint(32, 65)))
dprint(z_name, z_reason)


# Get a special random number
pre_cp = subprocess.run(["curl", "https://www.wjx.top/m/21310150.aspx", "-c", COOKIE_FILE], stdout=subprocess.PIPE, stderr=nullfile)
rndnum = None
for line in pre_cp.stdout.decode("utf-8").split("\n"):
    if "rndnum" in line:
        rndnum = line.split('"')[1]
        break
print(rndnum)


# Generate the command
curl = ["curl"]
curl.append("https://www.wjx.top/joinnew/processjq.ashx?curid={curid}&starttime={starttime}&source=directphone&submittype=1&rn={rn}&t={t}".format(curid=(21310150), starttime=url.quote(datetime.now().strftime("%Y/%m/%d %H:%M:%S")), rn=rndnum, t=int(1000 * datetime.now().timestamp()), stub_rn="3663635443.41498584"))
# We're omitting the cookie here because it's too complex
#curl.append("-H")
#curl.append("cookie: " + base64.b64encode(b"\x85\x97\xf2\xd7\xdd\x13\xd4\x01\x24\x00\x00\x00" + str(uuid.uuid4().encode("ascii"))).rstrip("=") + "_IyIuyRsgETBkLigrrpc1; ")

# Cookie Beta
curl.extend(["-b", COOKIE_FILE])
#curl.extend(["-H", "cookie: .ASPXANONYMOUS=hZfy190T1AEkAAAANWQ5ZDRlMjctMDM3MC00MGMyLThkNDEtN2Y0ZGIxY2JiZjVmEZhRlGC_IyIuyRsgETBkLigrrpc1; UM_distinctid=1630190e233ef-0d740d5f8ada74-b34356b-1fa400-1630190e234ae0; CNZZDATA4478442=cnzz_eid%3D1473385925-1524739061-%26ntime%3D1524739061; Hm_lvt_21be24c80829bd7a683b2c536fcf520b=1524739663; jac21310150={}".format(rndnum.split(".")[-1])])
#LastActivityJoin=21310150,101494579661; Hm_lpvt_21be24c80829bd7a683b2c536fcf520b=1524739998

curl.extend(["-H", "origin: https://www.wjx.top", "-H", "accept-encoding: gzip, deflate, br", "-H", "accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6", "-H", "user-agent: Mozilla/5.0 (Linux; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", "-H", "content-type: application/x-www-form-urlencoded; charset=UTF-8", "-H", "accept: text/plain, */*; q=0.01", "-H", "referer: https://www.wjx.top/m/21310150.aspx", "-H", "authority: www.wjx.top", "-H", "x-requested-with: XMLHttpRequest", "-H", "dnt: 1", "--data"])
curl.append("submitdata=" + url.quote("1${name}}}2$2}}3${reason}".format(name=z_name, reason=z_reason)))
curl.append("--compressed")


# Execure cURL
oprint("Running curl:")
#oprint(" ".join(curl))
cp = subprocess.run(curl, stdout=sys.stdout, stderr=sys.stderr)
os.remove(COOKIE_FILE)
dprint("\nExecuted curl with return value {}".format(cp.returncode))
sys.exit(cp.returncode)
