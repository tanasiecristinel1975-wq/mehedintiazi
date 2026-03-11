/**
 * add-to-homepage.js
 * Adauga automat un articol nou in grila de pe homepage (index.html)
 *
 * Utilizare: node add-to-homepage.js nume-articol.html
 */

const fs = require('fs');
const path = require('path');

const articleFile = process.argv[2];
if (!articleFile) {
  console.log('Utilizare: node add-to-homepage.js nume-articol.html');
  process.exit(1);
}

const articlePath = path.resolve(articleFile);
if (!fs.existsSync(articlePath)) {
  console.error('Fisierul nu exista: ' + articlePath);
  process.exit(1);
}

const html = fs.readFileSync(articlePath, 'utf8');
const slug = path.basename(articleFile);

// --- Extrage titlul ---
const titleMatch = html.match(/<h1[^>]*class="article-title"[^>]*>\s*([\s\S]*?)\s*<\/h1>/i);
const title = titleMatch ? titleMatch[1].replace(/<[^>]+>/g, '').trim() : 'Stire noua';

// --- Extrage imaginea principala ---
const imgMatch = html.match(/class="article-img-main"[\s\S]*?<img[^>]*src="([^"]+)"/i);
let imgSrc = imgMatch ? imgMatch[1] : '';

if (!imgSrc) {
  const ogImgMatch = html.match(/<meta[^>]*property="og:image"[^>]*content="([^"]+)"/i);
  if (ogImgMatch) {
    imgSrc = ogImgMatch[1].replace('https://www.mehedintiazi.ro', '');
  }
}

// --- Extrage categoria (text + culoare) ---
const catMatch = html.match(/<span[^>]*class="article-category"[^>]*style="[^"]*background:\s*([^;"]+)[^"]*"[^>]*>([\s\S]*?)<\/span>/i);
const catColor = catMatch ? catMatch[1].trim() : '#1a3a5c';
const catText = catMatch ? catMatch[2].replace(/<[^>]+>/g, '').trim() : 'Actualitate';

// --- Extrage excerptul (subtitle) ---
const excerptMatch = html.match(/<p[^>]*class="article-subtitle"[^>]*>([\s\S]*?)<\/p>/i);
const excerpt = excerptMatch ? excerptMatch[1].replace(/<[^>]+>/g, '').trim().substring(0, 120) + '...' : '';

// --- Extrage data ---
const dateMatch = html.match(/article:published_time.*?content="(\d{4}-\d{2}-\d{2})/i);
let dateStr = '7 Martie 2026';
if (dateMatch) {
  const d = new Date(dateMatch[1]);
  const luni = ['Ianuarie','Februarie','Martie','Aprilie','Mai','Iunie','Iulie','August','Septembrie','Octombrie','Noiembrie','Decembrie'];
  dateStr = d.getDate() + ' ' + luni[d.getMonth()] + ' ' + d.getFullYear();
}

// --- Genereaza cardul ---
const card = `
          <!-- ARTICOL - ${slug.toUpperCase().replace('.HTML','').replace(/-/g,' ')} -->
          <div class="article-card" style="border-top:3px solid ${catColor};">
            <div class="card-img">
              <img src="${imgSrc}" alt="${title}" style="width:100%;height:100%;object-fit:cover;" />
            </div>
            <div class="card-body">
              <span class="card-category" style="background:${catColor};">${catText}</span>
              <h3 class="card-title"><a href="${slug}">${title}</a></h3>
              <p class="card-excerpt">${excerpt}</p>
              <div class="card-meta"><span>&#128336; ${dateStr}</span><a href="${slug}" class="card-read">Citeste &rsaquo;</a></div>
            </div>
          </div>
`;

// --- Insereaza in index.html ---
const indexPath = path.resolve('index.html');
let indexHtml = fs.readFileSync(indexPath, 'utf8');

// Verifica daca stirea e deja adaugata
if (indexHtml.includes(slug)) {
  console.log('Stirea este deja pe homepage: ' + slug);
  process.exit(0);
}

// -------------------------------------------------------
// 1. Actualizeaza HERO SECTION
//    - stirea noua devine hero-main
//    - vechiul hero-main devine primul hero-side
//    - vechiul primul hero-side devine al doilea hero-side
// -------------------------------------------------------

// Extrage datele din hero-main curent
const heroMainMatch = indexHtml.match(/<!-- STIRE PRINCIPALA HERO -->\s*<div class="hero-main">([\s\S]*?)<\/div>\s*<\/div>\s*<\/div>\s*\n\s*\n\s*<!-- STIRI SECUNDARE/);

// Extrage img, href, titlu si data din hero-main curent
const heroImgMatch = indexHtml.match(/<!-- STIRE PRINCIPALA HERO -->[\s\S]*?<img src="([^"]+)"[^>]*\/>/);
const heroBadgeMatch = indexHtml.match(/<!-- STIRE PRINCIPALA HERO -->[\s\S]*?<span class="hero-badge"[^>]*>([\s\S]*?)<\/span>/);
const heroHrefMatch = indexHtml.match(/<!-- STIRE PRINCIPALA HERO -->[\s\S]*?<h2><a href="([^"]+)">([\s\S]*?)<\/a><\/h2>/);
const heroDateMatch = indexHtml.match(/<!-- STIRE PRINCIPALA HERO -->[\s\S]*?<span>(&#128336;[^<]+)<\/span>/);

const oldHeroImg = heroImgMatch ? heroImgMatch[1] : '';
const oldHeroBadge = heroBadgeMatch ? heroBadgeMatch[1].trim() : 'Actualitate';
const oldHeroHref = heroHrefMatch ? heroHrefMatch[1] : '#';
const oldHeroTitle = heroHrefMatch ? heroHrefMatch[2].replace(/<[^>]+>/g, '').trim() : '';
const oldHeroDate = heroDateMatch ? heroDateMatch[1] : '&#128336; 2026';

// Extrage primul side-article curent
const sideMatch = indexHtml.match(/<!-- STIRI SECUNDARE -->\s*<div class="hero-side">\s*<div class="side-article">([\s\S]*?)<\/div>\s*<div class="side-article">/);
const side1ImgMatch = indexHtml.match(/<!-- STIRI SECUNDARE -->[\s\S]*?<div class="side-article">[\s\S]*?<img src="([^"]+)"/);
const side1HrefMatch = indexHtml.match(/<!-- STIRI SECUNDARE -->[\s\S]*?<div class="side-article">[\s\S]*?<h4><a href="([^"]+)">([\s\S]*?)<\/a><\/h4>/);
const side1BadgeMatch = indexHtml.match(/<!-- STIRI SECUNDARE -->[\s\S]*?<div class="side-article">[\s\S]*?<div class="badge"[^>]*>([\s\S]*?)<\/div>/);
const side1DateMatch = indexHtml.match(/<!-- STIRI SECUNDARE -->[\s\S]*?<div class="side-article">[\s\S]*?<div class="meta">([\s\S]*?)<\/div>/);

