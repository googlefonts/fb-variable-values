import os, sys
from vanilla import *
from AppKit import NSFilenamesPboardType, NSDragOperationCopy
from mojo.UI import AccordionView
from mojo.roboFont import *
from fontTools.designspaceLib import DesignSpaceDocument

'''
A tool to check sources for glyph consistency between each other.

'''

def getSegmentTypes(glyph):
    segments = []
    for ci, c in enumerate(glyph.contours):
        for si, s in enumerate(c.segments):
            segmentType = 'C' if s.type == 'curve' else 'L'
            segments.append(segmentType)
        # segments.append(' ')
    return segments
    
class VarGlyphAssistant:
    
    title        = 'VarGlyph Assistant'
    key          = 'com.hipertipo.varGlyphAssistant'
    width        = 123*5
    height       = 640
    padding      = 10
    lineHeight   = 22
    verbose      = True
    buttonWidth  = 100

    _colGlyphs   = 100
    _colFontName = 240
    _colValue    = 80

    _tabsTitles = [
        'designspace',
        'attributes',
        'compatibility',
        'validation',
    ]

    _designspaces     = {}
    _sources          = {}

    _glyphAttributes       = {}
    _glyphAttributesLabels = [
        'contours',
        'segments',
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
        'is compatible',
        'match width',
        'match left',
        'match right',
        'match anchors',
        'match components',
    ]

    def __init__(self):
        self.w = FloatingWindow(
                (self.width, self.height), title=self.title,
                minSize=(self.width*0.9, 360))

        x = y = p = self.padding
        self.w.tabs = Tabs((x, y, -p, -p), self._tabsTitles)

        self.initializeDesignspacesTab()
        self.initializeAttributesTab()
        self.initializeCompatibilityTab()
        self.initializeValidationTab()

        self.w.open()

    # initialize UI

    def initializeDesignspacesTab(self):

        tab = self._tabs['designspace']

        x = p = self.padding
        y = p/2
        tab.designspacesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'designspaces')

        y += self.lineHeight + p/2
        tab.designspaces = List(
                (x, y, -p, self.lineHeight*5),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                enableDelete=True,
                # editCallback=self.selectDesignspaceCallback,
                selectionCallback=self.selectDesignspaceCallback,
                otherApplicationDropSettings=dict(
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
                    callback=self.dropDesignspaceCallback),
            )

        y += self.lineHeight*5 + p
        tab.glyphNamesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'glyph names')

        y += self.lineHeight + p/2
        tab.glyphNames = EditText(
                (x, y, -p, self.lineHeight*5),
                'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z',
            )

        y += self.lineHeight*5 + p
        tab.sourcesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'sources')

        y += self.lineHeight + p/2
        tab.sources = List(
                (x, y, -p, -(self.lineHeight + p*2)),
                [],
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
                columnDescriptions=[{"title": t, 'width': self._colFontName*1.5, 'minWidth': self._colFontName} if ti == 0 else {"title": t, 'width': self._colValue} for ti, t in enumerate(['file name'] + self._glyphAttributesLabels) ],
            )

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'update',
                callback=self.updateAttributesCallback,
            )

        x += self.buttonWidth + p
        tab.visualizeValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'visualize',
                # callback=self.visualizeMeasurementsCallback,
            )

        x += self.buttonWidth + p
        tab.exportValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'export',
                # callback=self.visualizeFontinfoCallback,
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

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'update',
                callback=self.updateCompatibilityCallback,
            )

        x += self.buttonWidth + p
        tab.visualizeValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'visualize',
                # callback=self.visualizeMeasurementsCallback,
            )

        x += self.buttonWidth + p
        tab.exportValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'export',
                # callback=self.visualizeFontinfoCallback,
            )

    def initializeValidationTab(self):

        tab = self._tabs['validation']

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
                'tests')

        y += self.lineHeight + p/2
        testItems = []
        for test in self._glyphTests:
            testItem = { 'Name' : test }
            for L in self._glyphTestsLabels[1:]:
                testItem[L] = ''
            testItems.append(testItem)
        tab.tests = List(
                (x2, y, -p, self.lineHeight*8),
                testItems,
                allowsMultipleSelection=True,
                allowsEmptySelection=False,
                columnDescriptions=[{"title": t} for t in self._glyphTestsLabels],
            )

        y += self.lineHeight*8 + p
        tab.resultsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'results')

        y += self.lineHeight + p/2
        tab.results = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                columnDescriptions=[{"title": t} for t in ['file name'] + self._glyphTests],
            )

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'update',
                # callback=self.updateMeasurementsCallback,
            )

        x += self.buttonWidth + p
        tab.visualizeValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'visualize',
                # callback=self.visualizeMeasurementsCallback,
            )

        x += self.buttonWidth + p
        tab.exportValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'export',
                # callback=self.visualizeFontinfoCallback,
            )

    # -------------
    # dynamic attrs
    # -------------

    @property
    def _tabs(self):
        tabsDict = {}
        for tabTitle in self._tabsTitles:
            tabIndex = self._tabsTitles.index(tabTitle)
            tabsDict[tabTitle] = self.w.tabs[tabIndex]
        return tabsDict

    # designspace

    @property
    def selectedDesignspace(self):
        tab = self._tabs['designspace']
        selection = tab.designspaces.getSelection()
        designspaces = tab.designspaces.get()
        selectedDesignspaces = [designspace for i, designspace in enumerate(designspaces) if i in selection]
        if not len(selectedDesignspaces):
            return
        return selectedDesignspaces[0]

    @property
    def selectedDesignspaceDocument(self):
        if not self.selectedDesignspace:
            return
        designspacePath = self._designspaces[self.selectedDesignspace]
        designspace = DesignSpaceDocument()
        designspace.read(designspacePath)
        return designspace

    @property
    def selectedSources(self):
        tab = self._tabs['designspace']
        selection = tab.sources.getSelection()
        sources = tab.sources.get()
        selectedSources = [source for i, source in enumerate(sources) if i in selection]
        if not len(selectedSources):
            return
        return selectedSources

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

    # designspace

    def dropDesignspaceCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.designspace']

        if not paths:
            return False

        if not isProposal:
            tab = self._tabs['designspace']
            for path in paths:
                label = os.path.splitext(os.path.split(path)[-1])[0]
                self._designspaces[label] = path
                tab.designspaces.append(label)
                tab.designspaces.setSelection([0])

        return True

    def selectDesignspaceCallback(self, sender):

        tab = self._tabs['designspace']

        # reset list
        sourcesPosSize = tab.sources.getPosSize()
        del tab.sources

        # empty list
        if not self.selectedDesignspace:
            tab.sources = List(sourcesPosSize, [])
            return

        # get selected designspace
        designspace = self.selectedDesignspaceDocument 

        # get column descriptions
        sourcesDescriptions = [{'title': 'file name', 'minWidth': self._colFontName*2}]
        sourcesDescriptions += [{'title': axis.name, 'width': self._colValue} for axis in designspace.axes]

        # make sources list items
        self._sources = {}
        sourcesItems = []
        for source in designspace.sources:
            sourceFileName = os.path.splitext(os.path.split(source.path)[-1])[0]
            self._sources[sourceFileName] = source.path
            sourceItem = { 'file name' : sourceFileName }
            for axis in designspace.axes:
                sourceItem[axis.name] = source.location[axis.name]
            sourcesItems.append(sourceItem)

        # create sources list UI
        tab.sources = List(
            sourcesPosSize, sourcesItems,
            columnDescriptions=sourcesDescriptions,
            allowsMultipleSelection=True,
            enableDelete=False)

    # attributes

    def updateAttributesCallback(self, sender):
        
        if not self.selectedSources:
            return

        tab = self._tabs['attributes']
        glyphNames = self._tabs['designspace'].glyphNames.get().split(' ')

        # collect glyph values into dict
        self._glyphAttributes = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)

            self._glyphAttributes[sourceFileName] = {}
            for glyphName in glyphNames:
                g = f[glyphName]
                self._glyphAttributes[sourceFileName][glyphName] = {}
                for attr in self._glyphAttributesLabels:
                    if attr == 'contours':
                        value = len(g.contours)
                    elif attr == 'segments':
                        value = 0
                        for c in g.contours:
                            value += len(c)
                    elif attr == 'anchors':
                        value = len(g.anchors)
                    elif attr == 'components':
                        value = len(g.components)
                    self._glyphAttributes[sourceFileName][glyphName][attr] = value

            f.close()

        tab.glyphs.set(glyphNames)
        tab.glyphs.setSelection([0])
        self.selectGlyphAttrsCallback(None)

    def selectGlyphAttrsCallback(self, sender):
        tab = self._tabs['attributes']
        glyphName = self.selectedGlyphAttributes

        listItems = []
        for sourceFileName in self._glyphAttributes:
            listItem = { 'file name' : sourceFileName }
            for attr in self._glyphAttributes[sourceFileName][glyphName]:
                listItem[attr] = self._glyphAttributes[sourceFileName][glyphName][attr]
            listItems.append(listItem)

        tab.glyphAttributes.set(listItems)

    # compatibility

    def updateCompatibilityCallback(self, sender):

        if not self.selectedSources:
            return

        tab = self._tabs['compatibility']
        glyphNames = self._tabs['designspace'].glyphNames.get().split(' ')

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

            f.close()

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
        for sourceFileName in self._glyphCompatibility:
            listItem = { 'file name' : sourceFileName }
            segmentsGlyph = self._glyphCompatibility[sourceFileName][glyphName]
            for si, segment in enumerate(segmentsGlyph):
                listItem[str(si)] = segment
            listItems.append(listItem)

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

