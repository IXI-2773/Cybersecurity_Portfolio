/* Loop while visible; preserve manual stops and independent fixture inspection. */
(() => {
  'use strict';
  const panel = document.querySelector('[data-signal-display]');
  if (!panel) return;
  const image = panel.querySelector('[data-signal-film]');
  const button = panel.querySelector('[data-film-play]');
  if (!image || !button) return;
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  const gif = image.dataset.gif, still = image.dataset.still;
  let running = false, wanted = true, visible = !globalThis.IntersectionObserver;
  function stop() {
    running = false;
    image.src = still;
    button.textContent = media.matches ? 'Still illustration' : 'Play animation';
    button.disabled = media.matches;
    panel.dataset.filmRunning = 'false';
  }
  function play() {
    if (running || media.matches || document.hidden || !visible) return;
    panel.querySelector('[data-signal-scenario]').value = 'ten_minute_boundary';
    panel.querySelector('[data-signal-reset]').click();
    panel.dataset.visual = 'film';
    image.src = gif;
    wanted = true;
    running = true;
    button.textContent = 'Stop animation';
    panel.dataset.filmRunning = 'true';
  }
  function update() {
    if (wanted && visible && !media.matches && !document.hidden) play();
    else stop();
  }
  button.hidden = false;
  stop();
  button.addEventListener('click', () => { wanted = !running; update(); });
  function inspect(event) {
    if (event.target.closest('[data-signal-stage], [data-signal-play], [data-signal-step], [data-signal-reset], [data-signal-scenario], [data-signal-event]')) {
      wanted = false;
      stop();
      panel.dataset.visual = 'events';
    }
  }
  panel.addEventListener('click', inspect);
  panel.addEventListener('change', inspect);
  document.addEventListener('visibilitychange', update);
  media.addEventListener('change', update);
  if (globalThis.IntersectionObserver) {
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      update();
    }).observe(panel.querySelector('.signal-visual'));
  } else play();
})();
