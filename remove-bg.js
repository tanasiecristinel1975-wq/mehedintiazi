const { Jimp } = require('jimp');

const INPUT = 'C:/Users/MONTAJ/Pictures/ideogram-v3.0_Elegant_photographer_watermark_signature_with_the_letters_MhA._Handwritten_calli-0.png';
const OUTPUT = 'img/watermark-logo.png';
const THRESHOLD = 230;

async function run() {
  const img = await Jimp.read(INPUT);
  const { width, height } = img.bitmap;

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const idx = (y * width + x) * 4;
      const r = img.bitmap.data[idx];
      const g = img.bitmap.data[idx + 1];
      const b = img.bitmap.data[idx + 2];
      if (r > THRESHOLD && g > THRESHOLD && b > THRESHOLD) {
        img.bitmap.data[idx + 3] = 0;
      }
    }
  }

  await img.write(OUTPUT);
  console.log('Gata! Salvat in ' + OUTPUT);
}

run().catch(console.error);
