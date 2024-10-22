# what

the source code to build animations used in the git course

# with what

this uses 3blue1brown's animation engine `manimlib`

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

also, each of the 5 python scripts produce one mp4

* `NoIndex.mp4`
* `WithIndex.mp4`
* `CloneAndPull.mp4`
* `PullDiverge.mp4`
* `PushAndNeedPull.mp4`

the ones with a `And` need to be split into 2

using avidemux for MacOS to split e.g. `CloneAndPull.mp4` into 2 clips `Clone.mp4` and `Pull.mp4`

## install avidemux

I used homebrew on mac with

```
brew install --HEAD avidemux
```

## install the GUI

search for avidemux on the web and download the dmg; might need to allow it to run in the security settings  
on sequoia, the option to "Allow apps from everywhere is not available anymore, to enable it again you need to

```bash
sudo spctl --master-disable
```

## split

open file under avidemux :

* **select mp4 muxer**
* load big clip (the one to be split in 2)
* use icons A and B to select start and stop, Save...

and done
