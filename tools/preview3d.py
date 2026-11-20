"""Automated screenshots of the 3D game in headless Chrome (runs on GitHub Actions).

Loads app3d/src/main/assets/index.html (with the bundled three.min.js), plays a short scripted
scenario and saves screenshots + the browser console log into ./preview/.
"""
import asyncio
import os

from playwright.async_api import async_playwright

SRC = 'app3d/src/main/assets'
OUT = 'preview'

# A copy of the game with a tiny test hook so the script can trigger crashes (police levels).
html = open(f'{SRC}/index.html', encoding='utf-8').read()
hook = "  reset();\n  init3D();\n"
assert hook in html, 'boot hook not found'
html = html.replace(hook, hook + "  window.__crash = ped => crash(bus.x, busY + 4, 'x', ped);\n"
                                 "  window.__brake = on => setBrake(on);\n")
open(f'{SRC}/_preview.html', 'w', encoding='utf-8').write(html)
os.makedirs(OUT, exist_ok=True)

CHROME_ARGS = ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']


async def main():
    logs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=CHROME_ARGS)
        page = await browser.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        page.on('console', lambda m: logs.append(f'[{m.type}] {m.text}'))
        page.on('pageerror', lambda e: logs.append(f'[PAGEERROR] {e}'))
        await page.goto('file://' + os.path.abspath(f'{SRC}/_preview.html'))
        await page.wait_for_timeout(3000)
        info = await page.evaluate("""() => { const c = document.createElement('canvas'); const g = c.getContext('webgl');
            return { three: !!window.THREE, rev: window.THREE && THREE.REVISION, webgl: !!g,
                     renderer: g ? g.getParameter(g.RENDERER) : null }; }""")
        logs.append(f'[INFO] {info}')
        await page.screenshot(path=f'{OUT}/1-menu.png')
        await page.click('#startBtn')
        await page.wait_for_timeout(7000)
        await page.screenshot(path=f'{OUT}/2-driving.png')
        await page.evaluate('__crash(false)')
        await page.wait_for_timeout(2500)
        await page.evaluate('__brake(true)')
        await page.wait_for_timeout(900)
        await page.screenshot(path=f'{OUT}/3-police-bike.png')
        await page.evaluate('__brake(false)')
        await page.evaluate('__crash(false)')
        await page.wait_for_timeout(1500)
        await page.evaluate('__crash(false)')
        await page.wait_for_timeout(2500)
        await page.screenshot(path=f'{OUT}/4-chase.png')
        await page.click('#honk')
        await page.wait_for_timeout(250)
        await page.screenshot(path=f'{OUT}/5-honk.png')
        # wide screen (tablet / desktop)
        await page.set_viewport_size({'width': 1280, 'height': 720})
        await page.wait_for_timeout(1500)
        await page.screenshot(path=f'{OUT}/6-landscape.png')
        fps = await page.evaluate("""() => new Promise(r => { let n = 0; const t0 = performance.now();
            (function f() { n++; if (performance.now() - t0 < 3000) requestAnimationFrame(f); else r(n / 3); })(); })""")
        logs.append(f'[INFO] fps (software renderer) = {fps:.1f}')
        await browser.close()
    open(f'{OUT}/log.txt', 'w', encoding='utf-8').write('\n'.join(logs) + '\n')
    print('\n'.join(logs))


asyncio.run(main())
