/* =========================================================
   Les Meublés de Luchon — Interactions
   ========================================================= */
(function () {
  'use strict';

  /* ---- Clés de réservation Superhôte (récupérées du site existant) ---- */
  var SUPERHOTE = {
    'perle-bleue':   'propertyKeyhYHKfobjxVxjHhLTkzJPTehXA',
    'echappee-verte':'propertyKey3VpakNcQ3X2LlAXOTujQsws6e',
    'refuge-thermal':'propertyKey8WSw0zYWOvWLL0rAslYrAKaOu'
  };
  var CONTACT_EMAIL = 'contact@lesmeublesdeluchon.com';

  function $(s, ctx) { return (ctx || document).querySelector(s); }
  function $all(s, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(s)); }

  /* ---- Header : ombre au scroll ---- */
  var header = $('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---- Menu mobile ---- */
  var toggle = $('.nav__toggle');
  if (toggle && header) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    $all('.nav__links a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---- Recherche de disponibilités (moteur Superhôte filtré) ---- */
  var SITE_KEY = 'bcGpXSkB3NtJCWmMbGnVucHbT';
  var GROUP = 'Les Meublés de Luchon';

  function buildSearchUrl(checkin, checkout, g) {
    g = g || {};
    var u = 'https://app.superhote.com/#/get-available-rentals/' + SITE_KEY +
            '?groups=' + encodeURIComponent(GROUP);
    if (checkin) u += '&startDate=' + checkin;
    if (checkout) u += '&endDate=' + checkout;
    if (g.adults) u += '&adultsNumber=' + g.adults;
    if (g.children) u += '&childrenNumber=' + g.children;
    if (g.babies) u += '&babiesNumber=' + g.babies;
    return u;
  }

  /* ---- Sélecteur voyageurs (adultes / enfants / bébés) ---- */
  function guestsLabel(box) {
    var n = 0;
    ['adults', 'children'].forEach(function (k) {
      var i = $('[name="' + k + '"]', box); if (i) n += parseInt(i.value, 10) || 0;
    });
    var b = $('[name="babies"]', box), nb = b ? parseInt(b.value, 10) || 0 : 0;
    var txt = n + ' voyageur' + (n > 1 ? 's' : '');
    if (nb) txt += ' · ' + nb + ' bébé' + (nb > 1 ? 's' : '');
    return txt;
  }

  $all('[data-guests]').forEach(function (box) {
    var btn = $('[data-guests-toggle]', box);
    var panel = $('.guests__panel', box);
    var label = $('[data-guests-label]', box);
    if (!btn || !panel) return;

    function open(v) {
      panel.hidden = !v;
      box.classList.toggle('is-open', v);
      btn.setAttribute('aria-expanded', v ? 'true' : 'false');
    }
    function refresh() { label.textContent = guestsLabel(box); }

    btn.addEventListener('click', function (e) { e.stopPropagation(); open(panel.hidden); });
    var close = $('[data-guests-close]', box);
    if (close) close.addEventListener('click', function () { open(false); btn.focus(); });
    panel.addEventListener('click', function (e) { e.stopPropagation(); });
    document.addEventListener('click', function () { if (!panel.hidden) open(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) { open(false); btn.focus(); }
    });

    $all('.guests__btn', box).forEach(function (b) {
      b.addEventListener('click', function () {
        var key = b.getAttribute('data-for');
        var input = $('[name="' + key + '"]', box);
        var out = $('[data-out="' + key + '"]', box);
        if (!input) return;
        var min = parseInt(input.getAttribute('data-min'), 10) || 0;
        var max = parseInt(input.getAttribute('data-max'), 10) || 12;
        var v = (parseInt(input.value, 10) || 0) + (parseInt(b.getAttribute('data-step'), 10) || 0);
        v = Math.max(min, Math.min(max, v));
        input.value = v;
        if (out) out.textContent = v;
        $all('.guests__btn[data-for="' + key + '"]', box).forEach(function (o) {
          var s = parseInt(o.getAttribute('data-step'), 10);
          o.disabled = (s < 0 && v <= min) || (s > 0 && v >= max);
        });
        refresh();
      });
    });
    refresh();
  });

  function readGuests(formEl) {
    var g = {};
    ['adults', 'children', 'babies'].forEach(function (k) {
      var i = $('[name="' + k + '"]', formEl);
      if (i) g[k] = parseInt(i.value, 10) || 0;
    });
    return g;
  }

  function buildSuperhoteUrl(key, checkin, checkout, guests) {
    return 'https://app.superhote.com/#/rental/' + key +
      '?startDate=' + (checkin || '') + '&endDate=' + (checkout || '') +
      '&adultsNumber=' + (guests || 1) + '&childrenNumber=0&lang=fr';
  }

  $all('[data-booking]').forEach(function (formEl) {
    var todayIso = new Date().toISOString().split('T')[0];
    var ci = $('[name="checkin"]', formEl);
    var co = $('[name="checkout"]', formEl);
    if (ci) ci.min = todayIso;
    if (co) co.min = todayIso;
    if (ci && co) {
      ci.addEventListener('change', function () {
        co.min = ci.value || todayIso;
        if (co.value && co.value <= ci.value) {
          var next = new Date(ci.value); next.setDate(next.getDate() + 1);
          co.value = next.toISOString().split('T')[0];
        }
      });
    }

    formEl.addEventListener('submit', function (e) {
      e.preventDefault();
      var checkin = ci ? ci.value : '';
      var checkout = co ? co.value : '';
      var guests = readGuests(formEl);
      var search = document.getElementById('bookingsearch');
      if (search) {
        search.src = buildSearchUrl(checkin, checkout, guests);
        search.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        window.location.href = '/nos-logements/?checkin=' + encodeURIComponent(checkin) +
          '&checkout=' + encodeURIComponent(checkout) +
          '&adults=' + (guests.adults || '') + '&children=' + (guests.children || '') +
          '&babies=' + (guests.babies || '');
      }
    });
  });

  /* ---- Pré-remplissage depuis l'URL (arrivée depuis l'accueil) ---- */
  (function () {
    if (!window.URLSearchParams) return;
    var p = new URLSearchParams(location.search);
    var ci = p.get('checkin') || '', co = p.get('checkout') || '';
    var g = { adults: p.get('adults') || '', children: p.get('children') || '', babies: p.get('babies') || '' };
    if (!ci && !co && !g.adults) return;
    var search = document.getElementById('bookingsearch');
    if (search) search.src = buildSearchUrl(ci, co, g);
    var set = function (sel, v) { var el = $(sel); if (el && v) el.value = v; };
    set('[name="checkin"]', ci); set('[name="checkout"]', co);
    if (search) setTimeout(function () { search.scrollIntoView({ block: 'start' }); }, 300);
  })();

  /* ---- Galerie / Lightbox ---- */
  var lightbox = $('#lightbox');
  if (lightbox) {
    var lbImg = $('.lightbox__img', lightbox);
    var items = $all('.gallery__item img');
    var current = 0;
    function show(i) {
      current = (i + items.length) % items.length;
      lbImg.src = items[current].getAttribute('data-full') || items[current].src;
      lbImg.alt = items[current].alt;
    }
    items.forEach(function (img, i) {
      img.parentElement.addEventListener('click', function () { lightbox.classList.add('open'); show(i); });
    });
    $('.lightbox__close', lightbox).addEventListener('click', function () { lightbox.classList.remove('open'); });
    $('.lightbox__nav--prev', lightbox).addEventListener('click', function () { show(current - 1); });
    $('.lightbox__nav--next', lightbox).addEventListener('click', function () { show(current + 1); });
    lightbox.addEventListener('click', function (e) { if (e.target === lightbox) lightbox.classList.remove('open'); });
    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape') lightbox.classList.remove('open');
      if (e.key === 'ArrowLeft') show(current - 1);
      if (e.key === 'ArrowRight') show(current + 1);
    });
  }

  /* ---- FAQ accordéon ---- */
  $all('.faq__q').forEach(function (q) {
    q.addEventListener('click', function () {
      var expanded = q.getAttribute('aria-expanded') === 'true';
      q.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      var a = q.nextElementSibling;
      if (a) a.setAttribute('data-open', expanded ? 'false' : 'true');
    });
  });

  /* ---- Carrousel photos (cartes logement) ---- */
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  $all('[data-slider]').forEach(function (sl) {
    var slides = $('.card__slides', sl);
    var items = $all('.card__slide', sl);
    var dots = $all('.card__dot', sl);
    if (items.length < 2) return;
    var i = 0, timer = null;
    function go(n) {
      i = (n + items.length) % items.length;
      slides.style.transform = 'translateX(-' + (i * 100) + '%)';
      dots.forEach(function (d, di) { d.setAttribute('aria-current', di === i ? 'true' : 'false'); });
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function play() { if (reduceMotion) return; stop(); timer = setInterval(function () { go(i + 1); }, 4500); }
    var next = $('.card__arrow--next', sl), prev = $('.card__arrow--prev', sl);
    if (next) next.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); go(i + 1); play(); });
    if (prev) prev.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); go(i - 1); play(); });
    dots.forEach(function (d, di) { d.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); go(di); play(); }); });
    sl.addEventListener('mouseenter', stop);
    sl.addEventListener('mouseleave', play);
    play();
  });

  /* ---- Reveal au scroll ---- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('visible'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    $all('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    $all('.reveal').forEach(function (el) { el.classList.add('visible'); });
  }

  /* ---- Bandeau cookies (CNIL) ---- */
  var cookie = $('#cookie');
  if (cookie) {
    var KEY = 'lml-consent';
    if (!localStorage.getItem(KEY)) { setTimeout(function () { cookie.classList.add('show'); }, 800); }
    function decide(val) {
      localStorage.setItem(KEY, val);
      cookie.classList.remove('show');
      if (val === 'accept') loadAnalytics();
    }
    $('#cookie-accept', cookie).addEventListener('click', function () { decide('accept'); });
    $('#cookie-refuse', cookie).addEventListener('click', function () { decide('refuse'); });
    if (localStorage.getItem(KEY) === 'accept') loadAnalytics();
  }
  function loadAnalytics() {
    // Placeholder : le tracking ne se charge QU'APRÈS consentement (conforme CNIL).
    // Remplacer par le vrai ID Google Analytics 4 en production.
    // Ex : injecter le script gtag ici avec l'ID G-XXXXXXXXXX.
    window.__consentGranted = true;
  }

  /* ---- Avis : déplier les textes tronqués ---- */
  $all('.review').forEach(function (r) {
    var t = $('.review__text', r);
    if (!t) return;
    if (t.scrollHeight - t.clientHeight > 4) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'review__more'; b.textContent = 'Lire la suite';
      b.setAttribute('aria-expanded', 'false');
      b.addEventListener('click', function () {
        var open = r.classList.toggle('is-open');
        b.textContent = open ? 'Réduire' : 'Lire la suite';
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      t.insertAdjacentElement('afterend', b);
    }
  });

  /* ---- Année dynamique footer ---- */
  $all('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
