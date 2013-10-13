##Creating GUI for playlists. We can add files, remove files or clear the list altogether. The filepaths are displayed in the list and are stored in a python list called 'files'.
import pygame
from pygame.locals import *
from pgu import gui

_count = 1 # for added items

files = [] #list with all filenames stored in it. 

def open_file_browser(arg):
    d = gui.FileDialog() 
    d.connect(gui.CHANGE, handle_file_browser_closed, d)
    d.open()
    

def handle_file_browser_closed(dlg):
    if dlg.value: 
	files.append(dlg.value) #adds to the file list
        add_list_item(dlg.value) #add to the list shown

def clear_list(arg):
    global _count
    my_list.clear()
    my_list.resize()
    my_list.repaint()
    files = []
    _count = 1

def remove_list_item(arg):
    v = my_list.value #v is an integer denoting the position of the item in the list starting from 1
    if v:
        item = v
        my_list.remove(item)
        my_list.resize()
        my_list.repaint()
        files.pop(item-1)

def add_list_item(arg):
    global _count
    my_list.add(arg,value=_count)
    my_list.resize()
    my_list.repaint()
    _count+=1

app = gui.Desktop()
app.connect(gui.QUIT,app.quit,None)

main = gui.Container(width=500, height=400)


main.add(gui.Label("Playlist", cls="h1"), 20, 20)

my_list = gui.List(width=400, height=400)
main.add(my_list, 0, 100)

add = gui.Button("Add file", width=150)
main.add(add, 420, 110)
add.connect(gui.CLICK, open_file_browser, None)

remove = gui.Button("Remove selected", width=150)
main.add(remove, 420, 140)
remove.connect(gui.CLICK, remove_list_item, None)

b = gui.Button("Clear", width=150)
main.add(b, 420, 170)
b.connect(gui.CLICK, clear_list, None)

app.run(main)


#for i in files:
#	print i
