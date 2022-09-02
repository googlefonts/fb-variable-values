import os, time
from hTools3.objects.hproject import hProject
from fontParts.world import OpenFont

print(os.getcwd())

def drawGlyph(g):
    if g.components:
        g.decompose()
    bez = BezierPath()
    g.draw(bez)
    drawPath(bez)

start = time.time()

# ---------
# functions
# ---------

def getAllKerningPairs(project, fontNames=None):
    allPairs = []
    if fontNames is None:
       fontNames = project.fonts.keys() 
    for sourceName, sourcePath in project.fonts.items():
        if sourceName not in fontNames:
            continue
        f = OpenFont(sourcePath, showInterface=False)
        allPairs += f.kerning.keys()
    return sorted(list(set(allPairs)))

def readKerningPairs(pairsListPath):
    allPairs = []
    with open(pairsListPath, mode='r', encoding='utf-8') as T:
        for L in T.readlines():
            g1, g2 = L.split(',')
            g1 = g1.strip()
            g2 = g2.strip()
            allPairs.append((g1, g2))
    return allPairs

def writeKerningPairs(project, pairsListPath, fontNames=None):
    allPairs = getAllKerningPairs(project, fontNames)
    txt = ''
    for g1, g2 in allPairs:
        txt += f'{g1}, {g2}\n'
    with open(pairsListPath, mode='w', encoding='utf-8') as T:
        T.write(txt)

# --------
# settings
# --------

wdths = [1, 5, 9]
wght  = 9
cntr  = 5
slnt  = 'A'

n, s = 573, 10 # int(n), int(s)
S = 0.085

lh = 1080
savePDF = False

# -----
# setup
# -----

folder   = '/hipertipo/fonts/Publica'

p = hProject(folder)

fontNames = [f'{wght}{wdth}{cntr}{slnt}' for wdth in wdths]

pairsListPath = os.path.join(p.libsFolder, 'kerning-pairs-all.txt')

writeKerningPairs(p, pairsListPath, fontNames)

start, end = n-1, n+s
totalPairs = readKerningPairs(pairsListPath)
allPairs = totalPairs[start:end]
print(start, end)

# # pairs = [
# #     ('R', 'B.sc'),
# #     ('R', 'D.sc'),
# #     ('R', 'F.sc'),
# #     # ('public.kern1.A', 'V.sc'),
# #     # ('V', 'public.kern2.A'),
# #     # ('V.sc', 'public.kern2.A'),
# # ]
# # allPairs = pairs

# -----
# draw!
# -----

txtBeforeUC = list('HOH')
txtAfterUC  = list('HOH')

txtBeforeLC = list('non')
txtAfterLC  = list('non')

# collect pairs
D = {}
for wdth in wdths:
    fontName = f'{wght}{wdth}{cntr}{slnt}'
    f = OpenFont(p.fonts[fontName], showInterface=False)
    D[fontName] = {}
    for pair in allPairs:
        k = f.kerning.get(pair)
        D[fontName][pair] = k
    f.close()

# draw pairs
for i, pair in enumerate(allPairs):
    g1, g2 = pair

    newPage('A4Landscape')
    fill(1, 0, 0)
    text(f'{g1} / {g2}', (40, height()-30), align='left')
    text(f'{n+i} / {len(totalPairs)}', (width()-40, height()-30), align='right')

    # blendMode('multiply')
    translate(40, height()*0.8)
    scale(S)

    for wdth in wdths:
        save()            
        fontName = f'{wght}{wdth}{cntr}{slnt}'
        f = OpenFont(p.fonts[fontName], showInterface=False)
        # k = f.kerning.get((g1, g2))
        k = D[fontName][(g1, g2)]
        k1 = g1.replace('public.kern1.', '')
        k2 = g2.replace('public.kern2.', '')

        # hack for Publica
        if k1 == 'a_alt2':
            k1 = k1.replace('_', '.')

        fill(0.5)
        if k1 in p.groups['latin_uc_basic']: # + p.groups['latin_uc_extra']:
            txtBefore = txtBeforeUC
        elif '.sc' in k1:
            txtBefore = [f'{g}.sc' for g in txtBeforeUC]
        else:
            txtBefore = txtBeforeLC
        
        for gName in txtBefore:
            g = f[gName]
            drawGlyph(g)
            translate(g.width, 0)

        fill(0)
        drawGlyph(f[k1])
        translate(f[k1].width, 0)

        yMin = -abs(f.info.descender)
        yMax = f.info.ascender
        if k is not None:
            with savedState():
                if k > 0:
                    fill(0, 0, 1, 0.35)
                else:
                    fill(1, 0, 0, 0.35)
                rect(0, yMin, k, abs(yMin)+yMax)
            translate(k, 0)

        drawGlyph(f[k2])
        fontSize(120)
        fill(1, 0, 0)
        if k:
            text(str(k), (abs(k)+10, yMin))
        translate(f[k2].width, 0)

        if k2 in p.groups['latin_uc_basic']: # + p.groups['latin_uc_extra']:
            txtAfter = txtAfterUC
        elif '.sc' in k2:
            txtAfter = [f'{g}.sc' for g in txtAfterUC]
        else:
            txtAfter = txtAfterLC

        fill(0.5)
        for gName in txtAfter:
            g = f[gName]
            drawGlyph(g)
            translate(g.width, 0)

        f.close()
        # translate(f['space'].width, 0)
        restore()
        translate(0, -lh)

    translate(0, -lh*0.25)

# # if savePDF:       
# #     pdfPath = os.path.join(folderPDFs, f'small-caps-ufos-proof_{style}.pdf')
# #     saveImage(pdfPath)
# #     print(pdfPath)

# end = time.time() 
# print(f"Finished in {((end - start)/1000)%60:.2f} seconds")
