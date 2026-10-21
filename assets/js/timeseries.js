/* Time-series player: shows one frame at a time, with play/pause, step buttons or a slider. */
(function () {
  'use strict';
  document.querySelectorAll('[data-timeseries]').forEach(function (fig) {
    var imgs = Array.prototype.slice.call(fig.querySelectorAll('.timeseries-stage img'));
    if (imgs.length < 2) return;
    var controls = fig.querySelector('[data-controls]');
    var play = fig.querySelector('[data-play]');
    var steps = Array.prototype.slice.call(fig.querySelectorAll('[data-step]'));
    var range = fig.querySelector('[data-range]');
    var output = fig.querySelector('[data-output]');
    var badge = fig.querySelector('[data-badge]');
    var live = fig.querySelector('[data-live]');
    var interval = parseInt(fig.getAttribute('data-interval'), 10) || 1500;
    var i = parseInt(fig.getAttribute('data-start'), 10) || 0;
    var timer = null;

    controls.hidden = false;
    // Preload the other frames once the page has finished loading, so stepping is instant
    // without competing with the main image for bandwidth.
    var preload = function () { imgs.forEach(function (im) { im.loading = 'eager'; }); };
    if (document.readyState === 'complete') setTimeout(preload, 300);
    else window.addEventListener('load', function () { setTimeout(preload, 300); });

    function show(n, announce) {
      i = (n + imgs.length) % imgs.length;
      imgs.forEach(function (im, k) { im.hidden = k !== i; });
      var label = imgs[i].getAttribute('data-label');
      if (badge) badge.textContent = label;
      steps.forEach(function (b, k) { b.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
      if (range) range.value = i;
      if (output) output.textContent = label;
      if (announce && live) live.textContent = label;
    }
    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
      fig.classList.remove('is-playing');
      play.setAttribute('aria-label', 'Play');
    }
    function start() {
      stop();
      timer = setInterval(function () { show(i + 1, false); }, interval);
      fig.classList.add('is-playing');
      play.setAttribute('aria-label', 'Pause');
    }
    play.addEventListener('click', function () { timer ? stop() : start(); });
    steps.forEach(function (b, k) { b.addEventListener('click', function () { stop(); show(k, true); }); });
    if (range) range.addEventListener('input', function () { stop(); show(parseInt(range.value, 10), true); });
    fig.addEventListener('keydown', function (e) {
      if (e.target === range) return;
      if (e.key === 'ArrowRight') { stop(); show(i + 1, true); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { stop(); show(i - 1, true); e.preventDefault(); }
    });
    show(i, false);
  });
})();
