from controller import Controller
from Tkinter import *
from tkMessageBox import askyesno

VERSION = 1.0

class Interface():
    #Initialize
    def __init__(self):
        '''Initializes the interface.'''
        self.c = Controller()
        
        self.c.setI(self)
        
        self.constructRoot()
        
        self.mode = ""
        
        self.runRoot()
    
    #Popup    
    def confirm(self, msg):
        '''Queries the user to confirm, returns their response.'''
        return askyesno("Confirm", msg)
        
    #Create
    def constructCreateWindow(self):
        '''Creates the creation window.'''
        self.createWindow = Toplevel()
        self.createFrame = Frame(self.createWindow)
        self.createFrame.grid()
    
    #Delete
    def deleteItem(self):
        '''Deletes an item from the disk.'''
        if self.rootItemsBox.curselection():
            self.c.deleteItem(self.rootItemsBox.get(self.rootItemsBox.curselection()[0]))
    
    #Root
    def constructRoot(self):
        '''Creates the root window.'''
        self.rootRoot = Tk()
        self.rootFrame = Frame(self.rootRoot)
        
        self.rootFrame.grid()
        
        self.rootRoot.title("EpiEngine Editor v%.1f" % VERSION)
        
        #MENU###################################################################
        self.rootMenuBar = Menu(self.rootRoot)
        
        #File menu
        filemenu = Menu(self.rootMenuBar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.rootMenuBar.quit)
        self.rootMenuBar.add_cascade(label="File", menu=filemenu)
        
        #Edit menu
        editmenu = Menu(self.rootMenuBar, tearoff=0)
        editmenu.add_command(label="Create", command=self.constructCreateWindow)
        editmenu.add_command(label="Delete", command=self.deleteItem)
        self.rootMenuBar.add_cascade(label="Edit", menu=editmenu)
        
        #Config Menu
        configmenu = Menu(self.rootMenuBar, tearoff=0)
        configmenu.add_command(label="System Information", command=self.c.openConfigureSystem)
        configmenu.add_command(label="CVars", command=self.c.openConfigureCVars)
        configmenu.add_command(label="Localization", command=self.c.openConfigureLocalization)
        configmenu.add_command(label="Input", command=self.c.openConfigureInput)
        configmenu.add_command(label="Preload", command=self.c.openConfigurePreload)
        self.rootMenuBar.add_cascade(label="Config", menu=configmenu)
        
        #Window Menu
        windowmenu = Menu(self.rootMenuBar, tearoff=0)
        windowmenu.add_command(label="Asset Browser", command=self.constructAssetWindow)
        windowmenu.add_command(label="Shader Editor", command=self.constructShaderEditor)
        windowmenu.add_command(label="Script Editor", command=self.constructScriptEditor)
        self.rootMenuBar.add_cascade(label="Window", menu=windowmenu)
        
        #Help Menu
        helpmenu = Menu(self.rootMenuBar, tearoff=0)
        helpmenu.add_command(label="About", command=self.constructAboutWindow)
        self.rootMenuBar.add_cascade(label="Help", menu=helpmenu)
        
        self.rootRoot.config(menu=self.rootMenuBar)
        
        #TYPES LIST###################################################################
        self.rootTypesLabel = Label(self.rootFrame, text="Categories:")
        self.rootTypesLabel.grid(row=1, column=1, sticky=W)
        
        self.rootScrollbar = Scrollbar(self.rootFrame)
        self.rootScrollbar.grid(row=2, column=2, sticky=N+S)
        
        self.rootHbar = Scrollbar(self.rootFrame, orient=HORIZONTAL)
        self.rootHbar.grid(row=3, column=1, sticky=E+W)
        
        self.rootBox = Listbox(self.rootFrame, width=25, height=40, yscrollcommand=self.rootScrollbar.set, xscrollcommand=self.rootHbar.set)
        self.rootBox.grid(row=2, column=1, sticky=N+S+E+W)
        
        self.rootScrollbar.config(command=self.rootBox.yview)
        self.rootHbar.config(command=self.rootBox.xview)
        
        self.rootBox.insert(END, "Animations")
        self.rootBox.insert(END, "Dialog")
        self.rootBox.insert(END, "Entities")
        self.rootBox.insert(END, "Levels")
        self.rootBox.insert(END, "Meshes")
        self.rootBox.insert(END, "Sounds")
        self.rootBox.insert(END, "Music")
        self.rootBox.insert(END, "UI")
        
        self.rootBox.bind('<<ListboxSelect>>', self.changeMode)
        
        #Items LIST###################################################################
        self.rootItemsLabel = Label(self.rootFrame, text="Assets:")
        self.rootItemsLabel.grid(row=1, column=3, sticky=W)
        
        self.rootItemsScrollbar = Scrollbar(self.rootFrame)
        self.rootItemsScrollbar.grid(row=2, column=4, sticky=N+S)
        
        self.rootItemsHbar = Scrollbar(self.rootFrame, orient=HORIZONTAL)
        self.rootItemsHbar.grid(row=3, column=3, sticky=E+W)
        
        self.rootItemsBox = Listbox(self.rootFrame, width=200, height=40, yscrollcommand=self.rootItemsScrollbar.set, xscrollcommand=self.rootItemsHbar.set)
        self.rootItemsBox.grid(row=2, column=3, sticky=N+S+E+W)
        
        self.rootItemsScrollbar.config(command=self.rootItemsBox.yview)
        self.rootItemsHbar.config(command=self.rootItemsBox.xview)
        
        self.rootItemsBox.bind('<Double-Button-1>', self.openUpdateItem)
        
        #BUTTONS######################################################################
        self.rootAddButton = Button(self.rootFrame, text=" + ", command=self.constructCreateWindow)
        self.rootAddButton.grid(row=4, column=3, sticky=W)
        
        self.rootRemoveButton = Button(self.rootFrame, text=" - ", command=self.deleteItem)
        self.rootRemoveButton.grid(row=4, column=3, sticky=E)
    
    def changeMode(self, event=None):
        '''Changes the mode of the root window.'''
        if self.rootBox.curselection():
            item = self.rootBox.get(self.rootBox.curselection()[0])
            self.mode = item
            
            self.updateRoot()
            
    def updateRoot(self):
        '''Updates the root.'''
        self.rootItemsBox.delete(0, END)
        
        items = self.c.getItems(self.mode)
        
        for item in items:
            self.rootItemsBox.insert(END, item)
        
    def runRoot(self):
        '''Runs the interface.'''
        self.rootRoot.mainloop()
    
    #Config windows
    def constructCVarWindow(self, data):
        '''Initializes the Cvar configuration window.'''
        pass
    
    def constructLocalizationWindow(self, data):
        '''Initializes the Localization configuration window.'''
        pass
    
    def constructSystemWindow(self, data):
        '''Initializes the System configuration window.'''
        pass
        
    def constructInputWindow(self, data):
        ''''Constructs the input configuration window.'''
        pass
    
    def constructPreloadWindow(self, data):
        '''Constructs the preload configuration window.'''
        pass
    
    #About Window
    def constructAboutWindow(self):
        '''Initializes the about window.'''
        self.aboutWindow = Toplevel()
        self.aboutFrame = Frame(self.aboutWindow)
        self.aboutFrame.grid()
        
        self.aboutWindow.title("About")
        
        self.aboutLabel = Label(self.aboutFrame, text="EpiEngine Editor v%.1f" % VERSION)
        self.aboutLabel.grid(row=1, column=1, sticky=W)
    
    #Asset Browser
    def constructAssetBrowser(self):
        '''Constructs the asset browser.'''
        pass
    
    #Script Editor
    def constructScriptEditor(self):
        '''Constructs the script editor.'''
        pass
    
    #Shader Editor
    def constructShaderEditor(self):
        '''Constructs the shader editor.'''
        pass
        
    #Update 
    def constructUpdateWindow(self, data):
        '''Initializes the update window.'''
        self.updateWindow = Toplevel()
        self.updateFrame = Frame(self.updateWindow)
        self.updateFrame.grid()
        
        self.updateWindow.title("Update")
        
        if self.mode == "Entities":
            #Name
            self.nameLabel = Label(self.updateFrame, text="Name:")
            self.nameLabel.grid(row=1, column=1, sticky=W)
            
            self.nameEntry = Entry(self.updateFrame)
            self.nameEntry.grid(row=1, column=2, sticky=W)
            
            self.nameEntry.insert(END, data["name"])
            
            #Type
            self.typeLabel = Label(self.updateFrame, text="Type:")
            self.typeLabel.grid(row=2, column=1, sticky=W)
            
            self.typeVar = StringVar()
            self.typeVar.set(data["type"])
            
            self.typeEntry = OptionMenu(self.updateFrame, self.typeVar, "Object", "Light", "Camera")
            self.typeEntry.grid(row=2, column=2, sticky=W)
            
            #ResourcePath
            self.resourceLabel = Label(self.updateFrame, text="Resource path:")
            self.resourceLabel.grid(row=3, column=1, sticky=W)
            
            self.resourceEntry = Entry(self.updateFrame)
            self.resourceEntry.grid(row=3, column=2, sticky=W)
            
            self.resourceEntry.insert(END, data["resourcePath"])
            
            #ScriptPath
            self.scriptLabel = Label(self.updateFrame, text="Script path:")
            self.scriptLabel.grid(row=4, column=1, sticky=W)
            
            self.scriptEntry = Entry(self.updateFrame)
            self.scriptEntry.grid(row=4, column=2, sticky=W)
            
            self.scriptEntry.insert(END, data["scriptPath"])
            
            #Flags
            self.flagsLabel = Label(self.updateFrame, text="Flags:")
            self.flagsLabel.grid(row=5, column=1, sticky=W)
            
            self.flagsEntry = Entry(self.updateFrame)
            self.flagsEntry.grid(row=5, column=2, sticky=W)
            
            self.flagsEntry.insert(END, str(data["flags"]))
            
            #Properties
            self.propLabel = Label(self.updateFrame, text="Properties:")
            self.propLabel.grid(row=6, column=1, sticky=W)
            
            self.propEntry = Entry(self.updateFrame)
            self.propEntry.grid(row=6, column=2, sticky=W)
            
            self.propEntry.insert(END, data["properties"])
            
        elif self.mode == "Meshes":
            #Name
            self.nameLabel = Label(self.updateFrame, text="Name:")
            self.nameLabel.grid(row=1, column=1, sticky=W)
            
            self.nameEntry = Entry(self.updateFrame)
            self.nameEntry.grid(row=1, column=2, sticky=W)
            
            self.nameEntry.insert(END, data["name"])
            
            #ResourcePath
            self.resourceLabel = Label(self.updateFrame, text="Resource path:")
            self.resourceLabel.grid(row=3, column=1, sticky=W)
            
            self.resourceEntry = Entry(self.updateFrame)
            self.resourceEntry.grid(row=3, column=2, sticky=W)
        
            self.resourceEntry.insert(END, data["resourcePath"])
        
        elif self.mode == "Sounds":
            #Name
            self.nameLabel = Label(self.updateFrame, text="Name:")
            self.nameLabel.grid(row=1, column=1, sticky=W)
            
            self.nameEntry = Entry(self.updateFrame)
            self.nameEntry.grid(row=1, column=2, sticky=W)
            
            self.nameEntry.insert(END, data["name"])
            
            #Resources
            self.resourceLabel = Label(self.updateFrame, text="Resources:")
            self.resourceLabel.grid(row=1, column=1, sticky=W)
            
            self.resourceEntry = Entry(self.updateFrame)
            self.resourceEntry.grid(row=1, column=2, sticky=W)
            
            self.resourceEntry.insert(END, data["resources"])
            
            #3D
            self.D3Label = Label(self.updateFrame, text="3D:")
            self.D3Label.grid(row=3, column=1, sticky=W)
            
            self.D3Var = IntVar()
            self.D3Var.set(data["3D"])
            self.D3Entry = Checkbutton(self.updateFrame, variable=self.D3Var)
            self.D3Entry.grid(row=3, column=2, sticky=W)
            
            #Loop
            self.loopLabel = Label(self.updateFrame, text="Loop:")
            self.loopLabel.grid(row=4, column=1, sticky=W)
            
            self.loopVar = IntVar()
            self.loopVar.set(data["loop"])
            self.loopEntry = Checkbutton(self.updateFrame, variable=self.loopVar)
            self.loopEntry.grid(row=4, column=2, sticky=W)
            
            #Volume
            self.volumeLabel = Label(self.updateFrame, text="Volume:")
            self.volumeLabel.grid(row=5, column=1, sticky=W)
            
            self.volumeEntry = Entry(self.updateFrame)
            self.volumeEntry.grid(row=5, column=2, sticky=W)
            
            self.volumeEntry.insert(END, data["volume"])
        
        elif self.mode == "Levels":
            #Name
            self.nameLabel = Label(self.updateFrame, text="Name:")
            self.nameLabel.grid(row=1, column=1, sticky=W)
            
            self.nameEntry = Entry(self.updateFrame)
            self.nameEntry.grid(row=1, column=2, sticky=W)
            
            self.nameEntry.insert(END, data["name"])
            
            #Type
            self.typeLabel = Label(self.updateFrame, text="Type:")
            self.typeLabel.grid(row=2, column=1, sticky=W)
            
            self.typeVar = StringVar()
            self.typeVar.set(data["type"])
            
            self.typeEntry = OptionMenu(self.updateFrame, self.typeVar, "Object")
            self.typeEntry.grid(row=2, column=2, sticky=W)
            
            #Skeleton
            self.resourceLabel = Label(self.updateFrame, text="Resource path:")
            self.resourceLabel.grid(row=3, column=1, sticky=W)
            
            self.resourceEntry = Entry(self.updateFrame)
            self.resourceEntry.grid(row=3, column=2, sticky=W)
            
            self.resourceEntry.insert(END, data["resourcePath"])
            
            #ScriptPath
            self.scriptLabel = Label(self.updateFrame, text="Script path:")
            self.scriptLabel.grid(row=4, column=1, sticky=W)
            
            self.scriptEntry = Entry(self.updateFrame)
            self.scriptEntry.grid(row=4, column=2, sticky=W)
            
            self.scriptEntry.insert(END, data["scriptPath"])
            
            #Properties
            self.propLabel = Label(self.updateFrame, text="Properties:")
            self.propLabel.grid(row=6, column=1, sticky=W)
            
            self.propEntry = Entry(self.updateFrame)
            self.propEntry.grid(row=6, column=2, sticky=W)
            
            self.propEntry.insert(END, data["properties"])
            
            #Sky
            self.skyLabel = Label(self.updateFrame, text="Sky:")
            self.skyLabel.grid(row=7, column=1, sticky=W)
            
            #R
            self.skyRLabel = Label(self.updateFrame, text="R:")
            self.skyRLabel.grid(row=8, column=1, sticky=W)
            
            self.skyREntry = Entry(self.updateFrame)
            self.skyREntry.grid(row=8, column=2, sticky=W)
            
            self.skyREntry.insert(END, data["sky"]["r"])
            
            #G
            self.skyGLabel = Label(self.updateFrame, text="G:")
            self.skyGLabel.grid(row=9, column=1, sticky=W)
            
            self.skyGEntry = Entry(self.updateFrame)
            self.skyGEntry.grid(row=9, column=2, sticky=W)
            
            self.skyGEntry.insert(END, data["sky"]["g"])
            
            #B
            self.skyBLabel = Label(self.updateFrame, text="B:")
            self.skyBLabel.grid(row=10, column=1, sticky=W)
            
            self.skyBEntry = Entry(self.updateFrame)
            self.skyBEntry.grid(row=10, column=2, sticky=W)
            
            self.skyBEntry.insert(END, data["sky"]["b"])
        
        elif self.mode == "UI":
            #Name
            self.nameLabel = Label(self.updateFrame, text="Name:")
            self.nameLabel.grid(row=1, column=1, sticky=W)
            
            self.nameEntry = Entry(self.updateFrame)
            self.nameEntry.grid(row=1, column=2, sticky=W)
            
            self.nameEntry.insert(END, data["name"])
            
            #Type
            self.typeLabel = Label(self.updateFrame, text="Type:")
            self.typeLabel.grid(row=2, column=1, sticky=W)
            
            self.typeVar = StringVar()
            self.typeVar.set(data["type"])
            
            self.typeEntry = OptionMenu(self.updateFrame, self.typeVar, "Object")
            self.typeEntry.grid(row=2, column=2, sticky=W)
            
            #ResourcePath
            self.resourceLabel = Label(self.updateFrame, text="Resource path:")
            self.resourceLabel.grid(row=3, column=1, sticky=W)
            
            self.resourceEntry = Entry(self.updateFrame)
            self.resourceEntry.grid(row=3, column=2, sticky=W)
            
            self.resourceEntry.insert(END, data["resourcePath"])
            
            #ScriptPath
            self.scriptLabel = Label(self.updateFrame, text="Script path:")
            self.scriptLabel.grid(row=4, column=1, sticky=W)
            
            self.scriptEntry = Entry(self.updateFrame)
            self.scriptEntry.grid(row=4, column=2, sticky=W)
            
            self.scriptEntry.insert(END, data["scriptPath"])
        
        elif self.mode == "Dialog":
            #Name
            self.nameLabel = Label(self.updateFrame, text="Name:")
            self.nameLabel.grid(row=1, column=1, sticky=W)
            
            self.nameEntry = Entry(self.updateFrame)
            self.nameEntry.grid(row=1, column=2, sticky=W)
            
            self.nameEntry.insert(END, data["name"])
            
            #Resources
            self.resourceLabel = Label(self.updateFrame, text="Resources:")
            self.resourceLabel.grid(row=1, column=1, sticky=W)
            
            self.resourceEntry = Entry(self.updateFrame)
            self.resourceEntry.grid(row=1, column=2, sticky=W)
            
            self.resourceEntry.insert(END, data["resources"])
            
            #3D
            self.D3Label = Label(self.updateFrame, text="3D:")
            self.D3Label.grid(row=3, column=1, sticky=W)
            
            self.D3Var = IntVar()
            self.D3Var.set(data["3D"])
            self.D3Entry = Checkbutton(self.updateFrame, variable=self.D3Var)
            self.D3Entry.grid(row=3, column=2, sticky=W)
            
            #Loop
            self.loopLabel = Label(self.updateFrame, text="Loop:")
            self.loopLabel.grid(row=4, column=1, sticky=W)
            
            self.loopVar = IntVar()
            self.loopVar.set(data["loop"])
            self.loopEntry = Checkbutton(self.updateFrame, variable=self.loopVar)
            self.loopEntry.grid(row=4, column=2, sticky=W)
            
            #Volume
            self.volumeLabel = Label(self.updateFrame, text="Volume:")
            self.volumeLabel.grid(row=5, column=1, sticky=W)
            
            self.volumeEntry = Entry(self.updateFrame)
            self.volumeEntry.grid(row=5, column=2, sticky=W)
            
            self.volumeEntry.insert(END, data["volume"])
        
        elif self.mode == "Music":
            #Name
            self.nameLabel = Label(self.updateFrame, text="Name:")
            self.nameLabel.grid(row=1, column=1, sticky=W)
            
            self.nameEntry = Entry(self.updateFrame)
            self.nameEntry.grid(row=1, column=2, sticky=W)
            
            self.nameEntry.insert(END, data["name"])
            
            #Resources
            self.resourceLabel = Label(self.updateFrame, text="Resources:")
            self.resourceLabel.grid(row=1, column=1, sticky=W)
            
            self.resourceEntry = Entry(self.updateFrame)
            self.resourceEntry.grid(row=1, column=2, sticky=W)
            
            self.resourceEntry.insert(END, data["resources"])
            
            #3D
            self.D3Label = Label(self.updateFrame, text="3D:")
            self.D3Label.grid(row=3, column=1, sticky=W)
            
            self.D3Var = IntVar()
            self.D3Var.set(data["3D"])
            self.D3Entry = Checkbutton(self.updateFrame, variable=self.D3Var)
            self.D3Entry.grid(row=3, column=2, sticky=W)
            
            #Loop
            self.loopLabel = Label(self.updateFrame, text="Loop:")
            self.loopLabel.grid(row=4, column=1, sticky=W)
            
            self.loopVar = IntVar()
            self.loopVar.set(data["loop"])
            self.loopEntry = Checkbutton(self.updateFrame, variable=self.loopVar)
            self.loopEntry.grid(row=4, column=2, sticky=W)
            
            #Volume
            self.volumeLabel = Label(self.updateFrame, text="Volume:")
            self.volumeLabel.grid(row=5, column=1, sticky=W)
            
            self.volumeEntry = Entry(self.updateFrame)
            self.volumeEntry.grid(row=5, column=2, sticky=W)
            
            self.volumeEntry.insert(END, data["volume"])
            
        elif self.mode == "Animations":
            #Name
            self.nameLabel = Label(self.updateFrame, text="Name:")
            self.nameLabel.grid(row=1, column=1, sticky=W)
            
            self.nameEntry = Entry(self.updateFrame)
            self.nameEntry.grid(row=1, column=2, sticky=W)
            
            self.nameEntry.insert(END, data["name"])
            
            #Mode
            self.modeLabel = Label(self.updateFrame, text="Mode:")
            self.modeLabel.grid(row=2, column=1, sticky=W)
            
            self.modeVar = StringVar()
            self.modeVar.set(data["mode"])
            
            self.modeEntry = OptionMenu(self.updateFrame, self.modeVar, "play", "loop", "frame")
            self.modeEntry.grid(row=2, column=2, sticky=W)
            
            #Skeleton
            self.skeletonLabel = Label(self.updateFrame, text="Skeleton:")
            self.skeletonLabel.grid(row=3, column=1, sticky=W)
            
            self.skeletonVar = IntVar()
            self.skeletonVar.set(data["skeleton"])
            self.skeletonEntry = Checkbutton(self.updateFrame, variable=self.skeletonVar)
            self.skeletonEntry.grid(row=3, column=2, sticky=W)
            
            #Start
            self.startLabel = Label(self.updateFrame, text="Start:")
            self.startLabel.grid(row=4, column=1, sticky=W)
            
            self.startEntry = Entry(self.updateFrame)
            self.startEntry.grid(row=4, column=2, sticky=W)
            
            self.startEntry.insert(END, data["start"])
            
            #End
            self.endLabel = Label(self.updateFrame, text="End:")
            self.endLabel.grid(row=5, column=1, sticky=W)
            
            self.endEntry = Entry(self.updateFrame)
            self.endEntry.grid(row=5, column=2, sticky=W)
            
            self.endEntry.insert(END, data["end"])
            
            #Layer
            self.layerLabel = Label(self.updateFrame, text="Layer:")
            self.layerLabel.grid(row=6, column=1, sticky=W)
            
            self.layerEntry = Entry(self.updateFrame)
            self.layerEntry.grid(row=6, column=2, sticky=W)
            
            self.layerEntry.insert(END, data["layer"])
            
            #TargetChild
            self.targetChildLabel = Label(self.updateFrame, text="Target child:")
            self.targetChildLabel.grid(row=7, column=1, sticky=W)
            
            self.targetChildEntry = Entry(self.updateFrame)
            self.targetChildEntry.grid(row=7, column=2, sticky=W)
            
            self.targetChildEntry.insert(END, data["targetChild"])
        
        self.submitButton = Button(self.updateFrame, text="Update", command=self.updateItem)
        self.submitButton.grid(row=11, column=2)
        
    def destructUpdateWindow(self):
        '''Clears the update window.'''
        self.updateWindow.destroy()

    def openUpdateItem(self, event=None):
        '''Brings up the dialog to update the item.'''
        if self.rootItemsBox.curselection():
            self.c.openUpdateItem(self.rootItemsBox.get(self.rootItemsBox.curselection()[0]))
            
    def updateItem(self):
        '''Collects arguments for the controller updateItem.'''    
        self.c.updateItem()
        
        self.destructUpdateWindow()

i = Interface()