from selenium import webdriver
import pandas as pd
from StandAlone import standalone_Scrape, standalone_images

# Creating Instances, User Input
driver = 0
username = str(input("Enter Username of Account: "))
post_count = int(input("Enter number of posts: "))
driver_path = str(input("Enter location path of driver, use double back-slashes: "))
file_path = str(input("Enter path for files to be stored locally: "))
user_log_in = str(input("Enter username to log into instagram, not to scrape from: "))
pass_log_in = str(input("Enter password for the username just entered: "))


def main():
    global driver
    print('Running')
    # The below line of code will create an instance of Firefox using selenium
    driver = webdriver.Firefox(executable_path=driver_path)
    driver.delete_all_cookies()
    print("Logging in...")
    driver.get('https://www.instagram.com/accounts/login/')
    standalone_Scrape.login_new(driver, user_log_in, pass_log_in)
    print("Fetching URLS...")
    instagram_urls = standalone_Scrape.insta_post_links(driver, username, post_count)
    print("Fetching Images...")
    standalone_images.url_to_img(driver, instagram_urls, file_path)
    print("Fetching Details...")
    instagram_details = [standalone_Scrape.insta_details(driver, url) for url in instagram_urls]
    print("Compiling into Dataframe...")
    details = pd.DataFrame(instagram_details)
    details.to_csv(file_path + "\\details.csv")
    print("Done!")
    driver.quit()


if __name__ == '__main__':
    main()
