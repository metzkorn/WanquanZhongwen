from bs4.element import NavigableString
import requests,json
from bs4 import BeautifulSoup 
test = "啻"

def find_def(char):
    url = f"https://www.zdic.net/hans/{char}"
    
   #"https://www.zdic.net/e/sci/index.php?field=0&classid=8&keyboard={char}"
    for x in range (10000):
        try: 
          response = requests.get(url, verify = False)
          break 
        except requests.exceptions.ConnectionError: 
            print("We're failing ahhhh")
            continue
        except requests.exceptions.RetryError: 
            print("We're failing ahhhh")
            continue
        

    html = BeautifulSoup(response.content.decode('utf-8'), "lxml")
    title = html.find('title')
    if(title == "查无此结果"):
        return "没有定义"
    get_ps = None
    if(len(char) != 1):
        if(html is not None):
            get_ps = html.find(attrs={"data-type-block":"成语解释"})
            if(get_ps is not None):
                get_ps = get_ps.find(class_="content definitions cnr").find_all("p")
            if(get_ps == None):
                get_ps = html.find(attrs={"data-type-block":"网络解释"})
                if(get_ps is not None):
                    get_ps = get_ps.find(class_="content definitions cnr").find_all("li")
    else: 
        get_ps = html.find(attrs={"data-type-block":"基本解释"})
        if(get_ps is not None):
            get_ps = get_ps.find("ol")
            if get_ps is None:
                with open("result.txt", "a", encoding = "utf-8") as f:
                    f.write(char + "\n")
                return "没有定义"
            check_li = get_ps.find_all("li")
            if(check_li is None or len(check_li) == 0):
                get_ps = get_ps.find_all("p")
            else:
                get_ps = check_li
        ##either we get a div class = "jnr" only 
        ##or there is <p> tags within. Should be second <p> tag? 
    if(get_ps == None):
        return "没有定义"
    

    
    ret_str = ""
    
    for x in get_ps: 
        if(type(x) != NavigableString):
            for tag in x.find_all():
                tag.decompose()   
        if(x.find(id) is None):
            ret_str += ("<li>" + x.get_text().strip() + "</li>")
        #maybe we go through and get rid of the ascii

    return ret_str 
if __name__ == '__main__':
    find_def(test)