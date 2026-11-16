// Local viewport setup/measurement only. No DOM, test actions, or page JS evaluation.
const width = Number(process.argv[2] || 0);
const height = Number(process.argv[3] || 0);
const pages = await (await fetch('http://127.0.0.1:18381/json')).json();
const target = pages.find(p => p.type === 'page' && p.url.startsWith('http://127.0.0.1:18380/'));
if (!target) throw new Error('Evaluation page target missing');
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {ws.addEventListener('open', resolve, {once:true}); ws.addEventListener('error', reject, {once:true});});
let id = 0;
async function command(method, params = {}) {
  const requestId = ++id;
  return await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('CDP environment setup timeout')), 5000);
    function receive(event) {
      const data = JSON.parse(event.data);
      if (data.id !== requestId) return;
      clearTimeout(timeout);ws.removeEventListener('message', receive);
      if (data.error) reject(new Error(data.error.message)); else resolve(data.result);
    }
    ws.addEventListener('message', receive);ws.send(JSON.stringify({id:requestId,method,params}));
  });
}
try {
  if (width) await command('Emulation.setDeviceMetricsOverride', {width,height,deviceScaleFactor:1,mobile:false});
  const metrics = await command('Page.getLayoutMetrics');
  console.log(JSON.stringify({viewport:metrics.cssLayoutViewport,visualViewport:metrics.cssVisualViewport,
    emulated:!!width,requestedViewport:width?{width,height}:null,
    measurementNote:'CDP layout clientWidth excludes the vertical scrollbar; the requested emulation width includes it.'}));
  // Device overrides belong to this CDP session. Keep it alive until the native
  // browser owner closes stdin; do not run task actions or inspect the DOM.
  if (process.argv.includes('--keep-alive')) {
    await new Promise(resolve => {process.stdin.once('end',resolve);process.stdin.resume();});
  }
} finally {ws.close();}
