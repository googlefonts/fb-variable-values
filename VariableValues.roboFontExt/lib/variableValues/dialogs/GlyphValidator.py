import os, sys, glob, csv
from AppKit import NSFilenamesPboardType, NSDragOperationCopy
from vanilla import *
from mojo.UI import AccordionView
from mojo.roboFont import *

'''
A tool to check individual sources for internal consistency.

'''

class GlyphValidator:
    
    title        = 'Glyph Validator'
    key          = 'com.hipertipo.glyphValidator'
    width        = 123*5
    height       = 640
    padding      = 10
    lineHeight   = 22
    verbose      = True
    buttonWidth  = 100

    _colGlyphs   = 120
    _colFontName = 180
    _colValue    = 60

    _tabsTitles  = ['definitions', 'validation']
    _memesTitles = ['glyph name', 'width', 'left', 'right', 'body', 'counter'] 

    _memesFolder = '/Users/sergiogonzalez/Desktop/hipertipo/tools/VariableValues/data/recipes' # '/hipertipo/tools/VarTools/_data/glyphMemes/'
    assert os.path.exists(_memesFolder)

    _fonts = {}

    def __init__(self):
        self.w = FloatingWindow(
                (self.width, self.height), title=self.title,
                minSize=(self.width*0.9, 360))

        x = y = p = self.padding
        self.w.tabs = Tabs((x, y, -p, -p), self._tabsTitles)

        # glyph memes

        tab1 = self.w.tabs[0]

        x, y = p, p/2
        tab1.memesFolderLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'source folder')

        y += self.lineHeight + p/2
        tab1.memesFolder = EditText(
                (x, y, -(self.buttonWidth+p*2), self.lineHeight),
                self._memesFolder)
        
        tab1.memesGetFolder = Button(
                (-(self.buttonWidth+p), y, self.buttonWidth, self.lineHeight),
                'get folder')
        
        y2 = y + self.lineHeight + p
        tab1.memesLabel = TextBox(
                (x, y2, -p, self.lineHeight),
                'glyph memes')

        y2 += self.lineHeight + p/2
        tab1.glyphs = List(
                (x, y2, self._colGlyphs, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.selectMemeCallback,
            )

        x2 = x + self._colGlyphs + p
        tab1.memes = List(
                (x2, y2, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=[{"title": t} for t in self._memesTitles],
            )

        y = -(self.lineHeight + p)
        tab1.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'update',
                # callback=self.updateMeasurementsCallback,
            )

        # validation

        tab2 = self.w.tabs[1]

        x, y = p, p/2
        tab2.fontsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'fonts')

        y += self.lineHeight + p/2
        tab2.fonts = List(
                (x, y, -p, self.lineHeight*5),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                # enableDelete=True,
                # editCallback=self.selectDesignspaceCallback,
                # selectionCallback=self.selectDesignspaceCallback,
                otherApplicationDropSettings=dict(
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
                    callback=self.dropFontsCallback),
            )

        y += self.lineHeight*5 + p
        tab2.memesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'validation results')

        y2 = y + self.lineHeight + p/2
        tab2.glyphs = List(
                (x, y2, self._colGlyphs, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
            )

        x2 = x + self._colGlyphs + p
        tab2.memes = List(
                (x2, y2, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=[{"title": t} for t in self._memesTitles],
                )

        y = -(self.lineHeight + p)
        tab2.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'update',
                # callback=self.updateMeasurementsCallback,
            )

        x += self.buttonWidth + p
        tab2.visualizeValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'visualize',
                # callback=self.visualizeMeasurementsCallback,
            )

        x += self.buttonWidth + p
        tab2.exportValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'export',
                # callback=self.visualizeFontinfoCallback,
            )

        self.loadMemes()
        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedGlyph(self):
        tab = self.w.tabs[0]
        selection = tab.glyphs.getSelection()
        glyphs = tab.glyphs.get()
        selectedGlyphs = [a for i, a in enumerate(glyphs) if i in selection]
        if not len(selectedGlyphs):
            return
        return selectedGlyphs[0]

    # ---------
    # callbacks
    # ---------

    def selectMemeCallback(self, sender):
        csvPath = os.path.join(self._memesFolder, f'{self.selectedGlyph}.csv')
        tab = self.w.tabs[0]

        # reset list
        memesPosSize = tab.memes.getPosSize()
        del tab.memes

        descriptions  = [{"title": self._memesTitles[0], 'width': self._colFontName*1.5, 'minWidth': self._colFontName}]
        descriptions += [{"title": t, 'width': self._colValue} for t in self._memesTitles[1:]]
        listItems = []

        if os.path.exists(csvPath):
            with open(csvPath, mode ='r') as f:
                csvFile = csv.reader(f)
                for lines in csvFile:
                    item = {}
                    for i, t in enumerate(self._memesTitles):
                        item[t] = lines[i]
                    listItems.append(item)

        tab.memes = List(
            memesPosSize,
            listItems,
            columnDescriptions=descriptions)

    def dropFontsCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.ufo']

        if not paths:
            return False

        if not isProposal:
            tab = self.w.tabs[1]
            for path in paths:
                fileName = os.path.splitext(os.path.split(path)[-1])[0]
                self._fonts[fileName] = path
                tab.fonts.append(fileName)
                tab.fonts.setSelection([0])

        return True

    # -------
    # methods
    # -------

    def loadMemes(self):
        tab = self.w.tabs[0]
        csvFolder = tab.memesFolder.get()
        csvFiles = glob.glob(f'{csvFolder}/*.csv')
        glyphNames = sorted([os.path.splitext(os.path.split(f)[-1])[0] for f in csvFiles])
        tab.glyphs.set(glyphNames)
        # load glyph names in validation tab
        tab2 = self.w.tabs[1]
        tab2.glyphs.set(glyphNames)



if __name__ == '__main__':

    OpenWindow(GlyphValidator)

