import AppKit
import os, csv
from operator import itemgetter, attrgetter
from vanilla import *
from AppKit import NSFilenamesPboardType, NSDragOperationCopy
from mojo.roboFont import OpenWindow
from fontParts.world import OpenFont
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.agl import UV2AGL


class VarFontAssistant:
    
    title             = 'VarFont Assistant'
    key               = 'com.hipertipo.varFontAssistant'
    width             = 123*5
    height            = 640
    padding           = 10
    lineHeight        = 22
    verbose           = True
    buttonWidth       = 100
    _colLeft          = 180
    _colFontName      = 240
    _colValue         = 80
    _tabsTitles       = ['designspace', 'font values', 'glyph values', 'kerning'] # 'measurements'
    _designspaces     = {}
    _axes             = {}
    _axesTitles       = ['name', 'tag', 'minimum', 'maximum', 'default']
    _sources          = {}
    _measurementFiles = {}
    _measurements     = {}
    _fontInfoAttrs    = {
        'unitsPerEm'             : 'unitsPerEm',
        'xHeight'                : 'xHeight',
        'capHeight'              : 'capHeight',
        'descender'              : 'descender',
        'ascender'               : 'ascender',
        'italicAngle'            : 'italic angle',
        'openTypeOS2WeightClass' : 'OS2 weight',
        'openTypeOS2WidthClass'  : 'OS2 width',
    }
    _fontInfo         = {}
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
        self.initializeFontInfoTab()
        # self.initializeMeasurementsTab()
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
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
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
        tab.measurementFilesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'measurement files')

        y += self.lineHeight + p/2
        tab.measurementFiles = List(
                (x, y, -p, self.lineHeight*3),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                enableDelete=True,
                selectionCallback=self.selectMeasurementFileCallback,
                otherApplicationDropSettings=dict(
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
                    callback=self.dropMeasurementFileCallback),
            )

        y += self.lineHeight*3 + p
        tab.measurementsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'measurements')

        y += self.lineHeight + p/2
        tab.measurements = List(
                (x, y, -p, self.lineHeight*7),
                [],
            )

        y += self.lineHeight*7 + p
        tab.valuesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'values')

        y += self.lineHeight + p/2
        tab.values = List(
                (x, y, -p, -(self.lineHeight + p*2)),
                [],
            )

        y = -(self.lineHeight + p)
        tab.loadValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.loadMeasurementsCallback,
            )

        # x += self.buttonWidth + p
        # tab.visualizeValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'visualize',
        #         callback=self.visualizeMeasurementsCallback,
        #     )

        # x += self.buttonWidth + p
        # tab.exportValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'export',
        #         # callback=self.visualizeFontInfoCallback,
        #     )

        # x = -(p + self.buttonWidth)
        # tab.saveValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'save',
        #         # callback=self.visualizeFontInfoCallback,
        #     )

    def initializeFontInfoTab(self):

        tab = self._tabs['font values']

        x = p = self.padding
        y = p/2
        col = self._colLeft
        x2 = x + col + p

        tab.fontInfoAttrsLabel = TextBox(
                (x, y, col, self.lineHeight),
                'attributes')

        y += self.lineHeight + p/2
        tab.fontInfoAttrs = List(
                (x, y, col, -(self.lineHeight + p*2)),
                self._fontInfoAttrs.values(),
                allowsMultipleSelection=True,
                allowsEmptySelection=False,
                selectionCallback=self.updateFontInfoValuesCallback,
            )

        y = p/2
        tab.fontInfoLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'font info values')

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
        tab.fontInfoValues = List(
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
                callback=self.loadFontInfoCallback,
            )

        # x += self.buttonWidth + p
        # tab.visualizeValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'visualize',
        #         callback=self.visualizeFontInfoCallback,
        #     )

        # x += self.buttonWidth + p
        # tab.exportValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'export',
        #         # callback=self.exportFontinfoCallback,
        #     )

        x = -(p + self.buttonWidth)
        tab.saveValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'save',
                callback=self.saveFontinfoCallback,
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
                'glyph attributes')

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
                'glyph values')

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
                callback=self.loadGlyphAttributesCallback,
            )

        # x += self.buttonWidth + p
        # tab.visualizeValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'visualize',
        #         # callback=self.visualizeFontInfoCallback,
        #     )

        # x += self.buttonWidth + p
        # tab.exportValues = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'export',
        #         # callback=self.exportFontinfoCallback,
        #     )

        x = -(p + self.buttonWidth)
        tab.saveValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'save',
                # callback=self.saveFontinfoCallback,
            )

    def initializeKerningTab(self):

        tab = self._tabs['kerning']

        x = p = self.padding
        y = p/2
        col = 280 # self._colLeft
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
                'kerning values')

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
    def selectedFontInfoAttr(self):
        tab = self._tabs['font values']
        selection = tab.fontInfoAttrs.getSelection()
        fontInfoAttrs = tab.fontInfoAttrs.get()
        selectedFontInfoAttrs = [fontinfo for i, fontinfo in enumerate(fontInfoAttrs) if i in selection]
        if not len(selectedFontInfoAttrs):
            return
        return selectedFontInfoAttrs[0]

    # measurements

    @property
    def selectedMeasurementFile(self):
        tab = self._tabs['measurements']
        selection = tab.measurementFiles.getSelection()
        measurementFiles = tab.measurementFiles.get()
        return [measurementFile for i, measurementFiles in enumerate(measurementFiles)] if len(measurementFiles) else None

    @property
    def selectedMeasurements(self):
        tab = self._tabs['measurements']
        selection = tab.measurements.getSelection()
        measurements = tab.measurements.get()
        selectedMeasurements = [measurement for i, measurement in enumerate(measurements) if i in selection]
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

        # -----------
        # reset lists
        # -----------

        sourcesPosSize = tab.sources.getPosSize()
        del tab.sources

        # -----------
        # empty lists
        # -----------

        if not self.selectedDesignspace:
            tab.axes.set([])
            tab.sources = List(sourcesPosSize, [])
            return

        # ------------------------
        # get selected designspace
        # ------------------------
        
        designspace = self.selectedDesignspaceDocument 

        # -----------
        # update axes
        # -----------
        
        # make list items
        self._axes = {}
        axesItems = []
        for axis in designspace.axes:
            axisItem = { attr : getattr(axis, attr) for attr in self._axesTitles }
            axesItems.append(axisItem)

        # create list UI with sources
        tab.axes.set(axesItems)

        # --------------
        # update sources
        # --------------

        # get column descriptions
        sourcesDescriptions  = [{'title': 'file name', 'minWidth': self._colFontName*2}]
        sourcesDescriptions += [{'title': axis.name, 'width': self._colValue} for axis in designspace.axes]

        # make list items
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
        # tab = self._tabs['designspace']
        # axesOrder = [ a['name'] for a in tab.axes.get() ]
        
        # if not hasattr(tab, 'sources'):
        #     return

        # _sourceItems = tab.sources.get()
        # sourceItems = []
        # for item in _sourceItems:
        #     D = {}
        #     for k, v in item.items():
        #         D[k] = v
        #     sourceItems.append(D)

        # print(sourceItems)
        # sourceItems = sorted(sourceItems, key=attrgetter(*axesOrder))
        # print(sourceItems)
        # tab.sources.set(sourceItems)
        pass

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

    def loadFontInfoCallback(self, sender):

        if not self.selectedSources:
            return

        tab = self._tabs['font values']

        # empty list
        if not self.selectedDesignspace:
            tab.fontInfo.set([])
            return

        # collect fontinfo values into dict
        self._fontInfo = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)
            info = f.info.asDict()
            self._fontInfo[sourceFileName] = {}
            for attr, attrLabel in self._fontInfoAttrs.items():
                self._fontInfo[sourceFileName][attrLabel] = info.get(attr)
            f.close()

        self.updateFontInfoValuesCallback(None)

    def updateFontInfoValuesCallback(self, sender):

        tab = self._tabs['font values']

        if not self.selectedSources or not self._fontInfo:
            tab.fontInfoValues.set([])
            return

        fontInfoAttr = self.selectedFontInfoAttr

        if self.verbose:
            print('updating font info values...\n')

        # create list items
        values = []
        fontInfoItems = []
        for fontName in self._fontInfo.keys():
            value = self._fontInfo[fontName][fontInfoAttr]
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
        fontInfoValuesPosSize = tab.fontInfoValues.getPosSize()
        del tab.fontInfoValues

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
                'cell'     : LevelIndicatorListCell(style="continuous", minValue=min(values), maxValue=max(values)),
            },
        ]
        tab.fontInfoValues = List(
            fontInfoValuesPosSize,
            fontInfoItems,
            allowsMultipleSelection=False,
            allowsEmptySelection=False,
            columnDescriptions=columnDescriptions,
            allowsSorting=True,
            editCallback=self.editFontInfoCallback,
            enableDelete=False)

    def visualizeFontInfoCallback(self, sender):
        print('visualize font infos')

    def editFontInfoCallback(self, sender):
        print('font info edited...')

    def exportFontinfoCallback(self, sender):
        pass

    def saveFontinfoCallback(self, sender):

        tab = self._tabs['font values']
        fontInfoAttrs = { v: k for k, v in self._fontInfoAttrs.items() }

        if self.verbose:
            print('saving font info data to fonts...\n')

        for item in tab.fontInfoValues.get():
            sourceFileName = item['file name']
            sourcePath = self._sources[sourceFileName]

            f = OpenFont(sourcePath, showInterface=False)
            fileChanged = False

            for key, value in item.items():
                if key == 'file name':
                    continue
                attr = fontInfoAttrs[key]
                if type(value) not in [int, float]:
                    try:
                        value = float(value) if attr == 'italicAngle' else int(value)
                    except:
                        continue
                if value == getattr(f.info, attr):
                    continue
                print(f'\t{sourceFileName}: writing {attr}: {getattr(f.info, attr)} (old) → {value} (new)')
                setattr(f.info, attr, value)
                if not fileChanged:
                    fileChanged = True

            if fileChanged:
                f.save()
            f.close()

        print('\n...done.\n')

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
        selection = sender.getSelection()
        measurementFiles = tab.measurementFiles.get()

        # delete current list
        posSize = tab.measurements.getPosSize()
        del tab.measurements

        # list of measurements is empty
        if not selection or not len(measurementFiles):
            tab.measurements = List(posSize, [])
            return

        # get measurements from selected measurement file
        measurementFileLabel = [F for i, F in enumerate(measurementFiles) if i in selection][0]
        measurementFilePath = self._measurementFiles[measurementFileLabel]

        with open(measurementFilePath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            self._measurementFiles = {}
            items = []
            for i, lines in enumerate(csvFile):
                # # get column descriptions
                if i == 0:
                    titles = lines.keys()
                    descriptions = [{"title": T} for T in titles]

                # skip empty measurements
                if not any( list(lines.values())[2:] ):
                    continue

                # replace unicode hex values with unicode character
                if lines['Glyph 1']:
                    uniHex = lines['Glyph 1']
                    uniInt = int(uniHex.lstrip("x"), 16)
                    glyphName = UV2AGL.get(uniInt)
                    lines['Glyph 1'] = glyphName

                if lines['Glyph 2']:
                    uniHex = lines['Glyph 2']
                    uniInt = int(uniHex.lstrip("x"), 16)
                    glyphName = UV2AGL.get(uniInt)
                    lines['Glyph 2'] = glyphName


                # create list item
                items.append(lines)

        # create list UI with items
        tab.measurements = List(
            posSize, items,
            columnDescriptions=descriptions,
            allowsMultipleSelection=True,
            enableDelete=False)

    def loadMeasurementsCallback(self, sender):

        if not self.selectedMeasurements:
            return

        tab = self._tabs['measurements']

        # reset list
        valuesPosSize = tab.values.getPosSize()
        del tab.values

        # empty list
        if not self.selectedMeasurements:
            tab.values = List(valuesPosSize, [])
            return

        # collect measurements into dict
        self._measurements = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]

            f = OpenFont(sourcePath, showInterface=False)

            self._measurements[sourceFileName] = {}
            for measurement in self.selectedMeasurements:
                measurementKey = measurement['Axis']
                self._measurements[sourceFileName][measurementKey] = 'XXX'

            f.close()

        # make list items
        valuesItems = []
        for sourceFileName in self._measurements.keys():
            valuesItem = { 'file name' : sourceFileName }
            for measurement in self._measurements[sourceFileName].keys():
                valuesItem[measurement] = self._measurements[sourceFileName][measurement]
            valuesItems.append(valuesItem)

        # create list UI with values
        valueDescriptions  = [{"title": 'file name', 'minWidth': self._colFontName}]
        valueDescriptions += [{"title": D['Axis'], 'width': self._colValue} for D in self.selectedMeasurements]
        tab.values = List(
            valuesPosSize, valuesItems,
            columnDescriptions=valueDescriptions,
            # allowsMultipleSelection=True,
            # enableDelete=False
            )

    def visualizeMeasurementsCallback(self, sender):
        print('visualize measurements')

    def exportMeasurementsCallback(self, sender):
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
        # print('editing glyph value...')
        pass

    def visualizeGlyphValuesCallback(self, sender):
        pass

    def exportGlyphValuesCallback(self, sender):
        pass

    def saveGlyphValuesCallback(self, sender):
        pass

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
        ### this will crash RF
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
        if self.verbose:
            print('visualize kerning...\n')

    def exportKerningCallback(self, sender):
        if self.verbose:
            print('export kerning...\n')

    def saveKerningCallback(self, sender):

        tab = self._tabs['kerning']

        if self.verbose:
            print('saving kerning data to fonts...\n')

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
            print('\n...done.\n')


# ----
# test
# ----

if __name__ == '__main__':

    OpenWindow(VarFontAssistant)

