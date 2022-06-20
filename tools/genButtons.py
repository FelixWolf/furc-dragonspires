#!/usr/bin/env python3
try:
    from PIL import Image, ImageDraw, ImageOps, ImageFont
except ModuleNotFoundError:
    pass
import fox5

Fox = fox5.Fox5()

Container = fox5.Fox5File()
Container["ImageList"] = []
Container["Generator"] = 0xFF
Fox.append(Container)


KS_FRAME = 29 #0x18
KS_STOP = 0x0c

def generateBar(container, color):
    Object = fox5.Fox5Object()
    container.append(Object)
    
    Object["EditType"] = 13
    Object["Flags"] = 0
    
    Shape = fox5.Fox5Shape()
    Object.append(Shape)
    
    healthImages = []
    for i in range(101):
        im = Image.new("RGBA", (14,117))
        draw = ImageDraw.Draw(im)
        h = ((i / 100) * 116)
        if h != 0:
            draw.rectangle([(0,116 - h), (14, 116)], fill=color)
        healthImages.append(fox5.Fox5Image.fromPIL(im))
    
    container["ImageList"].extend(healthImages)
    
    Shape["KitterSpeak"] = [(11,100,0)]
    for i in range(101):
        Shape["KitterSpeak"].append((KS_FRAME, i, 0))
        Shape["KitterSpeak"].append((KS_STOP, 0, 0))
    
    Shape["State"] = 0
    Shape["Direction"] = 0
    Shape["Ratio"] = (1, 1)
    Shape["Purpose"] = 5
    
    for i in range(101):
        Frame = fox5.Fox5Frame()
        Frame["FrameOffset"] = (0, 0)
        Frame["FurreOffset"] = (0, 0)
        Shape.append(Frame)
        
        Sprite = fox5.Fox5Sprite()
        Frame.append(Sprite)
        
        Sprite["Purpose"] = 16
        Sprite["Image"] = container["ImageList"].index(healthImages[i]) + 1

font = ImageFont.truetype("/home/felix/.fonts/Timesbd.TTF", 11)
font.fontmode = "0"

def generateText(container, count, color, bg="#000000", mode = 0):
    Object = fox5.Fox5Object()
    container.append(Object)
    
    Object["EditType"] = 13
    Object["Flags"] = 0
    
    Shape = fox5.Fox5Shape()
    Object.append(Shape)
    
    healthImages = []
    for i in range(count):
        if mode == 0:
            im = Image.new("RGBA", (12,12))
        elif mode == 1:
            im = Image.new("RGBA", (54,12))
        draw = ImageDraw.Draw(im)
        draw.fontmode = "1"
        offset = font.getlength(str(i))
        if mode == 0:
            offset = im.width - offset
        elif mode == 1:
            offset = (im.width - offset) / 2
        draw.text((offset + 1, 1), str(i), font=font, fill=bg)
        draw.text((offset, 0), str(i), font=font, fill=color)
        healthImages.append(fox5.Fox5Image.fromPIL(im))
    
    container["ImageList"].extend(healthImages)
    
    Shape["KitterSpeak"] = [(11,100,0)]
    for i in range(count):
        Shape["KitterSpeak"].append((KS_FRAME, i, 0))
        Shape["KitterSpeak"].append((KS_STOP, 0, 0))
    
    Shape["State"] = 0
    Shape["Direction"] = 0
    Shape["Ratio"] = (1, 1)
    Shape["Purpose"] = 5
    
    for i in range(count):
        Frame = fox5.Fox5Frame()
        Frame["FrameOffset"] = (0, 0)
        Frame["FurreOffset"] = (0, 0)
        Shape.append(Frame)
        
        Sprite = fox5.Fox5Sprite()
        Frame.append(Sprite)
        
        Sprite["Purpose"] = 16
        Sprite["Image"] = container["ImageList"].index(healthImages[i]) + 1


def generateBlank(container):
    Object = fox5.Fox5Object()
    container.append(Object)
    
    Object["EditType"] = 13
    Object["Flags"] = 0
    
    Shape = fox5.Fox5Shape()
    Object.append(Shape)
    
    Shape["State"] = 0
    Shape["Direction"] = 0
    Shape["Ratio"] = (1, 1)
    Shape["Purpose"] = 5
    
    Frame = fox5.Fox5Frame()
    Frame["FrameOffset"] = (0, 0)
    Frame["FurreOffset"] = (0, 0)
    Shape.append(Frame)
    
    Sprite = fox5.Fox5Sprite()
    Frame.append(Sprite)
    
    Sprite["Purpose"] = 16
    Sprite["Image"] = 0
    

generateBar(Container, "#00cf00")
generateBlank(Container)
generateBar(Container, "#0000cf")
generateBlank(Container)
generateText(Container, 100, "#00ff00")
generateBlank(Container)
generateText(Container, 100, "#00ff00")
generateBlank(Container)
generateText(Container, 1000, "#FFD700", mode = 1)
generateBlank(Container)
with open("test.fox", "wb") as f:
    f.write(bytes(Fox))
