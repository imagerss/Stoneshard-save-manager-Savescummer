#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import os
import shutil
import time
import datetime
from PIL import Image, ImageTk

appdataPath = os.getenv('APPDATA')
appdataLocalPath = os.getenv('LOCALAPPDATA')
pathToSaveFolder = os.path.join(appdataPath, 'StoneshardSaver')
pathToCharacterFolder=os.path.join(appdataLocalPath,'StoneShard','characters_v1')



def show_info():
    selected_item = characters_select.get()
    info_text.delete("1.0", tk.END)
    selected_path = os.path.join(pathToCharacterFolder, selected_item)
    selected_path = os.path.join(selected_path, "exitsave_1")
    info_text.insert(tk.END, f"Selected item: {selected_path}")

def save_game():
    selected_item = characters_select.get()
    selected_path = os.path.join(pathToCharacterFolder, selected_item, "exitsave_1")
    src_folder = selected_path
    dst_folder = os.path.join(pathToSaveFolder, selected_item)

    timestamp = int(time.time())
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    date_string = dt_object.strftime("%Y-%m-%d-%H-%M-%S")

    dst_folder = os.path.join(dst_folder, date_string)

    if (shutil.copytree(src_folder, os.path.join(dst_folder, "exitsave_1"))):
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, f"Saved success " + str(int(time.time())))
        update_box()



def update_box(*args):
    selection=characters_select.get()
    saveBox.delete(0, tk.END)
    path=os.path.join(pathToSaveFolder,selection)
    if(os.path.exists(path) and os.listdir(path)):
        savepoints=[d for d in os.listdir(path)]
        for savepoint in reversed(savepoints):
            saveBox.insert(tk.END,savepoint)
        saveBox.select_clear(0,tk.END)
        saveBox.select_set(0)
        loadSavePreview()
    else:
        saveBox.insert(tk.END,"Make first save")
        loadSavePreview()
        

def delete_save():
    selectedSave=saveBox.curselection()
    selectedSave=saveBox.get(selectedSave)

    selectedSave = str(selectedSave)
    selection=characters_select.get()
    saveToDelete=os.path.join(pathToSaveFolder,selection,selectedSave)
    info_text.delete("1.0", tk.END)
    try:
        shutil.rmtree(saveToDelete)
        info_text.insert(tk.END,"Deleted "+ selectedSave)
    except FileNotFoundError:
        info_text.insert(tk.END,"No such save "+ selectedSave)
    except Exception as e:
        info_text.insert(tk.END,"Error: "+ e)


    update_box()


def loadSavePreview(*args):
    selection=characters_select.get()
    path=os.path.join(pathToSaveFolder,selection)
    if(os.path.exists(path) and os.listdir(path)):
        selectedSave=str(saveBox.get(saveBox.curselection()))
        for widget in image_frame.winfo_children():
            widget.destroy()

        image=Image.open(os.path.join(pathToSaveFolder,selection,selectedSave,"exitsave_1","preview.png"))
        image=image.resize((309, 106), Image.ANTIALIAS)
    else:
        image=Image.open("example.png")

    image = ImageTk.PhotoImage(image)
    label = tk.Label(image_frame, image=image)
    label.image = image
    label.grid(row=0, column=0)
    currentSavePath=os.path.join(pathToCharacterFolder,characters_select.get(),'exitsave_1','preview.png')
    
    for widget in FrameCurrentSave.winfo_children():
            widget.destroy()
    if(os.path.exists(currentSavePath)):
        currentSave=Image.open(currentSavePath)
        curImage=ImageTk.PhotoImage(currentSave)

    else:
        currentSave=Image.open("example.png")
        curImage=ImageTk.PhotoImage(currentSave)

    labelCurrent=tk.Label(FrameCurrentSave,image=curImage)
    labelCurrent.image=curImage
    labelCurrent.grid(row=0, column=0)



        
