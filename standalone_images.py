from urllib.request import urlretrieve
from selenium.common.exceptions import NoSuchElementException


def url_to_img(driver, instagram_urls, file_path):
    """
    Getting the actual photo file from an Instagram url
    Works with multiple images, stand-alone images, or video thumbnails
    :param driver: Get's the current driver session
    :param instagram_urls: List of instagram post URLS to get image from
    :param file_path: Specified file path for images to be saved locally
    :return: Saves image locally to file_path
    """
    image = ""
    driver.implicitly_wait(2)
    post_num = -1
    for url in instagram_urls:
        post_num = post_num + 1
        driver.get(url)
        driver.implicitly_wait(2)
        flag = 0
        try:
            image = driver.find_element_by_xpath(
                """/html/body/span/section/main/div/div/article/
                    div[1]/div/div/div[1]/div[1]/img""")
        except NoSuchElementException:
            try:
                image = driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/div/article/div[2]/div/div/
                div[1]/div[1]/img""")
            except NoSuchElementException:
                try:
                    image = driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/div/article/div[2]/div/
                    div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/img""")
                except NoSuchElementException:
                    try:
                        image = driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/div/article/div[
                        2]/div/ div/div[1]/div/div/img""")
                    except NoSuchElementException:
                        try:
                            image = driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/div[
                            1]/article/div [2]/div/div/div[1]/img""")
                        except NoSuchElementException:
                            try:
                                # Multiple Images
                                image = driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/div/article/
                                div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img""")
                            except NoSuchElementException:
                                # Multiple Videos
                                try:
                                    image = driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/div/
                                                                         article/div[2]/div/div[1]/div[2]/div/div/div/
                                                                         ul/li[2]/div/div/div/div[1]/div/div/video""")
                                # except NoSuchElementException:
                                #     # Picture with new source
                                #     print("photo - 1")
                                #     flag = 2
                                #     try:
                                #         image = driver.find_element_by_xpath("""/html/body/div[1]/section/main/div/
                                #         div[1]/article/div[2]/div/div/div[1]/div[1]/img""")
                                except NoSuchElementException:
                                    # Video in picture-to-picture mode
                                    print("video - 2")
                                    flag = 1
                                    try:
                                        image = driver.find_element_by_xpath("""/html/body/div[1]/section/main/div
                                        /div[1]/article/div[2]/div/div/div[1]/div/div/video""")
                                    except NoSuchElementException:
                                        print("No image or thumbnail found.")
        if flag == 1:
            # Video
            image = image.get_attribute("poster")
            print(image)
            urlretrieve(image, file_path + " image" + str(post_num) + ".jpg")

        else:
            # Flag = 0
            image = image.get_attribute("src")
            print(image)
            urlretrieve(image, file_path + " image" + str(post_num) + ".jpg")
