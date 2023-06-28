# flashcard_generator

Contains two Python scripts: one to create Anki flashcards from a poem, another to create Anki flashcards from a sequence.
See the comments at the top of either program for more information (synopsis of program, how to format input, guidance on usage).

The flashcards for poems shows two lines of the poem on the front, and the user must recall the following line. The flashcards for sequences ask for the user to recall successor and predecessor of some element in the sequence, as well as to recall an element from its position or the position of some element. If any of these cards are unnecessary or inappropriate for your use, simply delete (or comment out) the part of the code which generates the extraneous material.

Credit to https://github.com/eudoxia0/spaced-repetition-tools for the idea, although a very different implementation was needed to create flashcards formatted for Anki (rather than Mochi); and to https://github.com/quentinsf/poem2anki, which inspired some of the implementation of the AnkiPoetry.py script. Leveraged Bing AI to aid code-writing.
