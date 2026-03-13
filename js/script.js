/* ============================================================
   MEHEDINTI AZI - script.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // ----------------------------------------------------------
  // 1. DATA SI ORA IN TIMP REAL
  // ----------------------------------------------------------
  function updateDateTime() {
    const el = document.getElementById('data-ora');
    if (!el) return;
    const now = new Date();
    const zile = ['Duminică','Luni','Marți','Miercuri','Joi','Vineri','Sâmbătă'];
    const luni = ['Ianuarie','Februarie','Martie','Aprilie','Mai','Iunie',
                  'Iulie','August','Septembrie','Octombrie','Noiembrie','Decembrie'];
    const z = zile[now.getDay()];
    const d = now.getDate();
    const l = luni[now.getMonth()];
    const y = now.getFullYear();
    const h = String(now.getHours()).padStart(2,'0');
    const m = String(now.getMinutes()).padStart(2,'0');
    el.textContent = `${z}, ${d} ${l} ${y} | ${h}:${m}`;
  }
  updateDateTime();
  setInterval(updateDateTime, 30000);

  // ----------------------------------------------------------
  // 2. MENIU MOBIL (hamburger)
  // ----------------------------------------------------------
  const hamburger = document.getElementById('hamburger');
  const navList   = document.getElementById('nav-list');
  if (hamburger && navList) {
    hamburger.addEventListener('click', function () {
      navList.classList.toggle('open');
      hamburger.textContent = navList.classList.contains('open') ? '✕' : '☰';
    });
  }

  // ----------------------------------------------------------
  // 3. STICKY NAV - adauga shadow la scroll
  // ----------------------------------------------------------
  const nav = document.querySelector('nav.main-nav');
  window.addEventListener('scroll', function () {
    if (!nav) return;
    if (window.scrollY > 80) {
      nav.style.boxShadow = '0 3px 15px rgba(0,0,0,0.3)';
    } else {
      nav.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
    }
  });

  // ----------------------------------------------------------
  // 4. COOKIE BAR
  // ----------------------------------------------------------
  const cookieBar = document.getElementById('cookie-bar');
  const cookieBtn = document.getElementById('cookie-accept');
  if (cookieBar && cookieBtn) {
    if (!localStorage.getItem('cookie_accepted')) {
      cookieBar.style.display = 'flex';
    }
    cookieBtn.addEventListener('click', function () {
      localStorage.setItem('cookie_accepted', '1');
      cookieBar.style.display = 'none';
    });
  }

  // ----------------------------------------------------------
  // 5. TICKER BREAKING NEWS - pauza la hover
  // ----------------------------------------------------------
  const breakingList = document.querySelector('.breaking-list');
  if (breakingList) {
    breakingList.addEventListener('mouseenter', function () {
      this.style.animationPlayState = 'paused';
    });
    breakingList.addEventListener('mouseleave', function () {
      this.style.animationPlayState = 'running';
    });
  }

  // ----------------------------------------------------------
  // 6. LAZY LOAD imagini (simplu, cu IntersectionObserver)
  // ----------------------------------------------------------
  const lazyImgs = document.querySelectorAll('img[data-src]');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    });
    lazyImgs.forEach(function(img) { observer.observe(img); });
  } else {
    lazyImgs.forEach(function(img) { img.src = img.dataset.src; });
  }

  // ----------------------------------------------------------
  // 7. CONTOR VIZITE ARTICOL (simulat - pt demonstratie)
  // ----------------------------------------------------------
  const viewCounters = document.querySelectorAll('.view-count');
  viewCounters.forEach(function(el) {
    const base = parseInt(el.dataset.base) || 100;
    const rand = Math.floor(Math.random() * 500) + base;
    el.textContent = rand.toLocaleString('ro-RO') + ' citiri';
  });

  // ----------------------------------------------------------
  // 8. BACK TO TOP button
  // ----------------------------------------------------------
  const backTop = document.getElementById('back-top');
  if (backTop) {
    window.addEventListener('scroll', function () {
      backTop.style.display = window.scrollY > 400 ? 'flex' : 'none';
    });
    backTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ----------------------------------------------------------
  // 9. SEARCH - focus effect
  // ----------------------------------------------------------
  const searchInput = document.querySelector('.header-search input');
  if (searchInput) {
    searchInput.addEventListener('focus', function() {
      this.style.width = '220px';
    });
    searchInput.addEventListener('blur', function() {
      this.style.width = '180px';
    });
    // Submit search
    const searchForm = document.querySelector('.header-search');
    if (searchForm) {
      searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const q = searchInput.value.trim();
        if (q) {
          window.location.href = '?s=' + encodeURIComponent(q);
        }
      });
    }
  }

  // ----------------------------------------------------------
  // 10. PROTECTIE CONTINUT - dezactiveaza copiere si click dreapta
  // ----------------------------------------------------------
  const continutArticol = document.querySelector('.article-content');
  if (continutArticol) {

    // Dezactiveaza click dreapta pe articol
    continutArticol.addEventListener('contextmenu', function(e) {
      e.preventDefault();
      afiseazaMesajCopyright();
    });

    // Dezactiveaza Ctrl+C, Ctrl+A, Ctrl+X pe articol
    continutArticol.addEventListener('keydown', function(e) {
      if (e.ctrlKey && (e.key === 'c' || e.key === 'a' || e.key === 'x')) {
        e.preventDefault();
        afiseazaMesajCopyright();
      }
    });

    // Dezactiveaza selectia textului pe articol
    continutArticol.style.userSelect = 'none';
    continutArticol.style.webkitUserSelect = 'none';
    continutArticol.style.msUserSelect = 'none';
  }

  // Dezactiveaza click dreapta pe toate imaginile
  document.querySelectorAll('img').forEach(function(img) {
    img.addEventListener('contextmenu', function(e) {
      e.preventDefault();
    });
    img.setAttribute('draggable', 'false');
  });

  function afiseazaMesajCopyright() {
    const mesajExistent = document.getElementById('mesaj-copyright');
    if (mesajExistent) return;
    const mesaj = document.createElement('div');
    mesaj.id = 'mesaj-copyright';
    mesaj.innerHTML = '&#169; MehedintiAzi.ro &mdash; Continutul este protejat. Preluarea stirilor este permisa doar cu citarea sursei.';
    mesaj.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#1a3a5c;color:#fff;padding:12px 24px;border-radius:4px;font-size:14px;z-index:99999;box-shadow:0 4px 15px rgba(0,0,0,0.3);text-align:center;max-width:90%;';
    document.body.appendChild(mesaj);
    setTimeout(function() { mesaj.remove(); }, 3000);
  }

  console.log('Mehedinti Azi - site incarcat cu succes!');

  // ----------------------------------------------------------
  // 11. RADIO PLAYER PLUTITOR
  // ----------------------------------------------------------
  var radioHTML = `
    <div id="radio-player" style="
      position:fixed; bottom:20px; left:20px; z-index:99999;
      background:#0d2240; border-radius:12px; padding:10px 14px;
      display:flex; align-items:center; gap:10px;
      box-shadow:0 4px 20px rgba(0,0,0,0.5);
      min-width:220px; max-width:260px;
      border:1px solid rgba(255,255,255,0.1);
    ">
      <img src="/img/radio-logo.png" alt="Radio MehedintiAzi" style="width:44px;height:44px;border-radius:8px;object-fit:cover;flex-shrink:0;" />
      <div style="flex:1;min-width:0;">
        <div style="color:#fff;font-size:12px;font-weight:700;letter-spacing:0.5px;">RADIO</div>
        <div style="color:#f0c040;font-size:11px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">MehedintiAzi.ro</div>
        <div id="radio-status" style="color:rgba(255,255,255,0.5);font-size:10px;">Apasa Play</div>
      </div>
      <button id="radio-btn" onclick="radioToggle()" style="
        background:#c0392b; border:none; border-radius:50%;
        width:36px; height:36px; cursor:pointer;
        display:flex; align-items:center; justify-content:center;
        flex-shrink:0; font-size:14px; color:#fff;
      ">&#9654;</button>
      <audio id="radio-audio" preload="none">
        <source src="http://radio.mehedintiazi.ro/radio" type="audio/mpeg" />
      </audio>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', radioHTML);

  // ----------------------------------------------------------
  // BANNER PUBLICITAR - Destine Broker de Asigurari
  // ----------------------------------------------------------
  var sidebars = document.querySelectorAll('.sidebar');
  if (sidebars.length > 0) {
    var bannerHTML = `
      <div class="sidebar-widget" style="padding:0;overflow:hidden;border:none;background:transparent;">
        <a href="tel:0770450730" title="Destine Broker de Asigurari - Tanasie Cristinel 0770 450 730">
          <img src="/img/banner-destine-broker-asigurari.jpg"
               alt="Destine Broker de Asigurari - RCA CASCO Locuinta Viata - Tanasie Cristinel 0770 450 730"
               style="width:100%;display:block;border-radius:6px;cursor:pointer;" />
        </a>
      </div>`;
    sidebars.forEach(function(sb) {
      sb.insertAdjacentHTML('afterbegin', bannerHTML);
    });
  }

  window.radioToggle = function() {
    var audio = document.getElementById('radio-audio');
    var btn = document.getElementById('radio-btn');
    var status = document.getElementById('radio-status');
    if (audio.paused) {
      audio.load();
      audio.play();
      btn.innerHTML = '&#9646;&#9646;';
      btn.style.background = '#27ae60';
      status.textContent = 'Live...';
    } else {
      audio.pause();
      audio.src = '';
      btn.innerHTML = '&#9654;';
      btn.style.background = '#c0392b';
      status.textContent = 'Apasa Play';
    }
  };
});
