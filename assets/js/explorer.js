'use strict';
(() => {
  const form = document.querySelector('#project-filters');
  if (!form) return;
  const role = form.querySelector('#role-filter');
  const search = form.querySelector('#project-search');
  const entries = [...document.querySelectorAll('[data-project-entry]')];
  const status = document.querySelector('#filter-status');
  const empty = document.querySelector('#filter-empty');
  const normalize = value => value.toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'');
  function update() {
    const words = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const card of entries) {
      const roles = card.dataset.roles.split(' ');
      const text = normalize(card.textContent + ' ' + card.dataset.keywords);
      const tokens = text.match(/[a-z0-9+#]+/g) || [];
      const match = (role.value === 'all' || roles.includes(role.value)) && words.every(word => word.length <= 3 ? tokens.includes(word) : text.includes(word));
      card.hidden = !match;
      if (match) shown++;
    }
    status.textContent = `${shown} of ${entries.length} entries shown`;
    empty.hidden = shown !== 0;
  }
  const requested = new URLSearchParams(location.search).get('role');
  if ([...role.options].some(option => option.value === requested)) role.value = requested;
  form.querySelector('fieldset').hidden = false;
  search.addEventListener('input',update);
  role.addEventListener('change',update);
  form.addEventListener('submit',event => {event.preventDefault();update();});
  form.addEventListener('reset',event => {event.preventDefault();search.value='';role.value='all';update();});
  update();
})();
