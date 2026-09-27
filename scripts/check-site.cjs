const { chromium } = require('../.tools/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
(async () => {
  fs.mkdirSync('qa',{recursive:true});
  const browser = await chromium.launch({channel:'chrome',headless:true});
  const issues = [];
  for (const width of [1440,390,320]) {
    const page = await browser.newPage({viewport:{width,height:1000},deviceScaleFactor:1});
    page.on('pageerror',e=>issues.push(e.message));
    for (const route of ['/',...fs.readdirSync('site/projects').filter(f=>f.endsWith('.html')).map(f=>'/projects/'+f)]) {
      await page.goto('http://127.0.0.1:4173'+route,{waitUntil:'networkidle'});
      await page.evaluate(async () => {
        for (const image of document.images) {
          if (image.loading === 'lazy') {
            image.scrollIntoView({behavior:'instant'});
            await image.decode().catch(()=>{});
          }
        }
        window.scrollTo({top:0,behavior:'instant'});
      });
      const broken = await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),h1:document.querySelectorAll('h1').length}));
      if(broken.overflow||broken.images.length||broken.h1!==1) issues.push({width,route,...broken});
      if(width!==320) await page.screenshot({path:`qa/${width}-${route==='/'?'home':path.basename(route,'.html')}.png`,fullPage:true});
      if(route==='/' && width!==320) await page.screenshot({path:`qa/${width}-hero.png`});
    }
    await page.goto('http://127.0.0.1:4173/');
    if(width<720){await page.locator('.menu').click();await page.getByRole('link',{name:'AI projects',exact:true}).click();if(await page.locator('.menu').getAttribute('aria-expanded')!=='false')issues.push('Mobile menu did not close');}
    await page.locator('.project-card').first().click();
    if(!page.url().includes('clinical-document-intelligence'))issues.push('Project navigation failed');
    await page.getByRole('link',{name:'All AI projects'}).click();
    if(!page.url().endsWith('index.html#projects'))issues.push('Back navigation failed');
    await page.close();
  }
  await browser.close();
  console.log(JSON.stringify({status:issues.length?'FAIL':'PASS',issues,pages:5,widths:[1440,390,320]},null,2));
  if(issues.length)process.exitCode=1;
})();
