// Read-only public/manual fixture probes using an isolated installed Chrome.
// Usage: node scripts/pg_public_probe.mjs --bundle FILE --out outputs/RUN --all
import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { createHash, randomUUID } from 'node:crypto';
import { atomicJson, validateBundle, clickTarget } from './pg_public_probe_helpers.mjs';
import { sectionSnapshots } from './pg_public_sections.mjs';
import { sidebar } from './pg_public_sidebar.mjs';

const args = process.argv.slice(2);
function argument(name) { const i = args.indexOf(name); if (i < 0 || !args[i + 1]) throw Error(`Missing ${name}`); return args[i + 1]; }
const raw = await fs.readFile(argument('--bundle'));
const bundle = validateBundle(JSON.parse(raw.toString('utf8').replace(/^\uFEFF/, '')));
const out = path.resolve(argument('--out')), outputs = path.resolve('outputs');
const relative = path.relative(outputs, out);
if (!relative || relative.startsWith('..') || path.isAbsolute(relative)) throw Error('Use a run directory below workspace outputs');
const requested = args.includes('--all') ? bundle.cases.map(c => c.name) : argument('--cases').split(',');
if (new Set(requested).size !== requested.length || requested.some(n => !bundle.cases.some(c => c.name === n))) throw Error('Unknown or duplicate requested cases');
await fs.mkdir(out, { recursive: true });
try { await fs.access(path.join(out, 'browser-checks.json')); throw Error('Use a new output directory; retain previous evidence'); }
catch (error) { if (error.code !== 'ENOENT') throw error; }
const run = { schema: 1, run_id: randomUUID(), status: 'running', origin: bundle.origin,
  major: String(bundle.major), source_commit: bundle.source_commit,
  bundle_sha256: createHash('sha256').update(raw).digest('hex'), cases_requested: requested,
  startedAt: new Date().toISOString(), results: [] };
const lock = path.join(out, '.probe.lock');
const handle = await fs.open(lock, 'wx');
await handle.writeFile(run.run_id); await handle.close();
const report = path.join(out, 'browser-checks.json');
const delay = ms => new Promise(r => setTimeout(r, ms));
let chrome, ws;
try {
  await atomicJson(report, run);
  const candidates = bundle.chromePath ? [bundle.chromePath] : process.env.PG_CHROME_PATH ? [process.env.PG_CHROME_PATH] :
    ['C:/Program Files/Google/Chrome/Application/chrome.exe', '/usr/bin/google-chrome', '/usr/bin/chromium'];
  let executable;
  for (const candidate of candidates) { try { await fs.access(candidate); executable = candidate; break; } catch {} }
  if (!executable) throw Error('Installed Chrome not found; set PG_CHROME_PATH');
  const profile = await fs.mkdtemp(path.join(out, 'cdp-isolated-'));
  chrome = spawn(executable, ['--headless=new', '--no-first-run', '--no-default-browser-check',
    '--disable-background-networking', '--disable-extensions', '--remote-debugging-port=0',
    `--user-data-dir=${profile}`, 'about:blank'], { windowsHide: true, stdio: 'ignore' });
  let launchError; chrome.on('error', e => { launchError = e; });
  let port;
  for (let i = 0; i < 100; i++) {
    if (launchError) throw launchError;
    try { port = (await fs.readFile(path.join(profile, 'DevToolsActivePort'), 'utf8')).trim().split('\n'); break; }
    catch { await delay(100); }
  }
  if (!port) throw Error('No isolated Chrome debugging endpoint');
  ws = new WebSocket(`ws://127.0.0.1:${port[0]}${port[1]}`);
  await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
  const waiting = new Map(); let next = 0;
  ws.onmessage = e => {
    const message = JSON.parse(e.data), pending = waiting.get(message.id);
    if (pending) { waiting.delete(message.id); clearTimeout(pending.timer); message.error ? pending.reject(Error(JSON.stringify(message.error))) : pending.resolve(message.result); }
  };
  ws.onclose = () => { for (const p of waiting.values()) { clearTimeout(p.timer); p.reject(Error('Chrome debugging connection closed')); } waiting.clear(); };
  const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    const id = ++next, timer = setTimeout(() => { waiting.delete(id); reject(Error(`CDP timeout: ${method}`)); }, 15000);
    waiting.set(id, { resolve, reject, timer });
    ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
  });
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const cmd = (method, params = {}) => send(method, params, sessionId);
  const evaluate = async expression => {
    const value = await cmd('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (value.exceptionDetails) throw Error(JSON.stringify(value.exceptionDetails));
    return value.result.value;
  };
  await cmd('Page.enable');
  for (const test of bundle.cases.filter(c => requested.includes(c.name))) {
    await cmd('Emulation.setDeviceMetricsOverride', { width: test.narrow ? 390 : 1440, height: test.narrow ? 844 : 1000, deviceScaleFactor: 1, mobile: false });
    const url = bundle.origin + test.path;
    await cmd('Page.navigate', { url });
    await delay(bundle.settleMs ?? 6500);
    const state = await evaluate(`(${snapshot.toString()})(${JSON.stringify(test)})`);
    if (test.sectionRanges) state.sections = await evaluate(`(${sectionSnapshots.toString()})(${JSON.stringify(test.sectionRanges)})`);
    if (test.inventoryAnchors) state.anchorInventory = await evaluate(`(${outline.toString()})(${JSON.stringify(test.inventoryAnchors)})`);
    state.batchJumps = [];
    const targets = test.batchTargets ?? (test.batchAnchors ?? []).map(anchor => ({ anchor, kind: test.allowHeadingLink ? 'any' : 'body' }));
    for (const target of targets) {
      await evaluate('scrollTo(0,0)');
      const clicked = await evaluate(`(${clickTarget.toString()})(${JSON.stringify(target)})`);
      await delay(bundle.clickSettleMs ?? 300);
      const arrival = await evaluate(`(${arrivalAt.toString()})(${JSON.stringify(target.anchor)})`);
      state.batchJumps.push({ ...clicked, anchor: target.anchor, idCount: arrival.count, targetTop: arrival.top, targetText: arrival.text, hash: arrival.hash, viewportHeight: arrival.viewportHeight });
    }
    if (test.targetOutline) state.targetOutline = await evaluate(`(${outline.toString()})(${JSON.stringify(test.targetOutline)})`);
    if (test.focusParagraph) state.focusedParent = await evaluate(`(()=>{const e=[...document.querySelectorAll('main p')].find(e=>!e.closest('pre,li')&&e.innerText.includes(${JSON.stringify(test.focusParagraph)}));return {exists:!!e,text:e?.innerText??null,insideList:!!e?.closest('li')};})()`);
    if (test.travel) {
      const target = { ...test.travel, kind: test.travel.kind ?? (test.travel.tableOnly ? 'table' : test.travel.paragraphPrefix ? 'compatibility' : test.travel.excludeHeading ? 'body' : 'any') };
      state.travel = await evaluate(`(${clickTarget.toString()})(${JSON.stringify(target)})`);
      await delay(bundle.travelSettleMs ?? 4000);
      state.travelArrival = await evaluate(`(${arrivalAt.toString()})(${JSON.stringify(target.anchor)})`);
    }
    if (test.navTargets) {
      state.sidebarProbe = []; state.sidebarScreenshots = [];
      for (const [index, target] of test.navTargets.entries()) {
        state.sidebarProbe.push(...await evaluate(`(${sidebar.toString()})(${JSON.stringify([target])})`));
        const filename = `${test.name}-sidebar-${index}.png`;
        const image = await cmd('Page.captureScreenshot', { format: 'png' });
        await fs.writeFile(path.join(out, filename), Buffer.from(image.data, 'base64'));
        state.sidebarScreenshots.push({ path: target, screenshot: filename });
      }
    }
    const shot = await cmd('Page.captureScreenshot', { format: 'png' });
    await fs.writeFile(path.join(out, test.name + '.png'), Buffer.from(shot.data, 'base64'));
    state.screenshot = test.name + '.png'; run.results.push(state);
    run.checkedAt = new Date().toISOString(); await atomicJson(report, run);
    console.log(JSON.stringify({ case: test.name, captured: true }));
  }
  run.status = 'complete'; run.completedAt = new Date().toISOString();
  await atomicJson(report, run);
  await send('Browser.close');
} catch (error) {
  run.status = 'failed'; run.error = String(error); run.completedAt = new Date().toISOString();
  await atomicJson(report, run); throw error;
} finally {
  ws?.close();
  if (chrome && chrome.exitCode === null) chrome.kill();
  if ((await fs.readFile(lock, 'utf8')) === run.run_id) await fs.unlink(lock);
}

