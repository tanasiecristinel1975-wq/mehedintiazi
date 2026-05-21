#!/usr/bin/env node
// Trimite URL-uri noi la IndexNow (Google, Bing, Yandex)
// Folosit automat de hook-ul pre-push

const https = require('https');

const KEY = 'a973f7c4d0576033b3742a7e1878fe37';
const HOST = 'www.mehedintiazi.ro';
const BASE_URL = `https://${HOST}`;

// URL-urile noi vin ca argumente
const slugs = process.argv.slice(2);
if (slugs.length === 0) {
  console.log('IndexNow: niciun URL nou de trimis.');
  process.exit(0);
}

const urls = slugs.map(slug => {
  // Elimina extensia .html si slash-ul initial
  const clean = slug.replace(/^\//, '').replace(/\.html$/, '');
  return `${BASE_URL}/${clean}`;
});

console.log('IndexNow: trimit', urls.length, 'URL-uri...');
urls.forEach(u => console.log(' -', u));

const body = JSON.stringify({
  host: HOST,
  key: KEY,
  keyLocation: `${BASE_URL}/${KEY}.txt`,
  urlList: urls
});

const options = {
  hostname: 'api.indexnow.org',
  path: '/indexnow',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body)
  }
};

const req = https.request(options, res => {
  if (res.statusCode === 200 || res.statusCode === 202) {
    console.log('OK IndexNow: URL-urile au fost trimise cu succes! Status:', res.statusCode);
  } else {
    console.log('WARN IndexNow: status', res.statusCode);
  }
});

req.on('error', e => console.log('ERR IndexNow:', e.message));
req.write(body);
req.end();
