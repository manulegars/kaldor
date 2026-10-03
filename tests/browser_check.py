"""Tests réels Firefox via Marionette (stdlib uniquement, Firefox installé requis)."""
import base64
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
from marionette_client import Marionette

with tempfile.TemporaryDirectory(prefix='wsps-firefox-', dir=ROOT/'tests') as profile:
    env=dict(os.environ,PORT='18082',MOZ_HEADLESS='1')
    reduced_mode=os.environ.get('TEST_REDUCED_MOTION')=='1'
    if reduced_mode: (Path(profile)/'user.js').write_text('user_pref("ui.prefersReducedMotion", 1);')
    server=subprocess.Popen(['python3','-m','app.server'],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    browser=None
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen('http://127.0.0.1:18082/health',timeout=1);break
            except OSError:time.sleep(.1)
        browser=subprocess.Popen(['firefox','--headless','--no-remote','--marionette','--profile',profile],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for _ in range(120):
            try:m=Marionette();break
            except OSError:time.sleep(.2)
        else:raise RuntimeError('Marionette indisponible')
        m.command('WebDriver:NewSession',{'capabilities':{'alwaysMatch':{'acceptInsecureCerts':True}}})
        m.command('WebDriver:SetWindowRect',{'width':1440,'height':1100})
        m.command('WebDriver:Navigate',{'url':'http://127.0.0.1:18082/ws-ps'})
        m.wait("document.getElementById('request-state').textContent==='À jour'")
        assert m.js("return document.getElementById('unemployment').textContent").startswith('10,0')
        assert m.js("return document.getElementById('wage').textContent")=='100,0'
        assert m.js("return document.querySelectorAll('#chart polyline').length")==2
        # Rapid input calls: the latest response must win.
        m.js("for(let i=0;i<25;i++){const e=document.getElementById('z-range');e.value=i/100;e.dispatchEvent(new Event('input',{bubbles:true}));} return true;")
        m.wait("document.getElementById('request-state').textContent==='À jour' && document.getElementById('unemployment').textContent.startsWith('19,6')")
        m.js("document.getElementById('axis').value='employment';document.getElementById('axis').dispatchEvent(new Event('change'));return true;")
        m.wait("document.getElementById('request-state').textContent==='À jour'")
        assert m.js("return document.getElementById('unemployment').textContent").startswith('19,6')
        # Observed unemployment leaves equilibrium unchanged.
        m.js("document.getElementById('advanced').open=true;let e=document.getElementById('observed-range');e.value=.7;e.dispatchEvent(new Event('input'));return true;")
        m.wait("document.getElementById('gap').textContent.includes('70,0')")
        assert m.js("return document.getElementById('unemployment').textContent").startswith('19,6')
        # Numeric input and out-of-domain handling.
        m.js("let e=document.getElementById('z-number');e.value=-1;e.dispatchEvent(new Event('input'));return true;")
        m.wait("!document.getElementById('domain-warning').hidden")
        assert m.js("return document.getElementById('unemployment').textContent")=='—'
        m.js("document.getElementById('reset').click();return true;")
        m.wait("document.getElementById('unemployment').textContent.startsWith('10,0')")
        # Keyboard range interaction through WebDriver actions.
        m.js("document.getElementById('A-range').focus();return true;")
        m.command('WebDriver:PerformActions',{'actions':[{'type':'key','id':'keyboard','actions':[{'type':'keyDown','value':'\ue014'},{'type':'keyUp','value':'\ue014'}]}]})
        m.wait("document.getElementById('A-number').value==='1.01'")
        m.wait("document.getElementById('request-state').textContent==='À jour'")
        assert m.js("return document.getElementById('unemployment').textContent").startswith('10,0')
        if reduced_mode:
            assert m.js("return matchMedia('(prefers-reduced-motion: reduce)').matches")
            m.js("document.getElementById('scenario').value='productivity-none';document.getElementById('replay').click();return true;")
            m.wait("document.getElementById('animation-status').textContent.includes('préférence de réduction')")
            assert m.js("return document.getElementById('unemployment').textContent").startswith('6,7')
        else:
            # Scenario, pause, replay, and fixed axis domain.
            m.js("document.getElementById('scenario').value='productivity-none';document.getElementById('replay').click();return true;")
            m.wait("Number(document.getElementById('progress').value)>.1")
            scale=m.js("return [...document.querySelectorAll('#chart text')].slice(0,6).map(x=>x.textContent)")
            m.js("document.getElementById('pause').click();return true;")
            value=m.js("return document.getElementById('progress').value")
            time.sleep(.3)
            assert value==m.js("return document.getElementById('progress').value")
            m.js("document.getElementById('animate').click();return true;")
            m.wait("document.getElementById('progress').value===1")
            m.wait("document.getElementById('request-state').textContent==='À jour'")
            assert m.js("return document.getElementById('unemployment').textContent").startswith('6,7')
            assert scale==m.js("return [...document.querySelectorAll('#chart text')].slice(0,6).map(x=>x.textContent)")
        # External resources must not be requested.
        assert m.js("return performance.getEntriesByType('resource').every(x=>x.name.startsWith(location.origin))")
        shots=ROOT/'tests'/'artifacts';shots.mkdir(exist_ok=True)
        shot=m.command('WebDriver:TakeScreenshot',{'full':True})['value']
        (shots/'desktop.png').write_bytes(base64.b64decode(shot))
        m.command('WebDriver:SetWindowRect',{'width':390,'height':844})
        assert m.js('return document.documentElement.scrollWidth <= window.innerWidth')
        assert m.js("return document.querySelector('.controls').getBoundingClientRect().top>=document.querySelector('.chart-card').getBoundingClientRect().bottom")
        shot=m.command('WebDriver:TakeScreenshot',{'full':True})['value']
        (shots/'mobile.png').write_bytes(base64.b64decode(shot))
        # A second tab starts at baseline, independent of first tab.
        handle=m.command('WebDriver:NewWindow',{'type':'tab'})['handle']
        m.command('WebDriver:SwitchToWindow',{'handle':handle})
        m.command('WebDriver:Navigate',{'url':'http://127.0.0.1:18082/ws-ps'})
        m.wait("document.getElementById('request-state').textContent==='À jour'")
        assert m.js("return document.getElementById('unemployment').textContent").startswith('10,0')
        print('OK : Firefox bureau/mobile, clavier, 25 entrées rapides, axes, observation, hors domaine, animation/pause/reprise, échelles fixes, ressources locales, onglets indépendants.')
    finally:
        if browser:browser.terminate();browser.wait(timeout=15)
        server.terminate();server.wait(timeout=10)
