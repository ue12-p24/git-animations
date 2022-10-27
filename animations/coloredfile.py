from manimlib.imports import *


# specifications for textcolors or blocks
# can be provided in several ways
# (l1, color) : one line is of that color
# ([l1, l2 ,l3]: all three lines are of this color
# ((l1, l2), color): a range of lines

def slice_colors(common_color_spec):
    """
    creates a 2-tuple (slice, color) from any of the 3 forms above
    """
    item1, color = common_color_spec
    if isinstance(item1, list):
        for i in item1:
            yield (slice(i, i+1), color)
    elif isinstance(item1, tuple):
        beg, end = item1
        yield (slice(beg, end), color)
    else: # expect int
        yield (slice(item1, item1+1), color)

def spanning_slice_color(common_color_spec):
    start, stop = None, None
    for s, color in slice_colors(common_color_spec):
        start = s.start if start is None else min(start, s.start)
        stop = s.stop if stop is None else max(stop, s.stop)
    return slice(start, stop), color


def any_text_as_list(arg):
    if isinstance(arg, list):
        return arg
    elif isinstance(arg, str):
        return arg.split("\n")
    elif isinstance(arg, ColoredFile):
        return arg.original_text.copy()
    else:
        raise ValueError(f"any_text_as_list: wrong arg type {type(arg)}")


class ColoredFile(Paragraph):

    def __init__(self, text,
                 font='courier', alignment='left',
                 *args, **kwds):
        self.original_text = any_text_as_list(text)
        super().__init__(*self.original_text,
                         alignment='left', font=font, *args, **kwds)
        #
        self._floatings = []

    # nail contains the settings, other is the thing
    # that gets nailed; typically an Index object can
    # have to nail an Editable
    def nail(self, other):
        """
        is used to set 'other' in place
        most of the time, other is self, but can also be the target
        of an animation
        """
        return self

    def apply_textcolors(self, textcolors):
        for color_spec in textcolors:
            for (slice, color) in slice_colors(color_spec):
                self[slice].set_color(color)

    def reset_textcolors(self):
        for line in self:
            line.set_color(WHITE)

    def get_block(self, block_spec):
        spanning_slice, color = spanning_slice_color(block_spec)
        return SurroundingRectangle(self[spanning_slice], color=color)

    def get_blocks(self, block_specs):
        return [self.get_block(block_spec) for block_spec in block_specs]


    def replace_animations(self, scene, target:str, textcolors=None):
        plain2 = self.__class__(target, font=self.font,
                                alignment=self.alignment)
        self.nail(plain2)
        if textcolors:
            plain2.apply_textcolors(textcolors)
        self.original_text = any_text_as_list(target)
        return [Transform(self, plain2)]


    def morph_animations(self, scene, original: 'ColoredFile'):
        """
        replace full contents with the one from original
        """
        assert isinstance(original, ColoredFile)
        floating = original.copy()
        floating.generate_target()
        floating.target.move_to(self.get_center())
        self.nail(floating.target)
        self._floatings.append(floating)
        self.original_text = any_text_as_list(original.original_text)
        return [MoveToTarget(floating),
                Transform(self, floating.target)]

    def morph_partial_animations(self, scene, source: 'ColoredFile', changes):
        """
        animate the copy of ranges of text from the source into here
        changes: iterable of tuples of the form
          beg_source, end_source, beg_here, end_here

        WARNING: the order of changes IS IMPORTANT
        the list is **first reversed** and applied in order

        it is desirable to start from the end of the contents because
        otherwise early changes will mess line numbering for the end

        this is why the list is reversed, to changes can be passed
        in the natural order
        """

        # starting from the end to apply the changes
        changes = list(reversed(changes))
        # take note of the distortion created by each change
        deltas = []


        new_text = self.original_text[:]

        for bs, es, bh, eh in changes:
            new_text[bh:eh] = source.original_text[bs:es]
            deltas.append((es-bs)-(eh-bh))
        self.original_text = new_text
        target = self.__class__(text=self.original_text,
                                font=self.font, alignment=self.alignment)
        self.nail(target)
        animations = [Transform(self, target)]
        self._floatings.append(target)

        # start from the beginning now
        # this will sum the distortions as we go
        D = 0
        for (bs, es, bh, eh), d in zip(reversed(changes), reversed(deltas)):
            # indices in new_index are shifted b/c of all the changes
            # so, at first the beginnings match, and D will account for
            # accumulated shifts
            beg = bh+D
            # the range length is preserved (same as in source)
            end = beg + (es-bs)
            D += d
            floating = source[bs:es].copy()
            floating.generate_target()
            floating.target.move_to(target[beg:end].get_center())
            animations.append(MoveToTarget(floating))
            self._floatings.append(floating)
        animations.append(FadeIn(target))
        return animations

    def clean_morph(self, scene):
        for f in self._floatings:
            scene.remove(f)
        self._floatings = []
        return self
