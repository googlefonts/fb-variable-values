---
title  : VariableValues tool
layout : default
---

A tool to view and edit font values in multiple designspace sources at once.
{: .lead}


designspace
-----------

Define which designspaces and font sources to look into.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarFontAssistant_1.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
designspaces
: Drag one or more designspace files into the list.

axes
: ^
  A list of axes in the selected designspace.  
  *Drag the items to change the font sorting order.*

sources
: ^
  A list of all sources in the selected designspace.  
  *Select which sources to collect values from.*
</div>

</div>


font values
-----------

Visualize and edit font values in selected sources.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarFontAssistant_2.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
attributes
: A list of font attributes to collect values from.

load
: Click the button to collect values from the fonts and display them in the UI.

values
: ^
  Values and visualization of the selected font attribute across all selected sources.  
  Double-click individual values to edit.

save
: Click the button to save the edited values back into the fonts.
</div>

</div>


measurements
------------

Collect custom measurements from the selected sources.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarFontAssistant_5.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
measurement files
: Drag one or more `.csv` files with measurement definitions from Finder into the list.

measurements
: ^
  A list of measurement definitions contained in the selected file.  
  *Select one measurement to display its values.*

values
: ^
  Values and visualization of the selected measurement across all selected sources.  

load
: Click the button to collect values from the fonts and display them in the UI.
</div>

</div>


glyph values
------------

Visualize and edit glyph-level values.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarFontAssistant_4.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
glyphs
: A list of all glyphs in all selected sources.

attributes
: A list of glyph attributes to collect values from.

load
: Click the button to collect values from the fonts and display them in the UI.

values
: ^
  Values and visualization of the selected glyph attribute across all selected sources.  
  Double-click individual values to edit.

save
: Click the button to save the edited values back into the fonts.
</div>

</div>


kerning
-------

Visualize and edit kerning values in selected sources.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarFontAssistant_5.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
pairs
: A list of all kerning pairs in all selected sources.

load
: Click the button to collect values from the fonts and display them in the UI.

values
: ^
  Values and visualization of the selected kerning pair across all selected sources.  
  Double-click individual values to edit.

save
: Click the button to save the edited values back into the fonts.
</div>

</div>
