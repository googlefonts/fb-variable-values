import os, csv
from fontTools.agl import UV2AGL
from fontParts.fontshell.point import RPoint

# ---------
# functions
# ---------

def getPointAtIndex(glyph, i):
    # make a linear index of all points
    n = 0
    points = {}
    for ci, c in enumerate(glyph.contours):
        for pi, p in enumerate(c.points):
            points[n] = ci, pi
            n += 1
    # n+1 : right margin
    if i > len(points)-1:
        P = RPoint()
        P.x = glyph.width
        P.y = 0
        return P
    # -1 : left margin
    if i < 0:
        P = RPoint()
        P.x = 0
        P.y = 0
        return P
    # get point at index
    ci, pi = points[i]
    return glyph.contours[ci].points[pi]

def exportMeasurementDescriptionsToCSV(measurements, csvPath):
    '''
    Export list of measurement descriptions to CSV file.

    :: 

        measurements = [
            ('XOPQ', 'general x opaque',          'x',   'H', '48',  0, '48', 11, ),
            ('XOUC', 'x stem uppercase',          'x',   'H', '48',  0, '48', 11, ),
            ('XOLC', 'x stem lowercase',          'x',   'n', '6E',  0, '6E', 20, ),
            ('XOFI', 'x stem figures',            'x',   '1', '31',  0, '31',  6, ),
            ('XTRA', 'general x transparent',     'x',   'H', '48', 11, '48',  8, ),
            ('XTUC', 'x trans uppercase',         'x',   'H', '48', 11, '48',  8, ),
            ('XTLC', 'x trans lowercase',         'x',   'n', '6E', 20, '6E', 12, ),
            ('XTFI', 'x trans figures',           'x',   '0', '30', 14, '30', 20, ),
            ('XTAB', 'figure width',              'x',   '0', '30',  0, '30',  8, ),
            ('GRAD', 'grade',                     'x',   'H', '48',  0, '48', 11, ),
            ('XTSB', 'general x sidebearing',     'x',   'H', '48',  7, '48', 12, ),
            ('XUCS', 'x sidebearing uppercase H', 'x',   'H', '48',  7, '48', 12, ),
            ('XUCR', 'x sidebearing uppercase O', 'x',   'O', '4F',  7, '4F', 28, ),
            ('XLCS', 'x sidebearing lowercase n', 'x',   'n', '6E', 11, '6E', 21, ),
            ('XLCR', 'x sidebearing lowercase o', 'x',   'o', '6F',  7, '6F', 28, ),
            ('XFIR', 'x sidebearing figure 0',    'x',   '0', '30',  7, '30', 28, ),
            ('YOPQ', 'general y opaque',          'y',   'H', '48',  0, '48',  1, ),
            ('YOUC', 'y opaque uppercase',        'y',   'H', '48',  0, '48',  1, ),
            ('YOLC', 'y opaque lowercase',        'y',   'f', '66',  0, '66',  4, ),
            ('YOFI', 'y opaque figures',          'y',   '0', '30', 11, '30',  4, ),
            ('YTAS', 'y transparent ascender',    'y',   'h', '68',  1,           ),
            ('YTDE', 'y transparent descender',   'y',   'p', '70',  0,           ),
            ('YTOS', 'general y overshoot',       'y', 'O-H', '48',  1, '4F',  4, ),
            ('YTUO', 'y uppercase overshoot',     'y', 'O-H', '48',  1, '4F',  4, ),
            ('YTLO', 'y lowercase overshoot',     'y', 'o-x', '78',  8, '6F',  4, ),
            ('YTFO', 'y figures overshoot',       'y', '0-5', '35', 17, '30',  4, ),
            ('YTDO', 'y descender overshoot',     'y', 'g-p', '67', 28, '70',  0, ),
            ('YTAO', 'y ascender overshoot',      'y', 'f-h', '68',  1, '66',  4, ),
            ('YTRA', 'y transparent',             'y', 'H+p', '70',  0, '48',  1, ),
            ('YTUC', 'y transparent uppercase',   'y',   'H', '48',  1,           ),
            ('YTLC', 'y transparent lowercase',   'y',   'x', '78',  8,           ),
            ('YTFI', 'y transparent figures',     'y',   '5', '35', 17,           ),
        ]

        csvPath = 'measurements.csv'
        exportMeasurementDescriptionsToCSV(measurements, csvPath)

    '''
    with open(csvPath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for m in measurements:
            writer.writerow(m)

def importMeasurementDescriptionsFromCSV(csvPath):
    '''
    Import measurement descriptions from CSV file into a Python list.

    '''
    measurements = []
    with open(csvPath, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            measurements.append(row)
    return measurements

# -------
# objects
# -------

class DesignspaceMeasurements:

    def __init__(self, designspacePath, mTuples):
        pass

class FontMeasurements:
    
    def __init__(self, font, mTuples):
        self.font = font
        self.measurements = {}
        for m in mTuples:
            M = Measurement(font, m)
            self.measurements[M.parameter] = M

class Measurement:

    labels = ['parameter', 'name', 'direction', 'note', 'glyph 1', 'point index 1', 'glyph 2', 'point index 2', 'formula']

    def __init__(self, font, mTuple):
        self.font        = font
        # parse tuple into attributes
        self.parameter   = mTuple[0]
        self.name        = mTuple[1]
        self.direction   = mTuple[2]
        self.note        = mTuple[3]
        self.glyph1Hex   = mTuple[4]
        self.pointIndex1 = int(mTuple[5])
        self.glyph2Hex   = mTuple[6] if len(mTuple) > 6 else None
        self.pointIndex2 = int(mTuple[7]) if len(mTuple) > 7 else None
        self.formula     = mTuple[8] if len(mTuple) > 8 else None

    @property
    def glyph1Name(self):
        glyph1Int = int(self.glyph1Hex, 16)
        return UV2AGL.get(glyph1Int)

    @property
    def glyph2Name(self):
        if self.glyph2Hex is None:
            return
        glyph2Int = int(self.glyph2Hex, 16)
        return UV2AGL.get(glyph2Int)
        
    @property
    def glyph1(self):
        return self.font[self.glyph1Name]

    @property
    def glyph2(self):
        if self.glyph2Name is None:
            return
        return self.font[self.glyph2Name]

    @property
    def point1(self):
        return getPointAtIndex(self.glyph1, self.pointIndex1)

    @property
    def point2(self):
        if self.glyph2 is None or self.pointIndex2 is None:
            return
        return getPointAtIndex(self.glyph2, self.pointIndex2)

    @property
    def value(self):
        # only one glyph / point
        if self.glyph2 is None:
            if self.direction == 'x':
                m = self.point1.x
            elif self.direction == 'y':
                m = self.point1.y
            else:
                m = sqrt((self.point1.x)**2 + (self.point1.y)**2)
        # two glyphs and/or points
        else:
            if self.direction == 'x':
                m = self.point2.x - self.point1.x
            elif self.direction == 'y':
                m = self.point2.y - self.point1.y
            else:
                m = sqrt((self.point2.x - self.point1.x)**2 + (self.point2.y - self.point1.y)**2)
        # done
        return m

# ----
# test
# ----

if __name__ == '__main__':

    csvPath = '/Users/sergiogonzalez/Desktop/hipertipo/tools/VariableValues/data/measurements/measurements.csv'

    measurements = importMeasurementDescriptionsFromCSV(csvPath)
    for m in measurements:
        print(m)
