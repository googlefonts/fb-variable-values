VarTools
========

A new set of tools to assist in the development of variable fonts.

1. VarFont Assistant
2. VarGlyph Assistant
3. Glyph Validator


VarFont Assistant
-----------------

A tool to view and edit font-level values in designspace sources.

### designspace

Use this tab to define which designspace and fonts sources to look into.

![](/hipertipo/tools/VarTools/_imgs/VarFontAssistant-1.png)

1. Drag one or more `.designspace` files into the first list. The UI will update to show the axes and sources in the designspace.
2. Select sources in which to collect values. Click on the column headers to sort the list using different parameters.

### fontinfo

Use this tab to visualize (and edit) font info values in selected sources.

![](/hipertipo/tools/VarTools/_imgs/VarFontAssistant-2.png)

1. Select which font info attributes to measure.
2. Click the *update* button to scan the fonts, collect values and display them in the UI.
3. Use the *visualize* button to plot the numbers with graphics in PDF format.
4. Use the *export* button to save the table as a CSV file.
5. Edit values in the table and use the *save* button to save them back to the fonts.

### glyphs

Use this tab to visualize (and edit) glyph values in selected sources.

![](/hipertipo/tools/VarTools/_imgs/VarFontAssistant-3.png)

1. Select one glyph attribute to collect values.
2. Type or paste a list of glyph names for value collection.
3. Click the *update* button to scan the fonts, collect values and display them in the UI.
4. Use the *visualize* button to plot the numbers with graphics in PDF format.
5. Use the *export* button to save the table as a CSV file.
6. Edit values in the table and use the *save* button to save them back to the fonts.

### measurements

Use this tab to measure and visualize specific distances in selected sources.

![](/hipertipo/tools/VarTools/_imgs/VarFontAssistant-4.png)

1. Drag one or more `.csv` files with measurement definitions into the fonts. The UI will update to show the various measurement definitions contained in the selected file.
2. Select which measurements to collect values.
3. Click the *update* button to scan the fonts, collect values and display them in the UI.
4. Use the *visualize* button to plot the numbers with graphics in PDF format.
5. Use the *export* button to save the table as a CSV file.


VarGlyph Assistant
------------------

A tool to view and edit glyph data in designspace sources.

### designspace

Use this tab to define which designspace and fonts sources to look into.

![](/hipertipo/tools/VarTools/_imgs/VarGlyphAssistant-1.png)

1. Drag one or more .designspace files into the first list. The UI will update to show the axes and sources in the designspace.
2. Type or paste a list of glyph names for value collection.
3. Select sources in which to collect values. Click on the column headers to sort the list using different parameters.

### attributes

Use this tab to visualize various glyph values in selected sources.

![](/hipertipo/tools/VarTools/_imgs/VarGlyphAssistant-2.png)

### compatibility

Use this tab to check for interpolation compatibility in glyphs from selected sources.

![](/hipertipo/tools/VarTools/_imgs/VarGlyphAssistant-3.png)

### validation

![](/hipertipo/tools/VarTools/_imgs/VarGlyphAssistant-4.png)


Glyph Validator
---------------

A tool to check individual fonts for internal consistency using glyph memes validation.

### definitions

![](/hipertipo/tools/VarTools/_imgs/GlyphValidator-1.png)

### validation

![](/hipertipo/tools/VarTools/_imgs/GlyphValidator-2.png)

