"""Parcours réel du laboratoire dans Firefox ; aucune dépendance Python tierce."""
import base64
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import urllib.request
from marionette_client import Marionette

ROOT=Path(__file__).resolve().parents[1]

def run():
    with tempfile.TemporaryDirectory(prefix='wsps-firefox-',dir=ROOT/'tests') as profile:
        env=dict(os.environ,PORT='18082',MOZ_HEADLESS='1')
        reduced=os.environ.get('TEST_REDUCED_MOTION')=='1'
        downloads=ROOT/'tests'/'artifacts'/'downloads';downloads.mkdir(parents=True,exist_ok=True)
        prefs={'browser.download.folderList':2,'browser.download.dir':str(downloads),
               'browser.download.useDownloadDir':True,'browser.download.alwaysOpenPanel':False,
               'browser.helperApps.neverAsk.saveToDisk':'application/json,image/svg+xml'}
        if reduced:prefs['ui.prefersReducedMotion']=1
        (Path(profile)/'user.js').write_text('\n'.join(f'user_pref({json.dumps(k)}, {json.dumps(v)});' for k,v in prefs.items()))
        server=subprocess.Popen(['python3','-m','app.server'],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        browser=None;m=None
        try:
            for _ in range(60):
                try:urllib.request.urlopen('http://127.0.0.1:18082/health',timeout=1);break
                except OSError:time.sleep(.1)
            # Exercise HTTP rejection and ensure API can serve different visitors.
            for data,status in [({'model':'phillips','parameters':{'u':8}},200),({'model':'phillips','parameters':{'u':-1}},400)]:
                req=urllib.request.Request('http://127.0.0.1:18082/api/lab',json.dumps(data).encode(),{'Content-Type':'application/json'})
                try:response=urllib.request.urlopen(req);assert response.status==status
                except urllib.error.HTTPError as e:assert e.code==status
            browser=subprocess.Popen(['firefox','--headless','--no-remote','--marionette','--profile',profile],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            for _ in range(120):
                try:m=Marionette();break
                except OSError:time.sleep(.2)
            if m is None:raise RuntimeError('Firefox indisponible')
            m.command('WebDriver:NewSession',{'capabilities':{'alwaysMatch':{'acceptInsecureCerts':True}}})
            m.command('WebDriver:SetWindowRect',{'width':1440,'height':1100})
            m.command('WebDriver:Navigate',{'url':'http://127.0.0.1:18082'})
            m.wait("document.getElementById('lab-status').textContent==='À jour'")
            assert m.js("return document.querySelectorAll('.relation-buttons a').length")==6
            assert m.js("return document.querySelector('.north strong').textContent")=='Croissance'
            assert m.js("return document.querySelector('.east strong').textContent")=='Extérieur'
            assert m.js("return document.getElementById('home-values').textContent.includes('Non calculé')")
            def screenshot(name):
                shots=ROOT/'tests'/'artifacts';shots.mkdir(exist_ok=True)
                (shots/name).write_bytes(base64.b64decode(m.command('WebDriver:TakeScreenshot',{'full':True})['value']))
            screenshot('kaldor-desktop.png')
            def navigate(model):
                m.js(f"location.hash='{model}';return true;")
                m.wait(f"document.getElementById('model-title').textContent==={json.dumps({'wsps':'WS–PS','phillips':'Phillips & anticipations','okun':'Loi d’Okun'}[model])} && document.getElementById('lab-status').textContent==='À jour'")
            def setvalue(key,value):
                m.js(f"let e=document.getElementById('number-{key}');e.value={json.dumps(value)};e.dispatchEvent(new Event('input',{{bubbles:true}}));return true;")
                m.wait("document.getElementById('lab-status').textContent==='À jour'")
            def metric(index=0):return m.js(f"return document.querySelectorAll('#lab-metrics strong')[{index}].textContent")
            navigate('wsps')
            assert metric()=='10'
            assert metric(1)=='100'
            m.js("document.getElementById('bridge-button').click();return true;")
            m.wait("document.getElementById('bridge-status').textContent.includes('Confirmer')")
            setvalue('mu',40)
            assert metric()=='14,76'
            m.js("document.getElementById('bridge-accepted').checked=true;document.getElementById('bridge-button').click();return true;")
            m.wait("location.hash==='#phillips' && document.getElementById('lab-status').textContent==='À jour'")
            assert m.js("return document.getElementById('link-provenance').textContent.includes('importé de WS–PS')")
            assert abs(float(m.js("return document.getElementById('number-ustar').value"))-14.761904)<1e-5
            # Reset then point movement vs curve shift.
            m.js("document.getElementById('lab-reset').click();return true;")
            m.wait("document.getElementById('lab-status').textContent==='À jour'")
            setvalue('u',8)
            assert metric()=='3'
            assert 'le long' in m.js("return document.getElementById('mechanism-kind').textContent")
            setvalue('cost',2)
            assert metric()=='5'
            assert 'Déplacement de la courbe' in m.js("return document.getElementById('mechanism-kind').textContent")
            # Rapid consecutive requests, latest result wins.
            m.js("for(let i=0;i<20;i++){let e=document.getElementById('number-u');e.value=10+i/10;e.dispatchEvent(new Event('input'));}return true;")
            m.wait("document.getElementById('lab-status').textContent==='À jour'")
            assert metric()=='3,05'
            # Actual trajectory, adaptation lambda .5 and fixed u=8.
            m.js("document.getElementById('lab-reset').click();return true;")
            m.wait("document.getElementById('lab-status').textContent==='À jour'")
            setvalue('u',8)
            m.js("document.getElementById('expectations').value='adaptive';document.getElementById('expectations').dispatchEvent(new Event('change'));document.getElementById('temporal').checked=true;document.getElementById('temporal').dispatchEvent(new Event('change'));return true;")
            m.wait("document.getElementById('trajectory-table').children.length===13 && document.getElementById('lab-status').textContent==='À jour'")
            assert metric()=='3'
            m.js("document.getElementById('lab-step').click();return true;")
            m.wait("document.getElementById('lab-status').textContent==='À jour'")
            assert metric()=='3,5'
            assert m.js("return document.getElementById('position-label').textContent").endswith('t1')
            screenshot('phillips-desktop.png')
            # JSON export then upload through the real input.
            before=set(downloads.glob('*.json'))
            m.js("document.getElementById('save-scenario').click();return true;")
            until=time.monotonic()+10
            while time.monotonic()<until:
                new=set(downloads.glob('*.json'))-before
                complete=[path for path in new if path.stat().st_size>0]
                if complete:
                    try:
                        saved=complete[0];data=json.loads(saved.read_text());break
                    except json.JSONDecodeError:pass
                time.sleep(.1)
            else:raise AssertionError('Le fichier JSON doit être réellement téléchargé')
            assert data['parameters']['u']==8 and data['period']==1
            setvalue('u',12)
            elem=m.command('WebDriver:FindElement',{'using':'css selector','value':'#load-scenario'})
            element=elem['value']
            identifier=element.get('element-6066-11e4-a52e-4f735466cecf',element.get('ELEMENT'))
            m.command('WebDriver:ElementSendKeys',{'id':identifier,'text':str(saved),'value':[str(saved)]})
            m.wait("document.getElementById('file-status').textContent.includes('rechargés')")
            assert metric()=='3,5'
            # SVG actual export contains graphical data and provenance.
            previous=set(downloads.glob('*.svg'))
            m.js("document.getElementById('export-svg').click();return true;")
            until=time.monotonic()+10
            while time.monotonic()<until:
                new_svg=set(downloads.glob('*.svg'))-previous
                complete_svg=[path for path in new_svg if path.stat().st_size>0]
                if complete_svg:
                    svg_path=complete_svg[0];content=svg_path.read_text()
                    if '<metadata' in content and 'polyline' in content:break
                time.sleep(.1)
            else:raise AssertionError('Un fichier SVG complet avec courbes et métadonnées doit être téléchargé')
            # Okun, keyboard, domains and discrete comparison.
            navigate('okun');setvalue('growth',1)
            assert metric()=='0,4'
            assert metric(1)=='10,4'
            m.js("document.getElementById('control-growth').focus();return true;")
            m.command('WebDriver:PerformActions',{'actions':[{'type':'key','id':'keys','actions':[{'type':'keyDown','value':'\ue014'},{'type':'keyUp','value':'\ue014'}]}]})
            m.wait("document.getElementById('number-growth').value==='1.1'")
            setvalue('growth',4)
            m.js("document.getElementById('lab-compare').click();return true;")
            m.wait("document.getElementById('lab-status').textContent==='À jour'")
            assert metric()=='0'
            m.js("document.getElementById('lab-step').click();return true;")
            m.wait("document.getElementById('lab-status').textContent==='À jour'")
            assert metric()=='−0,2' or metric()=='-0,2'
            scale=m.js("return [...document.querySelectorAll('#lab-chart text')].slice(0,11).map(n=>n.textContent)")
            m.js("document.getElementById('lab-play').click();return true;")
            if reduced:
                m.wait("document.getElementById('lab-status').textContent.includes('animations réduites')")
            else:
                m.wait("Number(document.getElementById('position').value)>40")
                m.js("document.getElementById('lab-pause').click();return true;")
                pos=m.js("return document.getElementById('position').value");time.sleep(.25)
                assert pos==m.js("return document.getElementById('position').value")
                m.js("document.getElementById('lab-play').click();return true;")
                m.wait("document.getElementById('position').value==='100' && document.getElementById('lab-status').textContent==='À jour'")
            assert metric() in ('−0,8','-0,8')
            assert scale==m.js("return [...document.querySelectorAll('#lab-chart text')].slice(0,11).map(n=>n.textContent)")
            setvalue('initial_u',0)
            assert metric(1)=='—'
            assert 'hors' in m.js("return document.getElementById('lab-warnings').textContent")
            # Narrow screen, independent second tab, no external requests.
            m.command('WebDriver:SetWindowRect',{'width':390,'height':844})
            assert m.js('return document.documentElement.scrollWidth<=innerWidth')
            assert m.js("return document.querySelector('#workshop .controls').getBoundingClientRect().top>=document.querySelector('#workshop .chart-card').getBoundingClientRect().bottom")
            screenshot('okun-mobile.png')
            m.js("location.hash='accueil';return true;")
            m.wait("!document.getElementById('home').hidden")
            assert m.js('return document.documentElement.scrollWidth<=innerWidth')
            screenshot('kaldor-mobile.png')
            assert m.js("return performance.getEntriesByType('resource').every(r=>r.name.startsWith(location.origin))")
            tab=m.command('WebDriver:NewWindow',{'type':'tab'})['handle'];m.command('WebDriver:SwitchToWindow',{'handle':tab})
            m.command('WebDriver:Navigate',{'url':'http://127.0.0.1:18082/#okun'})
            m.wait("document.getElementById('lab-status').textContent==='À jour'")
            assert metric()=='0'
            print('OK : accueil et 6 relations ; parcours WS–PS → Phillips → Okun ; consentement de liaison ; unités ; anticipations ; 20 entrées rapides ; clavier ; comparaisons et échelles ; téléchargement JSON, rechargement et SVG ; mobile ; état indépendant ; mode réduit='+str(reduced))
        except Exception:
            if m:
                try:
                    (ROOT/'tests'/'artifacts'/'failure.png').write_bytes(base64.b64decode(m.command('WebDriver:TakeScreenshot',{'full':True})['value']))
                    print('Page:',m.js('return document.body.innerText').__str__()[:3500])
                except Exception:pass
            raise
        finally:
            if browser:browser.terminate();browser.wait(timeout=15)
            server.terminate();server.wait(timeout=10)

if __name__=='__main__':run()
