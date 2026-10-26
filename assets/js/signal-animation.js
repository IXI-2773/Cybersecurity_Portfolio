/* Finite explanatory GIF. Existing fixture inspection remains independent. */
(() => {
  'use strict';
  const panel = document.querySelector('[data-signal-display]');
  if (!panel) return;
  const image = panel.querySelector('[data-signal-film]');
  const button = panel.querySelector('[data-film-play]');
  if (!image || !button) return;
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  const gif = image.getAttribute('src'), still = image.dataset.still;
  let timer, replay = 0, running = false, started = false;
  function stop() {
    clearTimeout(timer);
    running = false;
    image.src = still;
    button.textContent = media.matches ? 'Still illustration' : 'Replay animation';
    button.disabled = media.matches;
    panel.dataset.filmRunning = 'false';
  }
  function play() {
    if (media.matches || document.hidden) return;
    panel.querySelector('[data-signal-scenario]').value = 'ten_minute_boundary';
    panel.querySelector('[data-signal-reset]').click();
    panel.dataset.visual = 'film';
    // A fresh image URL restarts a finite GIF, including after its final frame.
    image.src = gif + '?replay=' + (++replay);
    started = true;
    running = true;
    button.textContent = 'Stop animation';
    panel.dataset.filmRunning = 'true';
    clearTimeout(timer);
    timer = setTimeout(stop, 4800);
  }
  button.hidden = false;
  stop();
  button.addEventListener('click', () => running ? stop() : play());
  function inspect(event) {
    if (event.target.closest('[data-signal-stage], [data-signal-play], [data-signal-step], [data-signal-reset], [data-signal-scenario]')) {
      started = true;
      stop();
      panel.dataset.visual = 'events';
    }
  }
  panel.addEventListener('click', inspect);
  panel.addEventListener('change', inspect);
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  media.addEventListener('change', stop);
  if (globalThis.IntersectionObserver) {
    new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) stop();
      else if (!started) play();
    }).observe(image);
  } else play();
})();
