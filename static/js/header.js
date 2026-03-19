(function () {
  const switcher = document.getElementById('accountSwitcher');
  const btn = document.getElementById('accountBtn');
  const menu = document.getElementById('accountMenu');
  const nameEl = document.getElementById('accountName');
  const addBtn = document.getElementById('addAccountBtn');

  const STORAGE_KEY = 'cashflow.selectedAccount';

  function openMenu() {
    switcher.classList.add('is-open');
    btn.setAttribute('aria-expanded', 'true');
  }

  function closeMenu() {
    switcher.classList.remove('is-open');
    btn.setAttribute('aria-expanded', 'false');
  }

  function toggleMenu() {
    if (switcher.classList.contains('is-open')) closeMenu();
    else openMenu();
  }

  function setAccount(name) {
    nameEl.textContent = name;
    try { localStorage.setItem(STORAGE_KEY, name); } catch (e) {}
  }

  // Восстановление выбора
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) setAccount(saved);
  } catch (e) {}

  // Открыть/закрыть меню
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleMenu();
  });

  // Выбор пункта меню (делегирование)
  menu.addEventListener('click', (e) => {
    const item = e.target.closest('.menu-item');
    if (!item) return;

    if (item.id === 'addAccountBtn') {
      // Редирект на страницу создания счёта
      window.location.href = '/create';
      return;
    }

    const account = item.getAttribute('data-account');
    if (account) {
      setAccount(account);
      closeMenu();
    }
  });

  // Закрытие по клику снаружи
  document.addEventListener('click', () => closeMenu());

  // Закрытие по Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMenu();
  });
})();
