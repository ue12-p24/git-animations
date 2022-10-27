# what

the source code to build animations used in the git course

# with what

this uses 3blue1brown's animation engine `manim`

# when

this is quite rough but did the trick for automn 2020

# how

there are 5 scenes (see bottom of Makefile) named
* `noindex`
* `withindex`
* `clone`
* `diverge`
* `push`


build any of these with e.g. with:

```bash
cd animations

make medium           # all 5 in medium quality
make clone            # just one
make medium-clone     # clone in one quality
make low-clone
```

# where

outputs go somewhere under  `animations/media/videos/scenes/`

```bash
make files-medium
make files-low
make files-clone
```

# how to split

it is important that all included videos are in mp4 format, as mkv is not supported by all browsers; typically firefox won't render it

using avidemux for MacOS to split e.g. `CloneAndPull.mp4` into 2 clips `Clone.mp4` and `Pull.mp4`

Open file under avidemux :

* select mp4 muxer
* load big clip
* use icons A and B to select start and stop, Save...

and done
