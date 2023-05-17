from panda3d.core import loadPrcFileData
loadPrcFileData("", "textures-power-2 up")
#loadPrcFileData("", "sync-video t")
loadPrcFileData("", "show-frame-rate-meter f")
loadPrcFileData("", "win-size 800 600")
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
import sys
import emscripten

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.loadingText=OnscreenText("Loading...",1,fg=(1,1,1,1),pos=(0,0),align=TextNode.ACenter,scale=.07,mayChange=1)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame() 
        base.graphicsEngine.renderFrame()
        url = "Bible.mf"
        handle = emscripten.async_wget2(url, "Bible.mf", onload=self.onload, onerror=self.onerror, onprogress=self.onprogress)
    def onload(self, handle, file):
        vfs = VirtualFileSystem.getGlobalPtr()
        vfs.mount(Filename("Bible.mf"), ".", VirtualFileSystem.MFReadOnly)
        self.loadingText.removeNode()
        self.LoadUpApp()
    def onprogress(self, handle, progress):
        print("Downloading files for the program")
    def onerror(self, handle, code):
        print("Download Error")       
    def LoadUpApp(self):
        # book num var. start at -1 since it is upcycled
        self.CurrentBibleBookNum = -1;
        # movement speed
        self.forward_speed = 5.0 # units per second
        self.backward_speed = 2.0
        self.IsInGallery = 0
        # Setup holding node
        self.TextHoldingNode = TextNode("node name")
        self.TextHoldingNode.setText("")
        self.TextHolder = aspect2d.attachNewNode(self.TextHoldingNode)
        self.TextHolder.reparentTo(render)
        #self.TextHoldingNode.setTextColor(1,1,1,1)
        self.GalleryButton = DirectButton(text = ("Bible Image Gallery"), scale=.15,frameColor=(0,255,0,255), command=self.ShowBibleImageGallery)
        self.GalleryButton.setPos(0,0,0.9)
        self.GalleryButton.setScale(0.07)
        # load first book
        self.LoadNextBook()
        # black background
        #base.setBackgroundColor(1,1,1,1)
        self.currentbibleimage = 1;
        # input
        base.accept("escape",sys.exit)
        base.accept("d",self.LoadNextBook)
        base.accept("arrow_right",self.LoadNextBook)
        base.accept("arrow_left",self.LoadPreviousBook)
        base.accept("a",self.LoadPreviousBook)
        # movement input
        self.forward_button = KeyboardButton.up()
        self.backward_button = KeyboardButton.down()
        self.space_button = KeyboardButton.space()
        # camera
        base.useTrackball()
        base.trackball.node().setPos(-7.55,0,6)
        self.NextBookButton = DirectButton(text = (">"), scale=.15,frameColor=(0,255,0,255), command=self.LoadNextBook)
        self.NextBookButton.setPos(1.26,0,0.9)
        self.PrevBookButton = DirectButton(text = ("<"), scale=.15,frameColor=(0,255,0,255), command=self.LoadPreviousBook)
        self.PrevBookButton.setPos(-1.27,0,0.9)
        self.DownButton = DirectButton(text = (">"), scale=.15,frameColor=(0,255,0,255),command=self.GoDown)
        self.DownButton.setHpr(0,0,90)
        self.DownButton.setPos(-1.28,0,-0.9)
        self.UpButton = DirectButton(text = ("<"), scale=.15,frameColor=(0,255,0,255), command=self.GoUp)
        self.UpButton.setHpr(0,0,90)
        self.UpButton.setPos(1.24,0,-0.9)
        taskMgr.add(self.MovementTask, "MovementTask")
        self.ShowBibleImageGallery()
    def LoadNextBook(self):
        if self.IsInGallery == 0:
            self.CurrentBibleBookNum = self.CurrentBibleBookNum + 1
            self.CheckBookNumValue()
            self.BookLoad()
        if self.IsInGallery == 1:
            self.NextBibleImage()
    def LoadPreviousBook(self):
        if self.IsInGallery == 0:
            self.CurrentBibleBookNum = self.CurrentBibleBookNum - 1
            self.CheckBookNumValue()
            self.BookLoad()
        if self.IsInGallery == 1:
            self.PreviousBibleImage()
    def ClearText(self):
        self.TextHolder.removeNode()
        self.TextHoldingNode = TextNode("node name")
        self.TextHoldingNode.setText("")
        self.TextHolder = aspect2d.attachNewNode(self.TextHoldingNode)
        self.TextHolder.reparentTo(render)
      #  self.TextHoldingNode.setTextColor(1,1,1,1)
    def BookLoad(self):
        self.ClearText()
        base.trackball.node().setPos(-7.55,0,6)
        self.GalleryButton.hide()
        if self.CurrentBibleBookNum == 0:
            self.GalleryButton.show()
            
      #  textfile = open("BibleText/" + str(self.CurrentBibleBookNum) + ".txt")
       # url = "BibleText/" + str(self.CurrentBibleBookNum) + ".txt"
        #handle = emscripten.async_wget2(url, str(self.CurrentBibleBookNum) + ".txt", onload=self.oneonload, onerror=self.oneonerror, onprogress=self.oneonprogress)
    def oneonload(self, handle, file):
        self.hi = 1
        for line in file.read().splitlines():
                self.text = TextNode("node name")
                self.text.setText(line)
                textNodePath = aspect2d.attachNewNode(self.text)
                textNodePath.setScale(0.4)
                textNodePath.setPos(-2,30,self.hi)
                textNodePath.reparentTo(self.TextHolder)
                self.text.setTextColor(1,1,1,1)
                self.hi = self.hi - 0.5
    def oneonprogress(self, handle, progress):
        print("Downloading File")
    def oneonerror(self, handle, code):
        print("Download Error")
    def CheckBookNumValue(self):
        if self.CurrentBibleBookNum == 67:
            self.CurrentBibleBookNum = 66              
        if self.CurrentBibleBookNum == -1:
            self.CurrentBibleBookNum = 0
    def GoDown(self):
        base.trackball.node().setPos(-7.55, 0, base.trackball.node().getZ() + 3)
    def GoUp(self):
        base.trackball.node().setPos(-7.55, 0, base.trackball.node().getZ() - 3)
    def ShowBibleImageGallery(self):        
        self.TextHolder.removeNode()
        taskMgr.remove("MovementTask")    
        self.GalleryButton.hide()    
        self.UpButton.hide()
        self.DownButton.hide()
        self.IsInGallery = 1
        self.currentbibleimage = 1;
        self.image = self.loadImageAsPlane("BibleImages/" + str(self.currentbibleimage) + ".jpg")
        self.image.reparentTo(render)    
        self.image.setPos(7.55,6.5,-6)   
        base.trackball.node().setPos(-7.55,0,6)
    def PreviousBibleImage(self):
        self.currentbibleimage = self.currentbibleimage - 1;
        if self.currentbibleimage <= 0:
            self.currentbibleimage = 1
        self.image.removeNode()
        self.image = self.loadImageAsPlane("BibleImages/" + str(self.currentbibleimage) + ".jpg")
        self.image.reparentTo(render) 
        self.image.setPos(7.55,6.5,-6)   
        base.trackball.node().setPos(-7.55,0,6)
    def NextBibleImage(self):
        self.currentbibleimage = self.currentbibleimage + 1;
        if self.currentbibleimage >= 8:
            self.currentbibleimage = 7
        self.image.removeNode()
        self.image = self.loadImageAsPlane("BibleImages/" + str(self.currentbibleimage) + ".jpg")
        self.image.reparentTo(render)
        self.image.setPos(7.55,6.5,-6)   
        base.trackball.node().setPos(-7.55,0,6)
    def loadImageAsPlane(self, filepath, yresolution = 600):
        tex = loader.loadTexture(filepath)
        tex.setBorderColor(Vec4(0,0,0,0))
        tex.setWrapU(Texture.WMBorderColor)
        tex.setWrapV(Texture.WMBorderColor)
        cm = CardMaker(filepath + " card")
        cm.setFrame(-tex.getOrigFileXSize(), tex.getOrigFileXSize(), -tex.getOrigFileYSize(), tex.getOrigFileYSize())
        card = NodePath(cm.generate())
        card.setTexture(tex)
        card.setTransparency(1)
        card.setScale(card.getScale()/ yresolution)
        card.flattenLight()
        return card
    def MovementTask(self,task):
        base.trackball.node().setPos(-7.55, 0, base.trackball.node().getZ())
        base.trackball.node().setHpr(0, 0, 0)
        speed = 0.0
        is_down = base.mouseWatcherNode.is_button_down
        if is_down(self.forward_button):
            speed += self.forward_speed
            y_delta = -5 * globalClock.get_dt()
            base.trackball.node().set_z(base.trackball.node().getZ() + y_delta)
        if is_down(self.backward_button):
            speed -= self.backward_speed
            y_delta = 5 * globalClock.get_dt()
            base.trackball.node().set_z(base.trackball.node().getZ() + y_delta)
        if is_down(self.space_button):
            speed -= self.backward_speed
            y_delta = 5 * globalClock.get_dt()
            base.trackball.node().set_z(base.trackball.node().getZ() + y_delta)
        return task.cont
app = MyApp()
app.run()