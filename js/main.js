// EOSDFW.com — main.js
// Theme toggle + mobile menu. Keep it tiny — no frameworks.

(function () {
  const root = document.documentElement;
  const toggle = document.querySelector('[data-theme-toggle]');

  const sunIcon =
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>';
  const moonIcon =
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

  let current = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  root.setAttribute('data-theme', current);
  if (toggle) {
    toggle.innerHTML = current === 'dark' ? sunIcon : moonIcon;
    toggle.setAttribute(
      'aria-label',
      'Switch to ' + (current === 'dark' ? 'light' : 'dark') + ' mode'
    );
    toggle.addEventListener('click', function () {
      current = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', current);
      toggle.innerHTML = current === 'dark' ? sunIcon : moonIcon;
      toggle.setAttribute(
        'aria-label',
        'Switch to ' + (current === 'dark' ? 'light' : 'dark') + ' mode'
      );
    });
  }

  // Mobile menu
  const menuBtn = document.querySelector('[data-menu-toggle]');
  const navLinks = document.querySelector('[data-nav-links]');
  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', function () {
      const open = navLinks.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();
