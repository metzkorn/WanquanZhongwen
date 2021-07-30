import requests,json
from bs4 import BeautifulSoup 
test = "一世"

def find_def(char):
    url = f"https://www.zdic.net/hans/{char}"
    
   #"https://www.zdic.net/e/sci/index.php?field=0&classid=8&keyboard={char}"
    response = requests.get(url)
    html = BeautifulSoup(response.content.decode('utf-8'), "lxml")
 
    get_ps = None
    if(html is not None):
        get_ps = html.find(attrs={"data-type-block":"成语解释"})
        if(get_ps is not None):
            get_ps = get_ps.find(class_="content definitions cnr").find_all("p")
        if(get_ps == None):
            get_ps = html.find(attrs={"data-type-block":"网络解释"})
            if(get_ps is not None):
                get_ps = get_ps.find(class_="content definitions cnr").find_all("li")
        ##either we get a div class = "jnr" only 
        ##or there is <p> tags within. Should be second <p> tag? 
    if(get_ps == None):
        return "没有定义"
    
    ret_str = ""
    for x in get_ps:      
        if(x.find(id) is None):
            ret_str += ("<li>" + x.get_text() + "</li>")
        #maybe we go through and get rid of the ascii

    return ret_str 
if __name__ == '__main__':
    find_def(test)