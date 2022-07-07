---
title  : VarFont Assistant
layout : default
order  : 1
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
  Drag the items to change the font sorting order.

sources
: ^
  A list of all sources in the selected designspace.  
  Click on the column headers to sort the list based on different axes.  
  Select which sources to collect values from.
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

{% comment %}
visualize
: Use the *visualize* button to plot the numbers with graphics in PDF format.†

export
: Use the *export* button to save the table as a CSV file.†
{% endcomment %}

save
: Click the button to save the edited values back into the fonts.
</div>

</div>


glyph values
------------

Visualize and edit glyph values to collect values from.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarFontAssistant_3.png){: .img-fluid}
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

{% comment %}
visualize
: Use the *visualize* button to plot the numbers with graphics in PDF format.†

export
: Use the *export* button to save the table as a CSV file.†
{% endcomment %}

save
: Click the button to save the edited values back into the fonts.
</div>

</div>


{% comment %}
measurements
------------

Measure and visualize specific distances in selected sources.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarFontAssistant_4.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
measurement files
: Drag one or more `.csv` files with measurement definitions from Finder into the list.

measurements
: ^
  A list of measurement definitions contained in the selected file.  
  Select one or more items to measure.

values
: ^
  Values and visualization of the selected measurement across all selected sources.  
  A list of measured values for the selected sources.†

: Click the button to collect values from the fonts and display them in the UI.

visualize
: Use the *visualize* button to plot the numbers with graphics in PDF format.†

export
: Use the *export* button to save the values table as a CSV file.†
</div>

</div>
{% endcomment %}


kerning
-------

Visualize and edit kerning values in selected sources.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarFontAssistant_4.png){: .img-fluid}
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

{% comment %}
visualize
: Use the *visualize* button to plot the numbers with graphics in PDF format.†

export
: Use the *export* button to save the kerning data as a CSV file.†
{% endcomment %}

save
: Click the button to save the edited values back into the fonts.
</div>

</div>
