import os, sys, glob, csv
from AppKit import NSFilenamesPboardType, NSDragOperationCopy
from vanilla import *
from mojo.UI import AccordionView
from mojo.roboFont import *

'''
A tool to check individual sources for internal consistency.

'''

class GlyphRelationships:
    
    title        = 'GlyphRelationships'
    key          = 'com.hipertipo.glyphRelationships'

    width        = 123*5
    height       = 640
    padding      = 10
    lineHeight   = 22
    verbose      = True
    buttonWidth  = 100

    _colGlyphs   = 140
    _colFontName = 240
    _colValue    = 80

    _tabsTitles  = ['relationships', 'validation']
    _relationshipsTitles = ['glyph', 'width', 'left', 'right'] # 'body', 'counter'

    _dataFolder = '/Users/sergiogonzalez/Desktop/hipertipo/tools/VariableValues/example/relationships'
    assert os.path.exists(_dataFolder)

    _fonts = {}

    def __init__(self):
        self.w = Window(
                (self.width, self.height), title=self.title,
                minSize=(self.width*0.9, 360))

        x = y = p = self.padding
        # self.w.tabs = Tabs((x, y, -p, -p), self._tabsTitles)

        # glyph relationships

        # tab1 = self.w.tabs[0]

        x, y = p, p/2
        x2 = x + self._colGlyphs + p
        self.w.patternsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'patterns')
        self.w.glyphsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'glyphs')

        y += self.lineHeight + p/2
        self.w.patterns = List(
                (x, y, self._colGlyphs, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                # selectionCallback=self.selectMemeCallback,
            )
        _columnDescriptions = [{"title": t, 'width': self._colGlyphs*1.5, 'minWidth': self._colGlyphs} if i == 0 else {"title": t, 'width': self._colValue} for i, t in enumerate(self._relationshipsTitles)]
        self.w.glyphs = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=_columnDescriptions,
            )

        y = -(self.lineHeight + p)
        self.w.importPatterns = Button(
                (-self.buttonWidth-p, y, self.buttonWidth, self.lineHeight),
                'import',
                # callback=self.updateMeasurementsCallback,
            )

        self.loadMemes()
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
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

    # def selectMemeCallback(self, sender):
    #     csvPath = os.path.join(self._dataFolder, f'{self.selectedGlyph}.csv')
    #     tab = self.w.tabs[0]

    #     # reset list
    #     memesPosSize = tab.memes.getPosSize()
    #     del tab.memes

    #     descriptions  = [{"title": self._relationshipsTitles[0], 'width': self._colFontName*1.5, 'minWidth': self._colFontName}]
    #     descriptions += [{"title": t, 'width': self._colValue} for t in self._relationshipsTitles[1:]]
    #     listItems = []

    #     if os.path.exists(csvPath):
    #         with open(csvPath, mode ='r') as f:
    #             csvFile = csv.reader(f)
    #             for lines in csvFile:
    #                 item = {}
    #                 for i, t in enumerate(self._relationshipsTitles):
    #                     item[t] = lines[i]
    #                 listItems.append(item)

    #     tab.memes = List(
    #         memesPosSize,
    #         listItems,
    #         columnDescriptions=descriptions)

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
        csvFiles = glob.glob(f'{self._dataFolder}/*.csv')
        glyphNames = sorted([os.path.splitext(os.path.split(f)[-1])[0] for f in csvFiles])
        self.w.patterns.set(glyphNames)


if __name__ == '__main__':

    OpenWindow(GlyphRelationships)

