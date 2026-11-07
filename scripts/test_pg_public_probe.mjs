import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { spawn } from 'node:child_process';
import { atomicJson, readJson, validateBundle } from './pg_public_probe_helpers.mjs';

const root = path.resolve('outputs/pg-tools-hardening');
await fs.mkdir(root, { recursive: true });
const work = await fs.mkdtemp(path.join(root, 'fixture-'));
const bundleBase = { origin: 'http://127.0.0.1', major: 19, source_commit: 'local-fixture',
  cases: [{ name: 'a', path: '/19/a' }] };

test('bundle rejects mixed versions, path traversal and duplicate cases', () => {
  assert.doesNotThrow(() => validateBundle(structuredClone(bundleBase)));
  for (const route of ['/18/a', '/19/../18/a', '//example.org/19/a']) {
    const b = structuredClone(bundleBase); b.cases[0].path = route;
    assert.throws(() => validateBundle(b));
  }
  const b = structuredClone(bundleBase); b.cases.push(b.cases[0]);
  assert.throws(() => validateBundle(b), /duplicate/);
  const bad = structuredClone(bundleBase); bad.cases[0].narrow = 'false';
  assert.throws(() => validateBundle(bad), /boolean/);
});

test('atomic progress JSON is always complete while it changes', async () => {
  const file = path.join(work, 'progress.json');
  await atomicJson(file, { sequence: 0, results: ['完整內容'] });
  let stop = false;
  const reader = (async () => {
    while (!stop) {
      const value = await readJson(file);
      assert.deepEqual(value.results, ['完整內容']);
      await new Promise(resolve => setTimeout(resolve, 1)); // Polling, not an unbounded handle-opening spin.
    }
  })();
  try { for (let sequence = 1; sequence <= 25; sequence++) await atomicJson(file, { sequence, results: ['完整內容'] }); }
  finally { stop = true; await reader; }
});

test('persistent Windows sharing errors are bounded and preserve the previous result', async () => {
  const file = path.join(work, 'busy.json');
  await atomicJson(file, { status: 'running', results: [1] });
  const rename = fs.rename; let attempts = 0;
  fs.rename = async () => { attempts++; throw Object.assign(Error('busy'), { code: 'EPERM' }); };
  try { await assert.rejects(atomicJson(file, { status: 'complete' }), /busy/); }
  finally { fs.rename = rename; }
  assert.equal(attempts, 6);
  assert.deepEqual(await readJson(file), { status: 'running', results: [1] });
});

test('malformed JSON remains an explicit error', async () => {
  const file = path.join(work, 'corrupt.json'); await fs.writeFile(file, '{broken');
  await assert.rejects(readJson(file), SyntaxError);
  assert.equal(await fs.readFile(file, 'utf8'), '{broken');
});

function run(args) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ['scripts/pg_public_probe.mjs', ...args], { windowsHide: true });
    let stdout = '', stderr = '';
    child.stdout.on('data', x => { stdout += x; }); child.stderr.on('data', x => { stderr += x; });
    child.on('error', reject); child.on('close', code => resolve({ code, stdout, stderr }));
  });
}

test('real Chrome selects heading, body, table and compatibility links on major 19', async t => {
  const candidates = [process.env.PG_CHROME_PATH, 'C:/Program Files/Google/Chrome/Application/chrome.exe', '/usr/bin/google-chrome', '/usr/bin/chromium'].filter(Boolean);
  let chromePath;
  for (const p of candidates) { try { await fs.access(p); chromePath = p; break; } catch {} }
  if (!chromePath) { t.skip('Installed Chrome unavailable'); return; }
  const start = `<!doctype html><meta charset="utf-8"><style>body{margin:20px} pre{white-space:pre-wrap}</style><main>
    <h2 id="root">Root <a href="#root">#</a></h2><a href="/19/child#dest">正文引用</a>
    <table><tr><td><a href="/19/child#dest">表內引用</a></td></tr></table>
    <p>完整內容請見 <a href="/19/child#dest">子頁</a></p><pre>  SELECT 19;\n</pre>
    </main>`;
  const server = http.createServer((request, response) => {
    response.setHeader('Content-Type', 'text/html; charset=utf-8');
    response.end(request.url.startsWith('/19/child') ? '<main><h2 id="dest">Child</h2><p>本文</p></main>' : start);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  try {
    const origin = `http://127.0.0.1:${server.address().port}`;
    const cases = [];
    for (const narrow of [false, true]) {
      const suffix = narrow ? '-narrow' : '';
      cases.push({ name: 'heading' + suffix, path: '/19/start', narrow,
        expected: { allCodeTexts: ['  SELECT 19;\n'], tableRows: [['表內引用']] },
        batchTargets: [{ anchor: 'root', kind: 'heading' }] });
      for (const kind of ['body', 'table', 'compatibility']) cases.push({ name: kind + suffix, path: '/19/start', narrow,
        expected: { allCodeTexts: ['  SELECT 19;\n'], tableRows: [['表內引用']] },
        travel: { path: '/19/child', anchor: 'dest', kind, ...(kind === 'compatibility' ? { paragraphPrefix: '完整內容請見' } : {}) } });
    }
    const bundle = { origin, major: 19, source_commit: 'local-fixture', chromePath, settleMs: 250, clickSettleMs: 100, travelSettleMs: 250, cases };
    const config = path.join(work, 'bundle.json'), out = path.join(work, 'browser');
    await atomicJson(config, bundle);
    const result = await run(['--bundle', config, '--out', out, '--all']);
    assert.equal(result.code, 0, result.stderr);
    const records = JSON.parse(await fs.readFile(path.join(out, 'browser-checks.json'), 'utf8'));
    assert.equal(records.status, 'complete'); assert.equal(records.results.length, 8);
    for (const record of records.results) {
      const name = record.screenshot;
      if (name.startsWith('heading')) { assert.equal(record.batchJumps[0].inHeading, true); assert.equal(record.batchJumps[0].clicked, true); }
      else { assert.equal(record.travel.clicked, true); assert.equal(record.travel.inHeading, false); assert.equal(record.travelArrival.count, 1); }
      if (name.startsWith('table')) assert.equal(record.travel.inTable, true);
      if (name.startsWith('compatibility')) assert.match(record.travel.paragraphText, /^完整內容請見/);
    }
    const saved = await fs.readFile(path.join(out, 'browser-checks.json'));
    const duplicate = await run(['--bundle', config, '--out', out, '--all']);
    assert.notEqual(duplicate.code, 0); assert.match(duplicate.stderr, /retain previous evidence/);
    assert.deepEqual(await fs.readFile(path.join(out, 'browser-checks.json')), saved);
    console.log(`FIXTURE_BUNDLE=${config}`);
    console.log(`FIXTURE_RESULTS=${path.join(out, 'browser-checks.json')}`);
  } finally { await new Promise(resolve => server.close(resolve)); }
});

test('launch failure persists failed status and retains provenance', async () => {
  const config = path.join(work, 'failure.json'), out = path.join(work, 'failed');
  await atomicJson(config, { ...bundleBase, chromePath: path.join(work, 'missing-chrome.exe') });
  const result = await run(['--bundle', config, '--out', out, '--all']);
  assert.notEqual(result.code, 0);
  const report = JSON.parse(await fs.readFile(path.join(out, 'browser-checks.json'), 'utf8'));
  assert.equal(report.status, 'failed'); assert.equal(report.source_commit, 'local-fixture');
  assert.equal(report.results.length, 0);
});
