document.documentElement.classList.add('js');
const themeToggle = document.querySelector('.theme-toggle');
const themeMeta = document.querySelector('meta[name="theme-color"]');
function applyTheme(mode) {
  const night = mode !== 'day';
  document.documentElement.dataset.theme = night ? 'night' : 'day';
  themeMeta?.setAttribute('content', night ? '#10211f' : '#173f3e');
  if (!themeToggle) return;
  themeToggle.setAttribute('aria-pressed', String(night));
  themeToggle.setAttribute('aria-label', night ? 'Switch to day mode' : 'Switch to night mode');
  themeToggle.title = night ? 'Switch to day mode' : 'Switch to night mode';
}
applyTheme(localStorage.getItem('theme') || 'night');
themeToggle?.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'night' ? 'day' : 'night';
  localStorage.setItem('theme', next);
  applyTheme(next);
});
const menu = document.querySelector('.menu');
const navigation = document.querySelector('#navigation');
function closeMenu() { navigation?.classList.remove('open'); menu?.setAttribute('aria-expanded', 'false'); }
menu?.addEventListener('click', () => {
  const expanded = menu.getAttribute('aria-expanded') === 'true';
  menu.setAttribute('aria-expanded', String(!expanded));
  navigation.classList.toggle('open', !expanded);
});
navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') { closeMenu(); if (document.activeElement?.closest('#navigation')) menu?.focus(); } });
