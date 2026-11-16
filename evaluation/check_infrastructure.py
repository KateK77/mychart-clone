"""No-cost local browser/server rehearsal. Does not execute or score a test."""
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime,timezone
from run_native_cua import start_server,write,HERE
from native_driver import NativeBrowser

folder=HERE/'.private'/('infrastructure-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'))
setup=subprocess.run([sys.executable,str(HERE/'prepare_environment.py'),'T001',str(folder)],capture_output=True,text=True)
if setup.returncode:raise SystemExit('Infrastructure fixture preparation failed')
server=log=browser=None
result={'checked_at':datetime.now(timezone.utc).isoformat(),'paid_requests':0,'scored_tests':0}
try:
    server,log=start_server(folder)
    browser=NativeBrowser(folder,'http://127.0.0.1:18380')
    shot=browser.screenshot()
    (folder/'infrastructure-only.png').write_bytes(shot)
    result.update(server_health='ok',native_browser_foreground_verified=True,native_screenshot_bytes=len(shot))
except Exception as exc:
    result.update(error=str(exc))
    raise
finally:
    if browser:browser.close()
    if server:server.terminate();server.wait(timeout=10)
    if log:log.close()
    write(HERE/'logs/infrastructure-check.json',result)
    print(json.dumps(result))
