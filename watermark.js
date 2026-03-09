/**
 * watermark.js — Adauga logo MehedintiAzi.ro pe imagini
 *
 * Utilizare:
 *   node watermark.js imagine.jpg
 *   node watermark.js img/poza.jpg
 *
 * Imaginea originala este INLOCUITA cu versiunea cu watermark.
 */

const { Jimp } = require('jimp');
const path = require('path');

const imagePath = process.argv[2];

if (!imagePath) {
  console.log('Utilizare: node watermark.js <cale-imagine>');
  console.log('Exemplu:   node watermark.js img/poza.jpg');
  process.exit(1);
}

// Calea catre logoul watermark
const LOGO_PATH = path.join(__dirname, 'img', 'watermark-logo.png');

// Dimensiunea logo-ului pe imagine (% din latimea imaginii)
const LOGO_SCALE = 0.22;

// Opacitate logo (0 = transparent, 1 = opac)
const LOGO_OPACITY = 0.80;

async function addWatermark(imgPath) {
  try {
    const image = await Jimp.read(imgPath);
    const logo = await Jimp.read(LOGO_PATH);

    const imgWidth = image.bitmap.width;
    const imgHeight = image.bitmap.height;

    // Redimensioneaza logo proportional
    const logoTargetWidth = Math.floor(imgWidth * LOGO_SCALE);
    const logoRatio = logo.bitmap.height / logo.bitmap.width;
    const logoTargetHeight = Math.floor(logoTargetWidth * logoRatio);
    logo.resize({ w: logoTargetWidth, h: logoTargetHeight });

    // Transforma logo: fundalul alb devine transparent, textul negru devine alb
    logo.scan(0, 0, logo.bitmap.width, logo.bitmap.height, function(x, y, idx) {
      const r = this.bitmap.data[idx];
      const g = this.bitmap.data[idx + 1];
      const b = this.bitmap.data[idx + 2];
      if (r > 200 && g > 200 && b > 200) {
        // Pixel alb (fundal) -> transparent
        this.bitmap.data[idx + 3] = 0;
      } else {
        // Pixel inchis (text/desen) -> alb
        this.bitmap.data[idx]     = 255;
        this.bitmap.data[idx + 1] = 255;
        this.bitmap.data[idx + 2] = 255;
      }
    });

    // Aplica opacitate
    logo.opacity(LOGO_OPACITY);

    // Pozitie: colt dreapta-jos cu margine 15px
    const x = imgWidth - logoTargetWidth - 15;
    const y = imgHeight - logoTargetHeight - 15;

    // Suprapune logo pe imagine
    image.composite(logo, x, y);

    // Salveaza
    await image.write(imgPath);

    console.log('OK Watermark adaugat: ' + imgPath);
  } catch (err) {
    console.error('Eroare:', err.message);
    process.exit(1);
  }
}

addWatermark(imagePath);
