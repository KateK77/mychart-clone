"""No-cost local browser/server rehearsal. Does not execute or score a test."""
import json
from pathlib import Path
import subprocess
import sys
import io
from PIL import Image
from datetime import datetime,timezone
from run_native_cua import start_server,write,HERE,execution_fingerprint
from native_driver import NativeBrowser

folder=HERE/'.private'/('infrastructure-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'))
setup=subprocess.run([sys.executable,str(HERE/'prepare_environment.py'),'T001',str(folder)],capture_output=True,text=True)
if setup.returncode:raise SystemExit('Infrastructure fixture preparation failed')
server=log=browser=None
result={'checked_at':datetime.now(timezone.utc).isoformat(),'paid_requests':0,'scored_tests':0,'execution_fingerprint':execution_fingerprint()}
try:
    server,log=start_server(folder)
    result['windows']=[]
    for mode,narrow in [('desktop',False),('narrow',True)]:
        browser_folder=folder/mode;browser_folder.mkdir()
        browser=NativeBrowser(browser_folder,'http://127.0.0.1:18380',narrow=narrow)
        shot=browser.screenshot()
        (browser_folder/'infrastructure-only.png').write_bytes(shot)
        pixels=Image.open(io.BytesIO(shot)).size
        probe=subprocess.run(['node',str(HERE/'browser_environment.mjs'),'0','0'],capture_output=True,text=True,timeout=15,
                             creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        if probe.returncode:raise RuntimeError('Independent viewport remeasurement failed')
        current=json.loads(probe.stdout)['viewport']
        stable=all(current[k]==browser.viewport['viewport'][k] for k in ['clientWidth','clientHeight'])
        if not stable:raise RuntimeError('Viewport changed after setup session')
        result['windows'].append({'mode':mode,'native_screenshot_pixels':pixels,'screenshot_bytes':len(shot),'viewport':browser.viewport,
                                  'viewport_confirmed_after_setup':stable})
        browser.close();browser=None
    result.update(server_health='ok',native_browser_foreground_verified=True)
    write(HERE/'.private/latest-browser-preflight.json',{'path':str(folder)})
except Exception as exc:
    result.update(error=str(exc))
    raise
finally:
    if browser:browser.close()
    if server:server.terminate();server.wait(timeout=10)
    if log:log.close()
    write(HERE/'logs/infrastructure-check.json',result)
    print(json.dumps(result))
