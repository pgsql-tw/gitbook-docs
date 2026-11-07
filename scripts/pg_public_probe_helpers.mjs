import fs from 'node:fs/promises';
import path from 'node:path';
import { randomUUID } from 'node:crypto';

const queues = new Map();
async function withJsonLock(file, action) {
  // Fair in-process queue prevents a rapid poller from repeatedly taking the
  // cross-process file lock just before a waiting writer.
  const previous = queues.get(file) ?? Promise.resolve();
  let release; const turn = new Promise(resolve => { release = resolve; });
  queues.set(file, turn);
  await previous;
  try { return await withFileLock(file, action); }
  finally { release(); if (queues.get(file) === turn) queues.delete(file); }
}

async function withFileLock(file, action) {
  const lock = file + '.io.lock'; let handle;
  for (let attempt = 0; ; attempt++) {
    try { handle = await fs.open(lock, 'wx'); break; }
    catch (error) {
      if (error.code !== 'EEXIST' || attempt === 9) throw error;
      await new Promise(resolve => setTimeout(resolve, 20));
    }
  }
  try { return await action(); }
  finally { await handle.close(); await fs.unlink(lock); }
}

export async function atomicJson(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  return withJsonLock(file, async () => {
  const temporary = path.join(path.dirname(file), `.${path.basename(file)}.${randomUUID()}.tmp`);
  try {
    const handle = await fs.open(temporary, 'wx');
    try { await handle.writeFile(JSON.stringify(value, null, 2) + '\n', 'utf8'); await handle.sync(); }
    finally { await handle.close(); }
    for (let attempt = 0; ; attempt++) {
      try { await fs.rename(temporary, file); break; }
      catch (error) {
        if (!['EPERM', 'EACCES'].includes(error.code) || attempt === 5) throw error;
        await new Promise(resolve => setTimeout(resolve, 20));
      }
    }
  } finally { await fs.rm(temporary, { force: true }); }
  });
}

export async function readJson(file) {
  for (let attempt = 0; ; attempt++) {
    try { return await withJsonLock(file, async () => JSON.parse((await fs.readFile(file, 'utf8')).replace(/^\uFEFF/, ''))); }
    catch (error) {
      if (!['EPERM', 'EACCES', 'ENOENT'].includes(error.code) || attempt === 5) throw error;
      await new Promise(resolve => setTimeout(resolve, 20));
    }
  }
}

export function validateBundle(bundle) {
  const origin = new URL(bundle.origin);
  if (!['http:', 'https:'].includes(origin.protocol) || origin.origin !== bundle.origin || origin.username || origin.password)
    throw Error('Supply an HTTP(S) origin without a path or credentials');
  if (!/^[1-9][0-9]*$/.test(String(bundle.major)) || typeof bundle.source_commit !== 'string' || !bundle.source_commit.trim())
    throw Error('Supply the manual major and reviewed source_commit');
  if (!Array.isArray(bundle.cases) || !bundle.cases.length) throw Error('Empty cases');
  const names = new Set();
  const checkPath = value => {
    const u = new URL(value, bundle.origin);
    if (typeof value !== 'string' || !(value === `/${bundle.major}` || value.startsWith(`/${bundle.major}/`)) ||
        u.origin !== bundle.origin || !(u.pathname === `/${bundle.major}` || u.pathname.startsWith(`/${bundle.major}/`)))
      throw Error('Case path differs from configured origin/manual major');
  };
  const checkTarget = target => {
    if (!['heading', 'body', 'table', 'compatibility', 'any'].includes(target.kind)) throw Error('Explicit link kind required');
    if (!target.anchor || (target.kind === 'compatibility' && !target.paragraphPrefix)) throw Error('Incomplete click target');
  };
  for (const test of bundle.cases) {
    if (!/^[A-Za-z0-9][A-Za-z0-9_.-]*$/.test(test.name) || names.has(test.name)) throw Error('Invalid or duplicate case name');
    names.add(test.name); checkPath(test.path);
    if (test.narrow !== undefined && typeof test.narrow !== 'boolean') throw Error('narrow must be a boolean');
    for (const t of test.batchTargets ?? []) checkTarget(t);
    if (test.travel) {
      checkPath(test.travel.path);
      if (test.travel.kind) checkTarget(test.travel);
    }
    if (test.navTargets) { if (test.navTargets.length !== 2) throw Error('Two sidebar paths required'); test.navTargets.forEach(checkPath); }
    if (test.sectionRanges) {
      if (!Array.isArray(test.sectionRanges)) throw Error('Section ranges must be an array');
      const sections = new Set();
      for (const section of test.sectionRanges) {
        if (typeof section.name !== 'string' || !section.name || sections.has(section.name) ||
            typeof section.start !== 'string' || !section.start ||
            (!!section.end === !!section.endParagraphPrefix) ||
            (section.end && typeof section.end !== 'string') ||
            (section.endParagraphPrefix && typeof section.endParagraphPrefix !== 'string'))
          throw Error('Specify unique section names, start IDs and exactly one end boundary');
        sections.add(section.name);
      }
    }
  }
  return bundle;
}

// Serialized into the inspected page. DOM context is recorded rather than inferred
// from a particular translated heading ID such as zhu-yi.
export function clickTarget(target) {
  const heading = 'h1,h2,h3,h4,h5,h6';
  const links = [...document.querySelectorAll('main a[href]')].filter(a => {
    try {
      const u = new URL(a.href);
      if (u.origin !== location.origin || u.pathname !== (target.path ?? location.pathname) ||
          decodeURIComponent(u.hash.slice(1)) !== target.anchor) return false;
      const inHeading = !!a.closest(heading), inTable = !!a.closest('table,[role="table"]');
      const text = a.innerText.trim();
      if (target.kind === 'heading' && !inHeading) return false;
      if (['body', 'table', 'compatibility'].includes(target.kind) && (inHeading || !text || text === '#' || a.closest('nav'))) return false;
      if (target.kind === 'table' && !inTable) return false;
      if (target.paragraphPrefix && !a.closest('p')?.innerText.startsWith(target.paragraphPrefix)) return false;
      return true;
    } catch { return false; }
  });
  const a = target.kind === 'any' ? links.find(a => !a.closest(heading)) ?? links[0] : links[0];
  const before = location.href, href = a?.href ?? null, text = a?.innerText ?? null;
  const inTable = !!a?.closest('table,[role="table"]'), inHeading = !!a?.closest(heading);
  const paragraphText = a?.closest('p')?.innerText ?? '';
  a?.click();
  return { before, href, text, clicked: !!a, inTable, inHeading, paragraphText };
}
