from browser import document, html, ajax, window, alert
import urllib.request
from javascript import JSON

moogleid = '904000103'
containerid = '904000115'
containername = {'en':'Prism Moogle', 'ko':'프리즘 모그리', 'zh':'信賴度莫古利（原晶）', 'es':'Moguri prismático', 'de':'Prismamogry', 'fr':'Prismog'}

def loadlanguage(event):
    global code
    code = event.target.value
    for b in lang_buttons:
        if 'active' in b.classList:
            b.classList.remove('active')
    event.target.classList.add('active')

def moogles(event):
    filestatus.textContent = '\t\t\t⏳'
    languages = ['de', 'es', 'fr', 'ko', 'zh']
    try:
        reqw = ajax.ajax()
        requ = ajax.ajax()
        if code in languages:
            reqw.open('GET', 'https://raw.githubusercontent.com/lyrgard/ffbeEquip/master/static/GL/data_' + code + '.json', False)
            requ.open('GET', 'https://raw.githubusercontent.com/lyrgard/ffbeEquip/master/static/GL/units_' + code + '.json', False)
        else:
            reqw.open('GET', 'https://raw.githubusercontent.com/lyrgard/ffbeEquip/master/static/GL/data.json', False)
            requ.open('GET', 'https://raw.githubusercontent.com/lyrgard/ffbeEquip/master/static/GL/units.json', False)
        reqw.bind('complete', reqwComplete)
        requ.bind('complete', requComplete)
        requ.send()
        reqw.send()
    except:
        alert("Error: Can't connect to ffbebuilder!")
        filestatus.textContent = '\t\t\t❌'
    reader = window.FileReader.new()
    try:
        reader.readAsText(choosefile.files[0])
        reader.bind('load', process_inventory)
        filestatus.textContent = '\t\t\t✔️'
    except IndexError:
        alert('Error: No file was selected!')
        filestatus.textContent = '\t\t\t❌'
    except:
        alert('Error: Invalid file!')
        filestatus.textContent = '\t\t\t❌'
    

def process_inventory(event):
    global inventory
    try:
        inventory = JSON.parse(event.target.result)   
        fusedict = {}
        mooglelist = [u['tmrId'] for u in inventory if u['id'] == moogleid]
        containerlist = [u['tmrId'] for u in inventory if u['id'] == containerid if u['tmr'] <1000]
        ownedunits = [u['id'][:-1] for u in inventory if u['id'][0] != '9' if u['tmr'] <1000 ]
        for tmrId in mooglelist:
            tmrName = weapondict[tmrId]['name']
            tmrUnit = weapondict[tmrId]['tmrUnit']
            unitName = unitdict[tmrUnit]['name']
            if tmrUnit[:-1] in ownedunits:
                    if tmrId in fusedict.keys():
                        fusedict[tmrId]['count'] += 1
                    else:
                        fusedict.update({tmrId:{'tmr':tmrName, 'unit':unitName, 'count':1, 'unitid':tmrUnit}})
            elif tmrId in containerlist:
                    if tmrId in fusedict.keys():
                        fusedict[tmrId]['count'] += 1
                    else:
                        fusedict.update({tmrId:{'tmr':tmrName, 'unit':containername[code], 'count':1, 'unitid':containerid}})        
        fusesort = sorted(fusedict.items(), key = lambda item: item[1]['tmr'])
        document['results'].clear()
        table = html.TABLE(Class='table table-hover')
        tbody = html.TBODY()
        table <= tbody
        for l in fusesort:
            tbody <= html.TR([html.TD(l[1]['tmr']), html.TD('\tx' + str(l[1]['count']) + '\t'), html.TD(l[1]['unit']), html.TD(html.IMG(src='https://ffbeequip.com/img/units/unit_icon_' + l[1]['unitid'] + '.png' ) )] )
        document['results'] <= table
    except:
        alert('Error: Invalid file!')
        filestatus.textContent = '\t\t\t❌'     

def reqwComplete(request):
    global weapondict
    weapondata = JSON.parse(request.responseText)
    weapondict = {w['id']:{'name':w['name'], 'tmrUnit':w['tmrUnit']} for w in weapondata if 'tmrUnit' in w.keys()}

def requComplete(request):
    global unitdict
    unitdict = JSON.parse(request.responseText)
          

code = 'en'
toolbar = html.DIV(id='toolbar', Class='container-fluid mx-3 mb-1')
document <= toolbar
langbar = html.DIV(id="langbar", Class="btn-group btn-group-toggle px-3", data_toggle="buttons", role="group", aria_label="Select language")
langlabel = html.BUTTON(Class='btn-secondary rounded-left', disabled=True)
langtext = document.createTextNode('Select language:     ')
langlabel <= langtext
langbar <= langlabel
toolbar <= langbar
filestatus = document.createTextNode('\t\t\t ')
res = document.createTextNode('')
docbar = html.DIV(id='docbar', Class='btn-group px-3')
doclabel = html.BUTTON(Class='btn-secondary rounded-left', disabled=True)
doctext = document.createTextNode('Select file:     ')
doclabel <= doctext
docbar <= doclabel
toolbar <= docbar
choosefile = html.INPUT(type='file', Class='btn btn-outline-primary')
docbar <= choosefile
buttonrun = html.BUTTON(id='buttonrun',  Class='btn btn-primary px-3')
buttontext = document.createTextNode('Show moogles!')
buttonrun <= buttontext
toolbar <= buttonrun
toolbar <= filestatus

results = html.SPAN(id='results', Class='zone')
document <= results

unitdict = {}
weapondict = {}
inventory = {}
flags = {'en':'🇬🇧', 'de':'🇩🇪', 'es':'🇪🇸', 'fr':'🇫🇷', 'ko':'🇰🇷', 'zh':'🇨🇳'}

lang_buttons = []
for l, f in flags.items():
    if l == 'en':
        elt = html.BUTTON(Class='btn btn-outline-primary active', type='radio', name='lang', value=l, checked='true', data_toggle='button')
    else:
        elt = html.BUTTON(Class='btn btn-outline-primary', type='radio', name='lang', value=l, data_toggle='button')
    txt = document.createTextNode(f'{f}\t\t\t')
    elt <= txt
    elt.bind('click', loadlanguage)
    langbar.appendChild(elt)
    lang_buttons.append(elt)



buttonrun.bind('click', moogles)