function arrivalAt(anchor) {
  const all = [...document.querySelectorAll('[id]')].filter(e => e.id === anchor), e = all[0];
  return { url: location.href, hash: location.hash, count: all.length, top: e?.getBoundingClientRect().top ?? null, text: e?.innerText ?? null, viewportHeight: innerHeight };
}
function outline(ids) {
  return ids.map(id => { const all = [...document.querySelectorAll('[id]')].filter(e => e.id === id), e = all[0]; return { id, count: all.length, tag: e?.tagName ?? null, text: e?.innerText ?? null }; });
}
function snapshot(test) {
  const heading = 'h1,h2,h3,h4,h5,h6', anchor = test.anchor, es = anchor ? [...document.querySelectorAll('[id]')].filter(e => e.id === anchor) : [], e = es[0];
  const paras = [...document.querySelectorAll('main p')];
  return { url: location.href, title: document.title, initialScrollY: scrollY,
    idExists: !!e, anchorCount: es.length, anchorTop: e?.getBoundingClientRect().top ?? null,
    documentWidth: document.documentElement.scrollWidth, viewportWidth: innerWidth, viewportHeight: innerHeight,
    allCodeTexts: [...document.querySelectorAll('main pre')].map(e => e.innerText),
    tableRows: [...document.querySelectorAll('main tr,main [role="row"]')].map(e => [...e.querySelectorAll('td,th,[role="cell"],[role="columnheader"]')].filter(c => c.closest('tr,[role="row"]') === e).map(c => c.innerText)),
    rootParagraphs: paras.filter(e => !e.closest('pre,li')).map(e => e.innerText),
    outsideCodeParagraphs: paras.filter(e => !e.closest('pre')).map(e => e.innerText),
    headingIds: [...document.querySelectorAll(heading)].map(e => ({ id: e.id, text: e.innerText })),
    mainLinks: [...document.querySelectorAll('main a[href]')].map(a => ({ href: a.href, text: a.innerText, heading: !!a.closest(heading), inTable: !!a.closest('table,[role="table"]'), inNavigation: !!a.closest('nav'), paragraphText: a.closest('p')?.innerText ?? '' })),
    listBlocks: [...document.querySelectorAll('main ul,main ol')].filter(e => !e.closest('nav')).map(e => { const text = n => n.nodeType === 3 ? n.textContent : ['UL','OL'].includes(n.tagName) ? '' : Array.from(n.childNodes).map(text).join('') + (['P','DIV','BR'].includes(n.tagName) ? ' ' : ''); let depth = 1; for (let a = e.parentElement.closest('ul,ol'); a && a.closest('main'); a = a.parentElement.closest('ul,ol')) depth++; return { tag: e.tagName.toLowerCase(), depth, items: [...e.children].filter(n => n.tagName === 'LI').map(text) }; }) };
}
