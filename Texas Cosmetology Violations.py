#!/usr/bin/env python
# coding: utf-8

# # Texas Cosmetologist Violations
# 
# Texas has a system for [searching for license violations](https://www.tdlr.texas.gov/cimsfo/fosearch.asp). You're going to search for cosmetologists!

# ## Setup: Import what you'll need to scrape the page
# 
# We'll be using Selenium for this, *not* BeautifulSoup and requests.

# In[30]:


import requests
from selenium import webdriver
import pandas as pd
driver = webdriver.Chrome()


# ## Starting your search
# 
# Starting from [here](https://www.tdlr.texas.gov/cimsfo/fosearch.asp), search for **cosmetologist violations** for people with the last name **Nguyen**.

# In[31]:


driver.get("https://www.tdlr.texas.gov/cimsfo/fosearch.asp")


# In[32]:


# first, select cosmetologist from "license program type" dropdown menu
dropdown = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/section/div/div/table/tbody/tr/td/form/table/tbody/tr[3]/td/select/option[10]")
dropdown.click()

# # then, click in "search by last name" and type Nguyen
last_name_search = driver.find_element_by_id("pht_lnm")
last_name_search.send_keys("Nguyen")

# finally, search
search_button = driver.find_element_by_name("B1")
search_button.click()


# ## Scraping
# 
# Once you are on the results page, do this.

# ### Loop through each result and print the entire row
# 
# Okay wait, that's a heck of a lot. Use `[:10]` to only do the first ten (`listname[:10]` gives you the first ten).

# In[4]:


# to view pg html:
#driver.page_source


# In[15]:


all_content = driver.find_elements_by_tag_name("tbody")
for item in all_content[:10]:
    print(item.text.strip())


# ### Loop through each result and print each person's name
# 
# You'll get an error because the first one doesn't have a name. How do you make that not happen?! If you want to ignore an error, you use code like this:
# 
# ```python
# try:
#    # try to do something
# except:
#    # Instead of stopping on an error, it'll jump down here instead
#    print("It didn't work')
# ```
# 
# It should help you out. If you don't want to print anything, you can type `pass` instead of the `print` statement. Most people use `pass`, but it's also nice to print out debug statements so you know when/where it's running into errors.
# 
# **Why doesn't the first one have a name?**

# In[16]:


all_content_two = driver.find_elements_by_tag_name("tr")
all_content_two[1].text.strip()


# In[6]:


len(all_content_two)


# In[10]:


for item in all_content_two[1:]:
        # note
        # can also do
        # thing = item.find_elements_by_class_name('results_text')[0]
        thing = item.find_element_by_class_name('results_text')
        print(thing.text.strip())


# In[11]:


# this prints out over a thousand names and I'm not sure why. It loops through the data set about 10 times

# while True:
#     try:
#         for item in all_content_two[1:]:
#             thing = item.find_element_by_class_name('results_text')
#             print(thing.text.strip())
#     except:
#         print("It didn't work")


# ## Loop through each result, printing each violation description ("Basis for order")
# 
# > - *Tip: You'll get an error even if you're ALMOST right - which row is causing the problem?*
# > - *Tip: You can get the HTML of something by doing `.get_attribute('innerHTML')` - it might help you diagnose your issue.*
# > - *Tip: Or I guess you could just skip the one with the problem...*

# In[7]:


all_content_two = driver.find_elements_by_tag_name("tr")
# all_content_two[1].find_elements_by_tag_name("td")[2].text.strip()


# In[16]:


try:
    for item in all_content_two[1:]:
        thing = item.find_elements_by_tag_name("td")[2]
        print(thing.text.strip())
except:
    print("wrong!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


# ## Loop through each result, printing the complaint number
# 
# - TIP: Think about the order of the elements

# In[6]:


all_content_three = driver.find_elements_by_tag_name("tr")
# all_content_three[1].find_elements_by_class_name('results_text')[5].text.strip()


# In[10]:


try:
    for item in all_content_three[1:]:
        thing = item.find_elements_by_class_name('results_text')[-2]
        print(thing.text.strip())
except:
    print('wrong!!!!!!!!!!!!!!!!!!!!!!!!')


# ## Saving the results
# 
# ### Loop through each result to create a list of dictionaries
# 
# Each dictionary must contain
# 
# - Person's name
# - Violation description
# - Violation number
# - License Numbers
# - Zip Code
# - County
# - City
# 
# Create a new dictionary for each result (except the header).
# 
# > *Tip: If you want to ask for the "next sibling," you can't use `find_next_sibling` in Selenium, you need to use `element.find_element_by_xpath("following-sibling::div")` to find the next div, or `element.find_element_by_xpath("following-sibling::*")` to find the next anything.

# In[ ]:


all_content_four = driver.find_elements_by_tag_name("tr")
# all_content_four[1].text.strip()


# In[48]:


# name, basis for order, complaint #, license #, zip, county, city

master_list = []

for item in all_content_four[1:]:
    item_dict = {}
    item_dict.setdefault('name', [])
    item_dict.setdefault('city', [])
    item_dict.setdefault('county', [])
    item_dict.setdefault('zip_code', [])
    item_dict.setdefault('license_number', [])
    item_dict.setdefault('complaint_number', [])
    item_dict.setdefault('basis_for_order', [])

    name = item.find_elements_by_class_name('results_text')[0]
    name1 = name.text.strip()
    city = item.find_elements_by_class_name('results_text')[-6]
    city1 = city.text.strip()
    county = item.find_elements_by_class_name('results_text')[-5]
    county1 = county.text.strip()
    zip_code = item.find_elements_by_class_name('results_text')[-4]
    zip_code1 = zip_code.text.strip()
    license_number = item.find_elements_by_class_name('results_text')[-3]
    license_number1 = license_number.text.strip()
    complaint_number = item.find_elements_by_class_name('results_text')[-2]
    complaint_number1 = complaint_number.text.strip()
    basis_for_order = item.find_elements_by_tag_name("td")[2]
    basis_for_order1 = basis_for_order.text.strip()
    
    item_dict['name'] = name1
    item_dict['city'] = city1
    item_dict['county'] = county1
    item_dict['zip_code'] = zip_code1
    item_dict['license_number'] = license_number1
    item_dict['complaint_number'] = complaint_number1
    item_dict['basis_for_order'] = basis_for_order1
    
    master_list.append(item_dict)


# In[58]:


master_list[:2]


# ### Save that to a CSV
# 
# - Tip: Use `pd.DataFrame` to create a dataframe, and then save it to a CSV.

# In[59]:


df = pd.DataFrame(master_list)
df.head()


# In[60]:


df.to_csv('/Users/ALukpat/Documents/Columbia/Fall_2020/Basic_Computing/week_six/10-homework/tx_cosmetology.csv')


# ### Open the CSV file and examine the first few. Make sure you didn't save an extra weird unnamed column.

# ## Let's do this an easier way
# 
# Use Selenium and `pd.read_html` to get the table as a dataframe.

# In[61]:


df2 = pd.read_html(driver.page_source)


# In[68]:


df2


# In[67]:


df2[0]

