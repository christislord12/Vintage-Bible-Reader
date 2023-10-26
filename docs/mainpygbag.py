import platform;
from panda3d.core import loadPrcFileData
loadPrcFileData('', 'textures-power-2 up')
loadPrcFileData("", "sync-video t")
loadPrcFileData("", "show-frame-rate-meter f")
#loadPrcFileData("", "win-size 800 600")
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.task import Task
import direct
from direct.showbase.DirectObject import DirectObject
import sys
import asyncio
from panda3d.core import WindowProperties


class Game(DirectObject):

    async def main(self):
        await asyncio.sleep(1)
        
        # load assets here
        base = ShowBase()
        platform.window.window_resize()
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
        self.TextHoldingNode.setTextColor(0,1,0,1)
        self.GalleryButton = DirectButton(text = ("Bible Image Gallery"), scale=.15,frameColor=(0,255,0,255), command=self.ShowBibleImageGallery)
        self.GalleryButton.setPos(0,0,0.9)
        self.GalleryButton.setScale(0.07)
        # load first book
        self.LoadNextBook()
        # black background
        base.setBackgroundColor(0,0,0,1)
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

        while not asyncio.get_running_loop().is_closed():
            try:
                direct.task.TaskManagerGlobal.taskMgr.step()
            except SystemExit:
                break

            # go to host
            await asyncio.sleep(0)
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
        self.TextHoldingNode.setTextColor(0,1,0,1)
    def BookLoad(self):
        self.ClearText()
        base.trackball.node().setPos(-7.55,0,6)
        self.GalleryButton.hide()
        textfile = open("BibleText/" + str(self.CurrentBibleBookNum) + ".txt")
        if self.CurrentBibleBookNum == 0:
            self.GalleryButton.show()
        self.hi = 1
        for line in textfile.read().splitlines():
                self.text = TextNode("node name")
                self.text.setText(line)
                textNodePath = aspect2d.attachNewNode(self.text)
                textNodePath.setScale(0.4)
                textNodePath.setPos(-2,30,self.hi)
                textNodePath.reparentTo(self.TextHolder)
                self.text.setTextColor(0,1,0,1)
                self.hi = self.hi - 0.5
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
        self.image.setPos(7.55,30,-6)   
        base.trackball.node().setPos(-7.55,0,6)
    def PreviousBibleImage(self):
        self.currentbibleimage = self.currentbibleimage - 1;
        if self.currentbibleimage <= 0:
            self.currentbibleimage = 1
        self.image.removeNode()
        self.image = self.loadImageAsPlane("BibleImages/" + str(self.currentbibleimage) + ".jpg")
        self.image.reparentTo(render) 
        self.image.setPos(7.55,30,-6)   
        base.trackball.node().setPos(-7.55,0,6)
        if self.currentbibleimage == 5:
            self.image.setScale(4)
    def NextBibleImage(self):
        self.currentbibleimage = self.currentbibleimage + 1;
        if self.currentbibleimage >= 9:
            self.currentbibleimage = 8

        self.image.removeNode()
        self.image = self.loadImageAsPlane("BibleImages/" + str(self.currentbibleimage) + ".jpg")
        self.image.reparentTo(render)
        self.image.setPos(7.55,30,-6)   
        base.trackball.node().setPos(-7.55,0,6)
        if self.currentbibleimage == 5:
            self.image.setScale(4)
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

asyncio.run(Game().main())

# Do not add anything from here, especially sys.exit/pygame.quit
# asyncio.run is non-blocking on pygame-wasm and code would be executed
# right before program start main()