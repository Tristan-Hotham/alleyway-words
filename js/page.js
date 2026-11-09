/* Ginnel, snicket or twitten? Every named alley in the UK coloured by the word in its name, on a plain OpenFreeMap
 * Positron base map, with the commonest regional word in each 20 km hexagon. Dr Tristan Hotham, Independent researcher,
 * 2026. MIT licence. */
(function () {
  'use strict';
  const qs = new URLSearchParams(location.search);
  const STYLE = 'https://tiles.openfreemap.org/styles/positron';
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const norm = s => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const small = matchMedia('(max-width:800px)').matches;
  const START = small ? [[-7.4, 50.0], [1.8, 58.8]] : [[-8.2, 49.9], [2.0, 58.9]];
  let map = null, D = null, PL = null, cur = qs.get('word') || 'all', popup = null;

  document.getElementById('theme').addEventListener('click', () => {
    const r = document.documentElement, dark = r.dataset.theme ? r.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    r.dataset.theme = dark ? 'light' : 'dark';
  });
  const ct = document.getElementById('cartouche');
  const fold = f => ct.classList.toggle('folded', f);
  if (small) fold(true);
  document.getElementById('ctToggle').addEventListener('click', () => fold(!ct.classList.contains('folded')));
  document.getElementById('ctFold').addEventListener('click', () => fold(true));

  function showPopup(r, ll) {
    const w = D.words[r[2]];
    let h = `<b class="t">${esc(r[3])}</b><div class="nt">${esc(r[5] ? r[5] + ', ' : '')}${esc(r[4])}</div><table>`;
    h += `<tr><td>Word</td><td><span class="sw" style="background:${w[2]}"></span><b>${esc(w[1])}</b></td></tr>`;
    h += `<tr><td>${w[3] === 'regional' ? 'Usually' : 'Kind'}</td><td>${esc(w[4])}</td></tr>`;
    h += `<tr><td>Mapped as</td><td>${esc(r[9])}${r[7] > 1 ? ` (${r[7]} pieces joined)` : ''}</td></tr>`;
    h += `<tr><td>In the data</td><td>${w[5].toLocaleString('en-GB')} named ${esc(w[1].split(' ')[0])}${w[5] === 1 ? '' : 's'} in the UK</td></tr></table>`;
    h += `<p class="nt">The street name as mapped in OpenStreetMap: an official or signposted name, not a record of everyday speech. The dot marks where the way begins.</p>`;
    h += `<div class="lk"><a href="https://www.openstreetmap.org/way/${r[6]}" target="_blank" rel="noopener">OpenStreetMap way ${r[6]}</a></div>`;
    if (popup) popup.remove();
    popup = new maplibregl.Popup({ maxWidth: '320px', offset: 8 }).setLngLat(ll).setHTML(h).addTo(map);
  }

  function apply() {
    const wi = D.words.findIndex(w => w[0] === cur);
    const showGen = document.getElementById('ckGen').checked, showReg = document.getElementById('ckReg').checked;
    const f = ['all'];
    if (cur !== 'all') f.push(['==', ['get', 'w'], wi]);
    else {
      if (!showGen) f.push(['==', ['get', 'k'], 1]);
      if (!showReg) f.push(['==', ['get', 'k'], 0]);
    }
    ['al', 'all'].forEach(id => map.setFilter(id, f));
    map.setLayoutProperty('hx', 'visibility', document.getElementById('ckHex').checked ? 'visible' : 'none');
    map.setLayoutProperty('hxl', 'visibility', document.getElementById('ckHex').checked ? 'visible' : 'none');
    map.setLayoutProperty('all', 'visibility', document.getElementById('ckLab').checked ? 'visible' : 'none');
    document.querySelectorAll('.chip[data-w]').forEach(b => b.setAttribute('aria-pressed', b.dataset.w === cur));
    const k = document.getElementById('key');
    if (cur === 'all') {
      k.innerHTML = '<b>Word in the name</b>' + D.words.filter(w => w[5] > 0 && w[3] === 'regional').map(w =>
        `<div class="row"><i class="dot" style="background:${w[2]}"></i>${esc(w[1])} <span class="nt">${w[5].toLocaleString('en-GB')}</span></div>`).join('') +
        `<div class="row"><i class="dot" style="background:#94A3B8"></i>alley, passage, steps... <span class="nt">general</span></div>`;
    } else {
      const w = D.words[wi];
      k.innerHTML = `<b>${esc(w[1])}</b><div class="row"><i class="dot" style="background:${w[2]}"></i>${w[5].toLocaleString('en-GB')} named in the UK</div><div class="row nt">${w[3] === 'regional' ? 'Usually: ' : ''}${esc(w[4])}</div>`;
    }
    const u = new URL(location.href); cur === 'all' ? u.searchParams.delete('word') : u.searchParams.set('word', cur); history.replaceState(null, '', u);
  }

  function setupLayers() {
    const before = (map.getStyle().layers.find(l => l.type === 'symbol') || {}).id;
    const feats = D.rows.map((r, i) => ({ type: 'Feature', properties: { i, w: r[2], k: D.words[r[2]][3] === 'regional' ? 1 : 0, n: r[3] }, geometry: { type: 'Point', coordinates: [r[0], r[1]] } }));
    map.addSource('hx', { type: 'geojson', data: 'data/hexagons.geojson' });
    const colours = ['match', ['get', 'top'], ...D.words.flatMap(w => [w[0], w[2]]), '#CCCCCC'];
    map.addLayer({ id: 'hx', type: 'fill', source: 'hx', filter: ['>=', ['get', 'regional'], 3], layout: { visibility: 'none' },
      paint: { 'fill-color': colours, 'fill-opacity': ['interpolate', ['linear'], ['zoom'], 5, 0.55, 10, 0.25] } }, before);
    map.addLayer({ id: 'hxl', type: 'line', source: 'hx', layout: { visibility: 'none' }, paint: { 'line-color': '#9C8656', 'line-width': 0.6, 'line-opacity': 0.7 } }, before);
    map.addSource('al', { type: 'geojson', data: { type: 'FeatureCollection', features: feats }, attribution: 'Alleys: <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors (ODbL)' });
    map.addLayer({ id: 'al', type: 'circle', source: 'al', layout: { 'circle-sort-key': ['get', 'k'] }, paint: {
      'circle-radius': ['interpolate', ['linear'], ['zoom'], 4, ['case', ['==', ['get', 'k'], 1], 3.4, 3], 8, ['case', ['==', ['get', 'k'], 1], 5, 4], 13, 8],
      'circle-color': ['case', ['==', ['get', 'k'], 1], ['match', ['get', 'w'], ...D.words.flatMap((w, i) => [i, w[2]]), '#999'], '#94A3B8'],
      'circle-stroke-color': '#FFFFFF', 'circle-stroke-width': ['interpolate', ['linear'], ['zoom'], 4, 0.6, 10, 1.5] } });
    map.addLayer({ id: 'all', type: 'symbol', source: 'al', minzoom: 12,
      layout: { 'text-field': ['get', 'n'], 'text-font': ['Noto Sans Italic'], 'text-size': 12, 'text-offset': [0, 0.9], 'text-anchor': 'top', 'text-optional': true },
      paint: { 'text-color': '#2B2119', 'text-halo-color': 'rgba(255,255,255,0.95)', 'text-halo-width': 1.6 } });
    map.on('click', e => {
      const f = map.queryRenderedFeatures([[e.point.x - 6, e.point.y - 6], [e.point.x + 6, e.point.y + 6]], { layers: ['al'] })[0];
      if (f) { showPopup(D.rows[f.properties.i], f.geometry.coordinates); return; }
      if (map.getLayoutProperty('hx', 'visibility') === 'visible') {
        const h = map.queryRenderedFeatures(e.point, { layers: ['hx'] })[0];
        if (h) { const p = h.properties; if (popup) popup.remove();
          popup = new maplibregl.Popup({ maxWidth: '300px' }).setLngLat(e.lngLat).setHTML(`<b class="t">20 km hexagon</b><div>${p.top === 'tie' ? 'A tie between two words' : 'Commonest regional word: <b>' + esc(p.top) + '</b>'}</div><div class="nt">${esc(p.words)}</div><div class="nt">Named alleys in OpenStreetMap (ODbL).</div>`).addTo(map); }
      }
    });
    ['al', 'hx'].forEach(id => { map.on('mouseenter', id, () => map.getCanvas().style.cursor = 'pointer'); map.on('mouseleave', id, () => map.getCanvas().style.cursor = ''); });
    const lp = document.getElementById('lp'), btn = document.getElementById('lyrBtn');
    btn.addEventListener('click', e => { e.stopPropagation(); const o = lp.classList.toggle('open'); btn.setAttribute('aria-expanded', o); });
    document.addEventListener('click', e => { if (!lp.contains(e.target) && e.target !== btn) { lp.classList.remove('open'); btn.setAttribute('aria-expanded', false); } });
    ['ckGen', 'ckReg', 'ckHex', 'ckLab'].forEach(id => document.getElementById(id).addEventListener('change', apply));
    document.querySelectorAll('.chip[data-w]').forEach(b => b.addEventListener('click', () => { cur = b.dataset.w; apply(); }));
    document.querySelectorAll('a[data-w]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); cur = a.dataset.w; apply(); document.getElementById('mapWrap').scrollIntoView({ behavior: 'smooth' }); }));
    if (qs.get('hex')) document.getElementById('ckHex').checked = true;
    apply();
  }

  function setupSearch() {
    const q = document.getElementById('q'), sug = document.getElementById('sug');
    let items = [], k = -1;
    const alleys = D.rows.map(r => ({ t: 'a', name: r[3], sub: (r[5] || r[4]), lon: r[0], lat: r[1], r }));
    const towns = PL.places.map(p => ({ t: 'p', name: p[0], sub: 'town', lon: p[1], lat: p[2] }));
    const show = () => {
      const v = norm(q.value.trim()); sug.innerHTML = ''; k = -1;
      if (v.length < 2) { sug.style.display = 'none'; return; }
      const m = arr => arr.filter(p => norm(p.name).startsWith(v)).concat(arr.filter(p => !norm(p.name).startsWith(v) && v.length > 2 && norm(p.name).includes(v)));
      items = m(towns).slice(0, 5).concat(m(alleys).slice(0, 9));
      items.forEach((p, i) => { const li = document.createElement('li'); li.setAttribute('role', 'option');
        li.innerHTML = `${esc(p.name)} <span>${esc(p.sub)}</span>`;
        li.addEventListener('mousedown', e => { e.preventDefault(); pick(i); }); sug.appendChild(li); });
      sug.style.display = items.length ? 'block' : 'none';
    };
    const pick = i => {
      const p = items[i]; if (!p) return; q.value = p.name; sug.style.display = 'none'; fold(true);
      map.flyTo({ center: [p.lon, p.lat], zoom: p.t === 'a' ? 15 : 12.5, duration: 1300 });
      if (p.t === 'a') map.once('moveend', () => showPopup(p.r, [p.lon, p.lat]));
    };
    q.addEventListener('input', show);
    q.addEventListener('keydown', e => {
      const lis = [...sug.children];
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); k = Math.max(0, Math.min(lis.length - 1, k + (e.key === 'ArrowDown' ? 1 : -1))); lis.forEach((l, i) => l.setAttribute('aria-selected', i === k)); }
      else if (e.key === 'Enter') { e.preventDefault(); if (!items.length) show(); pick(k < 0 ? 0 : k); }
      else if (e.key === 'Escape') sug.style.display = 'none';
    });
    q.addEventListener('blur', () => setTimeout(() => sug.style.display = 'none', 150));
  }

  Promise.all([fetch('data/alleys.json').then(r => r.json()), fetch('data/places.json').then(r => r.json())]).then(([d, p]) => {
    D = d; PL = p;
    const at = (qs.get('at') || '').split(',').map(Number);
    const mo = at.length === 3 && at.every(isFinite) ? { center: [at[1], at[0]], zoom: at[2] } : { bounds: START, fitBoundsOptions: { padding: 6 } };
    const m0 = new maplibregl.Map(Object.assign({ container: 'map', style: STYLE, attributionControl: { compact: true }, maxZoom: 18 }, mo));
    return new Promise((res, rej) => { m0.once('load', () => res(m0)); m0.once('error', e => { if (!m0.loaded()) rej(e.error || e); }); });
  }).then(m => {
    map = m; window.__map = m;
    m.on('error', e => { const er = e && e.error; if (er && (er.name === 'AbortError' || /abort/i.test(er.message || ''))) return; console.error(er || e); });
    const n = document.getElementById('nojs'); if (n) n.remove();
    m.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right');
    const foldAt = () => document.querySelectorAll('.maplibregl-ctrl-attrib.maplibregl-compact').forEach(a => { a.classList.remove('maplibregl-compact-show'); a.removeAttribute('open'); });
    m.once('idle', foldAt); setTimeout(foldAt, 1500);
    setupLayers(); setupSearch();
    document.getElementById('mapWrap').addEventListener('pointerdown', e => { if (e.target.closest && e.target.closest('.cartouche,.ov,.lp,.keys,.mfs-btn,.maplibregl-ctrl,.maplibregl-popup')) return; fold(true); }, { capture: true, passive: true, once: true });
    if (qs.get('open')) { const r = D.rows.find(r => String(r[6]) === qs.get('open')); if (r) { m.jumpTo({ center: [r[0], r[1]], zoom: 15 }); showPopup(r, [r[0], r[1]]); } }
  }).catch(e => { console.error(e); const n = document.getElementById('nojs'); if (n) n.textContent = 'The map could not load: ' + e.message; });
})();
