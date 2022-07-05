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
: Drag one or more `.designspace` files into the list.

axes
: ^
  A list of axes in the selected designspace.  
  Reorder the list items to change the font sorting order.†

sources
: ^
  A list of sources in the selected designspace.  
  Click on the column headers to sort the list using different parameters.  
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
: A list of font attributes to measure.

values
: Double-click table cells to edit individual values.

load
: Use the *load* button to scan the fonts, collect values and display them in the UI.

<!--
visualize
: Use the *visualize* button to plot the numbers with graphics in PDF format.†

export
: Use the *export* button to save the table as a CSV file.†
-->

save
: Use the *save* button to save the edited values back into the fonts.
</div>

</div>


glyph values
------------

Visualize and edit glyph values in selected sources.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/VarFontAssistant_3.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
glyphs
: A list of all glyphs in all selected sources.

attributes
: A list of glyph attributes to measure.

values
: Double-click table cells to edit individual values.

load
: Click the *load* button to scan the fonts, collect values and display them in the UI.

<!--
visualize
: Use the *visualize* button to plot the numbers with graphics in PDF format.†

export
: Use the *export* button to save the table as a CSV file.†
-->

save
: Use the *save* button to save the edited values back into the fonts.†
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
: A list of measured values for the selected sources.†

load
: Click the *load* button to scan the fonts, collect values and display them in the UI.

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

values
: Values of the selected kerning pair across all selected sources.

load
: Click the *load* button to scan the fonts, collect values and display them in the UI.

<!--
visualize
: Use the *visualize* button to plot the numbers with graphics in PDF format.†

export
: Use the *export* button to save the kerning data as a CSV file.†
-->

save
: Use the *save* button to save the edited values back into the fonts.
</div>

</div>

† not implemented yet