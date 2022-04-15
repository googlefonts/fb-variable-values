Variable font toolkit
=====================

The following description cover a set of Python scripts to be developed and amalgamated into a single checker of the conditions of each glyph.

Glyph sets
----------

There will be three kinds of glyph sets that can be checked:

- A. A string, I.e. a list of glyphs provided  
- B. A sort, I.e. the result of seeking a particular feature type, or value.  
- C. All the glyphs of a font

Glyph values
------------

There are three kinds of values of interest within fonts:

### Protruding values

In contours and composites, “protruding values” are measures of glyph extents vs. set width and em height, as well as the recipes for assembly and shifting of composite glyphs.

This is an order in the checking glyphs for:

#### 1. Contour and point compatibility

- set C

#### 2. Width issues (Google sheet currently under development)

- A.width match, set A (`.tf` e.g.), or C (if a monospaced font)
- B.lsb match, set B
- C.rsb match, Set B
- D.Centered?
- E.glyph width, (width - lsb -rsb = x)

#### 3. Height issues

- A. Cap ht 
- B. Cap os
- C. Cap us
- D. L.c. ht
- E. L.c. os
- F. L.c. us
- G. Fig ht.
- H. Fig os
- I. Fig us

#### 4. Composite recipe

- A. Y shift
- B. X shift
 
### Intruding values
 
There are “intruding values”, or internal features, where in the case of a small subset of simple glyphs, their feature(s) can be determined from their extents alone. In most glyphs, internal features like stems, hairlines, intersections, terminals and counters that may be identified by index value, index pair or point range for observation of its measure.

#### 5. Feature checking 
- A. On simple glyphs, little formulae to check for circles, rectangles, chevrons, ?!¡?¿, parentheticals, diacritics. (e.g. respectively, is . round?, is H bar progressing correctly over width? Are chevrons right? Is `!` and `¡` equal, are parentheses flipped in x?), are diacritics right ht centered and right os/us?)
- B. Features of more complex glyphs… (later)
- C. Curves and lines… (later)
