/* Decorative, fictional workflow. No network, telemetry or real findings. */
(function () {
  'use strict';
  const panel = document.querySelector('[data-signal-display]');
  if (!panel) return;
  const button = panel.querySelector('button');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let userPaused = false, visible = false;
  function render() {
    panel.dataset.running = String(visible && !document.hidden && !reduced.matches && !userPaused);
    button.textContent = userPaused ? 'Play animation' : 'Pause animation';
    button.hidden = reduced.matches;
  }
  button.addEventListener('click', () => { userPaused = !userPaused; render(); });
  document.addEventListener('visibilitychange', render);
  if (reduced.addEventListener) reduced.addEventListener('change', render);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; render(); }).observe(panel);
  } else { visible = true; }
  render();
})();
