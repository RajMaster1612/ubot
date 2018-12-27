import random
import requests
import json
import urllib
TOKEN = '729605770:AAEpFeVRkrOF_nG4jrsxz8JlHRpNVBxAewg'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

Request=[['HI','HII','HELLO','HIII','HEY','HEYYY'],['HAPPY BIRTHDAY','HAPPY BIRTHDAY TO YOU','HBD','HAPPY BDAY','CONGRATULATION','CONGRATULATIONS','CONGRATS','BEST OF LUCK','ALL THE BEST'],['THANK YOU','THANKS','THANX','THANK YOU VERY MUCH'],['WHO ARE YOU?','WHO ARE YOU','WRU?','WHAT IS YOUR NAME?'],['HOW ARE YOU?','WHAT CAN YOU DO?','HRU?','HRU','HOW ARE YOU'],['BYE','BYEE','BYEEE','SEE YOU LATER','TAKE CARE','SEE YOU','SEE YOU AGAIN','TC'],['GOOD MORNING','GM','HAVE A NICE DAY','HAVE A NICE DAY!'],['GOOD NIGHT','GN','SD','SWEET DREAMS']]

Response={0:['HI','HII','HEY','HELLO','HEY!'],1:['THANK YOU','THANKS','THANX','THANK YOU VERY MUCH','THANKS A LOT'],2:['WELCOME','MY PLEASURE','ALWAYS WELCOME','MOST WELCOME','WELCOME, CAN I DO ANYTHING ELSE FOR YOU?'],3:['I AM A CHATBOT, I HOPE I AM DOING WELL.','I AM ULTRON',' I AM ULTRON, I HOPE I AM DOING WELL.'],4:['I AM FINE, HOW ARE YOU?','I AM FINE, WHAT CAN I DO FOR YOU ?','I AM GOOD, HOW ARE YOU?','I AM FINE, WHAT CAN I DO FOR YOU ?','I AM GOOD, HOW ARE YOU?'],5:['BYE','SEE YOU AGAIN','TAKE CARE'],6:['GOOD MORNING','HAVE A NICE DAY','GOOD MORNING, HAVE A NICE DAY'],7:['GOOD NIGHT','SD','SWEET DREAMS','GN','SEE YOU TOMORROW'],100:["I HEARD YOU!","SO, YOU ARE TALKING TO ME.","CONTINUE, I’M LISTENING.","VERY INTERESTING CONVERSATION.","TELL ME MORE..."]}


def get_url(url):
    response = requests.get(url)
    content=response.content.decode("UTF-8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return chat_id

def get_last_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    return text

def reply(text):
    if text!='/start':
        text=text.upper()
        index=100
        for i in range(0,len(Request)):
            if text in Request[i]:
                index=i
                break;
        random_number=random.randint(0,len(Response[index])-1);
        reply_markup=Response[index]
        return reply_markup[random_number]
    else:
        reply_markup="Hello, I am Billy (@Billy_Batson_bot). \n\n Created By Gaurav Kosrekar and Raj Master..... \n\n "
        reply_markup+="You can Send me Follwing Messages. \n\n "
        reply_markup+="Hello\nHii\nGood Morning\nGm\nGood night\nGn\nHow are you?\nWho are you?\nThank You\nHappy Birthday\nCongratulations\nBye\nTake care\nSweet Dreams\nHave a Nice day\nSee You again\nBest of Luck\nAll the Best\n....\n\nYou can try it......"
        return reply_markup;

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?chat_id={}&text={}&parse_mode=Markdown".format(chat_id, text)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    last_update_id= None
    text= None
    chat_id=None
    while (True):
        try:
            updates = get_updates(last_update_id)
            if (len(updates["result"]) > 0):
                last_update_id=get_last_update_id(updates)+1;
                chat_id= get_last_chat_id(updates);
                text=get_last_text(updates);
                text_reply=reply(text);
                send_message(text_reply,chat_id);
                #print(last_update_id)
                print("Message : "+ text)
                #print(chat_id)
                print("Reply   : "+text_reply)
        except Exception as e:
            print(e)
            send_message("We do not support Sticker. \n Please Enter Text.",chat_id);
            pass
main()