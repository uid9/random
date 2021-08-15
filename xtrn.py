#!/usr/bin/python

# Draw a transparent window in the center of the screen

import sys
from Xlib import X, display, Xatom, Xutil

win_w = 400
win_h = 200
shading = 0.2

d = display.Display()
s = d.screen()
root = s.root
W = root.get_geometry().width
H = root.get_geometry().height

win_x = int(W/2 - win_w/2 - 1)
win_y = int(H/2 - win_h/2 - 1)

win = root.create_window(
    win_x, win_y, win_w, win_h, 0,
    s.root_depth,
    window_class=X.InputOutput,
    visual=X.CopyFromParent,
    colormap=X.CopyFromParent, 
    event_mask=(X.ExposureMask|X.StructureNotifyMask)
)
win_gc = win.create_gc()
win.map()

atom = d.intern_atom('_XROOTPMAP_ID', True)
rootpmid = root.get_property(atom, Xatom.PIXMAP, 0, 1).value[0]
rootpm = d.create_resource_object('pixmap', rootpmid)

img = rootpm.get_image(0, 0, W, H, X.ZPixmap, 0xffffffff)
data = bytes([int(i * shading) for i in img.data])

pm = root.create_pixmap(W, H, 24)
gc = pm.create_gc()
for j in range(0, H):
    k = j * W * 4
    l = (j+1) * W * 4
    pm.put_image(gc, 0, j, W, 1, X.ZPixmap, 24, 0, bytes(data[k:l]))

def refresh():
    g = win.get_geometry()
    win.copy_area(win_gc, pm, g.x, g.y, g.width, g.height, 0, 0)

refresh()

while True:
    try:
        e = d.next_event()
        if e.type in [X.Expose, X.ConfigureNotify]:
            refresh()
    except KeyboardInterrupt:
        win.destroy()
        d.flush()
        sys.exit()
