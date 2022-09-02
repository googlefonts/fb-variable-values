from importlib import reload

import os, shutil, pathlib
from mojo.extensions import ExtensionBundle
from hTools3.modules.sys import pycClear, pyCacheClear, removeGitFiles

# --------
# settings
# --------

version          = '0.1.1'
baseFolder       = os.path.dirname(__file__)
libFolder        = os.path.join(baseFolder, 'code', 'Lib')
licensePath      = None # os.path.join(baseFolder, 'license.txt')
resourcesFolder  = None # os.path.join(baseFolder, 'Resources')
imagePath        = None # os.path.join(resourcesFolder, 'punch.png')

outputFolder     = baseFolder 
extensionPath    = os.path.join(outputFolder, 'VariableSpacing.roboFontExt')
docsFolder       = None # os.path.join(outputFolder, 'docs', '_site')

# ---------------
# build extension
# ---------------

def buildExtension():

    pycOnly = False # [ "3.6", "3.7" ]

    B = ExtensionBundle()
    B.name                 = "Variable Spacing"
    B.developer            = 'Gustavo Ferreira'
    B.developerURL         = 'http://hipertipo.com/'
    B.icon                 = imagePath
    B.version              = version
    B.expireDate           = '' # '2020-12-31'
    B.launchAtStartUp      = True
    B.html                 = False
    B.mainScript           = 'start.py'
    # B.uninstallScript      = ''
    B.requiresVersionMajor = '3'
    B.requiresVersionMinor = '4'
    B.addToMenu = [
        {
            'path'          : 'variableSpacing/dialogs/variableSpacingTool.py',
            'preferredName' : 'Spacing States',
            'shortKey'      : '',
        },
    ]
    # with open(licensePath) as license:
    #     B.license = license.read()

    if os.path.exists(extensionPath):
        print('\tdeleting existing .roboFontExt package...')
        shutil.rmtree(extensionPath)

    print('\tbuilding .roboFontExt package...')
    B.save(extensionPath,
        libPath=libFolder,
        # htmlPath=None, # docsFolder,
        resourcesPath=resourcesFolder,
        # pycExclude=pycExcludeFiles,
        pycOnly=pycOnly)

    errors = B.validationErrors()
    if len(errors):
        print('ERRORS:')
        print(errors)

# ---------------
# build extension
# ---------------

pycClear(baseFolder)
pyCacheClear(baseFolder)
print(f'building Variable Spacing extension {version}...\n')
buildExtension()
print('\n...done!\n')
