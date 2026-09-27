const { chromium } = require('../.tools/node_modules/playwright');
const fs = require('node:fs/promises');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const expected = await fs.readFile('site/assets/puspamitra-mishra-profile.pdf');
    for (const width of [1440, 390, 320]) {
      const page = await browser.newPage({ viewport: { width, height: 900 }, acceptDownloads: true });
      await page.goto('http://127.0.0.1:4173/', { waitUntil: 'networkidle' });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      const links = page.getByRole('link', { name: 'Download profile (PDF, 3 pages)', exact: true });
      assert.equal(await links.count(), 2);
      for (let i = 0; i < 2; i++) {
        const href = await links.nth(i).getAttribute('href');
        const response = await page.request.get(new URL(href, page.url()).href);
        assert.equal(response.status(), 200);
        assert.match(response.headers()['content-type'], /application\/pdf/);
        const received = await response.body();
        assert.ok(received.equals(expected), 'Served file differs from the generated profile');
        assert.equal(received.subarray(0, 5).toString(), '%PDF-');
        const [download] = await Promise.all([page.waitForEvent('download'), links.nth(i).click()]);
        assert.equal(download.suggestedFilename(), 'Puspamitra-Mishra-Profile.pdf');
        // Verify delivery above; avoid depending on Chrome's OS download scanning.
        await download.cancel();
      }
      await page.close();
    }
    console.log('PASS: both links trigger correctly named downloads and serve the exact PDF at desktop, mobile, and narrow mobile widths.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