def loadGame():
    selection=characters_select.get()

    selectedSave=saveBox.curselection()
    selectedSave=saveBox.get(selectedSave)
    selectedSave = str(selectedSave)

    path=os.path.join(pathToSaveFolder,selection,selectedSave,"exitsave_1")
    dest=os.path.join(pathToCharacterFolder,selection,"exitsave_1")
    if(shutil.copytree(path, dest, dirs_exist_ok=True)):
        info_text.delete("1.0",tk.END)
        info_text.insert(tk.END,"Save loaded sucesfully " + selectedSave)
        loadSavePreview()

characters = [d for d in os.listdir(pathToCharacterFolder) if os.path.isdir(
    os.path.join(pathToCharacterFolder, d))]       

        # build ui
toplevel = tk.Tk() 
toplevel.configure(
    background="#ffffff",
    height=500,
    highlightbackground="#ffffff",
    width=800)

image_frame = ttk.Frame(toplevel)
image_frame.configure(height=81, width=200)
image_frame.place(
anchor="nw",
    bordermode="outside",
    height=100,
    relwidth=0.39,
    relx=0.6,
    rely=0.75)

saveBox = tk.Listbox(toplevel)
saveBox.configure(height=10, width=50)
saveBox.place(
    anchor="nw",
    relheight=0.6,
    relwidth=0.29,
    relx=0.70,
    rely=0.1,
    x=0,
    y=0)
ButtonSave = ttk.Button(toplevel, command=delete_save)
ButtonSave.configure(text='Delete')
ButtonSave.place(
    anchor="nw",
    relwidth=0.08,
    relx=0.60,
    rely=0.2,
    x=0,
    y=0)
ButtonLoad = ttk.Button(toplevel, command=loadGame)
ButtonLoad.bind("<<ButtonPressed>>",loadSavePreview)
ButtonLoad.configure(text='Load')
ButtonLoad.place(
    anchor="nw",
    relwidth=0.08,
    relx=0.60,
    rely=0.1,
    x=0,
    y=0)
LabelSavePoints = ttk.Label(toplevel)
LabelSavePoints.configure(
    background="#ffffff", text='Save Points:')
LabelSavePoints.place(anchor="nw", relx=0.8, rely=0.05, x=0, y=0)
info_text = tk.Text(toplevel)
info_text.configure(height=81, width=200)
info_text.place(
    anchor="nw",
    bordermode="inside",
    height=100,
    relwidth=0.55,
    relx=0.01,
    rely=0.75)
label9 = ttk.Label(toplevel)
label9.configure(background="#ffffff", text='Current exit save:')
label9.place(anchor="nw", relx=0.01, rely=0.25, x=0, y=0)
FrameCurrentSave = ttk.Frame(toplevel)
FrameCurrentSave.configure(height=200, width=200)
FrameCurrentSave.place(
    anchor="nw",
    height=180,
    relx=0.01,
    rely=0.30,
    width=400,
    x=0)

characters_select = ttk.Combobox(toplevel, values=characters)
characters_select.current(0)
characters_select.bind("<<ComboboxSelected>>", update_box)

characters_select.place(
    anchor="nw", relx=0.2, rely=.1, x=0, y=0)
LabelCharSelect = ttk.Label(toplevel)
LabelCharSelect.configure(
    background="#ffffff",
    compound="bottom",
    text='Character:')
LabelCharSelect.place(anchor="nw", relx=0.12, rely=.1, x=0, y=0)
ButtonDelete = ttk.Button(toplevel,command=save_game)
ButtonDelete.configure(text='Save')
ButtonDelete.place(anchor="nw", relx=.429, rely=.24, x=0, y=0)
saveBox.bind("<<ListboxSelect>>", loadSavePreview)

update_box()
loadSavePreview()
toplevel.title("Stoneshard Savecummer v1.0")
toplevel.resizable(False,False)
toplevel.mainloop()
