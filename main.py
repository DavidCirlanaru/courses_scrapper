from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
import re
import os
import io

# Vars
main_url = 'https://codewithmosh.com'
url = 'https://codewithmosh.com/sign_in'
courses_bundle_link_list = []
chunk_size = 5120
path = os.getcwd()

# Functions


def format_file_name(string):
    new_string = " ".join(string.split())
    string = re.sub(r"\(.*?\)", "", new_string)
    string = string.replace('- ', ' - ')
    for ch in ['Start ', ':', '?', '"', '<', '>', '|',  '\\', '/', '*', '\n', '\'']:
        string = string.replace(ch, '')
    return string.strip()


driver = webdriver.Chrome()
driver.implicitly_wait(10)  # delay

# Navigate to the url
driver.get(url)

time.sleep(7)

username_input = driver.find_element_by_id('user_email')
password_input = driver.find_element_by_id('user_password')
login_btn = driver.find_element_by_class_name('login-button')

username_input.send_keys('cirlanaru.david77@gmail.com')
password_input.send_keys('password_for_python')
login_btn.click()

time.sleep(2)
driver.get('https://codewithmosh.com/courses/enrolled/240431')

soup = BeautifulSoup(driver.page_source, 'lxml')

# Get the course bundle links
course_bundle_links = soup.find_all('a', href=re.compile("^/courses/enrolled"))
for a in course_bundle_links:
    course_link = main_url+a['href']
    courses_bundle_link_list.append(course_link)

# Bundle courses page
for course_bundle_link in courses_bundle_link_list:
    print(f'Switching to another course: {course_bundle_link}')
    source = requests.get(course_bundle_link)
    content = source.content
    soup = BeautifulSoup(content, "lxml")

    i = 1
    # Individual course main page
    for link in soup.find_all('a', {'class': 'item'}):
        full_url = main_url + link['href']
        driver.get(full_url)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        if (soup.find('a', {'class': 'download'}) is not None):
            url = soup.find('a', {'class': 'download'})
        else:
            continue

        folder_name = soup.select('.course-sidebar h2')
        request = requests.get(url['href'], stream=True)
        print(f'Writing the video: {format_file_name(link.text)}')

        current_file_path = f"{folder_name[0].text}/{i}) {format_file_name(link.text)}.mp4"
        current_folder_path = f'{path}/{folder_name[0].text}'
        i += 1

        if (not os.path.isdir(current_folder_path)):
            os.makedirs(current_folder_path)

        if (os.path.isfile(current_file_path)):
            if (not os.stat(current_file_path).st_size == 0):
                continue

        with open(current_file_path, "wb") as f:
            for chunk in request.iter_content(chunk_size=chunk_size):
                f.write(chunk)


driver.quit()
exit()
