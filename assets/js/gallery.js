/**
 * Pomocnik slideshowa — bez własnych importów.
 * HTML importuje PhotoSwipeLightbox bezpośrednio z CDN,
 * a ten moduł dodaje tylko przycisk ▶/⏸.
 */

const SLIDESHOW_INTERVAL = 4000;

/**
 * Dodaje pokaz slajdów do już utworzonego obiektu PhotoSwipeLightbox.
 * Wywołaj przed lb.init().
 */
export function addSlideshow(lb, intervalMs = SLIDESHOW_INTERVAL) {
  let timer = null;
  let playing = false;
  let btnEl = null;

  lb.on('uiRegister', () => {
    lb.pswp.ui.registerElement({
      name: 'slideshow-button',
      order: 9,
      isButton: true,
      title: 'Pokaz slajdów (Spacja)',
      html: iconPlay(),
      onClick(_, el) {
        playing ? stop(el) : start(el);
      },
    });
  });

  lb.on('afterInit', () => {
    btnEl = lb.pswp.element.querySelector('.pswp__button--slideshow-button');
    lb.pswp.element.addEventListener('keydown', (e) => {
      if (e.code === 'Space') {
        e.preventDefault();
        playing ? stop(btnEl) : start(btnEl);
      }
    });
  });

  lb.on('change', () => {
    if (!playing) return;
    clearInterval(timer);
    timer = setInterval(advance, intervalMs);
  });

  lb.on('close', () => {
    clearInterval(timer);
    timer = null;
    playing = false;
  });

  function advance() { lb.pswp?.next(); }

  function start(el) {
    playing = true;
    if (el) el.innerHTML = iconPause();
    timer = setInterval(advance, intervalMs);
  }

  function stop(el) {
    playing = false;
    if (el) el.innerHTML = iconPlay();
    clearInterval(timer);
    timer = null;
  }
}

function iconPlay() {
  return `<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>`;
}

function iconPause() {
  return `<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20" aria-hidden="true"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`;
}
