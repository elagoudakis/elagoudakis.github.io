/* Deep zoom viewer built on OpenSeadragon (self-hosted, assets/js/lib). */
(function () {
  'use strict';
  if (!window.OpenSeadragon) return;
  document.querySelectorAll('[data-zoom]').forEach(function (fig) {
    var el = fig.querySelector('[data-viewer]');
    var preview = fig.querySelector('[data-preview]');
    var controls = fig.querySelector('[data-controls]');
    var viewer = OpenSeadragon({
      element: el,
      tileSources: fig.getAttribute('data-dzi'),
      showNavigationControl: false,   // our own buttons below
      gestureSettingsMouse: { scrollToZoom: false, clickToZoom: false, dblClickToZoom: true },
      gestureSettingsTouch: { pinchToZoom: true, dblClickToZoom: true },
      visibilityRatio: 1,
      constrainDuringPan: true,
      maxZoomPixelRatio: 2,
      animationTime: 0.6,
      crossOriginPolicy: false
    });
    viewer.addHandler('open', function () {
      fig.classList.add('is-ready');
      if (preview) preview.setAttribute('aria-hidden', 'true');
      controls.hidden = false;
    });
    viewer.addHandler('open-failed', function () { fig.classList.remove('is-ready'); });
    controls.addEventListener('click', function (e) {
      var b = e.target.closest('[data-act]');
      if (!b) return;
      var vp = viewer.viewport, act = b.getAttribute('data-act');
      if (act === 'in') vp.zoomBy(1.6);
      if (act === 'out') vp.zoomBy(1 / 1.6);
      if (act === 'home') vp.goHome();
      if (act === 'full') viewer.setFullScreen(!viewer.isFullPage());
      vp.applyConstraints();
    });
  });
})();
