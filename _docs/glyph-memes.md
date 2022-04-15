Glyph memes
===========

The long-term goal of the project is a database of Latin glyph memes, i.e. general descriptions of the contents of each glyph, its contours, spaces and sources from other glyphs, either directly via composites or indirectly via compatible contours and spaces.

This database will include separate x-dimension (i.e. objects measured parallel to the horizon), and y-dimension, (obviously objects measured parallel to the horizon), as well as separation of diagonal features as well as round, square and triangular spaces.

Details of shape terminals and intersections, or any stylistic characteristics are not a part of the memes.

Note: The development path is to first complete the memes for `XTRA` (horizontal white space), for the Roboto Flex Glyph repertoire to facilitate analysis of the work in progress. I.e. we start with:

Glyph meme format
-----------------

### Glyph attributes

| column | contents    |
|--------|-------------|
| A      | glyph name  |
| B      | width       | 
| C      | left side   |
| D      | right side  |
| E      | body        |
| F      | counter     |

### Possible values

| Value                       | Key                                                         |
|-----------------------------|-------------------------------------------------------------|
| 0                           | does not match cardinal glyph, is not systematic            |
| 1                           | matches cardinal glyph                                      |
| C                           | a letter it matches another column (e.g. C) of the Cardinal |
| C (and a letter)            | it matches a column of another letter                       |
| C (and a [F])               | it comes from another column and a formula                  |
| C (and a letter, and a [F]) | it comes from a column of another letter and a formula¹    |

¹ An example of a formula is an `Î`, where the composition of the diacritic changes the side bearing by amount that should be checked. See also \* below


² All glyphs with a negative sidebearing also use a [F]ormula to determine the value of column E.
All gyphs with placed diacritics that change the side bearings use [F]ormulas to determine the values of columns C and D.

(The sheet has many more columns available for stem types and values, alignment types and locations, and color coding for canon / parent / child relationships.

Example
-------

### A

| glyph name           | width | left | right | body | counter |    |    |     |
|----------------------|-------|------|-------|------|---------|----|----|-----|
| A                    | 1     | 1    | 1     | 1    | 1       |    | H  | A   |
| Agrave               | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Aacute               | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Acircumflex          | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Atilde               | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Adieresis            | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Aring                | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Amacron              | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Abreve               | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Aogonek              | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Aringacute           | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Adblgrave            | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Ainvertedbreve       | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Adotbelow            | 1     | 1    | 1     | 1    | 1       |    |    |     |
| Ahookabove           | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Acircumflexacute     | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Acircumflexgrave     | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Acircumflexhookabove | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Acircumflextilde     | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Acircumflexdotbelow  | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Abreveacute          | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Abrevegrave          | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Abrevehookabove      | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Abrevetilde          | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Abrevedotbelow       | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Alpha                | 1     | 1    | 1     | 1    | 1       |    |    |     |
| Alphatonos           | 1     | 1    | 1     | [F]  | 1       |    |    |     |
| Delta                | 0     | 1    | 1     | 0    | 1       |    |    |     |
| Lambda               | 0     | 1    | 1     | 0    | 1       |    |    |     |
| Acyr                 | 1     | 1    | 1     | 1    | 1       |    |    |     |
| Abrevecyr            | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| Adieresiscyr         | 1     | 1    | 1     | 1    | [F]     |    |    |     |
| El.bgr               | 1     | 1    | 1     | 1    | 1       |    |    |     |
| Amacroncyr           |       | 1    | 1     | 1    | [F]     |    |    |     |
| V                    | 0     | D    | C     | 0    | 0       |    |    |     |