---
title  : Glyph Validator
layout : default
order  : 3
---

A tool to check individual fonts for internal consistency using glyph memes.
{: .lead}


definitions
-----------

Use this tab to load and edit glyph memes.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/GlyphValidator-1.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
source folder
: Choose a folder containing the database of glyph memes as a set of `.csv` files.

glyphs
: ^
  A list of glyphs for which glyph memes are available.  
  Select a glyph to update the list of memes for the current glyph.

memes
: A list of glyph memes available for the selected glyph.

update
: Use the *update* button to load the `.csv` file contents again.
</div>

</div>


validation
----------

Use this tab to validate glyphs against the glyph memes.

<div class='row'>

<div class='col-sm' markdown='1'>
![]({{ site.url }}/images/GlyphValidator-2.png){: .img-fluid}
</div>

<div class='col-sm' markdown='1'>
fonts
: ^
  Drag one or more UFO fonts into the horizontal list at the top.  
  Select one font to look into.

update
: Click the *update* button to scan the fonts, perform tests, and display the results in the UI.†

visualize
: Use the *visualize* button to plot the results with graphics in PDF format.†

export
: Use the *export* button to save the table as a CSV file.†
</div>

</div>

† not implemented yet
