import AppKit
import os, sys
from vanilla import  Window, EditText, TextBox, Box, List, Button, Tabs, LevelIndicatorListCell
from defconAppKit.controls.glyphCollectionView import GlyphCollectionView
from mojo.roboFont import OpenWindow
from variableValues.dialogs.base import DesignSpaceSelector

'''
A tool to check sources for glyph consistency between each other.

'''

def getSegmentTypes(glyph):
    segments = []
    for ci, c in enumerate(glyph.contours):
        for si, s in enumerate(c.segments):
            if s.type == 'curve':
                segmentType = 'C'
            elif s.type == 'qcurve':
                segmentType = 'Q'
            else:
                segmentType = 'L'
            segments.append(segmentType)
        # segments.append(' ')
    return segments


class VarGlyphAssistant(DesignSpaceSelector):
    
    title         = 'VarGlyph Assistant'
    key           = 'com.hipertipo.varGlyphAssistant'

    _colGlyphs    = 100
    _colFontName  = 240
    _colValue     = 80

    _tabsTitles   = ['designspace', 'glyphs', 'attributes', 'compatibility', 'relationships']

    _glyphAttrs       = {}
    _glyphAttrsLabels = [
        'width',
        'left',
        'right',
        'contours',
        'segments',
        'points',
        'anchors',
        'components',
    ]

    _glyphCompatibility  = {}

    _glyphTestsLabels = [
        'Name',
        'Glyph 2',
        'Formula',
    ]
    _glyphTests = [
        'is centered',
        'match left',
        'match right',
        'match width',
    ]

    def __init__(self):
        self.w = Window(
                (self.width, self.height), title=self.title,
                minSize=(self.width*0.9, 360))

        x = y = p = self.padding
        self.w.tabs = Tabs((x, y, -p, -p), self._tabsTitles)

        self.initializeDesignspacesTab()
        self.initializeGlyphsTab()
        self.initializeAttributesTab()
        self.initializeCompatibilityTab()
        self.initializeValidationTab()

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    # initialize UI

    def initializeGlyphsTab(self):

        tab = self._tabs['glyphs']

        x = p = self.padding
        y = p/2
        tab.glyphNameFilesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'glyph name files')

        y += self.lineHeight + p/2
        tab.glyphNameFiles = List(
                (x, y, -p, self.lineHeight*5),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                # selectionCallback=self.selectGlyphAttrsCallback,
            )

        y += self.lineHeight*5 + p
        tab.glyphsNamesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'glyph names')

        y += self.lineHeight + p/2
        tab.glyphNames = EditText(
                (x, y, -p, -self.lineHeight-p*2),
                'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z',
            )

        # tab.glyphs = GlyphCollectionView((x, y, -p, -self.lineHeight -p*2),
        #     # allowDrag=True,
        #     # selectionCallback=self.collectionViewSelectionCallback,
        #     # doubleClickCallback=self.collectionViewDoubleClickCallback,
        #     # deleteCallback=self.collectionViewDeleteCallback,
        #     # selfDropSettings=selfDropSettings,
        #     # selfApplicationDropSettings=dropSettings
        # )

        y = -(self.lineHeight + p)
        tab.updateGlyphs = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                # callback=self.updateMeasurementsCallback,
            )

    def initializeAttributesTab(self):

        tab = self._tabs['attributes']

        x = p = self.padding
        y = p/2
        tab.glyphsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'glyphs')

        y += self.lineHeight + p/2
        tab.glyphs = List(
                (x, y, self._colGlyphs, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.selectGlyphAttrsCallback,
            )

        y = p/2
        x2 = x + self._colGlyphs + p
        tab.glyphAttributesLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'attributes')

        y += self.lineHeight + p/2
        tab.glyphAttributes = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=[{"title": t, 'width': self._colFontName*1.5, 'minWidth': self._colFontName} if ti == 0 else {"title": t, 'width': self._colValue} for ti, t in enumerate(['file name'] + self._glyphAttrsLabels)],
            )

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.updateAttributesCallback,
            )

    def initializeCompatibilityTab(self):

        tab = self._tabs['compatibility']

        x = p = self.padding
        y = p/2
        tab.glyphsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'glyphs')

        y += self.lineHeight + p/2
        tab.glyphs = List(
                (x, y, self._colGlyphs, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.selectGlyphCompatibilityCallback,
            )

        y = p/2
        x2 = x + self._colGlyphs + p
        tab.segmentsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'segments')

        y += self.lineHeight + p/2
        tab.segments = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                # columnDescriptions=[{"title": t} for t in ['file name'] + list(range(9))],
            )

        # y = -(self.lineHeight*2 + p*4)
        # tab.box = Box((x2, y, -p, self.lineHeight+p*2))
        # tab.box.text = TextBox((p, p/2, -p, self.lineHeight), "")

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.updateCompatibilityCallback,
            )

    def initializeValidationTab(self):

        tab = self._tabs['relationships']

        x = p = self.padding
        y = p/2
        tab.glyphsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'glyphs')

        y += self.lineHeight + p/2
        tab.glyphs = List(
                (x, y, self._colGlyphs, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
            )

        y = p/2
        x2 = x + self._colGlyphs + p
        tab.testsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'test files')

        y += self.lineHeight + p/2
        tab.tests = List(
                (x2, y, -p, self.lineHeight*5),
                [], # testItems,
                allowsMultipleSelection=True,
                allowsEmptySelection=False,
                # columnDescriptions=[{"title": t} for t in self._glyphTestsLabels],
            )

        y += self.lineHeight*5 + p
        tab.resultsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'test results')

        y += self.lineHeight + p/2
        _columnDescriptions  = [{"title": t, 'minWidth': self._colFontName, 'width': self._colFontName*1.5} for t in ['file name']]
        _columnDescriptions += [{"title": t, 'width': self._colValue} for t in self._glyphTests]
        tab.results = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                columnDescriptions=_columnDescriptions,
            )

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                # callback=self.updateMeasurementsCallback,
            )

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedGlyphAttributes(self):
        tab = self._tabs['attributes']
        selection = tab.glyphs.getSelection()
        glyphs = tab.glyphs.get()
        selectedGlyphs = [a for i, a in enumerate(glyphs) if i in selection]
        if not len(selectedGlyphs):
            return
        return selectedGlyphs[0]

    @property
    def selectedGlyphCompatibility(self):
        tab = self._tabs['compatibility']
        selection = tab.glyphs.getSelection()
        glyphs = tab.glyphs.get()
        selectedGlyphs = [a for i, a in enumerate(glyphs) if i in selection]
        if not len(selectedGlyphs):
            return
        return selectedGlyphs[0]

    # ---------
    # callbacks
    # ---------

    # attributes

    def updateAttributesCallback(self, sender):
        
        if not self.selectedSources:
            return

        tab = self._tabs['attributes']
        glyphNames = self._tabs['glyphs'].glyphNames.get().split(' ')

        # collect glyph values into dict
        self._glyphAttrs = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)

            self._glyphAttrs[sourceFileName] = {}
            for glyphName in glyphNames:
                g = f[glyphName]
                self._glyphAttrs[sourceFileName][glyphName] = {}
                for attr in self._glyphAttrsLabels:
                    if attr == 'width':
                        value = g.width
                    elif attr == 'left':
                        value = g.leftMargin
                    elif attr == 'right':
                        value = g.rightMargin
                    elif attr == 'contours':
                        value = len(g.contours)
                    elif attr == 'segments':
                        value = 0
                        for c in g.contours:
                            value += len(c)
                    elif attr == 'points':
                        value = 0
                        for c in g.contours:
                            value += len(c.points)
                    elif attr == 'anchors':
                        value = len(g.anchors)
                    elif attr == 'components':
                        value = len(g.components)
                    self._glyphAttrs[sourceFileName][glyphName][attr] = value

            # f.close()

        tab.glyphs.set(glyphNames)
        tab.glyphs.setSelection([0])
        self.selectGlyphAttrsCallback(None)

    def selectGlyphAttrsCallback(self, sender):
        tab = self._tabs['attributes']
        glyphName = self.selectedGlyphAttributes

        listItems = []
        for sourceFileName in self._glyphAttrs:
            listItem = { 'file name' : sourceFileName }
            for attr in self._glyphAttrs[sourceFileName][glyphName]:
                listItem[attr] = self._glyphAttrs[sourceFileName][glyphName][attr]
            listItems.append(listItem)

        tab.glyphAttributes.set(listItems)

    # compatibility

    def updateCompatibilityCallback(self, sender):

        if not self.selectedSources:
            return

        tab = self._tabs['compatibility']
        glyphNames = self._tabs['glyphs'].glyphNames.get().split(' ')

        # collect glyph compatibility data into dict
        self._glyphCompatibility = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)

            self._glyphCompatibility[sourceFileName] = {}
            for glyphName in glyphNames:
                g = f[glyphName]
                segments = getSegmentTypes(g)
                self._glyphCompatibility[sourceFileName][glyphName] = segments

            # f.close()

        tab.glyphs.set(glyphNames)
        tab.glyphs.setSelection([0])
        self.selectGlyphCompatibilityCallback(None)

    def selectGlyphCompatibilityCallback(self, sender):

        tab = self._tabs['compatibility']
        glyphName = self.selectedGlyphCompatibility

        segmentsPosSize = tab.segments.getPosSize()
        del tab.segments

        sMax = 0
        for sourceFileName in self._glyphCompatibility:
            segmentsGlyph = self._glyphCompatibility[sourceFileName][glyphName]
            if len(segmentsGlyph) > sMax:
                sMax = len(segmentsGlyph)

        listItems = []
        segmentsGlyphs = []
        for sourceFileName in self._glyphCompatibility:
            listItem = { 'file name' : sourceFileName }
            segmentsGlyph = self._glyphCompatibility[sourceFileName][glyphName]
            for si, segment in enumerate(segmentsGlyph):
                listItem[str(si)] = segment
            listItems.append(listItem)
            segmentsGlyphs.append(segmentsGlyph)

        for S in segmentsGlyphs:
            print(S)

        segmentsDescriptions  = [{'title': 'file name', 'minWidth': self._colFontName, 'width': self._colFontName*1.5}]
        segmentsDescriptions += [{'title': str(i), 'width': 20} for i in range(sMax)]

        # create list UI with sources
        tab.segments = List(
                segmentsPosSize, listItems,
                columnDescriptions=segmentsDescriptions,
                allowsMultipleSelection=True,
                enableDelete=False,
                allowsEmptySelection=False,
            )

    # validation


if __name__ == '__main__':

    OpenWindow(VarGlyphAssistant)

