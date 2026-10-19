/* Before/after swipe: the range input drives the --pos custom property. */
(function () {
  'use strict';
  document.querySelectorAll('[data-compare]').forEach(function (fig) {
    var range = fig.querySelector('.compare-range');
    if (!range) return;
    fig.classList.add('is-ready');
    var update = function () { fig.style.setProperty('--pos', range.value + '%'); };
    range.addEventListener('input', update);
    update();
  });
})();
