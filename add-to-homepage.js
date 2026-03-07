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
const imgSrc = imgMatch ? imgMatch[1] : '';

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

// --- Insereaza in index.html dupa marcajul grilei ---
const indexPath = path.resolve('index.html');
let indexHtml = fs.readFileSync(indexPath, 'utf8');

const MARKER = '<!-- GRID 4 ARTICOLE - Copiaza blocul article-card pentru fiecare stire noua -->\n        <div class="articles-grid mb-20">';

if (!indexHtml.includes(MARKER)) {
  console.error('Nu am gasit marcajul in index.html. Verifica structura homepage-ului.');
  process.exit(1);
}

// Verifica daca stirea e deja adaugata
if (indexHtml.includes(slug)) {
  console.log('Stirea este deja pe homepage: ' + slug);
  process.exit(0);
}

indexHtml = indexHtml.replace(MARKER, MARKER + card);
fs.writeFileSync(indexPath, indexHtml, 'utf8');

console.log('OK Adaugat pe homepage: ' + slug);
