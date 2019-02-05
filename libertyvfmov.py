from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from tmdbv3api import TMDb
from tmdbv3api import Movie
import imdb
import requests
moviename = ''
options = Options()
im = imdb.IMDb()
tmdb = TMDb()
movie = Movie()
tmdb.api_key = '39e601c13665591ea51c63c874900060'
options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=options)
for page in range(200):
    try:
        startingurl = "https://ww3.libertyvf.org/films/nouveautes/page-"+str(page)+".html"
        soup1 = BeautifulSoup(requests.get(startingurl).text, "html.parser")
        h2 = soup1.findAll("h2")
        for link in h2:
            movieurl = link.a['href']
            soup2 = BeautifulSoup(requests.get(movieurl).text, "html.parser")
            tk = [tag['href'] for tag in soup2.find_all('a', {'class': "btn btn-info quality_dispo_btn"})]
            try:
                soup3 = BeautifulSoup(requests.get(tk[0]).text, "html.parser")
                h2tags = soup3.findAll("div", attrs={"class": "blogtext"})
                h2tags1 = soup3.find("div", attrs={"class": "blogtext"}).find("h2")
                moviename = h2tags1.get_text()
                moviename = moviename.lower()
                print("Movie Name--", moviename)
                check = 1
                try:
                    imsearch = im.search_movie(moviename)

                    for ims in imsearch :
                        if check == 1:
                            try:
                                imtitle = ims['title']
                                imtitle = imtitle.lower()
                            except Exception as e:
                                print("Title Extraction Error",e)
                            try:
                                imakas  = ims['akas'][0]
                                imakas = imakas.lower()
                            except Exception as e:
                                print("AKAS Extraction error",e)
                            if (moviename.lower() == imtitle or moviename.lower() == imakas) and check == 1 :
                                print("IMDB id",ims.getID())
                                check = 2

                    tmsearch = movie.search(moviename)
                    for tmmv in tmsearch:
                        tmdbmv = tmmv.title
                        tmdbmv = tmdbmv.lower()
                        print("TMDB--",tmmv.id)
                        break

                except Exception as e:
                    print("Error IMDB Movie Search Error",e)

                del imakas
                del imtitle
            except Exception as e:
                print("Movie Name Extraction Error:", e)
            for number in [2,3]:
                driver.get(tk[0])
                if number == 2 or number == 3:
                    xpatch = '//*[@id="lien_telechargement"]/div[2]/div/div/div[' + str(number) + ']/button'
                    try:
                        btnclick = driver.find_element_by_xpath(xpatch).click()
                        try:
                            wait(driver, 20).until(
                                lambda x: len(
                                    driver.find_elements_by_xpath('//*[@id="lien_telechargement"]/div[3]/div[2]/iframe')))
                            try:
                                openloadfrm = driver.find_elements_by_tag_name("iframe")
                                for ol1 in openloadfrm:
                                    if 'openload' in ol1.get_property("src"):
                                        print("Openload--", ol1.get_property("src"))
                                    elif 'streamango' in ol1.get_property("src"):
                                        print("streamango--", ol1.get_property("src"))
                                        openloadfrm = ""
                            except Exception as e:
                                print("Unable to load IFrame", e)
                        except Exception as e:
                            print("Timeout Error:", e)
                    except Exception as e:
                        print("Error Clicking Button",e)
    except Exception as e:
        print("Error Navigating to Page",e)

    #exit()

