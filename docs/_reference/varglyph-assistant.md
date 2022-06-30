---
title  : VarGlyph Assistant
layout : default
order  : 2
---

A tool to view and edit glyph data in designspace sources.
{: .lead}


designspace
-----------

Use this tab to define which designspace, font sources and glyphs to look into.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarGlyphAssistant-1.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
designspaces
: Drag one or more `.designspace` files from Finder into the list.

axes†
: ^
  A list of axes in the selected designspace.  
  Drag the axes to change the font sorting order.

glyph names
: Type or paste a list of glyph names for analysis.

sources
: ^
  A list of sources in the selected designspace.  
  Click on the column headers to sort the list using different parameters.  
  Select which sources to collect values from.
</div>

</div>


attributes
----------

Use this tab to visualize various glyph values in selected sources.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarGlyphAssistant-2.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
glyphs
: A list of all glyphs in all selected fonts.

attributes
: A list of attributes of the current glyph across all selected sources.

update
: Click the *update* button to scan the fonts, collect values and display them in the UI.

visualize
: Use the *visualize* button to plot the numbers with graphics in PDF format.†

export
: Use the *export* button to save the kerning data as a CSV file.†
</div>

</div>


compatibility
-------------

Use this tab to check if glyphs from selected sources are compatible for interpolation.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarGlyphAssistant-3.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
glyphs
: A list of all glyphs in all selected fonts.

segments
: ^
  A list of segments of the current glyph across all selected sources.
  - Line segments are identified by a letter `L`. 
  - Curve segments are identified by a letter `C`.

visualize
: Use the *visualize* button to plot the segment types with graphics in PDF format.†

export
: Use the *export* button to save the table as a CSV file.†

save
: Use the *save* button to save the edited values back into the fonts.†
</div>

</div>


validation
----------

Use this tab to perform various tests to glyphs in the selected sources.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarGlyphAssistant-4.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
glyphs
: ...

tests
: ...

results
: ...
</div>

</div>

† not implemented yet
