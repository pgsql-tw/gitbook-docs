// Serialized into the browser by pg_public_probe.mjs; keep this self-contained.
export async function sidebar(paths) {
  const links = [...document.querySelectorAll('a[href]')].filter(a =>
    !a.closest('main') && paths.includes(new URL(a.href).pathname));
  const result = [];
  for (const a of links) {
    const initial = a.getBoundingClientRect();
    // Reveal each left sidebar item independently. Centering a distant child
    // can legitimately scroll its parent outside the sidebar's viewport.
    const reveal = initial.width > 0 && initial.height > 0 && initial.left < 320;
    if (reveal) {
      a.scrollIntoView({ block: 'center', inline: 'nearest', behavior: 'instant' });
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    }
    const r = a.getBoundingClientRect();
    let top = Math.max(0, r.top), bottom = Math.min(innerHeight, r.bottom);
    let left = Math.max(0, r.left), right = Math.min(innerWidth, r.right);
    for (let p = a.parentElement; p; p = p.parentElement) {
      const style = getComputedStyle(p), box = p.getBoundingClientRect();
      if (/(auto|scroll|hidden|clip)/.test(style.overflowY)) {
        top = Math.max(top, box.top); bottom = Math.min(bottom, box.bottom);
      }
      if (/(auto|scroll|hidden|clip)/.test(style.overflowX)) {
        left = Math.max(left, box.left); right = Math.min(right, box.right);
      }
    }
    const walker = document.createTreeWalker(a, NodeFilter.SHOW_TEXT);
    let n; while ((n = walker.nextNode()) && !n.textContent.trim()) {}
    let textX = null;
    if (n) { const range = document.createRange(); range.selectNodeContents(n); textX = range.getBoundingClientRect().left; }
    result.push({ path: new URL(a.href).pathname, text: a.innerText, x: r.left, textX,
      visible: r.width > 0 && r.height > 0 && bottom > top && right > left,
      measurement: reveal ? 'individually_revealed' : 'unscrolled',
      top: r.top, bottom: r.bottom });
  }
  return result;
}
