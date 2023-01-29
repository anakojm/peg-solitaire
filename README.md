# Peg solitaire
A game of peg solitaire in the terminal, written in python

<br>

- Select "from" with the arrow keys or hjkl, confirm with enter or space (configurable)
- Cancel by reselecting "from" and confirming with enter or space
- Select "to" with the arrow keys or hjkl, confirm with enter or space
- Quit anytime with ESC, q or m (configurable)
- You can switch between the European and the English version by switching a boolean in the code, a custom board is also possible.

<br>

UI: `·` indicates a peg in a hole, `*` emboldened indicates the peg to be moved,
and `o` indicates an empty hole. A blue `¤` is the hole the current peg moved from;
a red `*` is the final position of that peg, a red `o` is the hole of the peg that was jumped and removed.

<br>

The goal of the game is to empty the board except for one center peg.

To reach that goal you can move a piece. You can only move a piece by "jumping"
over another one, "eating" it in the process. 

The destination must be empty.

<br>

Screenshot:

![UI showcase](https://gist.github.com/anakojm/f6ef6eba4160d95a59cfa3d500244051/raw/33848f36bfda2865ddaf2a5af69d1eac6794bfa6/showcase.png)

<br>

TODO: `grep "TODO" peg_solitaire.py`

Thank you to [u/RiceKrispyPooHead](https://www.reddit.com/user/RiceKrispyPooHead/) for their help!
