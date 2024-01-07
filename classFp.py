import telebot
import time
from FunPayAPI import Account, Runner, types, enums
from discord_webhook import DiscordEmbed,DiscordWebhook
from threading import Thread


class FP:
    def __init__(self, discordWebToken = None,telegramToken = None, chatTGid = None,golden_key = None):
        if(golden_key == None):
            raise Exception("[ERROR] golden_key not found")
        self.acc = Account(golden_key=golden_key).get()
        self.runner = Runner(self.acc)

        self.isDiscordBool = False
        self.isTelegramBool = False

        self.chatTGid = None
        self.disocrdToken = None

       
        self.telegramToken = telegramToken

        if discordWebToken != None:
            self.disocrdToken = discordWebToken
            self.isDiscordBool = True

        if telegramToken != None: 
            if chatTGid == None:
                raise Exception("[ERROR] chatIDTelegram  == None")
            self.chatTGid = chatTGid
            self.isTelegramBool = True


    def Message(self):

        if not self.isDiscordBool  and not self.isTelegramBool:
            return 0
        if self.isDiscordBool and self.isTelegramBool:
            exit(0)
            raise Exception("[true] isDiscordBool and isTelegramBool = TRUE")

            

        if self.isDiscordBool:
            webHook = DiscordWebhook(self.disocrdToken)
            for eventMessage in self.runner.listen(requests_delay=4):
                
                if eventMessage.type is enums.EventTypes.NEW_MESSAGE:
           
                    if eventMessage.message.author_id == self.acc.id:
                        continue
                    
                    embed = DiscordEmbed(title=f"NEW MESSAGE в чате {eventMessage.message.chat_name}",description=f"TEXT MESSAGE: `{eventMessage.message.text}`")
                    webHook.add_embed(embed=embed)
                    webHook.execute()
        if self.isTelegramBool:
            botTG = telebot.TeleBot(token=self.telegramToken)
            Thread(target=botTG.polling,args=(True,)).start()

            for eventMessage in self.runner.listen(requests_delay=4):
                if eventMessage.type is enums.EventTypes.NEW_MESSAGE:
                    if eventMessage.message.author_id == self.acc.id:
                        continue
                    botTG.send_message(chat_id=self.chatTGid,text=f"|NEW MESSAGE в чате {eventMessage.message.chat_name}|\n\n TEXT: {eventMessage.message.text}")

    def AutoLot(self):
        while True:
            for lot in self.acc.get_sorted_categories():
                self.acc.get_raise_modal(lot)
            if self.isDiscordBool:
                webHook = DiscordWebhook(self.disocrdToken)
                embed = DiscordEmbed(title=f"ЛОТЫ ПОДНЯТЫ")
                webHook.add_embed(embed=embed)
                webHook.execute()
            if self.isTelegramBool:
                botTG = telebot.TeleBot(token=self.telegramToken)
                botTG.send_message(chat_id=self.chatTGid,text="ЛОТЫ ПОДНЯТЫ")
            time.sleep(15000)
            


            




        
        
    