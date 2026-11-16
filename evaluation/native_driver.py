"""Native Windows screenshot/input motor. No selectors, DOM reads, or scripted test steps."""
import ctypes
from ctypes import wintypes
import io
import json
from pathlib import Path
import subprocess
import time
import queue
import threading
from urllib.request import urlopen
from urllib.parse import urlsplit

class NativeBrowser:
    def __init__(self, folder, origin, narrow=False):
        if not hasattr(ctypes,'windll'): raise RuntimeError('Windows interactive desktop required')
        import pyautogui
        self.gui=pyautogui
        self.gui.FAILSAFE=True
        self.gui.PAUSE=0.12
        self.user32=ctypes.windll.user32
        self.user32.GetForegroundWindow.restype=wintypes.HWND
        self.user32.GetWindowThreadProcessId.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.DWORD)]
        self.user32.GetWindowRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)]
        self.user32.IsWindowVisible.argtypes=[wintypes.HWND]
        self.user32.SetProcessDPIAware()
        self.origin=origin
        self.folder=Path(folder)
        self.viewport_process=None
        self.profile=self.folder/'browser-profile'
        default=self.profile/'Default';default.mkdir(parents=True,exist_ok=True)
        downloads=self.folder/'downloads';downloads.mkdir(exist_ok=True)
        (default/'Preferences').write_text(json.dumps({'download':{'default_directory':str(downloads.resolve()),'prompt_for_download':False},'credentials_enable_service':False,'profile':{'password_manager_enabled':False}}),encoding='utf-8')
        candidates=[Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'),Path('C:/Program Files/Microsoft/Edge/Application/msedge.exe')]
        exe=next((p for p in candidates if p.exists()),None)
        if not exe: raise RuntimeError('Microsoft Edge executable unavailable')
        args=[str(exe),'--user-data-dir='+str(self.profile.resolve()),'--no-first-run','--no-default-browser-check',
              '--disable-background-networking','--disable-sync','--disable-extensions','--remote-debugging-port=18381',
              '--remote-debugging-address=127.0.0.1','--proxy-server=http://127.0.0.1:9','--proxy-bypass-list=127.0.0.1;localhost',
              '--force-device-scale-factor=1','--window-position=0,0','--window-size='+('500,950' if narrow else '1280,880'),origin+'/login']
        self.process=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # Opening a fresh browser is infrastructure. Login and all task actions belong to CUA.
        ready=False
        for _ in range(60):
            time.sleep(.2)
            try:
                self.activate_owned_window(500 if narrow else 1280,950 if narrow else 880)
                self.bounds();self.check_origins();ready=True;break
            except Exception: pass
        if not ready:
            self.close();raise RuntimeError('Dedicated browser did not acquire a verifiable foreground window')
        # The native window can exist before Chromium paints its first frame.
        time.sleep(3)
        try:
            # Chromium can replace its startup window during first-run initialization.
            for attempt in range(50):
                try:
                    self.activate_owned_window(500 if narrow else 1280,950 if narrow else 880)
                    self.bounds();break
                except RuntimeError:
                    if attempt==49:raise
                    time.sleep(.2)
            # Environment sizing only. No DOM reads or task actions use CDP.
            self.viewport_process=subprocess.Popen(['node',str(Path(__file__).with_name('browser_environment.mjs')),
                                '390' if narrow else '0','844' if narrow else '0','--keep-alive'],
                                stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            lines=queue.Queue()
            threading.Thread(target=lambda:lines.put(self.viewport_process.stdout.readline()),daemon=True).start()
            line=lines.get(timeout=15)
            if not line:raise RuntimeError('Browser viewport setup/measurement failed')
            self.viewport=json.loads(line)
            (self.folder/'viewport.json').write_text(json.dumps(self.viewport,indent=2),encoding='utf-8')
            if narrow:
                measured=self.viewport['viewport']
                # Layout clientWidth excludes Chromium's native vertical scrollbar.
                if self.viewport.get('requestedViewport')!={'width':390,'height':844} or not 370<=measured['clientWidth']<=390 or measured['clientHeight']!=844:
                    raise RuntimeError('Required 390x844 viewport was not established')
            time.sleep(.3)
            self.activate_owned_window(500 if narrow else 1280,950 if narrow else 880)
            self.bounds()
        except Exception:
            self.close();raise

    def activate_owned_window(self,width,height):
        """Startup environment only: restore/size/focus a window of our exact PID."""
        found=[]
        callback_type=ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
        @callback_type
        def visit(hwnd,_):
            pid=wintypes.DWORD();self.user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
            if pid.value==self.process.pid and self.user32.IsWindowVisible(hwnd):
                rect=wintypes.RECT();self.user32.GetWindowRect(hwnd,ctypes.byref(rect))
                found.append(((rect.right-rect.left)*(rect.bottom-rect.top),hwnd))
            return True
        self.user32.EnumWindows(visit,0)
        if not found:raise RuntimeError(f'Owned browser window not visible (process exit={self.process.poll()})')
        hwnd=max(found,key=lambda v:v[0])[1]
        self.user32.ShowWindow.argtypes=[wintypes.HWND,ctypes.c_int]
        self.user32.SetWindowPos.argtypes=[wintypes.HWND,wintypes.HWND,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_uint]
        self.user32.SetForegroundWindow.argtypes=[wintypes.HWND]
        self.user32.ShowWindow(hwnd,9)
        self.user32.SetWindowPos(hwnd,None,0,0,width,height,0x0040)
        self.user32.SetForegroundWindow(hwnd)

    def bounds(self):
        hwnd=self.user32.GetForegroundWindow();pid=wintypes.DWORD()
        self.user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
        if pid.value!=self.process.pid:
            raise RuntimeError('Foreground left the isolated browser; refusing desktop input/capture')
        rect=wintypes.RECT();self.user32.GetWindowRect(hwnd,ctypes.byref(rect))
        sw,sh=self.gui.size()
        work=wintypes.RECT()
        if not self.user32.SystemParametersInfoW(48,0,ctypes.byref(work),0):
            raise RuntimeError('Cannot identify desktop work area safely')
        x=max(0,work.left,rect.left);y=max(0,work.top,rect.top)
        return x,y,min(sw,work.right,rect.right)-x,min(sh,work.bottom,rect.bottom)-y

    def check_origins(self):
        # Infrastructure metadata only; never supplied to the model as a DOM observation.
        with urlopen('http://127.0.0.1:18381/json',timeout=3) as response:
            pages=json.load(response)
        for page in pages:
            if page.get('type')!='page':continue
            url=page.get('url','');parts=urlsplit(url)
            if url in {'about:blank',''} or url.startswith(('chrome://downloads','edge://downloads','chrome://print','edge://print','chrome-extension://')):continue
            if parts.scheme in {'http','https'} and parts.netloc==urlsplit(self.origin).netloc:continue
            raise RuntimeError('Browser navigated outside the evaluation origin')

    def screenshot(self):
        if self.viewport_process and self.viewport_process.poll() is not None:
            raise RuntimeError('Viewport setup session ended; refusing an unverified viewport')
        self.check_origins()
        x,y,w,h=self.bounds()
        shot=self.gui.screenshot(region=(x,y,w,h))
        stream=io.BytesIO();shot.save(stream,format='PNG')
        return stream.getvalue()

    def execute(self,action):
        self.check_origins();ox,oy,w,h=self.bounds()
        kind=action['type']
        def point(v):
            x,y=float(v['x']),float(v['y'])
            if not 0<=x<w or not 0<=y<h:raise ValueError('Action outside observed browser window')
            return ox+x,oy+y
        if kind in {'click','double_click','move'}:
            x,y=point(action)
            if kind=='move': self.gui.moveTo(x,y,.15)
            else:
                button=action.get('button','left')
                if button not in {'left','right','middle'}:raise ValueError('Unsupported mouse button')
                self.gui.click(x,y,clicks=2 if kind=='double_click' else 1,interval=.1,button=button)
        elif kind=='scroll':
            self.gui.moveTo(*point(action))
            # PyAutoGUI wheel units are detents; API scroll is a pixel-like delta.
            dy=action.get('scroll_y',0);dx=action.get('scroll_x',0)
            if dy:self.gui.scroll(-int(dy/100) or (-1 if dy>0 else 1))
            if dx:self.gui.hscroll(int(dx/100) or (1 if dx>0 else -1))
        elif kind=='type':
            text=action['text']
            if any(v in text.lower() for v in ['javascript:','file://','data:text/html','powershell','cmd.exe']):
                raise ValueError('Executable or out-of-scope input refused')
            if not text.isascii():raise ValueError('Only English/ASCII fixture input is supported in this adapter')
            self.gui.write(text,interval=.002)
        elif kind=='keypress':
            aliases={'CTRL':'ctrl','CONTROL':'ctrl','CMD':'ctrl','META':'win','ALT':'alt','SHIFT':'shift','ENTER':'enter','RETURN':'enter','ESC':'esc','ESCAPE':'esc','SPACE':'space','BACKSPACE':'backspace','TAB':'tab','ARROWUP':'up','ARROWDOWN':'down','ARROWLEFT':'left','ARROWRIGHT':'right','PAGEUP':'pageup','PAGEDOWN':'pagedown','DELETE':'delete','HOME':'home','END':'end'}
            keys=[aliases.get(k.upper(),k.lower()) for k in action['keys']]
            if 'win' in keys or 'f12' in keys or ('ctrl' in keys and 'shift' in keys and any(k in keys for k in ['i','j','c'])):
                raise ValueError('OS launcher/developer-tool shortcuts are out of scope')
            if any(k not in self.gui.KEYBOARD_KEYS for k in keys):raise ValueError('Unknown native key')
            self.gui.hotkey(*keys)
        elif kind=='drag':
            path=action['path']
            if not path:raise ValueError('Empty drag path')
            self.gui.moveTo(*point(path[0]));self.gui.mouseDown()
            try:
                for p in path[1:]:self.gui.moveTo(*point(p),duration=.1)
            finally:self.gui.mouseUp()
        elif kind=='wait':time.sleep(min(2,max(0,float(action.get('ms',1000))/1000)))
        elif kind=='screenshot':pass
        else:raise ValueError('Unsupported native computer action: '+kind)
        time.sleep(.25)

    def close(self):
        if self.viewport_process:
            if self.viewport_process.stdin:self.viewport_process.stdin.close()
            try:self.viewport_process.wait(timeout=3)
            except subprocess.TimeoutExpired:self.viewport_process.terminate();self.viewport_process.wait(timeout=3)
            for stream in [self.viewport_process.stdout,self.viewport_process.stderr]:
                if stream:stream.close()
        if self.process.poll() is None:
            # Only terminate the specific isolated browser process tree created by this adapter.
            subprocess.run(['taskkill','/PID',str(self.process.pid),'/T','/F'],capture_output=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
