from importlib import reload
import variableValues.measurements
reload(variableValues.measurements)

import AppKit
import os
from operator import itemgetter, attrgetter
from vanilla import Window, TextBox, List, Button, Tabs, LevelIndicatorListCell
from fontParts.world import OpenFont
from fontTools.designspaceLib import DesignSpaceDocument
from mojo.roboFont import OpenWindow
from variableValues.measurements import importMeasurementDescriptionsFromCSV, FontMeasurements

class DesignSpaceSelector:
    
    title             = 'DesignSpaceSelector'
    width             = 123*5
    height            = 640
    padding           = 10
    lineHeight        = 22
    verbose           = True
    buttonWidth       = 100
    _colLeft          = 160
    _colFontName      = 160
    _colValue         = 60
    _tabsTitles       = ['designspace']

    _designspaces     = {}
    _axes             = {}
    _axesOrder        = []
    _axesTitles       = ['name', 'tag', 'minimum', 'maximum', 'default']
    _sources          = {}

    def __init__(self):
        ### OVERWRITE IN SUBCLASS
        self.w = Window(
                (self.width, self.height), title=self.title,
                minSize=(self.width, 360))

        x = y = p = self.padding
        self.w.tabs = Tabs((x, y, -p, -p), self._tabsTitles)
        self.initializeDesignspacesTab()
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
                (x, y, -p, self.lineHeight*3),
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

        y += self.lineHeight*3 + p
        tab.axesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'axes')

        y += self.lineHeight + p/2
        axesDescriptions = [{"title": D} for D in self._axesTitles]
        tab.axes = List(
                (x, y, -p, self.lineHeight*7),
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

        y += self.lineHeight*7 + p
        tab.sourcesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'sources')

        y += self.lineHeight + p/2
        tab.sources = List(
                (x, y, -p, -(self.lineHeight + p*2)),
                [])

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
            allowsSorting=False,
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


# ----
# test
# ----

if __name__ == '__main__':

    OpenWindow(DesignSpaceSelector)

