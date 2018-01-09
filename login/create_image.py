# coding:utf-8
from PIL import Image,ImageDraw,ImageFont
import time,os

class Creator(object):
    def __init__(self,bgpath,fontpath,fontsize):
        self.ttffont = ImageFont.truetype(fontpath,fontsize)
        self.im = Image.open(bgpath)
        self.draw = ImageDraw.Draw(self.im)

    def addText(self,text,color,position):
        self.draw.text(position, text, fill = color, font=self.ttffont)

    def save(self,outpath):
        self.im.save(outpath)

def run(data):
	root = os.path.join(os.getcwd(),"share")
	ctor = Creator(os.path.join(root,"bg.jpg"),os.path.join(root,"msyhbd.ttf"),36)
	x,y = 180,580
	for value in data:
		ctor.addText(value["text"],value["color"],(x,y))
		x = x + ctor.ttffont.getsize(value["text"])[0]
	
	ctor.save(os.path.join(root,"out.jpg"))

if __name__ == "__main__":
	# run([{"text":u"累计淘汰 1 名 获得 ","color":(18,10,10)},{"text":u"1.88","color":(255,0,0)},{"text":u' 微信红包',"color":(18,10,10)}])
	run([{"text":u" 获得 ","color":(18,10,10)},{"text":u"1.88","color":(255,0,0)},{"text":u' 微信红包',"color":(18,10,10)}])
	# run([{"text":u"1.88","color":(255,0,0)},{"text":u' 微信红包',"color":(18,10,10)}])
