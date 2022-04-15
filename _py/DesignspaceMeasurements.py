import os, csv
from vanilla import *
from AppKit import NSFilenamesPboardType, NSDragOperationCopy
from mojo.roboFont import OpenWindow
from fontParts.world import OpenFont
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.agl import UV2AGL

class FontMeasurementsDialog:
    
    title      = 'VarFont Measurements'
    key        = 'com.hipertipo.varFontMeasurements'
    width      = 123*3
    height     = 640
    padding    = 10
    lineHeight = 22
    verbose    = True

    _designspaces = {}
    _axes = {}
    _sources = {}
    
    _measurementFiles = {}
    _measurements = {}

    _fontinfoAttrs = ['unitsPerEm', 'xHeight', 'capHeight', 'descender', 'ascender', 'italicAngle', 'openTypeOS2WeightClass', 'openTypeOS2WidthClass']
    _fontinfo = {}

    def __init__(self):
        self.w = FloatingWindow(
                (self.width, self.height), title=self.title,
                minSize=(self.width, 360))

        x = y = p = self.padding
        self.w.tabs = Tabs((x, y, -p, -p), ["designspace", "fontinfo", "measurements"])

        self.initializeDesignspacesTab(0)
        self.initializeFontInfoTab(1)
        self.initializeMeasurementsTab(2)

        self.w.open()

    def initializeDesignspacesTab(self, tabIndex):

        tab = self.w.tabs[tabIndex]
        
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
        tab.axes = List(
                (x, y, -p, self.lineHeight*5),
                [],
            )

        y += self.lineHeight*5 + p
        tab.sourcesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'sources')

        y += self.lineHeight + p/2
        tab.sources = List(
                (x, y, -p, -p),
                [],
            )

    def initializeMeasurementsTab(self, tabIndex):

        tab = self.w.tabs[tabIndex]

        x = p = self.padding
        y = p/2
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
                selectionCallback=self.selectMeasurementFileCallback,
                otherApplicationDropSettings=dict(
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
                    callback=self.dropMeasurementFileCallback),
            )

        y += self.lineHeight*5 + p
        tab.measurementsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'measurements')

        y += self.lineHeight + p/2
        tab.measurements = List(
                (x, y, -p, -p),
                [],
            )

    def initializeFontInfoTab(self, tabIndex):

        tab = self.w.tabs[tabIndex]

        x = p = self.padding
        y = p/2

        fontinfoDescriptions  = [{"title": 'font name'}]
        fontinfoDescriptions += [{"title": D} for D in self._fontinfoAttrs]

        tab.fontinfo = List(
                (x, y, -p, -(self.lineHeight + p*2)),
                [],
                # allowsMultipleSelection=False,
                # allowsEmptySelection=False,
                # enableDelete=True,
                # selectionCallback=self.selectMeasurementFileCallback,
                columnDescriptions=fontinfoDescriptions,
            )

        y = -(self.lineHeight + p)
        buttonWidth = 100
        tab.updateValues = Button(
                (x, y, buttonWidth, self.lineHeight),
                'update',
                callback=self.updateFontinfoCallback,
            )
        x += buttonWidth + p
        tab.visualizeValues = Button(
                (x, y, buttonWidth, self.lineHeight),
                'visualize',
                callback=self.visualizeFontinfoCallback,
            )

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedDesignspace(self):
        tab = self.w.tabs[0]
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
        tab = self.w.tabs[0]
        selection = tab.sources.getSelection()
        sources = tab.sources.get()
        selectedSources = [source for i, source in enumerate(sources) if i in selection]
        if not len(selectedSources):
            return
        return selectedSources

    @property
    def selectedMeasurementFile(self):
        tab = self.w.tabs[2]
        selection = tab.measurementFiles.getSelection()
        measurementFiles = tab.measurementFiles.get()
        return [measurementFile for i, measurementFiles in enumerate(measurementFiles)] if len(measurementFiles) else None

    # ---------
    # callbacks
    # ---------

    def dropDesignspaceCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.designspace']

        if not paths:
            return False

        if not isProposal:
            tab = self.w.tabs[0]
            for path in paths:
                label = os.path.splitext(os.path.split(path)[-1])[0]
                self._designspaces[label] = path
                tab.designspaces.append(label)
                tab.designspaces.setSelection([0])

        return True

    def selectDesignspaceCallback(self, sender):

        tab = self.w.tabs[0]

        # -----------
        # reset lists
        # -----------

        axesPosSize    = tab.axes.getPosSize()
        sourcesPosSize = tab.sources.getPosSize()
        del tab.axes
        del tab.sources

        # -----------
        # empty lists
        # -----------

        if not self.selectedDesignspace:
            tab.axes    = List(axesPosSize, [])
            tab.sources = List(sourcesPosSize, [])
            return

        # ------------------------
        # get selected designspace
        # ------------------------
        
        designspace = self.selectedDesignspaceDocument 

        # -----------
        # update axes
        # -----------

        # get column descriptions
        axesTitles  = ['name', 'tag', 'minimum', 'maximum', 'default']
        axesDescriptions = [{"title": D} for D in axesTitles]
        
        # make list items
        self._axes = {}
        axesItems = []
        for axis in designspace.axes:
            axisItem = { attr : getattr(axis, attr) for attr in axesTitles }
            axesItems.append(axisItem)

        # create list UI with sources
        tab.axes = List(
            axesPosSize, axesItems,
                columnDescriptions=axesDescriptions,
                allowsMultipleSelection=True,
                enableDelete=False,
                allowsEmptySelection=False,
            )

        # --------------
        # update sources
        # --------------

        # get column descriptions
        sourcesTitles  = ['file name' ]
        sourcesTitles += [axis.name for axis in designspace.axes]
        sourcesDescriptions = [{"title": D} for D in sourcesTitles]

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

    def dropMeasurementFileCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.csv']

        if not paths:
            return False

        if not isProposal:
            tab = self.w.tabs[2]
            for path in paths:
                label = os.path.splitext(os.path.split(path)[-1])[0]
                self._measurementFiles[label] = path
                tab.measurementFiles.append(label)
                tab.measurementFiles.setSelection([0])

        return True

    def selectMeasurementFileCallback(self, sender):

        tab = self.w.tabs[2]
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

    def updateFontinfoCallback(self, sender):

        if not self.selectedSources:
            return

        tab = self.w.tabs[1]

        # reset list
        fontinfoPosSize = tab.fontinfo.getPosSize()
        del tab.fontinfo

        # empty list
        if not self.selectedDesignspace:
            tab.fontinfo = List(fontinfoPosSize, [])
            return

        # collect fontinfo values into dict
        self._fontinfo = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)
            info = f.info.asDict()
            self._fontinfo[sourceFileName] = {}
            for attr in self._fontinfoAttrs:
                self._fontinfo[sourceFileName][attr] = info[attr]
            f.close()

        # make list items
        fontinfoItems = []
        for sourceFileName in self._fontinfo.keys():
            fontinfoItem = { 'file name' : sourceFileName }
            for attr in self._fontinfo[sourceFileName].keys():
                fontinfoItem[attr] = self._fontinfo[sourceFileName][attr]
            fontinfoItems.append(fontinfoItem)

        # create list UI with sources
        fontinfoDescriptions  = [{"title": 'file name'}]
        fontinfoDescriptions += [{"title": D} for D in self._fontinfoAttrs]
        tab.fontinfo = List(
            fontinfoPosSize, fontinfoItems,
            columnDescriptions=fontinfoDescriptions,
            allowsMultipleSelection=True,
            enableDelete=False)

    def visualizeFontinfoCallback(self, sender):
        print('peekaboo')
        pass


if __name__ == '__main__':

    OpenWindow(FontMeasurementsDialog)

