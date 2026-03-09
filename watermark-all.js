/**
 * watermark-all.js — Aplica watermark pe TOATE pozele din img/
 *
 * Utilizare:
 *   node watermark-all.js           -> aplica pe toate
 *   node watermark-all.js --dry-run -> doar afiseaza ce ar procesa
 */

const { Jimp } = require('jimp');
const path = require('path');
const fs = require('fs');

const LOGO_PATH = path.join(__dirname, 'img', 'watermark-logo.png');
const LOGO_SCALE = 0.22;
const LOGO_OPACITY = 0.80;

const SKIP = [
  'logo.jpg', 'banner-mehedintiazi.jpg', 'watermark-logo.png',
  'sigla-11plus-tv.png', 'salvati-copiii-romania-logo.png',
  'harta-drum-expres-filiasi-drobeta-2026.png',
  'carte-organizarea-nuntii-fara-regrete.jpg',
  'frf-sesiune-cluburi-juvenile-sibiu-2026-poster.jpg',
  'test-watermark.jpg', 'test-watermark-nou.jpg'
];

async function addWatermark(imgPath) {
  const image = await Jimp.read(imgPath);
  const logo = await Jimp.read(LOGO_PATH);

  const imgWidth = image.bitmap.width;
  const imgHeight = image.bitmap.height;

  const logoW = Math.floor(imgWidth * LOGO_SCALE);
  const logoH = Math.floor(logoW * (logo.bitmap.height / logo.bitmap.width));
  logo.resize({ w: logoW, h: logoH });

  // Transforma logo: fundal alb -> transparent, text inchis -> alb
  logo.scan(0, 0, logo.bitmap.width, logo.bitmap.height, function(x, y, idx) {
    const r = this.bitmap.data[idx];
    const g = this.bitmap.data[idx + 1];
    const b = this.bitmap.data[idx + 2];
    if (r > 200 && g > 200 && b > 200) {
      this.bitmap.data[idx + 3] = 0;
    } else {
      this.bitmap.data[idx]     = 255;
      this.bitmap.data[idx + 1] = 255;
      this.bitmap.data[idx + 2] = 255;
    }
  });

  logo.opacity(LOGO_OPACITY);
  image.composite(logo, imgWidth - logoW - 15, imgHeight - logoH - 15);
  await image.write(imgPath);
}

async function run() {
  const dryRun = process.argv[2] === '--dry-run';

  const files = fs.readdirSync('img').filter(function(f) {
    return /\.(jpg|jpeg|png)$/i.test(f) && SKIP.indexOf(f) === -1;
  });

  console.log('=== WATERMARK ALL ===');
  console.log('Total imagini gasite: ' + files.length);
  if (dryRun) console.log('(DRY RUN - nu se modifica nimic)\n');
  else console.log('');

  let ok = 0, skip = 0;
  for (let i = 0; i < files.length; i++) {
    const f = files[i];
    if (dryRun) {
      console.log('  [DRY] ' + f);
      ok++;
    } else {
      try {
        await addWatermark('img/' + f);
        console.log('  OK ' + f);
        ok++;
      } catch(e) {
        console.log('  SKIP ' + f + ' - ' + e.message);
        skip++;
      }
    }
  }

  console.log('\nGATA — Procesate: ' + ok + ' | Sarite: ' + skip);
}

run();