const side1Img = side1ImgMatch ? side1ImgMatch[1] : '';
const side1Href = side1HrefMatch ? side1HrefMatch[1] : '#';
const side1Title = side1HrefMatch ? side1HrefMatch[2].replace(/<[^>]+>/g, '').trim() : '';
const side1Badge = side1BadgeMatch ? side1BadgeMatch[1].trim() : 'Actualitate';
const side1Date = side1DateMatch ? side1DateMatch[1].trim() : '';

// Noul hero-main cu stirea noua
const newHeroMain = `      <!-- STIRE PRINCIPALA HERO -->
      <div class="hero-main">
        <div class="img-wrapper">
          <img src="${imgSrc}" alt="${title}" />
        </div>
        <div class="hero-text">
          <span class="hero-badge" style="background:${catColor};">${catText}</span>
          <h2><a href="${slug}">${title}</a></h2>
          <p class="excerpt">${excerpt}</p>
          <div class="hero-meta">
            <span>&#128336; ${dateStr}</span>
          </div>
        </div>
      </div>`;

// Noul hero-side: vechiul hero-main + vechiul side1
const newHeroSide = `      <!-- STIRI SECUNDARE -->
      <div class="hero-side">
        <div class="side-article">
          <div class="side-img">
            <img src="${oldHeroImg}" alt="${oldHeroTitle}" style="object-fit:cover;" />
          </div>
          <div class="side-text">
            <div class="badge">${oldHeroBadge}</div>
            <h4><a href="${oldHeroHref}">${oldHeroTitle}</a></h4>
            <div class="meta">${oldHeroDate}</div>
          </div>
        </div>
        <div class="side-article">
          <div class="side-img">
            <img src="${side1Img}" alt="${side1Title}" style="object-fit:cover;" />
          </div>
          <div class="side-text">
            <div class="badge">${side1Badge}</div>
            <h4><a href="${side1Href}">${side1Title}</a></h4>
            <div class="meta">${side1Date}</div>
          </div>
        </div>
      </div>`;

// Inlocuieste toata sectiunea hero-grid
const heroGridMatch = indexHtml.match(/<!-- STIRE PRINCIPALA HERO -->[\s\S]*?<!-- STIRI SECUNDARE -->[\s\S]*?<\/div>\s*<\/div>\s*\n\s*\n\s*<\/div>\s*<\/div>\s*<\/section>/);
if (heroGridMatch) {
  indexHtml = indexHtml.replace(
    /<!-- STIRE PRINCIPALA HERO -->[\s\S]*?<\/div>\s*\n\n\s*<\/div>\s*<\/div>\s*<\/section>/,
    newHeroMain + '\n\n' + newHeroSide + '\n\n    </div>\n  </div>\n</section>'
  );
  console.log('OK Hero actualizat cu: ' + slug);
} else {
  console.log('WARN: Nu am putut actualiza hero section');
}

// -------------------------------------------------------
// 2. Adauga in grila de articole (top)
// -------------------------------------------------------
const MARKER = '<!-- GRID 4 ARTICOLE - Copiaza blocul article-card pentru fiecare stire noua -->\n        <div class="articles-grid mb-20">';

if (!indexHtml.includes(MARKER)) {
  console.error('Nu am gasit marcajul grilei in index.html.');
} else {
  indexHtml = indexHtml.replace(MARKER, MARKER + card);
  console.log('OK Adaugat in grila: ' + slug);
}

fs.writeFileSync(indexPath, indexHtml, 'utf8');
console.log('OK Homepage actualizat: ' + slug);
