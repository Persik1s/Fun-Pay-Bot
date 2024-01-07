import os
import json
from classFp import FP
from threading import Thread

if (__name__ == "__main__"):
    #CREATE FILE
    if not os.path.isfile('jsonSettings.json'):
        print("CREATE FILE")
        fileJson = open('jsonSettings.json','+w')

        js = json.dumps({"chatIDTelegram": 0,"tokenTGBot": "","settingsMessage": 0, "goldenKeyFunPay": "", "discordUrlHook": "", "AutoLot": 0}, separators=(",",":"),sort_keys=True)
        
        
        fileJson.write(js)
        fileJson.close()
        exit(0)
    
    #Read File Settings 
    fileJson = open('jsonSettings.json','r')
    jsonReadFile = fileJson.read() 
    jsonRead = json.loads(jsonReadFile)

    fileJson.close()
    fp = FP(
        discordWebToken=jsonRead["discordUrlHook"],
          telegramToken=None,
          golden_key=jsonRead["goldenKeyFunPay"],
          chatTGid=None)
    
    Thread(target=fp.Message).start()
    Thread(target=fp.AutoLot).start()
    
    
    
   

    
  