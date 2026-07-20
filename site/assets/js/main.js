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

  /* ---- Calendrier de dates (remplace les champs date natifs) ---- */
  var MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
              'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
  var JOURS = ['Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa', 'Di'];

  function iso(d) {
    return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  }
  function parseIso(s) {
    if (!s) return null;
    var p = s.split('-'); if (p.length !== 3) return null;
    var d = new Date(+p[0], +p[1] - 1, +p[2]);
    return isNaN(d.getTime()) ? null : d;
  }
  function joli(d) {
    var m = MOIS[d.getMonth()];
    return d.getDate() + ' ' + (m.length > 4 ? m.slice(0, 4) + '.' : m) + ' ' + d.getFullYear();
  }

  function initCalendar(form) {
    var panel = $('[data-cal]', form);
    if (!panel) return null;
    var monthsBox = $('[data-cal-months]', panel);
    var titleEl = $('[data-cal-title]', panel);
    var inHidden = $('[data-cal-in]', form);
    var outHidden = $('[data-cal-out]', form);
    var today = new Date(); today.setHours(0, 0, 0, 0);

    var state = { start: null, end: null, hover: null, picking: 'in' };
    var view = new Date(today.getFullYear(), today.getMonth(), 1);

    function nbMonths() {
      return (window.matchMedia && window.matchMedia('(min-width: 760px)').matches) ? 2 : 1;
    }

    function renderMonth(y, m) {
      var first = new Date(y, m, 1);
      var offset = (first.getDay() + 6) % 7;          // semaine qui commence le lundi
      var total = new Date(y, m + 1, 0).getDate();
      var cells = '';
      for (var i = 0; i < offset; i++) cells += '<span class="cal__day cal__day--empty"></span>';
      for (var day = 1; day <= total; day++) {
        var d = new Date(y, m, day);
        var key = iso(d);
        var past = d < today;
        var cl = 'cal__day';
        var end = state.end;
        if (state.start && key === iso(state.start)) cl += ' is-start';
        if (state.end && key === iso(state.end)) cl += ' is-end';
        if (state.start && end && d > state.start && d < end) cl += ' is-in';
        cells += '<button type="button" class="' + cl + '" data-day="' + key + '"' +
                 (past ? ' disabled aria-disabled="true"' : '') +
                 ' aria-label="' + day + ' ' + MOIS[m] + ' ' + y + '">' + day + '</button>';
      }
      return '<div class="cal__month"><p class="cal__mname">' + MOIS[m].charAt(0).toUpperCase() +
             MOIS[m].slice(1) + ' ' + y + '</p><div class="cal__dow">' +
             JOURS.map(function (j) { return '<span>' + j + '</span>'; }).join('') +
             '</div><div class="cal__grid">' + cells + '</div></div>';
    }

    function labels() {
      var set = function (k, d) {
        var el = $('[data-cal-label="' + k + '"]', form);
        if (!el) return;
        el.textContent = d ? joli(d) : 'Ajouter une date';
        el.classList.toggle('is-set', !!d);
      };
      set('in', state.start); set('out', state.end);
      if (inHidden) inHidden.value = state.start ? iso(state.start) : '';
      if (outHidden) outHidden.value = state.end ? iso(state.end) : '';
    }

    function render() {
      var n = nbMonths(), html = '', names = [];
      for (var i = 0; i < n; i++) {
        var d = new Date(view.getFullYear(), view.getMonth() + i, 1);
        html += renderMonth(d.getFullYear(), d.getMonth());
        names.push(MOIS[d.getMonth()].charAt(0).toUpperCase() + MOIS[d.getMonth()].slice(1) + ' ' + d.getFullYear());
      }
      monthsBox.innerHTML = html;
      titleEl.textContent = names.join(' — ');
      var prev = $('[data-cal-prev]', panel);
      if (prev) prev.disabled = view <= new Date(today.getFullYear(), today.getMonth(), 1);
      labels();
    }

    function open(v, which) {
      panel.hidden = !v;
      form.classList.toggle('cal-open', v);
      $all('[data-cal-open]', form).forEach(function (b) { b.setAttribute('aria-expanded', v ? 'true' : 'false'); });
      if (v) {
        state.picking = which || 'in';
        var anchor = state.start || today;
        view = new Date(anchor.getFullYear(), anchor.getMonth(), 1);
        render();
        // le panneau est haut : on fait remonter la page juste ce qu'il faut
        requestAnimationFrame(function () {
          var over = panel.getBoundingClientRect().bottom - (window.innerHeight - 12);
          if (over > 0) window.scrollBy({ top: over, behavior: 'smooth' });
        });
      }
    }

    function pick(d) {
      if (!state.start || state.end || d <= state.start) {
        state.start = d; state.end = null; state.picking = 'out';
      } else {
        state.end = d; state.picking = 'in';
      }
      render();
      if (state.start && state.end) setTimeout(function () { open(false); }, 220);
    }

    monthsBox.addEventListener('click', function (e) {
      var b = e.target.closest('[data-day]');
      if (!b || b.disabled) return;
      pick(parseIso(b.getAttribute('data-day')));
    });
    // Aperçu de la plage au survol : on repeint les classes sans regénérer la grille
    // (un innerHTML ici supprimerait le bouton entre le mousedown et le mouseup → clic perdu).
    monthsBox.addEventListener('mouseover', function (e) {
      var b = e.target.closest('[data-day]');
      if (!b || b.disabled || state.picking !== 'out' || !state.start || state.end) return;
      var end = parseIso(b.getAttribute('data-day'));
      $all('[data-day]', monthsBox).forEach(function (cell) {
        var d = parseIso(cell.getAttribute('data-day'));
        cell.classList.toggle('is-in', !!(end && d > state.start && d < end));
      });
    });

    $('[data-cal-prev]', panel).addEventListener('click', function () {
      view = new Date(view.getFullYear(), view.getMonth() - 1, 1); render();
    });
    $('[data-cal-next]', panel).addEventListener('click', function () {
      view = new Date(view.getFullYear(), view.getMonth() + 1, 1); render();
    });
    $('[data-cal-clear]', panel).addEventListener('click', function () {
      state.start = null; state.end = null; state.hover = null; state.picking = 'in'; render();
    });
    $('[data-cal-close]', panel).addEventListener('click', function () { open(false); });

    $all('[data-cal-open]', form).forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        open(panel.hidden, b.getAttribute('data-cal-open'));
      });
    });
    panel.addEventListener('click', function (e) { e.stopPropagation(); });
    document.addEventListener('click', function () { if (!panel.hidden) open(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) open(false); });
    window.addEventListener('resize', function () { if (!panel.hidden) render(); });

    labels();
    return {
      setRange: function (a, b) {
        state.start = parseIso(a); state.end = parseIso(b); labels();
      }
    };
  }

  /* Tout conteneur [data-cal-host] reçoit un calendrier : le widget de réservation
     comme le formulaire de demande de tarif cure. */
  $all('[data-cal-host]').forEach(function (host) { host.__cal = initCalendar(host); });

  /* Champs de dates obligatoires : on bloque l'envoi et on ouvre le calendrier. */
  $all('[data-cal-required]').forEach(function (panel) {
    var host = panel.closest('[data-cal-host]');
    var form = panel.closest('form');
    if (!host || !form) return;
    form.addEventListener('submit', function (e) {
      var a = $('[data-cal-in]', host), b = $('[data-cal-out]', host);
      if (a && b && a.value && b.value) return;
      e.preventDefault();
      var btn = $('[data-cal-open="in"]', host);
      if (btn) { btn.click(); btn.focus(); }
    });
  });

  $all('[data-booking]').forEach(function (formEl) {
    formEl.addEventListener('submit', function (e) {
      e.preventDefault();
      var ciEl = $('[data-cal-in]', formEl), coEl = $('[data-cal-out]', formEl);
      var checkin = ciEl ? ciEl.value : '';
      var checkout = coEl ? coEl.value : '';
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
    $all('[data-booking]').forEach(function (f) { if (f.__cal) f.__cal.setRange(ci, co); });

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

  /* ---- Filtres (page Activités) ---- */
  var filtres = $('[data-filtres]');
  if (filtres) {
    var grille = $('[data-filtres-grid]');
    var compteur = $('[data-filtres-count]', filtres);
    var vide = $('[data-filtres-vide]');
    var cartes = $all('.act', grille);
    var etat = { sec: 'all', cat: 'all' };

    function appliquer() {
      var n = 0;
      cartes.forEach(function (c) {
        var ok = (etat.sec === 'all' || c.getAttribute('data-sec') === etat.sec) &&
                 (etat.cat === 'all' || c.getAttribute('data-cat') === etat.cat);
        c.hidden = !ok;
        if (ok) n++;
      });
      compteur.textContent = n + (n > 1 ? ' activités' : ' activité');
      if (vide) vide.hidden = n > 0;
      var filtre = etat.sec !== 'all' || etat.cat !== 'all';
      if (reset) reset.hidden = !filtre;
    }

    var reset = $('[data-filtres-reset]');
    var selects = $all('[data-filtre]', filtres);

    selects.forEach(function (sel) {
      sel.addEventListener('change', function () {
        etat[sel.getAttribute('data-filtre')] = sel.value;
        appliquer();
      });
    });

    if (reset) reset.addEventListener('click', function () {
      etat.sec = 'all'; etat.cat = 'all';
      selects.forEach(function (sel) { sel.value = 'all'; });
      appliquer();
    });

    appliquer();
  }

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
