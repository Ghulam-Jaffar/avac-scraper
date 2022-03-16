import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# scrappedData = []


def Scrapper(productName):

    options = Options()
    options.headless = False
    # This code simplify management of binary driver for chromer
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # path = "C:\Program Files (x86)\chromedriver.exe"
    # driver = webdriver.Chrome(path)
    driver.get("https://www.alibaba.com/")
    driver.maximize_window()

    def searchSupplier(productName):
        selectSupplier = driver.find_element(
            By.XPATH, "//div[@class='ui-searchbar-type-value']")
        selectSupplier.click()
        selectMenu = driver.find_element(
            By.XPATH, "//*[@id='J_SC_header']/header/div[2]/div[3]/div/div/form/div[1]/div/ul/li[2]/a")
        selectMenu.click
        searchProduct = driver.find_element(By.NAME, "SearchText")
        searchProduct.send_keys(productName)
        searchProduct.send_keys(Keys.Return)

    # sProduct = {'title': '', 'price': '', 'amazonChoice': '', 'bestSeller': '', 'ratings': '',
    #             'reviews': '', 'image': '', 'sellersStore': '', 'pageUrl': '', 'ASIN': ''}

    def check(length, main):
        for j in range(0, length):
            print("product ", 1 + j)
            try:
                titles = main.find_elements(
                    By.XPATH, "//span[@class='a-size-base-plus a-color-base a-text-normal']")
                titles[j].click()
                try:
                    title = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH, "//*[@id='productTitle']"))
                    )
                    sProduct.update({'title': title.text})
                except:
                    sProduct.update({'title': "Not Found"})

                try:
                    url = driver.current_url
                    array = []
                    array = url.split("/")
                    sProduct.update({'ASIN': array[5]})
                except:
                    sProduct.update({'ASIN': "Not Found"})

                try:
                    price = driver.find_element(
                        By.XPATH, "//span[@class='a-price a-text-price a-size-medium apexPriceToPay']")
                    filteredPrice = price.text.replace("$", "")
                    sProduct.update({'price': filteredPrice})
                except:
                    sProduct.update({"price": 0})

                try:
                    amazonChoice = driver.find_element(
                        By.XPATH, "//span[@class='a-size-small aok-float-left ac-badge-rectangle']")
                    sProduct.update({'amazonChoice': True})
                except:
                    sProduct.update({'amazonChoice': False})

                try:
                    bestSeller = driver.find_element(
                        By.XPATH, "//i[@class='a-icon a-icon-addon p13n-best-seller-badge']")
                    sProduct.update({'bestSeller': True})
                except:
                    sProduct.update({'bestSeller': False})

                try:
                    ratings = driver.find_element(
                        By.ID, "acrCustomerReviewText")
                    if " ratings" in ratings.text:
                        filteredRating = ratings.text.replace(" ratings", "")
                        sProduct.update({'ratings': filteredRating})
                    elif " rating" in ratings.text:
                        filteredRating = ratings.text.replace(" rating", "")
                        sProduct.update({'rating': filteredRating})
                except:
                    sProduct.update({'ratings': 0})

                try:
                    reviews = driver.find_element(
                        By.XPATH, "//span[@class='a-size-medium a-color-base']")
                    filteredReview = reviews.text.replace(" out of 5", "")
                    sProduct.update({'reviews': filteredReview})
                except:
                    sProduct.update({'reviews': 0})

                try:
                    image = driver.find_element(
                        By.XPATH, "//img[@id='landingImage']").get_attribute("src")
                    sProduct.update({'image': image})
                except:
                    sProduct.update({'image': "Not Found"})

                try:
                    sellersStore = driver.find_element(
                        By.XPATH, "//a[@id='bylineInfo']").get_attribute('href')
                    sProduct.update({'sellersStore': sellersStore})
                except:
                    sProduct.update({'sellersStore': "Not Found"})

                try:
                    pageUrl = driver.current_url
                    sProduct.update({'pageUrl': pageUrl})
                except:
                    sProduct.update({'pageUrl': "Not Found"})

                try:
                    pDetails = {}
                    tHeaders = driver.find_elements(
                        By.XPATH, "//table[@id='productDetails_detailBullets_sections1']/tbody/tr/th")
                    tData = driver.find_elements(
                        By.XPATH, "//table[@id='productDetails_detailBullets_sections1']/tbody/tr/td")
                    for i in range(len(tHeaders)):
                        if tHeaders[i].text == "Best Sellers Rank":
                            bestSeller = tData[i].text
                            removeHash = bestSeller.replace("#", "")
                            bestRank = " ".join(removeHash.split()[0:1])
                            pDetails[tHeaders[i].text] = bestRank
                        elif tHeaders[i].text == "Item Dimensions LxWxH":
                            newDim = tData[i].text.replace(" inches", "")
                            pDetails[tHeaders[i].text] = newDim
                        elif tHeaders[i].text == "Product Dimensions":
                            newDim = tData[i].text.replace(" inches", "")
                            pDetails[tHeaders[i].text] = newDim
                        elif tHeaders[i].text == "Item Weight":
                            if "pounds" in tData[i].text:
                                newWeight = tData[i].text.replace(
                                    " pounds", "")
                                pDetails[tHeaders[i].text] = newWeight
                            elif "ounces" in tData[i].text:
                                newWeight = tData[i].text.replace(
                                    " ounces", "")
                                pDetails[tHeaders[i].text] = newWeight
                        else:
                            pDetails[tHeaders[i].text] = tData[i].text
                    sProduct.update(pDetails)
                    pDetails.clear()
                except:
                    sProduct.update(0)

                try:
                    pDetails = {}
                    tHeaders = driver.find_elements(
                        By.XPATH, "//table[@id='productDetails_techSpec_section_1']/tbody/tr/th")
                    tData = driver.find_elements(
                        By.XPATH, "//table[@id='productDetails_techSpec_section_1']/tbody/tr/td")
                    for i in range(len(tHeaders)):
                        if tHeaders[i].text == "Best Sellers Rank":
                            bestSeller = tData[i].text
                            removeHash = bestSeller.replace("#", "")
                            bestRank = " ".join(removeHash.split()[0:1])
                            pDetails[tHeaders[i].text] = bestRank
                        elif tHeaders[i].text == "Item Dimensions LxWxH":
                            newDim = tData[i].text.replace(" inches", "")
                            pDetails[tHeaders[i].text] = newDim
                        elif tHeaders[i].text == "Product Dimensions":
                            newDim = tData[i].text.replace(" inches", "")
                            pDetails[tHeaders[i].text] = newDim
                        elif tHeaders[i].text == "Item Weight":
                            if "pounds" in tData[i].text:
                                newWeight = tData[i].text.replace(
                                    " pounds", "")
                                pDetails[tHeaders[i].text] = newWeight
                            elif "ounces" in tData[i].text:
                                newWeight = tData[i].text.replace(
                                    " ounces", "")
                                pDetails[tHeaders[i].text] = newWeight
                        else:
                            pDetails[tHeaders[i].text] = tData[i].text
                    sProduct.update(pDetails)
                    pDetails.clear()
                except:
                    sProduct.update(0)

            except:
                print("masti kr reya")

            sProduct_Copy = sProduct.copy()
            scrappedData.append(sProduct_Copy)
            sProduct.clear()
            driver.back()
            main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            titles = main.find_elements(
                By.XPATH, "//span[@class='a-size-base-plus a-color-base a-text-normal']")

    def main(nPages):
        try:
            main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            for i in range(0, nPages):
                print("page", i+1)
                main = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "search"))
                )
                titles = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((
                        By.XPATH, "//span[@class='a-size-base-plus a-color-base a-text-normal']")))
                length = len(titles)
                print("total number of products on page ", i+1, " : ", length)
                check(length, main)
                try:
                    main = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "search"))
                    )
                    pagination = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")))
                    pagination.click()
                except:
                    main = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "search"))
                    )
                    pagination = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH, "//li[@class='a-last']")))
                    pagination.click()
        finally:
            driver.quit()

    # def selectCategory(cat, subCat, lastCategory, nPages):
    #     if cat == 1:
    #         #subCat = int(input("Choose a category \n 1. Painting, Drawing & Art Supplies \n 2. Beading and Jewelary Making \n 3. Crafting \n 4. Knitting & Crochet \n 5. Party Decorations and Supplies \n"))

    #         if subCat == 1:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Arts & Crafts' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Painting, Drawing & Art Supplies']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Art Paper \n 2. Boards and Canvas \n 3. Drawing \n 4. Painting \n 5. Brush and Pen Cleaner \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Art Paper']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Boards & Canvas']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Drawing']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Painting']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Brush & Pen Cleaners']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 2:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Arts & Crafts' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Beading & Jewelry Making']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Beading Supplies \n 2. Beads & Bead Assortments \n 3. Charms \n 4. Engraving Machines & Tools \n 5. Jewelry Making Display & Packaging Supplies \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Beading Supplies']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Beads & Bead Assortments']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Charms']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Engraving Machines & Tools']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Jewelry Making Display & Packaging Supplies']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 3:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Arts & Crafts' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Crafting']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Candle Making \n 2. Ceramics & Pottery \n 3. Paper & Paper Crafts \n 4. Leathercraft \n 5. Craft Supplies \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Candle Making']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Ceramics & Pottery']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Paper & Paper Crafts']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Leathercraft']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Craft Supplies']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 4:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Arts & Crafts' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Knitting & Crochet']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Ball Winders \n 2. Crochet Hooks \n 3. Knitting Looms & Boards \n 4. Yarn \n 5. Yarn Storage \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Ball Winders']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Crochet Hooks']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Knitting Looms & Boards']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Yarn']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Yarn Storage']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 5:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Arts & Crafts' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Party Decorations & Supplies']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Balloons \n 2. Banners \n 3. Garlands \n 4. Tablecovers \n 5. Sky Lanterns \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Balloons']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Banners']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Garlands']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Tablecovers']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Sky Lanterns']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #     elif cat == 2:
    #         # subCat = int(input(
    #         #     "Choose a sub category \n 1. Apparel and Accessories \n 2. Baby & Toddler Toys \n 3. Baby Stationary \n 4. Baby Gifts \n 5. Safety Products \n"))

    #         if subCat == 1:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Baby' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Apparel & Accessories']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(
    #                 #     input("Choose a sub category \n 1. Baby Girls \n 2. Baby Boys \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Baby Girls']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Baby Boys']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 # elif lastCategory == 3:
    #                 #     try:
    #                 #         try:
    #                 #             productCat = driver.find_element(By.XPATH, "// *[text() = 'Drawing']")
    #                 #             productCat.click()
    #                 #         except:
    #                 #             print("last cat click didnt work")
    #                 #         time.sleep(1)
    #                 #         try:
    #                 #             main(nPages)
    #                 #         except:
    #                 #             print("coudlnt run main")
    #                 #     except:
    #                 #         print("masti++")

    #                 # elif lastCategory == 4:
    #                 #     try:
    #                 #         try:
    #                 #             productCat = driver.find_element(By.XPATH, "// *[text() = 'Painting']']")
    #                 #             productCat.click()
    #                 #         except:
    #                 #             print("last cat click didnt work")
    #                 #         time.sleep(1)
    #                 #         try:
    #                 #             main(nPages)
    #                 #         except:
    #                 #             print("coudlnt run main")
    #                 #     except:
    #                 #         print("masti++")

    #                 # elif lastCategory == 5:
    #                 #     try:
    #                 #         try:
    #                 #             productCat = driver.find_element(By.XPATH, "// *[text() = 'Brush & Pen Cleaners']")
    #                 #             productCat.click()
    #                 #         except:
    #                 #             print("last cat click didnt work")
    #                 #         time.sleep(1)
    #                 #         try:
    #                 #             main(nPages)
    #                 #         except:
    #                 #             print("coudlnt run main")
    #                 #     except:
    #                 #         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 2:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Baby' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Baby & Toddler Toys']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Balls \n 2. Early Development & Activity Toys \n 3. Rattles & Plush Rings \n 4. Bath Toys \n 5. Car Seat & Stroller Toys \n 6. Activity Centers \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Balls']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Early Development & Activity Toys']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Rattles & Plush Rings']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Bath Toys']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Car Seat & Stroller Toys']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 6:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Activity Centers']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 3:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Baby' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Baby Stationery']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Birth Announcements \n 2. Door Hangers \n 3. Invitations \n 4. Thank You Cards \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Birth Announcements']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Door Hangers']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Invitations']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Thank You Cards']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 # elif lastCategory == 5:
    #                 #     try:
    #                 #         try:
    #                 #             productCat = driver.find_element(By.XPATH, "// *[text() = 'Brush & Pen Cleaners']")
    #                 #             productCat.click()
    #                 #         except:
    #                 #             print("last cat click didnt work")
    #                 #         time.sleep(1)
    #                 #         try:
    #                 #             main(nPages)
    #                 #         except:
    #                 #             print("coudlnt run main")
    #                 #     except:
    #                 #         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 4:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Baby' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Gifts']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1.Albums, Frames & Journals \n 2. Gift Baskets \n 3. Gift Sets \n 4. Keepsakes \n 5. Rattles \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Albums, Frames & Journals']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Gift Baskets']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Gift Sets']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Keepsakes']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Rattles']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 5:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Baby' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Safety']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Monitors \n 2. Edge & Corner Guards \n 3. Electrical Safety \n 4. Gates & Gate Extensions \n 5. Kitchen Safety \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Monitors']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Edge & Corner Guards']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Electrical Safety']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Gates & Gate Extensions']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Kitchen Safety']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #     elif cat == 3:
    #         # subCat = int(input(
    #         #     "Choose a sub category \n 1. Kitchen & Dining \n 2. Bedding \n 3. Home Decor \n 4. Wall Art \n 5. Event & Party Supplies \n"))

    #         if subCat == 1:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Home and Kitchen' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Kitchen & Dining']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat click me masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Cookware \n 2. Dining & Entertaining \n 3. Home Brewing & Wine Making \n 4. Kitchen & Table Linens \n 5. Kitchen Utensils & Gadgets \n 6. Small Appliances \n 7. Storage & Organization \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Cookware']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Dining & Entertaining']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Home Brewing & Wine Making']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Kitchen & Table Linens']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Kitchen Utensils & Gadgets']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 6:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Small Appliances']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 7:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Storage & Organization']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 2:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Home and Kitchen' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Bedding']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat me masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Quilts & Sets \n 2. Bed Pillows & Positioners \n 3. Bedding Sets & Collections \n 4. Blankets & Throws \n 5. Duvets & Down Comforters \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Quilts & Sets']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Bed Pillows & Positioners']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Bedding Sets & Collections']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Blankets & Throws']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Duvets & Down Comforters']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 3:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Home and Kitchen' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Home Décor']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat me masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Draft Stoppers \n 2. Artificial Plants & Flowers \n 3. Home Décor Accents \n 4. Home Fragrance \n 5. Kids' Room Décor \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Draft Stoppers']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Artificial Plants & Flowers']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Home Décor Accents']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Home Fragrance']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Kids' Room Décor")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 4:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Home and Kitchen' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Wall Art']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Mixed Media \n 2. Photographs \n 3. Drawings \n 4. Paintings \n 5. Posters & Prints \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Mixed Media']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Photographs']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Drawings']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Paintings']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Posters & Prints']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 5:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Home and Kitchen' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Event & Party Supplies']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Children's Party Supplies \n 2. Favors \n 3. Ceremony Supplies \n 4. Invitations \n 5. Hats \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Children's Party Supplies']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Favors']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Ceremony Supplies']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Invitations']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Hats']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #     elif cat == 4:
    #         # subCat = int(input("Choose a sub category \n 1. Accessories and Supplies \n 2. Camera & Photo \n 3. Office Electronics \n 4. Car & Vehicle Accessories  \n 5. Cell Phones & Accessories \n"))

    #         if subCat == 1:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Electronics' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Accessories & Supplies']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Camera & Photo Accessories \n 2. Cell Phone Accessories \n 3. Vehicle Electronics Accessories \n 4. Blank Media \n 5. Cord Management \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Camera & Photo Accessories']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Cell Phone Accessories']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Vehicle Electronics Accessories']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Blank Media']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Cord Management']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 2:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Electronics' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Camera & Photo']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Video Surveillance \n 2. Accessories \n 3. Lighting & Studio \n 4. Printers & Scanners \n 5. Tripods & Monopods \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Video Surveillance']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Accessories']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Lighting & Studio']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Printers & Scanners']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Tripods & Monopods']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 3:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Electronics' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Office Electronics']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Printers & Accessories \n 2. Electronic Dictionaries, Thesauri & Translators \n 3. Scanners & Accessories \n 4. Calculators \n 5. Point-of-Sale (POS) Equipment \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Printers & Accessories']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Electronic Dictionaries, Thesauri & Translators']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Scanners & Accessories']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Calculators']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Point-of-Sale (POS) Equipment']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 4:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Electronics' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Car & Vehicle Electronics']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Car Electronics \n 2. Marine Electronics \n 3. Powersports Electronics \n 4. Vehicle Electronics Accessories \n 5. Vehicle GPS \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Car Electronics']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Marine Electronics']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Powersports Electronics']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Vehicle Electronics Accessories']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Vehicle GPS']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 5:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.XPATH, "//div[ text() = 'Electronics' ]")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//*[text() = 'Cell Phones & Accessories']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Accessories \n 2. Cases, Holsters & Clips \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Accessories']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Cases, Holsters & Clips']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 # elif lastCategory == 3:
    #                 #     try:
    #                 #         try:
    #                 #             productCat = driver.find_element(By.XPATH, "// *[text() = 'Drawing']")
    #                 #             productCat.click()
    #                 #         except:
    #                 #             print("last cat click didnt work")
    #                 #         time.sleep(1)
    #                 #         try:
    #                 #             main(nPages)
    #                 #         except:
    #                 #             print("coudlnt run main")
    #                 #     except:
    #                 #         print("masti++")

    #                 # elif lastCategory == 4:
    #                 #     try:
    #                 #         try:
    #                 #             productCat = driver.find_element(By.XPATH, "// *[text() = 'Painting']']")
    #                 #             productCat.click()
    #                 #         except:
    #                 #             print("last cat click didnt work")
    #                 #         time.sleep(1)
    #                 #         try:
    #                 #             main(nPages)
    #                 #         except:
    #                 #             print("coudlnt run main")
    #                 #     except:
    #                 #         print("masti++")

    #                 # elif lastCategory == 5:
    #                 #     try:
    #                 #         try:
    #                 #             productCat = driver.find_element(By.XPATH, "// *[text() = 'Brush & Pen Cleaners']")
    #                 #             productCat.click()
    #                 #         except:
    #                 #             print("last cat click didnt work")
    #                 #         time.sleep(1)
    #                 #         try:
    #                 #             main(nPages)
    #                 #         except:
    #                 #             print("coudlnt run main")
    #                 #     except:
    #                 #         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #     elif cat == 5:
    #         # subCat = int(input(
    #         #     "Choose a sub category \n 1. Clothing \n 2. Shoes \n 3. Watches \n 4. Accessories \n"))

    #         if subCat == 1:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.CSS_SELECTOR, "#hmenu-content > ul.hmenu.hmenu-visible > ul:nth-child(11) > li:nth-child(6) > a > div")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//a[@href='/s?bbn=16225019011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225019011%2Cn%3A1040658&ref_=nav_em__nav_desktop_sa_intl_clothing_0_2_13_2']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Shirts \n 2. Fashion Hoodies & Sweatshirts \n 3. Socks & Hosiery \n 4. T-Shirts & Tanks \n 5. Sweaters \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Shirts']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Fashion Hoodies & Sweatshirts']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Socks & Hosiery']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'T-Shirts & Tanks']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Sweaters']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 2:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.CSS_SELECTOR, "#hmenu-content > ul.hmenu.hmenu-visible > ul:nth-child(11) > li:nth-child(6) > a > div")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//a[@href='/s?bbn=16225019011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225019011%2Cn%3A679255011&ref_=nav_em__nav_desktop_sa_intl_shoes_0_2_13_3']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Outdoor \n 2. Athletic \n 3. Boots \n 4. Mules & Clogs \n 5. Slippers \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Outdoor']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Athletic']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Boots']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Mules & Clogs']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Slippers']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 3:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.CSS_SELECTOR, "#hmenu-content > ul.hmenu.hmenu-visible > ul:nth-child(11) > li:nth-child(6) > a > div")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//a[@href='/s?bbn=16225019011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225019011%2Cn%3A6358539011&ref_=nav_em__nav_desktop_sa_intl_watches_0_2_13_4']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Wrist Watches \n 2. Watch Bands \n 3. Pocket Watches \n 4. Smartwatches \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Wrist Watches']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Watch Bands']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Pocket Watches']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Smartwatches']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 # elif lastCategory == 5:
    #                     # try:
    #                     #     try:
    #                     #         productCat = driver.find_element(By.XPATH, "// *[text() = 'Brush & Pen Cleaners']")
    #                     #         productCat.click()
    #                     #     except:
    #                     #         print("last cat click didnt work")
    #                     #     time.sleep(1)
    #                     #     try:
    #                     #         main(nPages)
    #                     #     except:
    #                     #         print("coudlnt run main")
    #                     # except:
    #                     #     print("masti++")
    #             except:
    #                 print("last tier category me masti")

    #         elif subCat == 4:
    #             try:
    #                 icon = driver.find_element(
    #                     By.XPATH, "//i[@class='hm-icon nav-sprite']")
    #                 icon.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 seeAll = driver.find_element(
    #                     By.XPATH, "//a[@class='hmenu-item hmenu-compressed-btn']")
    #                 seeAll.click()
    #             except:
    #                 print("masti")
    #             time.sleep(1)
    #             try:
    #                 category = driver.find_element(
    #                     By.CSS_SELECTOR, "#hmenu-content > ul.hmenu.hmenu-visible > ul:nth-child(11) > li:nth-child(6) > a > div")
    #                 category.click()
    #             except:
    #                 print("category click me masti")
    #             time.sleep(1)
    #             try:
    #                 subCategory = driver.find_element(
    #                     By.XPATH, "//a[@href='/s?bbn=16225019011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225019011%2Cn%3A2474937011&ref_=nav_em__nav_desktop_sa_intl_accessories_0_2_13_5']")
    #                 subCategory.click()
    #             except:
    #                 print("subcat masti")
    #             time.sleep(1)

    #             try:
    #                 # lastCategory = int(input(
    #                 #     "Choose a sub category \n 1. Wallets, Card Cases & Money Organizers \n 2. Ties, Cummerbunds & Pocket Squares \n 3. Collar Stays \n 4. Cuff Links, Shirt Studs & Tie Clips \n 5. Gloves & Mittens \n  5. Hats & Caps \n"))
    #                 # nPages = int(input("how many pages to scrap: \n"))

    #                 if lastCategory == 1:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Wallets, Card Cases & Money Organizers']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 2:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Ties, Cummerbunds & Pocket Squares']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 3:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Collar Stays']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 4:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Cuff Links, Shirt Studs & Tie Clips']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 5:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Gloves & Mittens']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")

    #                 elif lastCategory == 6:
    #                     try:
    #                         try:
    #                             productCat = driver.find_element(
    #                                 By.XPATH, "// *[text() = 'Hats & Caps']")
    #                             productCat.click()
    #                         except:
    #                             print("last cat click didnt work")
    #                         time.sleep(1)
    #                         try:
    #                             main(nPages)
    #                         except:
    #                             print("coudlnt run main")
    #                     except:
    #                         print("masti++")
    #             except:
    #                 print("last tier category me masti")

    searchSupplier(productName)
   
   
   
   
   
   
   
   
   
   
   
    # selectCategory(cat, subCat, lastCategory, nPages)
    # jsonData = json.dumps(scrappedData, sort_keys=True)
    # return scrappedData

    # cat = int(input("Choose a department \n 1. Arts and Crafts \n 2. Baby \n 3. Home and Kitchen \n 4. Electronics \n 5. Men's Fashion \


Scrapper("mobile covers")
