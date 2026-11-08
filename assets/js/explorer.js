'use strict';
(() => {
  const form = document.querySelector('#project-filters');
  if (!form) return;

  const search = form.querySelector('#project-search');
  const buttons = [...form.querySelectorAll('[data-work-filter]')];
  const status = form.querySelector('#filter-status');
  const empty = form.querySelector('#filter-empty');
  const categoryNav = document.querySelector('#work-categories');
  const sections = [...document.querySelectorAll('.directory-section[data-work-type]')];
  const normalize = value => value.toLocaleLowerCase().normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9+#]+/g, ' ');
  const entries = sections.flatMap(section => [...section.querySelectorAll('.directory-entry')]
    .map(element => ({element, section, text: normalize(element.textContent)})));
  let active = 'all';

  function update() {
    const words = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let shown = 0;

    for (const item of entries) {
      const match = (active === 'all' || item.section.dataset.workType === active)
        && words.every(word => item.text.includes(word));
      item.element.hidden = !match;
      if (match) shown++;
    }
    for (const section of sections) {
      section.hidden = !entries.some(item => item.section === section && !item.element.hidden);
    }
    for (const button of buttons) {
      button.setAttribute('aria-pressed', String(button.dataset.workFilter === active));
    }
    if (categoryNav) categoryNav.hidden = active !== 'all' || words.length > 0;
    status.textContent = `${shown} of ${entries.length} entries shown`;
    empty.hidden = shown !== 0;
  }

  for (const button of buttons) {
    button.addEventListener('click', () => {
      active = button.dataset.workFilter;
      update();
    });
  }
  form.addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', update);
  form.hidden = false;
  update();
})();
