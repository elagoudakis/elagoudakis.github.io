// POI Capture service worker – bump VERSION when you change any app file
const VERSION = 'poi-v4';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './leaflet.js', './leaflet.css',
  './icon-192.png', './icon-512.png', './icon-maskable-512.png'];
const TILES = 'poi-tiles';          // map tiles you have viewed
const DEFAULT_TILE_LIMIT = 750;     // ~15 MB; the app stores the user's choice in cache 'poi-settings'

self.addEventListener('install', e => { e.waitUntil(caches.open(VERSION).then(c => c.addAll(ASSETS))); self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k.startsWith('poi-v') && k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

async function tileLimit() {
  try { const r = await (await caches.open('poi-settings')).match('tile-limit'); return r ? +(await r.text()) : DEFAULT_TILE_LIMIT; }
  catch { return DEFAULT_TILE_LIMIT; }
}
let puts = 0;
async function trim(cache, limit) {
  const keys = await cache.keys();                 // oldest first
  for (let i = 0; i < keys.length - limit; i++) await cache.delete(keys[i]);
}
async function tile(req) {
  const limit = await tileLimit();
  if (limit > 0) {
    const c = await caches.open(TILES);
    const hit = await c.match(req.url);
    if (hit) return hit;
    const res = await fetch(req);
    if (res.ok && res.type !== 'opaque') { await c.put(req.url, res.clone()); if (++puts % 20 === 0) trim(c, limit); }
    return res;
  }
  return fetch(req);
}

self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  const url = new URL(r.url);
  if (url.hostname === 'tile.openstreetmap.org') { e.respondWith(tile(r)); return; }
  if (url.origin !== location.origin) return;
  if (r.mode === 'navigate') {
    // network first so updates arrive when online; cached copy when offline
    e.respondWith(fetch(r).then(res => { const c = res.clone(); caches.open(VERSION).then(x => x.put('./index.html', c)); return res; })
      .catch(() => caches.match('./index.html')));
  } else {
    e.respondWith(caches.match(r, { ignoreSearch: true }).then(hit => hit || fetch(r)));
  }
});
