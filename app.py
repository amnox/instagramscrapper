from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import requests, re, json ,pprint
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask,render_template,request
from .InstaForm import InstaForm
app = Flask(__name__)


def lord_giveth_formatting(text):
    if text.find("k")<0:
        return int((text.replace(',', '')))
    else:
        return int(float((text.replace(',', '').replace('k','')))*1000)

def get_profile_data(profiles,tag):
    print profiles
    base_url = "https://www.instagram.com/"
    profile_dict = []
    for stuff in profiles:
        r = requests.get(base_url+stuff+'/')
        soup = BeautifulSoup(r.content, "html5lib")
        script = soup.find('script', text=re.compile('window\._sharedData'))
        json_text = re.search(r'^\s*window\._sharedData\s*=\s*({.*?})\s*;\s*$',script.string, flags=re.DOTALL | re.MULTILINE).group(1)
        data = json.loads(json_text)
        #print json.dumps(data, indent=4, sort_keys=True)
        bio = data["entry_data"]["ProfilePage"][0]["user"]["biography"]
        usr_url = data["entry_data"]["ProfilePage"][0]["user"]["external_url"]
        followers = data["entry_data"]["ProfilePage"][0]["user"]["followed_by"]["count"]
        following = data["entry_data"]["ProfilePage"][0]["user"]["follows"]["count"]
        full_name = data["entry_data"]["ProfilePage"][0]["user"]["full_name"]
        insta_id = data["entry_data"]["ProfilePage"][0]["user"]["id"]
        media_count = data["entry_data"]["ProfilePage"][0]["user"]["media"]["count"]
        username = data["entry_data"]["ProfilePage"][0]["user"]["username"]
        profile_pic = data["entry_data"]["ProfilePage"][0]["user"]["profile_pic_url_hd"]
        profile_dict.append({'insta_id':insta_id, 'username':username, 'profile_url': usr_url, 
                             'full_name':full_name, 
                            'bio':bio, 'followers':followers,'following':following, 'media_count':media_count,'hash_tag':tag})
    #pd.DataFrame(profile_dict).to_csv(tag,encoding = "utf-8")
    return profile_dict


# index view function suppressed for brevity

@app.route('/', methods=['GET', 'POST'])
def login():
    form = InstaForm()
    return render_template('funk.html', 
                           title='Sign In',
                           form=form)

@app.route('/results',methods=['GET', 'POST'])
def hello_buck():
    print request.form
    form = InstaForm(request.form)
    driver = webdriver.Chrome('/home/amnox/Projects/Scraping/Selenium/chromedriver')
    driver.implicitly_wait(10)
    booga = []
    tags = (form.name.data).split(",")
    posts_to_dig = form.depth.data
    thresh_hold = form.min_likes.data

    for shit in tags:
        media = []
        profiles = []
        
        driver.get("https://www.instagram.com/explore/tags/"+shit)
        elem = driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/a")
        elem.click()
        while len(media)<=posts_to_dig:
            media = driver.find_elements_by_xpath("//*[@id='react-root']/section/main/article/div/div/div/div")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        for dish in media:
            ActionChains(driver).move_to_element(dish).perform()
            #WebDriverWait(driver, 10).until(EC.presence_of_element_located(shit.find_element_by_xpath("//a/div/ul/li/span")))
            likes_count = lord_giveth_formatting(dish.find_element_by_xpath("//a/div/ul/li/span").get_attribute('innerHTML'))
            if likes_count<thresh_hold:
                media.pop(media.index(dish))
                continue
            dish.click()
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div/div[2]/div/article/header/div/a[@href]")))
            profiles.append(element.get_attribute('innerHTML'))
            #element.click()
            #driver.back()
            driver.back()
            #driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div[2]/div/article/header").click()
        booga.extend(get_profile_data(list(set(profiles)),shit))

    driver.close()
    return pd.DataFrame(booga).to_csv(encoding = "utf-8")
