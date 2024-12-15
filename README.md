# GlyphForge
Generate the glyphs based off [Gorilla of Denstiny](https://github.com/GorillaOfDestiny)'s science of magic system

# Usage
1. Run the `app.py` file
2. Fill in the dropdown boxes with desired values
3. Click the `Generate Glyph` button.

OR

1. Run the `app.py` file
2. Click the `Random Spell` button to generate a random glyph.

# Requirements

```bash
pip install -r requirements.txt
```

## Current Development
Currently the project is pretty much finished - I just have to solve the duplicate spell problem

I'll continue to make minor improvements/add features upon request but otherwise I'm calling it a success.

Thank you to GorillaOfDestiny for supporting this project and everyone in the Discord who I bounced ideas off of.

## Issues
There are spells that are basically identical, even with conditions and casting time
```
Spells with attributes:
Level: 0
School: Evocation
Duration: Instantaneous
Range: 60 feet
Area Type: None
Damage Type: Cold
Concentration: False
Ritual: False
Matching spells: Frostbite, Ray of Frost
```
And so I have to find a way to add unique identifiers. I've only finished cantrips but I imagine this will be common considering that there are only 32 cantrips and other levels like Level 2 have 61. 

### Contains Duplicates:
- [X] Level 0 (Cantrips) 
- [X] Level 1
- [X] Level 2
    - [X] SRD
- [X] Level 3
- [X] Level 4

### Possible Solutions:
- ~~Add conditions~~
- ~~Add damage of spells~~
    - Doesn't work with spells that don't have damage (`Elementalism`, `Mold Earth`, `Shape Water`)
- Add casting time of spells (unlikely)
    - Most casting spells take 1 action
- Add category of spell
    - Control, Communication, Detection, Deception, etc.
    - This might be the best solution and may be able to be implemented without adding a whole set of attributes
        - Possibly just modifying the image to have a characteristic depending on the category
            - Will likely be difficult if different line type or base shape is used because I am bad at algorithms

# Primary Tasks
- [X] Update to work with draw_spell_2 from original project
- [X] Standardize the Attributes
- [X] Fix original code to allow for concentration and ritual attributes
- [X] Allow users to select base shape
- [X] Allow users to select line shape
- [X] Randomly generate glyphs

## Secondary Tasks
- [X] Make a catalog of all spells and their attributes
    - [X] Cantrips
    - [X] 1st Level
    - [X] 2nd Level
    - [X] 3rd Level
    - [X] 4th Level
    - [X] 5th Level
    - [X] 6th Level
    - [X] 7th Level
    - [X] 8th Level
    - [X] 9th Level
- [ ] Allow users to search for spell and return glyph - This probably isn't going to happen
- [X] Have generated glyph return spell

## Tertiary Tasks
- [X] Be able to change random spell values after generation
- [ ] Allow users to select colors
    - [ ] Whole glyph
    - [ ] Individual attributes

# DISCLAIMER
I did not create any of the algorithms used in the backend of this program. I exclusively made the GUI and assembled the JSONs used in the spell lookup. Aside from slight modifications, I have done nothing to the `bases.py` and `line_shapes.py`. I have made a number of changes to `writer.py`, but the majority is still the original code.
