import webapp2,json
import pickle
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Data(db.Model):
	filename=db.StringProperty()
	imagedata=db.StringListProperty()


class MainPage(webapp2.RequestHandler):
	def get(self):
		filelist=[]
		imagedata=[]
		for i in Data.all():
			filelist.append(i.filename)

		filename=self.request.path[1:]

		self.response.out.write('<font size="5">'+filename+'</font>')	

		if filename!="":
			for i in Data.all():
				if i.filename==filename:
					for j in i.imagedata:
						imagedata.append(pickle.loads(j))
			#self.response.out.write(json.dumps(imagedata))
			self.response.out.write('<script>lis='+json.dumps(filelist)+';fill=0; j=new Array();imagedata='+json.dumps(imagedata)+';</script>')
		else:
			self.response.out.write('<script>lis='+json.dumps(filelist)+';fill=0; j=new Array();imagedata='+json.dumps("")+' ;</script>') 			

		self.response.out.write(template.render("paint.html",{}));



	def post(self):
		fname=self.request.get('fnam')
		image=self.request.get('image')	
		imageDict=json.loads(image)
		database=Data(parent=db.Key.from_path('filename',fname))
		database.filename=fname
		for i in imageDict:
			database.imagedata.append(pickle.dumps(i))
		query=db.GqlQuery("SELECT * FROM Data WHERE ANCESTOR IS :c",c=db.Key.from_path('filename',fname))
		count=0
		for i in query:
			count=count+1
			i.imagedata=[]
			for j in imageDict:
				i.imagedata.append(pickle.dumps(j))
			db.put(i)
		if count==0:
			database.put()
		self.redirect("/")

app=webapp2.WSGIApplication([('/.*',MainPage)],debug=True)		
