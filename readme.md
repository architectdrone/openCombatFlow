# OpenCombatFlow

Hello, and welcome to OpenCombatFlow! I am Owen Mellema, and I am pleased to present you with this package. OCF is distributed under the MIT License.


## Usage (As of 1.0)

Using OpenCombatFlow (also known as OCF) is easy. All that is required to make a small game is contained within the module "character". The workflow looks something like this:

1. Create a new character class that extends the base Character class.

2. Implement getActionBlock and getReactionBlock. (If you forget, a NotImplementedError will be raised.)

3. Create a new combatHandler object.

4. Add objects from your new character class to the combatHandler, using the addCharacter() method.

5. Use turn() to increment through the characters.

Everything else (how attacks work, how results will be shown, etc) is up to you.


## Blocks

In OCF, I use a system of structured dictionaries to store and pass information between objects. I think this is useful for a variety of reasons. The required structure of these blocks (as I call them) is detailed in a document called "DSD.txt", which can be found in the directory where OCF is installed. You can also access it on my website (https://architectdrone.github.io/openCombatFlow/DSD-documentation.html). "MANDATORY" means that the tag musgt be included, "NOT MANDATORY" means that it is optional, and "CONDITIONALLY MANDATORY" means that it is mandatory only in certain circumstances, as indicated by the description.


## Dice

Features involving dice can also be implemented, using dice strings. A dice string is an expression that indicates a number of dice, modifiers, and conditional statements. An example dice string is "1d4+5>6", which means "roll one four sided die, add five, and see if the result is greater than six." (The results of a failed conditional depend on the circumstances, but usually it defaults to returning 0.) To use dice strings directly, import the dice module from OpenCombatFlow, and use the evaluate() function. Additionally, several fields in the DSD specify that they are "Dice Safe" (abbreviated "DS"), meaning that either dice strings  or integers can be passed to them. For the format of Dice Strings, please view "DiceStringFormat.txt" in the directory where OCF is installed, or view the page on my website (https://architectdrone.github.io/openCombatFlow/dice-string-documentation.html).


## Caveat

This is the first package I have ever made for python, so if I mess up, I apologize. Python's module system is both elegant and arcane. Please give me any feedback you might have on the github repo (https://github.com/architectdrone/OpenCombatFlow). Please be sure to remember the human when/if you do. :)


## Links

The OpenCombatFlow Website: https://architectdrone.github.io/openCombatFlow/index.html

The Repo: https://github.com/architectdrone/OpenCombatFlow


## License (MIT)

MIT License

Copyright (c) 2019 Owen Mellema

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Conclusion

Have fun, and happy hacking!