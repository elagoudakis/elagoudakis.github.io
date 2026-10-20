/* DScape site script: theme toggle, mission filters, copy link, archive tag filter. */
(function () {
  'use strict';

  // Retire the old Chirpy service worker and its offline cache.
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(function (regs) {
      regs.forEach(function (r) { r.unregister(); });
    });
    if (window.caches) caches.keys().then(function (ks) { ks.forEach(function (k) { caches.delete(k); }); });
  }

  // Theme toggle (light is the default).
  var root = document.documentElement;
  var toggle = document.querySelector('[data-theme-toggle]');
  function syncToggle() {
    if (toggle) toggle.setAttribute('aria-pressed', root.getAttribute('data-theme') === 'dark' ? 'true' : 'false');
  }
  syncToggle();
  if (toggle) toggle.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
    syncToggle();
  });

  // Mission filters on the homepage (the grid shows everything without JS).
  var filters = document.querySelector('[data-filters]');
  var grid = document.querySelector('[data-grid]');
  if (filters && grid) {
    filters.hidden = false;
    var empty = document.querySelector('[data-empty]');
    filters.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-filter]');
      if (!btn) return;
      var value = btn.getAttribute('data-filter');
      filters.querySelectorAll('[data-filter]').forEach(function (b) {
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
      var shown = 0;
      grid.querySelectorAll('[data-mission]').forEach(function (tile) {
        var match = value === 'all' || tile.getAttribute('data-mission') === value;
        tile.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    });
  }

  // Copy link button on posts.
  document.querySelectorAll('[data-copy-link]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var done = function () { btn.textContent = 'Link copied'; setTimeout(function () { btn.textContent = 'Copy link'; }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done, function () {});
    });
  });

  // Looping animations: autoplay (muted) unless the reader prefers reduced motion.
  var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('video[data-autoplay]').forEach(function (v) {
    if (calm) return;
    var p = v.play(); if (p && p.catch) p.catch(function () {});
  });

  // Archive: ?tag=fire shows only posts with that tag.
  var note = document.querySelector('[data-tag-note]');
  if (note) {
    var tag = new URLSearchParams(location.search).get('tag');
    if (tag) {
      tag = tag.toLowerCase();
      note.hidden = false;
      note.querySelector('[data-tag-name]').textContent = tag;
      document.querySelectorAll('[data-tags]').forEach(function (li) {
        li.hidden = li.getAttribute('data-tags').split(' ').indexOf(tag) === -1;
      });
      document.querySelectorAll('[data-year]').forEach(function (y) {
        y.hidden = !y.querySelector('li:not([hidden])');
      });
    }
  }
})();
