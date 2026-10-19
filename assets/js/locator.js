/* Locator globe: an orthographic view centred on the post's location.
   Land: Natural Earth 1:110m (public domain), via world-atlas. */
(function () {
  'use strict';
  var figs = document.querySelectorAll('[data-locator]');
  if (!figs.length || !window.d3) return;
  var NS = 'http://www.w3.org/2000/svg';

  fetch(document.querySelector('[data-land-url]').getAttribute('data-land-url'))
    .then(function (r) { return r.json(); })
    .then(function (land) { figs.forEach(function (fig) { draw(fig, land); }); })
    .catch(function () { /* map is decorative; the location is also given as text */ });

  function el(name, attrs) {
    var e = document.createElementNS(NS, name);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }

  function draw(fig, land) {
    var lat = parseFloat(fig.getAttribute('data-lat'));
    var lon = parseFloat(fig.getAttribute('data-lon'));
    var size = 220, r = size / 2 - 2;
    var projection = d3.geoOrthographic()
      .scale(r)
      .translate([size / 2, size / 2])
      .rotate([-lon, -lat])
      .clipAngle(90)
      .precision(0.5);
    var path = d3.geoPath(projection);

    var svg = el('svg', {
      viewBox: '0 0 ' + size + ' ' + size, width: size, height: size,
      role: 'img', 'aria-label': 'Globe centred on ' + fig.getAttribute('data-name')
    });
    svg.appendChild(el('path', { d: path({ type: 'Sphere' }), class: 'globe-sphere' }));
    svg.appendChild(el('path', { d: path(d3.geoGraticule10()), class: 'globe-graticule' }));
    svg.appendChild(el('path', { d: path(land), class: 'globe-land' }));
    var c = projection([lon, lat]);
    svg.appendChild(el('circle', { cx: c[0], cy: c[1], r: 11, class: 'globe-halo' }));
    svg.appendChild(el('circle', { cx: c[0], cy: c[1], r: 4.5, class: 'globe-dot' }));
    svg.appendChild(el('path', { d: path({ type: 'Sphere' }), class: 'globe-outline' }));
    fig.querySelector('.locator-map').appendChild(svg);
  }
})();
