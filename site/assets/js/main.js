/* =========================================================
   Les Meublés de Luchon — Interactions
   ========================================================= */
(function () {
  'use strict';

  /* ---- Clés de réservation Superhôte (récupérées du site existant) ---- */
  var SUPERHOTE = {
    'perle-bleue':   'propertyKeyhYHKfobjxVxjHhLTkzJPTehXA',
    'echappee-verte':'propertyKey3VpakNcQ3X2LlAXOTujQsws6e'
    // 'refuge-thermal' : pas encore de clé Superhôte -> demande par formulaire/contact
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

  /* ---- Widget de réservation ---- */
  function buildSuperhoteUrl(key, checkin, checkout, adults, children) {
    return 'https://app.superhote.com/#/rental/' + key +
      '?startDate=' + (checkin || '') +
      '&endDate=' + (checkout || '') +
      '&adultsNumber=' + (adults || 1) +
      '&childrenNumber=' + (children || 0) +
      '&lang=fr';
  }

  $all('[data-booking]').forEach(function (formEl) {
    // date min = aujourd'hui
    var todayIso = new Date().toISOString().split('T')[0];
    var ci = $('[name="checkin"]', formEl);
    var co = $('[name="checkout"]', formEl);
    if (ci) { ci.min = todayIso; }
    if (co) { co.min = todayIso; }
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
      var lodgingSel = $('[name="lodging"]', formEl);
      var slug = formEl.getAttribute('data-lodging') || (lodgingSel ? lodgingSel.value : '');
      var checkin = ci ? ci.value : '';
      var checkout = co ? co.value : '';
      var adults = $('[name="adults"]', formEl) ? $('[name="adults"]', formEl).value : 1;
      var children = $('[name="children"]', formEl) ? $('[name="children"]', formEl).value : 0;

      if (SUPERHOTE[slug]) {
        window.open(buildSuperhoteUrl(SUPERHOTE[slug], checkin, checkout, adults, children), '_blank', 'noopener');
      } else {
        // Pas de clé (ex : Le Refuge Thermal) -> demande par email pré-remplie
        var subj = encodeURIComponent('Demande de réservation — ' + (slug ? slug.replace(/-/g, ' ') : 'séjour'));
        var body = encodeURIComponent(
          'Bonjour Nathalie,\n\nJe souhaite réserver le logement : ' + (slug || 'à définir') +
          '.\nArrivée : ' + (checkin || 'à préciser') +
          '\nDépart : ' + (checkout || 'à préciser') +
          '\nVoyageurs : ' + adults + ' adulte(s), ' + children + ' enfant(s)' +
          '\n\nMerci de me confirmer la disponibilité.\n');
        window.location.href = 'mailto:' + CONTACT_EMAIL + '?subject=' + subj + '&body=' + body;
      }
    });
  });

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

  /* ---- Année dynamique footer ---- */
  $all('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
