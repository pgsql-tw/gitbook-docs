// Serialized into a read-only page probe. Indices preserve ownership even when
// identical prose occurs in several sections; no source-specific IDs are guessed.
export function sectionSnapshots(ranges) {
  const heading = 'h1,h2,h3,h4,h5,h6';
  const paragraphs = [...document.querySelectorAll('main p')];
  const elements = {
    allCodeTexts: [...document.querySelectorAll('main pre')],
    tableRows: [...document.querySelectorAll('main tr,main [role="row"]')],
    rootParagraphs: paragraphs.filter(e => !e.closest('pre,li')),
    outsideCodeParagraphs: paragraphs.filter(e => !e.closest('pre')),
    headingIds: [...document.querySelectorAll('main ' + heading.split(',').join(',main '))],
    listBlocks: [...document.querySelectorAll('main ul,main ol')].filter(e => !e.closest('nav')),
  };
  const value = (field, e) => {
    if (field === 'headingIds') return { id: e.id, text: e.innerText };
    if (field === 'tableRows') return [...e.querySelectorAll('td,th,[role="cell"],[role="columnheader"]')]
      .filter(c => c.closest('tr,[role="row"]') === e).map(c => c.innerText);
    if (field === 'listBlocks') {
      const text = n => n.nodeType === 3 ? n.textContent : ['UL', 'OL'].includes(n.tagName) ? '' :
        Array.from(n.childNodes).map(text).join('') + (['P', 'DIV', 'BR'].includes(n.tagName) ? ' ' : '');
      let depth = 1;
      for (let a = e.parentElement.closest('ul,ol'); a && a.closest('main'); a = a.parentElement.closest('ul,ol')) depth++;
      return { tag: e.tagName.toLowerCase(), depth, items: [...e.children].filter(n => n.tagName === 'LI').map(text) };
    }
    return e.innerText;
  };
  return ranges.map(spec => {
    const starts = [...document.querySelectorAll('main [id]')].filter(e => e.id === spec.start);
    const ends = spec.end ? [...document.querySelectorAll('main [id]')].filter(e => e.id === spec.end) :
      paragraphs.filter(e => !e.closest('pre,li,table,[role="table"]') && e.innerText.startsWith(spec.endParagraphPrefix));
    const start = starts[0]?.closest(heading) ?? starts[0], end = ends[0]?.closest(heading) ?? ends[0];
    const result = { name: spec.name, startCount: starts.length, endCount: ends.length,
      valid: starts.length === 1 && ends.length === 1 && !!(start.compareDocumentPosition(end) & Node.DOCUMENT_POSITION_FOLLOWING),
      indices: {}, fields: {} };
    if (!result.valid) return result;
    const within = e => (start === e || !!(start.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING)) &&
      !!(e.compareDocumentPosition(end) & Node.DOCUMENT_POSITION_FOLLOWING);
    for (const [field, nodes] of Object.entries(elements)) {
      result.indices[field] = nodes.map((e, i) => within(e) ? i : -1).filter(i => i >= 0);
      result.fields[field] = result.indices[field].map(i => value(field, nodes[i]));
    }
    return result;
  });
}
