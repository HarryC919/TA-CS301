#!/usr/bin/env node
// Browser regression checks. Requires Node 24 and local Chrome; no npm packages.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {spawn} = require('node:child_process');
const {setTimeout: delay} = require('node:timers/promises');
const root = path.resolve(__dirname, '../..');

(async () => {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'cs301-ui-'));
  const chrome = spawn(process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new', '--no-sandbox', '--disable-gpu-sandbox', '--disable-gpu',
    '--remote-debugging-port=0', `--user-data-dir=${profile}`
  ], {stdio: 'ignore'});
  let socket;
  try {
    const active = path.join(profile, 'DevToolsActivePort');
    for (let i = 0; i < 100 && !fs.existsSync(active); i++) await delay(100);
    const [port, route] = fs.readFileSync(active, 'utf8').split('\n');
    socket = new WebSocket(`ws://127.0.0.1:${port}${route}`);
    await new Promise((resolve, reject) => {socket.onopen = resolve; socket.onerror = reject;});
    let sequence = 0;
    const pending = new Map();
    socket.onmessage = event => {
      const result = JSON.parse(event.data);
      if (pending.has(result.id)) {
        const {resolve, reject} = pending.get(result.id);
        pending.delete(result.id);
        result.error ? reject(result.error) : resolve(result.result);
      }
    };
    function send(method, params = {}, sessionId) {
      return new Promise((resolve, reject) => {
        const id = ++sequence;
        const timer = setTimeout(() => {pending.delete(id); reject(new Error(`Timed out: ${method}`));}, 10000);
        pending.set(id, {resolve: value => {clearTimeout(timer); resolve(value);}, reject: e => {clearTimeout(timer); reject(e);}});
        socket.send(JSON.stringify({id, method, params, sessionId}));
      });
    }
    const {targetId} = await send('Target.createTarget', {url: 'about:blank'});
    const {sessionId} = await send('Target.attachToTarget', {targetId, flatten: true});
    const call = (method, params) => send(method, params, sessionId);
    async function evaluate(expression) {
      const result = await call('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
      if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
      return result.result.value;
    }
    async function ready(selector) {
      for (let i = 0; i < 100; i++) {
        if (await evaluate(`document.readyState === 'complete' && !!document.querySelector(${JSON.stringify(selector)})`)) return;
        await delay(50);
      }
      throw new Error(`Page not ready: ${selector}`);
    }
    await call('Emulation.setDeviceMetricsOverride', {width: 1440, height: 1200, deviceScaleFactor: 1, mobile: false});
    await call('Page.navigate', {url: 'file://' + path.join(root, 'site/recitation1.html')});
    await ready('#p1-stub-java');
    assert.equal(await evaluate('document.querySelectorAll("textarea.code-input").length'), 36, '36 editable starter panels');
    assert.equal(await evaluate('document.querySelectorAll("[data-editable] textarea").length'), 36);
    assert.equal(await evaluate('document.querySelectorAll("[id*=solution] textarea").length'), 0);
    assert.equal(await evaluate('document.querySelectorAll(".reset-btn").length'), 6);
    assert.ok(await evaluate('document.querySelector("#p1-stub-java .syntax-keyword") !== null'));
    console.log('PASS editor count, read-only answers, reset buttons, initial highlighting');
    assert.equal(await evaluate(`Array.from(document.querySelectorAll('.tab-panel')).every(panel => {
      var original=panel.querySelector('pre code');
      var input=panel.querySelector('textarea');
      return original && original.textContent.length>0 && (!input || input.value===original.textContent);
    })`),true,'highlighting preserves all 72 source blocks');
    for (const lang of ['c','cpp','cs','java','py','js']) {
      const sample = lang==='py' ? '# comment\nvalue = "text"\nif value: return 42\n'
        : '/* comment */\nif (true) { return "text"; } // end\n';
      await evaluate(`var field=document.querySelector('#p1-stub-${lang} textarea');field.value=${JSON.stringify(sample)};field.dispatchEvent(new Event('input'));`);
      assert.equal(await evaluate(`var preview=document.querySelector('#p1-stub-${lang} .code-preview');
        preview.querySelector('.syntax-keyword')!==null && preview.querySelector('.syntax-comment')!==null && preview.querySelector('.syntax-string')!==null`),true,`${lang} token colors`);
      assert.equal(await evaluate(`document.querySelector('#p1-stub-${lang} .code-preview code').textContent`),sample+' ');
      await evaluate(`document.querySelector('#p1-stub-${lang}').restoreCode()`);
    }
    console.log('PASS all six language highlighters preserve source text');


    await evaluate(`window.originalJava = document.querySelector('#p1-stub-java textarea').value;
      window.originalPython = document.querySelector('#p1-stub-py textarea').value;
      window.originalSecond = document.querySelector('#p2-stub-java textarea').value;
      var field = document.querySelector('#p1-stub-java textarea');field.focus();field.select();`);
    const draft = 'public class Demo {\n    // draft <img src=x onerror="window.injected=true">\n    String word = "hello";\n    int count = 42;\n}\n';
    await call('Input.insertText', {text: draft});
    assert.equal(await evaluate('document.querySelector("#p1-stub-java textarea").value'), draft);
    assert.equal(await evaluate('document.querySelector("#p1-stub-java .code-preview code").textContent'), draft + ' ');
    assert.ok(await evaluate('document.querySelector("#p1-stub-java .syntax-comment") !== null && document.querySelector("#p1-stub-java .syntax-string") !== null && document.querySelector("#p1-stub-java .syntax-number") !== null'));
    assert.equal(await evaluate('!!window.injected || !!document.querySelector("#p1-stub-java img")'), false);
    await evaluate(`document.querySelector('#p1-stub-java-tab').closest('.tabs').querySelector('[data-lang=py]').click()`);
    assert.equal(await evaluate('document.querySelector("#p1-stub-py textarea").value === originalPython'), true);
    await evaluate(`document.querySelector('#p2-stub-java-tab').click()`);
    assert.equal(await evaluate('document.querySelector("#p1-stub-java textarea").value'), draft);
    assert.equal(await evaluate('document.querySelector("#p2-stub-java textarea").value === originalSecond'), true);
    console.log('PASS real typing, escaping, live highlighting, isolated drafts, synced language switching');

    await evaluate(`Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText: text => {window.copiedText=text; return Promise.resolve();}}});
      document.querySelector('#p1-stub-java').closest('.tabs').querySelector('.copy-btn').click();`);
    assert.equal(await evaluate('window.copiedText'), draft.replace(/\s+$/, ''));
    await evaluate(`document.querySelector('#p1-stub-java').closest('.tabs').querySelector('.reset-btn').click()`);
    assert.equal(await evaluate('document.querySelector("#p1-stub-java textarea").value === originalJava'), true);
    await evaluate(`var field=document.querySelector('#p1-stub-java textarea');field.focus();field.setSelectionRange(0,0);`);
    await call('Input.dispatchKeyEvent', {type:'keyDown', key:'Tab', code:'Tab', windowsVirtualKeyCode:9});
    await call('Input.dispatchKeyEvent', {type:'keyUp', key:'Tab', code:'Tab', windowsVirtualKeyCode:9});
    assert.equal(await evaluate('document.querySelector("#p1-stub-java textarea").value.startsWith("    ")'), true);
    await call('Input.dispatchKeyEvent', {type:'keyDown', key:'Escape', code:'Escape', windowsVirtualKeyCode:27});
    await call('Input.dispatchKeyEvent', {type:'keyUp', key:'Escape', code:'Escape', windowsVirtualKeyCode:27});
    await call('Input.dispatchKeyEvent', {type:'keyDown', key:'Tab', code:'Tab', windowsVirtualKeyCode:9});
    await call('Input.dispatchKeyEvent', {type:'keyUp', key:'Tab', code:'Tab', windowsVirtualKeyCode:9});
    assert.equal(await evaluate('document.activeElement.matches("textarea")'), false, 'Escape then Tab exits the editor');
    console.log('PASS edited copy, reset, indentation, keyboard escape');

    await call('Page.reload');
    await ready('textarea.code-input');
    assert.equal(await evaluate('document.querySelector("#p1-stub-java textarea").value'), await evaluate('document.querySelector("#p1-stub-java pre:not(.code-preview) code").textContent'));
    assert.equal(await evaluate(`Object.keys(localStorage).some(key => key !== 'cs301-week1-lang') || sessionStorage.length > 0`), false);
    console.log('PASS refresh restores templates; no draft storage');
    await evaluate(`var field=document.querySelector('#p1-stub-java textarea');
      field.value = Array.from({length:80}, (_, i) => '    int line' + i + ' = 123; //' + 'x'.repeat(200)).join('\\n');
      field.dispatchEvent(new Event('input'));field.scrollTop=300;field.scrollLeft=200;
      field.dispatchEvent(new Event('scroll'));`);
    assert.equal(await evaluate(`var field=document.querySelector('#p1-stub-java textarea');
      var preview=document.querySelector('#p1-stub-java .code-preview');
      field.scrollTop===preview.scrollTop && field.scrollLeft===preview.scrollLeft && field.scrollTop>0 && field.scrollLeft>0`),true);
    await evaluate(`document.querySelector('#p1-stub-java').closest('.tabs').querySelector('.reset-btn').click()`);
    console.log('PASS long-code horizontal and vertical scroll alignment');


    // Visual evidence for the editing state and the mobile layout.
    fs.mkdirSync(path.join(root, '.tmp'), {recursive:true});
    for (const width of [1440,390]) {
      await call('Emulation.setDeviceMetricsOverride', {width,height:1100,deviceScaleFactor:1,mobile:width===390});
      await evaluate(`document.documentElement.style.scrollBehavior='auto';document.querySelector('#p1-stub-java textarea').scrollIntoView({behavior:'instant',block:'center'})`);
      assert.equal(await evaluate('document.documentElement.scrollWidth <= innerWidth'), true, 'no page overflow');
      const {data} = await call('Page.captureScreenshot', {format:'png',captureBeyondViewport:false});
      fs.writeFileSync(path.join(root, `.tmp/code-editor-${width}.png`), Buffer.from(data,'base64'));
    }
    await call('Page.navigate', {url:'file://' + path.join(root,'site/recitation1.html')});
    await ready('.code-block .syntax-keyword');
    assert.equal(await evaluate('document.querySelectorAll("#notes textarea").length'),0);
    assert.equal(await evaluate('document.querySelectorAll(".code-block pre code .syntax-keyword").length > 4'),true);
    console.log('PASS notes highlighted and read-only; desktop/mobile screenshots saved');
    for (const width of [1440,390]) {
      await call('Emulation.setDeviceMetricsOverride', {width,height:1100,deviceScaleFactor:1,mobile:width===390});
      for (const name of ['index.html','intro.html',...Array.from({length:8},(_,n)=>`recitation${n}.html`)]) {
        await call('Page.navigate',{url:'file://' + path.join(root,'site',name)});
        await ready('.recitation-menu');
        assert.equal(await evaluate('document.querySelectorAll(".recitation-options a").length'),8);
        assert.equal(await evaluate('document.querySelector(".site-nav a.active").getAttribute("href")'),name);
        await evaluate('document.querySelector(".recitation-menu summary").focus()');
        await call('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',text:'\r',windowsVirtualKeyCode:13});
        await call('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
        assert.equal(await evaluate('document.querySelector(".recitation-menu").open'),true, name+" @"+width+" menu opened by keyboard; focus="+await evaluate('document.activeElement.outerHTML'));
        assert.equal(await evaluate('document.documentElement.scrollWidth<=innerWidth'),true);
        assert.equal(await evaluate('var rect=document.querySelector(".recitation-options").getBoundingClientRect();rect.left>=0 && rect.right<=innerWidth'),true,name+' @'+width+' bounds='+await evaluate('JSON.stringify({left:rect.left,right:rect.right,width:innerWidth})'));
        if (['index.html','recitation0.html','recitation1.html','recitation7.html'].includes(name)) {
          const {data}=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
          fs.writeFileSync(path.join(root,`.tmp/${name}-menu-${width}.png`),Buffer.from(data,'base64'));
        }
        await call('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
        await call('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
        assert.equal(await evaluate('document.querySelector(".recitation-menu").open'),false);
      }
    }
    for (const [old,hash] of [['week1-notes.html','#merge-sort'],['week1-exercises.html','#problem-6']]) {
      await call('Page.navigate',{url:'file://' + path.join(root,'site',old)+hash});
      await ready('#p1-stub-java');
      assert.equal(await evaluate('location.pathname.endsWith("recitation1.html") && location.hash==='+JSON.stringify(hash)),true);
    }
    await evaluate(`var field=document.querySelector('#p1-stub-java textarea');field.value='temporary navigation draft';field.dispatchEvent(new Event('input'));document.querySelector('a[href="#notes"]').click();`);
    assert.equal(await evaluate('document.querySelector("#p1-stub-java textarea").value'), 'temporary navigation draft');
    console.log('PASS all ten primary pages, keyboard dropdowns at two widths, legacy deep links, and same-page draft preservation');

    await call('Page.navigate',{url:'file://' + path.join(root,'site/recitation0.html')});
    await ready('#uv');
    assert.ok(await evaluate('document.querySelectorAll(".code-block[data-language]").length > 10'), 'labeled setup code blocks');
    assert.equal(await evaluate('Array.from(document.querySelectorAll(".code-block[data-language]")).every(block => block.querySelector(".lang-tag") && block.querySelector(".copy-btn:not([hidden])"))'),true);
    assert.equal(await evaluate('document.querySelector("#uv [data-language=powershell] .syntax-comment") !== null'),true);
    assert.equal(await evaluate('document.querySelector("#uv [data-language=zsh] .syntax-function") !== null'),true);
    assert.equal(await evaluate('document.querySelector("#mise [data-language=bash] .syntax-function") !== null'),true);
    await evaluate(`Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:text=>{window.setupCopied=text;return Promise.resolve();}}});
      document.querySelector('#uv [data-language=powershell] .copy-btn').click();`);
    assert.equal(await evaluate('window.setupCopied'), await evaluate('document.querySelector("#uv [data-language=powershell] pre code").textContent.replace(/\\s+$/, "")'));
    assert.ok(await evaluate('window.setupCopied.includes("#") && !window.setupCopied.includes("<span")'));
    assert.equal(await evaluate('document.querySelector("#create-folder").textContent.includes("mkdir") && !document.querySelector("#create-folder").textContent.includes("uv venv")'),true);
    for (const width of [1440,390]) {
      await call('Emulation.setDeviceMetricsOverride',{width,height:1200,deviceScaleFactor:1,mobile:width===390});
      for (const anchor of ['uv','create-folder']) {
        await evaluate(`document.getElementById('${anchor}').scrollIntoView({behavior:'instant',block:'start'})`);
        assert.equal(await evaluate('document.documentElement.scrollWidth<=innerWidth'),true);
        const {data}=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
        fs.writeFileSync(path.join(root,`.tmp/rec0-shell-${anchor}-${width}.png`),Buffer.from(data,'base64'));
      }
    }
    console.log('PASS shell labels/highlighting, literal command/comment copy, separate folder step, desktop/mobile layout');

    await call('Emulation.setScriptExecutionDisabled', {value:true});
    await call('Page.navigate', {url:'file://' + path.join(root,'site/recitation1.html')});
    await ready('#p1-stub-java');
    assert.equal(await evaluate('document.querySelectorAll("textarea").length'),0);
    assert.equal(await evaluate('Array.from(document.querySelectorAll(".tab-panel")).filter(panel => getComputedStyle(panel).display !== "none").length'),72);
    assert.equal(await evaluate('document.querySelectorAll(".recitation-options a").length'),8);
    await evaluate('document.querySelector(".recitation-menu summary").focus()');
    await call('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',text:'\r',windowsVirtualKeyCode:13});
    await call('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
    assert.equal(await evaluate('document.querySelector(".recitation-menu").open'),true);
    console.log('PASS no-JavaScript fallback: all 72 original code panels readable');
    console.log('ALL CODE UI CHECKS PASSED');
  } finally {
    if (socket) socket.close();
    chrome.kill();
    await new Promise(resolve => chrome.exitCode !== null ? resolve() : chrome.once('exit',resolve));
    fs.rmSync(profile,{recursive:true,force:true});
  }
})().catch(error => {console.error(error);process.exitCode=1;});
