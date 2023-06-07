from importlib import reload
import variableValues.measurements
reload(variableValues.measurements)

import AppKit
import os, csv
from operator import itemgetter, attrgetter
from vanilla import Window, TextBox, List, Button, Tabs, LevelIndicatorListCell
from mojo.roboFont import OpenWindow
from fontParts.world import OpenFont
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.agl import UV2AGL
from variableValues.measurements import * # importMeasurementDescriptionsFromCSV, FontMeasurements, Measurement

class VarFontAssistant:
    
    title             = 'VarFont Assistant'
    key               = 'com.hipertipo.varFontAssistant'
    width             = 123*5
    height            = 640
    padding           = 10
    lineHeight        = 22
    verbose           = True
    buttonWidth       = 100
    _colLeft          = 160
    _colFontName      = 160
    _colValue         = 60
    _tabsTitles       = ['designspace', 'font values', 'measurements', 'glyph values', 'kerning']
    _designspaces     = {}
    _axes             = {}
    _axesOrder        = []
    _axesTitles       = ['name', 'tag', 'minimum', 'maximum', 'default']
    _sources          = {}
    _measurementFiles = {}
    _measurements     = {}
    _fontAttrs    = {
        'unitsPerEm'                   : 'unitsPerEm',
        'xHeight'                      : 'xHeight',
        'capHeight'                    : 'capHeight',
        'descender'                    : 'descender',
        'ascender'                     : 'ascender',
        'italicAngle'                  : 'italic angle',
        'openTypeOS2WeightClass'       : 'OS2 weight',
        'openTypeOS2WidthClass'        : 'OS2 width',
        'openTypeOS2WeightClass'       : 'OS2 weight',
        'openTypeOS2TypoAscender'      : 'OS2 typo ascender',
        'openTypeOS2TypoDescender'     : 'OS2 typo descender',
        'openTypeOS2TypoLineGap'       : 'OS2 line gap',
        'openTypeOS2WinAscent'         : 'OS2 win ascender',
        'openTypeOS2WinDescent'        : 'OS2 win descender',
        'openTypeOS2StrikeoutSize'     : 'OS2 strikeout size',
        'openTypeOS2StrikeoutPosition' : 'OS2 strikeout position',
        'openTypeHheaAscender'         : 'hhea ascender',
        'openTypeHheaDescender'        : 'hhea descender',
        'openTypeHheaLineGap'          : 'hhea line gap',
    }
    _fontValues       = {}
    _glyphNamesAll    = []
    _glyphAttrs       = ['width', 'leftMargin', 'rightMargin']
    _glyphValues      = {}
    _kerningPairsAll  = []
    _kerning          = {}

    def __init__(self):
        self.w = Window(
                (self.width, self.height), title=self.title,
                minSize=(self.width, 360))

        x = y = p = self.padding
        self.w.tabs = Tabs((x, y, -p, -p), self._tabsTitles)

        self.initializeDesignspacesTab()
        self.initializeFontValuesTab()
        self.initializeMeasurementsTab()
        self.initializeGlyphValuesTab()
        self.initializeKerningTab()

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
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
                    type=AppKit.NSFilenamesPboardType,
                    operation=AppKit.NSDragOperationCopy,
                    callback=self.dropDesignspaceCallback),
                )

        y += self.lineHeight*5 + p
        tab.axesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'axes')

        y += self.lineHeight + p/2
        axesDescriptions = [{"title": D} for D in self._axesTitles]
        tab.axes = List(
                (x, y, -p, self.lineHeight*5),
                [],
                drawFocusRing=False,
                editCallback=self.editAxesCallback,
                selfDropSettings=dict(type="genericListPboardType",
                        operation=AppKit.NSDragOperationMove,
                        callback=self.genericDropSelfCallback),
                dragSettings=dict(type="genericListPboardType",
                        callback=self.genericDragCallback),
                columnDescriptions=axesDescriptions,
            )

        y += self.lineHeight*5 + p
        tab.sourcesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'sources')

        y += self.lineHeight + p/2
        tab.sources = List(
                (x, y, -p, -(self.lineHeight + p*2)),
                [])

    def initializeMeasurementsTab(self):

        tab = self._tabs['measurements']

        x = p = self.padding
        y = p/2
        col = self._colLeft
        x2 = x + col + p

        tab.measurementFilesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'measurement files')

        y += self.lineHeight + p/2
        tab.measurementFiles = List(
                (x, y, -p, self.lineHeight*5),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                enableDelete=True,
                # editCallback=self.selectDesignspaceCallback,
                selectionCallback=self.selectMeasurementFileCallback,
                otherApplicationDropSettings=dict(
                    type=AppKit.NSFilenamesPboardType,
                    operation=AppKit.NSDragOperationCopy,
                    callback=self.dropMeasurementFileCallback),
                )

        y += self.lineHeight*5 + p

        # tab.button = Button((x, y, -p, self.lineHeight),
        #         "get measurements…",
        #         # callback=self.buttonCallback,
        #         )

        tab.measurementsLabel = TextBox(
                (x, y, col, self.lineHeight),
                'measurements')

        y += self.lineHeight + p/2
        tab.measurements = List(
                (x, y, col, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.updateMeasurementsCallback,
            )

        y = self.lineHeight*6 + p*2
        tab.fontMeasurementsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'values')

        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", maxValue=1600),
            },
        ]
        y += self.lineHeight + p/2
        tab.fontMeasurements = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                # editCallback=self.editFontInfoValueCallback,
                enableDelete=False)

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.loadFontValuesCallback,
            )

    def initializeFontValuesTab(self):

        tab = self._tabs['font values']

        x = p = self.padding
        y = p/2
        col = self._colLeft
        x2 = x + col + p

        tab.fontAttrsLabel = TextBox(
                (x, y, col, self.lineHeight),
                'attributes')

        y += self.lineHeight + p/2
        tab.fontAttrs = List(
                (x, y, col, -(self.lineHeight + p*2)),
                self._fontAttrs.values(),
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.updateFontValuesCallback,
            )

        y = p/2
        tab.fontInfoLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'values')

        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", maxValue=1600),
            },
        ]
        y += self.lineHeight + p/2
        tab.fontValues = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                # editCallback=self.editFontInfoValueCallback,
                enableDelete=False)

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.loadFontValuesCallback,
            )

        # x += self.buttonWidth + p
        # tab.visualizeValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'visualize',
        #         callback=self.visualizeFontValuesCallback,
        #     )

        # x += self.buttonWidth + p
        # tab.exportValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'export',
        #         # callback=self.exportFontValuesCallback,
        #     )

        x = -(p + self.buttonWidth)
        tab.saveFontValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'save',
                callback=self.saveFontValuesCallback,
            )

    def initializeGlyphValuesTab(self):

        tab = self._tabs['glyph values']

        x = p = self.padding
        y = p/2
        col = self._colLeft
        x2 = x + col + p

        tab.glyphLabel = TextBox(
                (x, y, col, self.lineHeight),
                'glyphs')

        tab.glyphCounter = TextBox(
                (x, y, col, self.lineHeight),
                '',
                alignment='right')

        y += self.lineHeight + p/2
        tab.glyphs = List(
                (x, y, col, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.updateGlyphValuesCallback)

        y = p/2
        tab.glyphAttrsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'attributes')

        y += self.lineHeight + p/2
        tab.glyphAttrs = List(
                (x2, y, -p, self.lineHeight*7),
                self._glyphAttrs,
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.updateGlyphValuesCallback)

        y += self.lineHeight*7 + p
        tab.glyphsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'values')

        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", maxValue=1600),
            },
        ]
        y += self.lineHeight + p/2
        tab.glyphValues = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                editCallback=self.editGlyphValueCallback,
                enableDelete=False)

        y = -(self.lineHeight + p)
        tab.loadValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.loadGlyphAttributesCallback)

        # x += self.buttonWidth + p
        # tab.visualizeValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'visualize',
        #         # callback=self.visualizeGlyphValuesCallback,
        #     )

        # x += self.buttonWidth + p
        # tab.exportValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'export',
        #         # callback=self.exportGlyphValuesCallback,
        #     )

        x = -(p + self.buttonWidth)
        tab.saveValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'save',
                callback=self.saveGlyphValuesCallback)

    def initializeKerningTab(self):

        tab = self._tabs['kerning']

        x = p = self.padding
        y = p/2
        col = self._colLeft * 1.5
        tab.pairsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'pairs')

        tab.pairsCounter = TextBox(
                (x, y, col, self.lineHeight),
                '',
                alignment='right')

        y += self.lineHeight + p/2
        tab.pairs = List(
                (x, y, col, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=[{"title": t} for t in ['1st', '2nd']],
                selectionCallback=self.updateKerningValuesCallback,
            )

        y = p/2
        x2 = x + col + p
        tab.kerningValuesLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'values')

        y += self.lineHeight + p/2
        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", maxValue=200),
            },
        ]
        tab.kerningValues = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                editCallback=self.editKerningCallback,
                enableDelete=False)

        y = -(self.lineHeight + p)
        tab.loadKerningValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.loadKerningPairsCallback,
            )

        # x += self.buttonWidth + p
        # tab.visualizeValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'visualize',
        #         callback=self.visualizeKerningCallback,
        #     )

        # x += self.buttonWidth + p
        # tab.exportValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'export',
        #         callback=self.exportKerningCallback,
        #     )

        x = -(p + self.buttonWidth)
        tab.saveValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'save',
                callback=self.saveKerningCallback,
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
    def sources(self):
        tab = self._tabs['designspace']
        return tab.sources.get()

    @property
    def selectedSources(self):
        tab = self._tabs['designspace']
        selection = tab.sources.getSelection()
        sources = tab.sources.get()
        selectedSources = [source for i, source in enumerate(sources) if i in selection]
        if not len(selectedSources):
            return
        return selectedSources

    # fontinfo

    @property
    def selectedFontAttr(self):
        tab = self._tabs['font values']
        selection = tab.fontAttrs.getSelection()
        fontAttrs = tab.fontAttrs.get()
        selectedFontAttrs = [fontinfo for i, fontinfo in enumerate(fontAttrs) if i in selection]
        if not len(selectedFontAttrs):
            return
        return selectedFontAttrs[0]

    # measurements

    @property
    def selectedMeasurementFile(self):
        tab = self._tabs['measurements']
        selection = tab.measurementFiles.getSelection()
        measurementFiles = tab.measurementFiles.get()
        selectedMeasurementFiles = [measurementFile for i, measurementFile in enumerate(measurementFiles) if i in selection]
        if not len(selectedMeasurementFiles):
            return
        return selectedMeasurementFiles[0]

    @property
    def selectedMeasurements(self):
        tab = self._tabs['measurements']
        selection = tab.measurements.getSelection()
        measurements = tab.measurements.get()
        selectedMeasurements = [m for i, m in enumerate(measurements) if i in selection]
        if not len(selectedMeasurements):
            return
        return selectedMeasurements

    # glyph values

    @property
    def selectedGlyphName(self):
        tab = self._tabs['glyph values']
        i = tab.glyphs.getSelection()[0]
        return self._glyphNamesAll[i], i

    @property
    def selectedGlyphAttrs(self):
        tab = self._tabs['glyph values']
        selection = tab.glyphAttrs.getSelection()
        glyphAttrs = tab.glyphAttrs.get()
        selectedGlyphAttrs = [a for i, a in enumerate(glyphAttrs) if i in selection]
        if not len(selectedGlyphAttrs):
            return
        return selectedGlyphAttrs

    # kerning

    @property
    def selectedKerningPair(self):
        tab = self._tabs['kerning']
        i = tab.pairs.getSelection()[0]
        return self._kerningPairsAll[i], i

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

        sourcesPosSize = tab.sources.getPosSize()
        del tab.sources

        if not self.selectedDesignspace:
            tab.axes.set([])
            tab.sources = List(sourcesPosSize, [])
            return

        designspace = self.selectedDesignspaceDocument 

        # make list items
        self._axes = {}
        axesItems = []
        for axis in designspace.axes:
            axisItem = { attr : getattr(axis, attr) for attr in self._axesTitles }
            axesItems.append(axisItem)

        # create list UI with sources
        tab.axes.set(axesItems)

        # make list items
        sourcesDescriptions  = [{'title': 'file name', 'width': self._colFontName*1.5, 'minWidth': self._colFontName, 'maxWidth': self._colFontName*3}]
        sourcesDescriptions += [{'title': axis.name, 'width': self._colValue} for axis in designspace.axes]
        self._sources = {}
        sourcesItems = []
        for source in designspace.sources:
            sourceFileName = os.path.splitext(os.path.split(source.path)[-1])[0]
            self._sources[sourceFileName] = source.path
            sourceItem = { 'file name' : sourceFileName }
            for axis in designspace.axes:
                sourceItem[axis.name] = source.location[axis.name]
            sourcesItems.append(sourceItem)

        # create list UI with sources
        tab.sources = List(
            sourcesPosSize, sourcesItems,
            columnDescriptions=sourcesDescriptions,
            allowsMultipleSelection=True,
            enableDelete=False)

    def editAxesCallback(self, sender):
        tab = self._tabs['designspace']
        self.axesOrder = [ a['name'] for a in tab.axes.get() ]
        
        if not hasattr(tab, 'sources'):
            return

        _sourceItems = tab.sources.get()
        sourceItems = []
        for item in _sourceItems:
            D = {}
            for k, v in item.items():
                D[k] = v
            sourceItems.append(D)

        sourceItems = sorted(sourceItems, key=itemgetter(*self.axesOrder))
        tab.sources.set(sourceItems)

    def genericDragCallback(self, sender, indexes):
        return indexes

    def genericDropSelfCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        if not isProposal:
            indexes = [int(i) for i in sorted(dropInfo["data"])]
            indexes.sort()
            rowIndex = dropInfo["rowIndex"]
            items = sender.get()
            toMove = [items[index] for index in indexes]
            for index in reversed(indexes):
                del items[index]
            rowIndex -= len([index for index in indexes if index < rowIndex])
            for font in toMove:
                items.insert(rowIndex, font)
                rowIndex += 1
            sender.set(items)
        return True

    # font info values

    def loadFontValuesCallback(self, sender):

        if not self.selectedSources:
            return

        tab = self._tabs['font values']

        # empty list
        if not self.selectedDesignspace:
            tab.fontInfo.set([])
            return

        # collect fontinfo values into dict
        self._fontValues = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)
            info = f.info.asDict()
            self._fontValues[sourceFileName] = {}
            for attr, attrLabel in self._fontAttrs.items():
                self._fontValues[sourceFileName][attrLabel] = info.get(attr)
            f.close()

        self.updateFontValuesCallback(None)

    def updateFontValuesCallback(self, sender):

        tab = self._tabs['font values']

        if not self.selectedSources or not self._fontValues:
            tab.fontValues.set([])
            return

        fontAttr = self.selectedFontAttr

        if self.verbose:
            print('updating font info values...\n')

        # create list items
        values = []
        fontInfoItems = []
        for fontName in self._fontValues.keys():
            value = self._fontValues[fontName][fontAttr]
            if value is None:
                value = '—'
            listItem = {
                "file name" : fontName,
                "value"     : value,
                "level"     : abs(value),
            }
            fontInfoItems.append(listItem)
            values.append(value)

        # set glyph values in table
        fontInfoValuesPosSize = tab.fontValues.getPosSize()
        del tab.fontValues

        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
                'maxWidth' : self._colFontName*3,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", minValue=min(values), maxValue=max(values)),
            },
        ]
        tab.fontValues = List(
            fontInfoValuesPosSize,
            fontInfoItems,
            allowsMultipleSelection=False,
            allowsEmptySelection=False,
            columnDescriptions=columnDescriptions,
            allowsSorting=True,
            editCallback=self.editFontValueCallback,
            enableDelete=False)

    def visualizeFontValuesCallback(self, sender):
        print('visualize font infos')

    def editFontValueCallback(self, sender):
        '''
        Save the edited font value back to the dict, so we can load values for another attribute.

        '''
        tab = self._tabs['font values']
        selection = tab.fontValues.getSelection()
        if not len(selection):
            return

        i = selection[0]
        item = tab.fontValues.get()[i]

        # save change to internal dict
        fontAttr = self.selectedFontAttr
        fontName = item['file name']
        newValue = item['value']
        oldValue = self._fontValues[fontName].get(fontAttr)
        if oldValue != newValue:
            if self.verbose:
                print(f'changed font value {fontAttr} in {fontName}: {oldValue} → {newValue}\n')
            self._fontValues[fontName][fontAttr] = int(newValue)

    def exportFontValuesCallback(self, sender):
        '''
        Export current font values as a CSV file.

        '''
        pass

    def saveFontValuesCallback(self, sender):
        '''
        Save the edited font values back into their source fonts.

        '''
        tab = self._tabs['font values']
        fontAttrs = { v: k for k, v in self._fontAttrs.items() }

        if self.verbose:
            print('saving edited font values to sources...')

        for fontName in self._fontValues.keys():
            sourcePath = self._sources[fontName]
            f = OpenFont(sourcePath, showInterface=False)
            fontChanged = False

            # for attr in self._fontValues[fontName]:
            for attr, newValue in self._fontValues[fontName].items():
                fontAttr = fontAttrs[attr]
                if newValue is None:
                    continue
                if type(newValue) is str:
                    if not len(newValue.strip()):
                        continue
                newValue = float(newValue)
                if newValue.is_integer():
                    newValue = int(newValue)
                oldValue = getattr(f.info, fontAttr)
                if newValue != oldValue:
                    if self.verbose:
                        print(f'\twriting new value for {attr} in {fontName}: {oldValue} → {newValue}')
                    setattr(f.info, fontAttr, newValue)
                    if not fontChanged:
                        fontChanged = True
            if fontChanged:
                # if self.verbose:
                #     print(f'\tsaving {fontName}...')
                f.save()
            f.close()

        if self.verbose:
            print('...done.\n')

    # measurements

    def dropMeasurementFileCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.csv']

        if not paths:
            return False

        if not isProposal:
            tab = self._tabs['measurements']
            for path in paths:
                label = os.path.splitext(os.path.split(path)[-1])[0]
                self._measurementFiles[label] = path
                tab.measurementFiles.append(label)
                tab.measurementFiles.setSelection([0])

        return True

    def selectMeasurementFileCallback(self, sender):

        tab = self._tabs['measurements']

        if not self.selectedMeasurementFile:
            tab.measurements.set([])
            return

        measurementFilePath = self._measurementFiles[self.selectedMeasurementFile]
        measurementTuples = importMeasurementDescriptionsFromCSV(measurementFilePath)
        measurementNames = [m[0] for m in measurementTuples]
        tab.measurements.set(measurementNames)

    def updateMeasurementsCallback(self, sender):

        if not self.selectedMeasurements:
            return

        tab = self._tabs['measurements']

        # empty list
        if not self.selectedMeasurements or not self.selectedSources:
            tab.fontMeasurements.set([])
            return

        # collect measurements into dict
        self._measurements = {}

        measurementFilePath = self._measurementFiles[self.selectedMeasurementFile]
        measurementTuples = importMeasurementDescriptionsFromCSV(measurementFilePath)

        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]

            f = OpenFont(sourcePath, showInterface=False)
            self._measurements[sourceFileName] = {}

            for measurementTuple in measurementTuples:
                if measurementTuple[0] not in self.selectedMeasurements:
                    continue

                M = Measurement(f, measurementTuple)
                measurementKey = measurementTuple[0]
                self._measurements[sourceFileName] = M.value

            f.close()

        # create list items
        values = []
        valuesItems = []
        for fontName, value in self._measurements.items():
            listItem = {
                "file name" : fontName,
                "value"     : value,
                "level"     : abs(value),
            }
            valuesItems.append(listItem)
            values.append(value)

        # set measurement values in table
        valuesPosSize = tab.fontMeasurements.getPosSize()
        del tab.fontMeasurements

        columnDescriptions  = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
                'maxWidth' : self._colFontName*3,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", minValue=min(values), maxValue=max(values)),
            },
        ]
        tab.fontMeasurements = List(
                valuesPosSize,
                valuesItems,
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                # editCallback=self.editGlyphValueCallback,
                enableDelete=False)

    def visualizeMeasurementsCallback(self, sender):
        pass

    def exportMeasurementsCallback(self, sender):
        '''
        Export measurement values as a CSV file.

        '''
        pass

    # glyph values

    def loadGlyphAttributesCallback(self, sender):
        '''
        Read glyph names and glyph values from selected sources and update UI.

        '''

        tab = self._tabs['glyph values']

        # collect glyph names and glyph values in selected fonts
        allGlyphs = []
        self._glyphValues = {}
    
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)
            allGlyphs += f.keys()
            self._glyphValues[sourceFileName] = {}
            for glyphName in f.keys():
                self._glyphValues[sourceFileName][glyphName] = {}
                for attr in self._glyphAttrs:
                    value = getattr(f[glyphName], attr)
                    self._glyphValues[sourceFileName][glyphName][attr] = value
            f.close()

        # store all pairs in dict
        self._glyphNamesAll = list(set(allGlyphs))
        self._glyphNamesAll.sort()

        # update glyphs column
        tab.glyphs.set(self._glyphNamesAll)

    def updateGlyphValuesCallback(self, sender):
        '''
        Update table with sources and glyph values based on the currently selected glyph attribute.

        '''
        tab = self._tabs['glyph values']

        if not self.selectedSources or not self.selectedGlyphAttrs:
            tab.glyphValues.set([])
            return

        glyphName, glyphIndex = self.selectedGlyphName
        glyphAttr  = self.selectedGlyphAttrs[0]

        if self.verbose:
            print(f'updating glyph values for glyph {glyphName} ({glyphIndex})...\n')

        # create list items
        values = []
        glyphValuesItems = []
        for fontName in self._glyphValues.keys():
            value = self._glyphValues[fontName][glyphName][glyphAttr] if glyphName in self._glyphValues[fontName] else 0
            listItem = {
                "file name" : fontName,
                "value"     : value,
                "level"     : abs(value),
            }
            glyphValuesItems.append(listItem)
            values.append(value)

        # set glyph values in table
        glyphValuesPosSize = tab.glyphValues.getPosSize()
        del tab.glyphValues

        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
                'maxWidth' : self._colFontName*3,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", minValue=min(values), maxValue=max(values)),
            },
        ]
        tab.glyphValues = List(
                glyphValuesPosSize,
                glyphValuesItems,
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                editCallback=self.editGlyphValueCallback,
                enableDelete=False)

        # update pairs list label
        tab.glyphCounter.set(f'{glyphIndex+1} / {len(self._glyphNamesAll)}')

    def editGlyphValueCallback(self, sender):
        '''
        Save the edited glyph value back to the dict, so we can load values for another glyph or attribute.

        '''
        tab = self._tabs['glyph values']
        selection = tab.glyphValues.getSelection()
        if not len(selection):
            return

        i = selection[0]
        item = tab.glyphValues.get()[i]
        glyphAttr  = self.selectedGlyphAttrs[0]

        # save change to internal dict
        glyphName, glyphIndex = self.selectedGlyphName
        fontName = item['file name']
        newValue = item['value']
        oldValue = self._glyphValues[fontName][glyphName][glyphAttr]
        if oldValue != newValue:
            if self.verbose:
                print(f'changed {glyphName}.{glyphAttr} in {fontName}: {oldValue} → {newValue}\n')
            self._glyphValues[fontName][glyphName][glyphAttr] = int(newValue)

    def visualizeGlyphValuesCallback(self, sender):
        pass

    def exportGlyphValuesCallback(self, sender):
        '''
        Export current glyph values as a CSV file.

        '''
        pass

    def saveGlyphValuesCallback(self, sender):
        '''
        Save the edited glyph values back into their source fonts.

        '''
        tab = self._tabs['kerning']

        if self.verbose:
            print('saving edited glyph values to sources...')

        for fontName in self._glyphValues.keys():
            sourcePath = self._sources[fontName]
            f = OpenFont(sourcePath, showInterface=False)
            fontChanged = False
            for glyphName in self._glyphValues[fontName]:
                for attr, newValue in self._glyphValues[fontName][glyphName].items():
                    if newValue is None:
                        continue
                    if type(newValue) is str:
                        if not len(newValue.strip()):
                            continue
                    newValue = float(newValue)
                    if newValue.is_integer():
                        newValue = int(newValue)
                    oldValue = getattr(f[glyphName], attr)
                    if newValue != oldValue:
                        if self.verbose:
                            print(f'\twriting new value for {glyphName}.{attr} in {fontName}: {oldValue} → {newValue}')
                        setattr(f[glyphName], attr, newValue)
                        if not fontChanged:
                            fontChanged = True
            if fontChanged:
                # if self.verbose:
                #     print(f'\tsaving {fontName}...')
                f.save()
            f.close()

        if self.verbose:
            print('...done.\n')

    # kerning

    def loadKerningPairsCallback(self, sender):
        '''
        Load kerning pairs and values from selected sources into the UI.

        '''
        if not self.selectedSources:
            return

        tab = self._tabs['kerning']
        
        # collect pairs and kerning values in selected sources
        allPairs = []
        self._kerning = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)
            allPairs += f.kerning.keys()
            self._kerning[sourceFileName] = {}
            for pair, value in f.kerning.items():
                self._kerning[sourceFileName][pair] = value
        self._kerningPairsAll = list(set(allPairs))
        self._kerningPairsAll.sort()

        # update pairs column
        pairListItems = []
        for g1, g2 in sorted(self._kerningPairsAll):
            pairItem = {'1st': g1, '2nd': g2}
            pairListItems.append(pairItem)
        tab.pairs.set(pairListItems)

    def updateKerningValuesCallback(self, sender):
        '''
        Update table with sources and kerning values based on the currently selected kerning pair.

        '''
        tab = self._tabs['kerning']

        if not self.selectedSources:
            tab.kerningValues.set([])
            return

        pair, pairIndex = self.selectedKerningPair

        if self.verbose:
            print(f'updating kerning values for pair {pair} ({pairIndex})...\n')

        # create list items
        values = []
        for fontName in self._kerning.keys():
            value = self._kerning[fontName][pair] if pair in self._kerning[fontName] else 0
            values.append(value)
        valuesMax = max(values) - min(values)

        kerningListItems = []
        for i, fontName in enumerate(self._kerning.keys()):
            value = values[i]
            listItem = {
                "file name" : fontName,
                "value"     : value,
                "level"     : value-min(values),
            }
            kerningListItems.append(listItem)

        # set kerning values in table
        kerningValuesPosSize = tab.kerningValues.getPosSize()
        del tab.kerningValues

        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", minValue=0, maxValue=valuesMax),
            },
        ]
        tab.kerningValues = List(
                kerningValuesPosSize,
                kerningListItems,
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                editCallback=self.editKerningCallback,
                enableDelete=False)

        # update kerning pair counter (current/total)
        tab.pairsCounter.set(f'{pairIndex+1} / {len(self._kerningPairsAll)}')

    def editKerningCallback(self, sender):
        '''
        Save the edited kerning pair back to the dict, so we can load values for another pair.

        '''
        tab = self._tabs['kerning']
        selection = tab.kerningValues.getSelection()
        if not len(selection):
            return

        i = selection[0]
        item = tab.kerningValues.get()[i]

        # save change to internal dict
        pair, pairIndex = self.selectedKerningPair
        fontName = item['file name']
        newValue = item['value']
        oldValue = self._kerning[fontName].get(pair)
        if oldValue != newValue:
            if self.verbose:
                print(f'changed kerning pair {pair} in {fontName}: {oldValue} → {newValue}\n')
            self._kerning[fontName][pair] = int(newValue)

        # update level indicator
        ### this will crash RF3!!
        # kerningListItems = []
        # for fontName in self._kerning.keys():
        #     value = self._kerning[fontName][pair] if pair in self._kerning[fontName] else 0
        #     listItem = {
        #         "file name" : fontName,
        #         "value"     : value,
        #         "level"     : abs(value),
        #     }
        #     kerningListItems.append(listItem)
        # tab.kerningValues.set(kerningListItems)

    def visualizeKerningCallback(self, sender):
        pass

    def exportKerningCallback(self, sender):
        '''
        Export current kerning values as a CSV file.

        '''
        pass

    def saveKerningCallback(self, sender):
        '''
        Save the edited kerning values back into their source fonts.

        '''
        tab = self._tabs['kerning']

        if self.verbose:
            print('saving edited kerning values to sources...')

        for fontName in self._kerning.keys():
            sourcePath = self._sources[fontName]
            f = OpenFont(sourcePath, showInterface=False)
            fontChanged = False
            for pair, newValue in self._kerning[fontName].items():
                if type(newValue) not in [int, float]:
                    if not len(newValue.strip()):
                        continue
                newValue = int(newValue)
                oldValue = f.kerning.get(pair)
                if newValue != oldValue:
                    if self.verbose:
                        print(f'\twriting new value for {pair} in {fontName}: {oldValue} → {newValue}')
                    f.kerning[pair] = newValue
                    if not fontChanged:
                        fontChanged = True
            if fontChanged:
                # if self.verbose:
                #     print(f'\tsaving {fontName}...')
                f.save()
            f.close()

        if self.verbose:
            print('...done.\n')


# ----
# test
# ----

if __name__ == '__main__':

    OpenWindow(VarFontAssistant)

