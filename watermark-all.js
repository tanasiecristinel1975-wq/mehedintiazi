const { Jimp } = require('jimp');
const path = require('path');
const fs = require('fs');

const LOGO_PATH = path.join(__dirname, 'img', 'watermark-logo.png');
const LOGO_SCALE = 0.22;
const LOGO_OPACITY = 0.65;

const SKIP = [
  'logo.jpg', 'banner-mehedintiazi.jpg', 'watermark-logo.png',
  'sigla-11plus-tv.png', 'salvati-copiii-romania-logo.png',
  'harta-drum-expres-filiasi-drobeta-2026.png',
  'carte-organizarea-nuntii-fara-regrete.jpg',
  'frf-sesiune-cluburi-juvenile-sibiu-2026-poster.jpg'
];

async function addWatermark(imgPath) {
  const image = await Jimp.read(imgPath);
  const logo = await Jimp.read(LOGO_PATH);
  const imgWidth = image.bitmap.width;
  const imgHeight = image.bitmap.height;
  const logoW = Math.floor(imgWidth * LOGO_SCALE);
  const logoH = Math.floor(logoW * (logo.bitmap.height / logo.bitmap.width));
  logo.resize({ w: logoW, h: logoH });
  logo.opacity(LOGO_OPACITY);
  image.composite(logo, imgWidth - logoW - 15, imgHeight - logoH - 15);
  await image.write(imgPath);
}

async function run() {
  const files = fs.readdirSync('img').filter(function(f) {
    return /\.(jpg|jpeg|png)$/i.test(f) && SKIP.indexOf(f) === -1;
  });
  for (var i = 0; i < files.length; i++) {
    var f = files[i];
    try {
      await addWatermark('img/' + f);
      console.log('OK ' + f);
    } catch(e) {
      console.log('SKIP ' + f + ' - ' + e.message);
    }
  }
  console.log('GATA - ' + files.length + ' imagini procesate');
}
run();
