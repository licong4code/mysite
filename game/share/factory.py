# coding:utf-8
from PIL import Image,ImageDraw,ImageFont
import time,os,io,datetime,hashlib,json
from urllib2 import urlopen

base_root = (os.path.realpath(os.path.join(os.path.split(__file__)[0],"../../")) + "/download/").replace("\\","/")
def md5(src):
	m2 = hashlib.md5()
	m2.update(src)
	return m2.hexdigest()

class Creator(object):
    img_cache_icons = {}
    img_cache_logs = {}
    img_cache_qrs = {}
    img_cache_bgs = {}
    def __init__(self):
        self.ttffont = ImageFont.truetype("{0}/share/msyhbd.ttf".format(base_root),36)
        self.head_path = os.path.join(base_root,"head")
        if os.path.exists(self.head_path) == False:
        	os.mkdir(self.head_path)

    def getBg(self,type):
        if self.img_cache_bgs.has_key(type) == False:
            img = Image.open("{0}/share/bg{1}.jpg".format(base_root,type))
            self.img_cache_bgs[type] = img

        return self.img_cache_bgs[type].copy()

    def getIcon(self,app_id):
        if self.img_cache_icons.has_key(app_id) == False:
            img = Image.open("{0}/share/icon{1}.png".format(base_root,app_id))
            self.img_cache_icons[app_id] = img
        return self.img_cache_icons[app_id]
    
    def downloadIcon(self,url): 

    	outpath = os.path.join(self.head_path,md5(url) + ".jpg")
    	img = None
    	if os.path.exists(outpath) == False:
	    	try:
	    		bytes = io.BytesIO(urlopen(url).read())
	    		img = Image.open(bytes)
	    		img.save(outpath)
	    		return img
	    	except Exception as e:
	    		print e
    	else:
    		return Image.open(outpath)

    	return None


    def getLogo(self,app_id):
        if self.img_cache_logs.has_key(app_id) == False:
            img = Image.open("{0}/share/logo{1}.png".format(base_root,app_id))
            self.img_cache_logs[app_id] = img
        return self.img_cache_logs[app_id]

    def getQR(self,app_id):
        if self.img_cache_qrs.has_key(app_id) == False:
            img = Image.open("{0}/share/qr{1}.png".format(base_root,app_id))
            self.img_cache_qrs[app_id] = img
        return self.img_cache_qrs[app_id]

    def addText(self,text,color,position):
        self.draw.text(position, text, fill = color, font=self.ttffont)

    def __dobuild(self,data):
    	filename = md5(json.dumps(data))
        now = datetime.datetime.now()
    	foleder = os.path.realpath(os.path.join(base_root, now.strftime('%Y-%m-%d')))
    	if os.path.exists(foleder) == False:
        	os.mkdir(foleder)
       	filename = "{0}/{1}.jpg".format(foleder, filename).replace("\\","/")
       	if os.path.exists(filename) == False:
	        bg = self.getBg(data["type"])
	        if data.has_key("icon"):
	        	icon = self.downloadIcon(data['icon'])
	        else:
	        	icon = self.getIcon(data["app_id"])
	        logo = self.getLogo(data["app_id"])
	        qr = self.getQR(data["app_id"])
	        draw=ImageDraw.Draw(bg)
	        bg.paste(qr,(bg.size[0]/2 - qr.size[0]/2,bg.size[1] - qr.size[1] - 10))
	        r,g,b,a = logo.split()
	        bg.paste(logo,(10,10),mask = a)
	        bg.paste(icon,(112 - icon.size[0]/2,384 -  icon.size[1]/2))
			
	        for v in data['data']:
	        	x,y = v['position'][0] - self.ttffont.getsize(v["text"])[0]/2,v['position'][1]
	        	draw.text((x,y),v['text'],font = self.ttffont,fill = v['color'])

	        bg.save(os.path.join(base_root,filename))
		
        return filename.replace(base_root,"")

    def build(self,data):

    	if data['type'] == 1:
    		return self.__dobuild({"type":data['type'],"app_id":data['app_id'],'icon':data['icon'],"data":[{"text":data['name'],"color":(0,0,0) , "position":(218,478)},{"text":str(data['total']),"color":(255,0,0) , "position":(336,560)}]})
    	else:
    		return self.__dobuild({"type":data['type'],"app_id":data['app_id'],'icon':data['icon'],"data":[{"text":data['name'],"color":(0,0,0) , "position":(192,478)},{"text":str(data['race']),"color":(255,0,0) , "position":(340,478)},{"text":str(data['rank']),"color":(255,0,0) , "position":(182,562)},{"text":str(data['red']),"color":(255,0,0) , "position":(432,562)}]})
if __name__ == "__main__":
	ctor = Creator()
	print ctor.build({"type":1,"app_id":1,"name":u'白金岛',"total":100,"icon":"http://wx.qlogo.cn/mmopen/vi_32/920MZaSOicrlLDvP5UmVp7uqxleZFIHZDdIFokkwBkYG1fHJe4rdNbpn8JHYvibzP5mXaH1Apa110r6TwTOKPndQ/132"})
	# ctor.dobuild({"type":1,"app_id":2,"data":[{"text":u"licong2","color":(0,0,0) , "position":(218,478)},{"text":u"50 ","color":(255,0,0) , "position":(336,560)}]},"share/out1.jpg")
	# ctor.dobuild({"type":2,"app_id":2,"data":[{"text":u"licong2","color":(0,0,0) , "position":(192,478)},{"text":u"100","color":(255,0,0) , "position":(340,478)},{"text":u"50","color":(255,0,0) , "position":(182,562)},{"text":u"50","color":(255,0,0) , "position":(432,562)}]},"share/out.jpg")
	# ctor.downloadIcon("http://wx.qlogo.cn/mmopen/vi_32/920MZaSOicrlLDvP5UmVp7uqxleZFIHZDdIFokkwBkYG1fHJe4rdNbpn8JHYvibzP5mXaH1Apa110r6TwTOKPndQ/132")

	print json.dumps({"type":1,"app_id":1,"name":u'白金岛',"total":100,"icon":"http://wx.qlogo.cn/mmopen/vi_32/920MZaSOicrlLDvP5UmVp7uqxleZFIHZDdIFokkwBkYG1fHJe4rdNbpn8JHYvibzP5mXaH1Apa110r6TwTOKPndQ/132"},ensure_ascii=False)