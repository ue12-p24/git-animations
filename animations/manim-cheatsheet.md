# cheatsheets

* https://infograph.tistory.com/184
* https://talkingphysics.wordpress.com/2018/06/11/learning-how-to-animate-videos-using-manim-series-a-journey/
* https://azarzadavila-manim.readthedocs.io/en/latest/geometry.html

# objects

```python
Text('content', font='courier')
Paragraph('line1', 'line2', alignment='left')

Dot()
Circle()
Ellipse()

Rectangle(height=, width=)
Square()

Arrow(UP, DOWN)
CurvedArrow()

Annulus()
```

## geometry

```python
line.get_width() 
line.get_height() -> float

line.get_bottom() 
line.get_top() 
line.get_left() 
line.get_right() -> array([x, y, z])


line.get_center() -> array([x, y, z])
```

## bounding boxes

```
```

## colors

<https://www.reddit.com/r/manim/comments/dzxoen/predefined_color_scheme/>

# scene content

```python
d= scene.add(Dot())
scene.remove(d)
```

# positions

may be used within `scene.play()`

```python
object.to_edge(UP)
object.to_edge(UP+RIGHT)
object.to_corner(UR)
###
# buff is used to specify margins
object.to_edge(UP, buff=1)
###
object.move_to(2UP+3DOWN) # absolute
object.move_to(other.get_center()+2UP+3DOWN) # relative
object.move_to(otherobject) # ?? suggested in tuto but untested
###
object.next_to(other, RIGHT, buff=1)
```

# groups

```python
group = VGroup(o1, o2, o3)
group.add(Circle(), Square())
group.arrange(direction=DOWN, center=True)
group.arrange_submobjects(RIGHT) # parts of the group not yet added ?
```

# animations

to be used within `scene.play()`

```python
scene.Write(text)   # only text ?
self.ShowCreation() 
self.FadeIn()
self.FadeOut()
```

## transformations

```python
self.Transform(x1, x2)        # x1 remains visible on the screen,
                              # it is physically changed
                              # and x2 does not show up at all
self.ReplacementTransform()   # x1 gets hidden, x2 gets displayed
                              # and that's x2 that receives
                              # the changes in memory
```

## using tragets

```python
obj.generate_target()
obj.target.move_to(...)
obj.target.scale(...)
scene.play(MoveToTarget(obj))
```

# updaters

```python
def updater(obj):
    pass # mess with obj
obj.add_updater(updater)
obj.clear_updaters # ???
```

# miscell

```python
scene.add_sound("click")

svg = SVGMobject("drawing")
scene.play(Write(svg))
```