import bottle 
import data 


@bottle.route('/')
def getHTML(): 
  return bottle.static_file('page.html', root = ".")
  
@bottle.route('/script.js')
def getScript(): 
  return bottle.static_file('script.js', root = ".") 

@bottle.route('/ajax.js')
def getAjax(): 
  return bottle.static_file('ajax.js', root = ".")

@bottle.get('/data')
def getData():
  dataJSON = data.betterJSONDic(14)
  return dataJSON 


bottle.run(host = "0.0.0.0", port = 8080)



