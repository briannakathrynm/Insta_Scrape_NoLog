import re
import time


def insta_post_links(driver, username, post_count):
    """
    Gathers post links from specified number of posts from a public Instagram Account
    :param driver: Gets current session from main program instance
    :param username: Specified Instagram username from input
    :param post_count: Specified number of posts to get links from
    :return: Returns a list of post links stored in post_links
    """
    url = "https://www.instagram.com/" + username + "/"
    driver.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    print("Getting Links...")
    post_num = 0
    while len(post_links) < post_count:
        links = [a.get_attribute('href')
                 for a in driver.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_num = post_num + 1
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(scroll_down)
        time.sleep(10)
    else:
        driver.stop_client()
        return post_links[:post_count]


def find_mentions(comment):
    """
    Finds mentions in the comments section of an Instagram post
    :param comment: Comments from specified Instagram post
    :return: Mentions found in comment, if any
    """
    mentions = re.findall('@[A-Za-z]+', comment)
    if (len(mentions) > 1) & (len(mentions) != 1):
        return mentions
    elif len(mentions) == 1:
        return mentions[0]
    else:
        return ""


def find_hashtags(comment):
    """
    Finds any hashtags used in a post's comments
    :param comment: Instagram comment from post
    :return: List of individual hashtags if found in comment
    """
    hashtags = re.findall('#[A-Za-z]+', comment)
    if (len(hashtags) > 1) & (len(hashtags) != 1):
        return hashtags
    elif len(hashtags) == 1:
        return hashtags[0]
    else:
        return ""


def insta_details(driver, url):
    """
    Takes a post (specified by URL) and returns comments, mentions, hashtags, likes, and date posted.
    :param driver: Driver from current session
    :param url: A list of urls from Instagram posts
    :return: Dictionary with all of the above information, stored in post_details
    """
    driver.get(url)
    try:
        # This captures the standard like count.
        likes = driver.find_element_by_xpath(
            """/html/body/div[1]/section/main/div/div/article/div[3]/section[2]/div/div/button""").text.split()[
            0]

        post_type = 'photo'

    except:
        # This captures the like count for videos which is stored
        likes = driver.find_element_by_xpath(
            """//*[@id="react-root"]/section/main/div/div/article/div[3]/section[2]/div/span""").text.split()[0]
        post_type = 'video'
    age = driver.find_element_by_css_selector('#react-root > section > main > div > div > article > div.eo2As > '
                                              'div.k_Q0X.NnvRN > a').text
    comment = driver.find_element_by_xpath(
        """/html/body/div[1]/section/main/div/div[1]/article/
        div[3]/div[1]/ul/div/li/div/div/div[2]/span""").text
    hashtags = find_hashtags(comment)
    mentions = find_mentions(comment)
    post_details = {'link': url, 'type': post_type, 'likes/views': likes, 'date posted': age, 'comments': comment,
                    'hashtags': hashtags, 'mentions': mentions}
    driver.implicitly_wait(2)
    return post_details
