import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import urllib.request as req
import bs4
import re
import webbrowser



class SearchWindow(Screen):

    model = ObjectProperty(None)

    def userinput(self):
        m = self.model.text
        modeltxt = open("ModelName.txt","w+")
        modeltxt.write(m)
        modeltxt.close()

    def reset_btn(self):
        self.model.text= ""
  


def ibike_data():
    modeltxt=open("ModelName.txt","r")
    if modeltxt.mode == "r":
        contents = modeltxt.read()
    sm = contents.replace(" ", "-")
    url = "http://www2.ibike.com.hk/buysell/buysell.asp?keyword=" + sm + "&B2=SEARCH"
    request = req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    
    })
    with req.urlopen(request) as response:
        ibike_data=response.read().decode("big5")
    ibike_Final_data=bs4.BeautifulSoup(ibike_data, "html.parser")
    return ibike_Final_data

def ibike_prices():    
    root=ibike_data()
    body=root.find("table", attrs={"border":"0", "width":"100%", "id":"table1", "cellpadding":"0", "cellspacing":"0"})
    prices=body.find_all("div")
    price_list=[]
    for price in prices:   
        if price != None:
            price_list.append(price.text)
    price_s_list = []
    for p_s in price_list:
        price_s_list.append(str(p_s))
    p_2 = [s.strip("\n\r\t") for s in price_s_list]
    p_3 = [s.replace("\r\n\t\t\t\t\t\t\t\t\t\n\n"," ") for s in p_2]
    p_4 = [s.replace("面議","Negotiable") for s in p_3]
    p_5 = [s.replace("原價","Old") for s in p_4]
    p_6 = [s.replace("特價","Discount") for s in p_5]
    return p_6

def ibike_links():
    root=ibike_data()           
    titles=root.find_all(href=re.compile("buysell_detail.asp"), attrs={"target":"_blank"})
    link_list=[]
    link_s_list=[]
    for title in titles:
        l=("http://www2.ibike.com.hk/buysell/"+ title["href"])
        if l not in link_list:    
            link_list.append(l)
    for l_s in link_list:
        link_s_list.append(str(l_s))
    return link_s_list   

def ibike_photos():
    root=ibike_data()
    body=root.find("table", attrs={"border":"0", "width":"100%", "id":"table1", "cellpadding":"0", "cellspacing":"0"})            
    photos=body.find_all("img", attrs={"border":"0"})
    photo_list = []
    for photo in photos:
        photo=("http://www2.ibike.com.hk/"+ photo["src"])
        photo_list.append(photo)
    return photo_list




def webike_data():
    modeltxt=open("ModelName.txt","r")
    if modeltxt.mode == "r":
        contents = modeltxt.read()
    sm = contents.replace(" ", "-")
    url = "https://www.webike.hk/motomarket/bike-list/old.html?q=" + sm
    request = req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    
    })
    with req.urlopen(request) as response:
        webike_data=response.read().decode("UTF-8")
    webike_Final_data=bs4.BeautifulSoup(webike_data, "html.parser")
    return webike_Final_data

def webike_prices():    
    root=webike_data()
    body=root.find("div", attrs={"class":"grid-item-bike"})
    prices=body.find_all("div",attrs={"class":"price"})
    price_list=[]
    for price in prices:   
        if price != None:
            price_list.append(price.text)
    p_2 = [s.strip("\n") for s in price_list]
    p_3 = [s.replace("電洽","Negotiable") for s in p_2]
    return p_3

def webike_links():
    root=webike_data()            
    titles=root.find_all(href=re.compile("https://www.webike.hk/motomarket/"), attrs={"itemprop":"url"})
    link_list=[]
    link_s_list=[]
    for title in titles:
        l=(title["href"])   
        link_list.append(l)
    for l_s in link_list:
        link_s_list.append(str(l_s))
    return link_s_list   

def webike_photos():
    root=webike_data()         
    photos=root.find_all("img", attrs={"itemprop":"image"})
    photo_list = []
    for photo in photos:
        photo=(photo["src"])
        photo_list.append(photo)
    return photo_list




def all_prices():
    all_prices = []
    all_prices = ibike_prices() + webike_prices()
    print(all_prices)
    print(len(all_prices))
    return all_prices
    
def all_links():
    all_links = []
    all_links = ibike_links() + webike_links()
    print(all_links)
    print(len(all_links))
    return all_links

def all_photos():
    all_photos = []
    all_photos = ibike_photos() + webike_photos()
    return all_photos



class ResultWindow(Screen):
    
    def __init__(self, **kwargs):
        super(ResultWindow,self).__init__(**kwargs)


    def on_enter(self):

        #List of the number/Key of the dictionary
        nnn_lst = []
        for r in range(len(all_prices())):
            nnn_lst.append(str(r))
        print(nnn_lst)

        #Making Dictionary
        price_link_dict = dict(zip(nnn_lst,all_links()))
        print(price_link_dict)
        print(len(price_link_dict))

        #Function that open the web
        def order_btn(btn):
            hyl = price_link_dict[btn.id]
            webbrowser.open(hyl)       

        #Scollview
        asimg_grid= self.ids["asimg_grid"]
        
        t_lst = all_prices()
        t=0
        #p are links, t is the dictionary's key
        for p in all_photos():
            ai = AsyncImage(source=p,size_hint_y=None, height=400)
            asimg_grid.add_widget(ai)
            btn = Button(text=str(t_lst[t]),id=str(t), color = (0.15,0.15,0.15,1), bold=True, size_hint_y=None, height=40, 
            background_normal="", background_color= (1,1,1,1))
            btn.bind(on_press=order_btn)
            asimg_grid.add_widget(btn)
            t+=1

    def goback_reset(self):
        self.ids.asimg_grid.clear_widgets() 

    def gotop(self):
        self.ids.scroll.scroll_y = 1 
    

        
        

        


class WindowManager(ScreenManager):
    pass


kv=Builder.load_file("usedCar.kv")



# Classify the app
class UsedCarApp(App):
    
    def build(self):
        return kv


# run the app
if __name__ == "__main__":
    UsedCarApp().run()
