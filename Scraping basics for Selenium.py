#!/usr/bin/env python
# coding: utf-8

# # Scraping basics for Selenium
# 
# If you feel comfortable with scraping, you're free to skip this notebook.

# ## Part 0: Imports
# 
# Import what you need to use Selenium, and start up a new Chrome to use for scraping. You might want to copy from the [Selenium snippets](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-snippets/) page.
# 
# **You only need to do `driver = webdriver.Chrome()` once,** every time you do it you'll open a new Chrome instance. You'll only need to run it again if you close the window (or want another Chrome, for some reason).

# In[1]:


import requests
from selenium import webdriver
driver = webdriver.Chrome()


# In[100]:


import pandas as pd


# ## Part 1: Scraping by class
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-class.html, printing out the title, subhead, and byline.

# In[40]:


driver.get("http://jonathansoma.com/lede/static/by-class.html")


# In[41]:


title = driver.find_elements_by_class_name("title")
subhead = driver.find_elements_by_class_name("subhead")
byline = driver.find_elements_by_class_name("byline")


# In[42]:


for item in title:
    print(item.text.strip())
for item in subhead:
    print(item.text.strip())
for item in byline:
    print(item.text.strip())


# ## Part 2: Scraping using tags
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-tag.html, printing out the title, subhead, and byline.

# In[37]:


driver.get("http://jonathansoma.com/lede/static/by-tag.html")


# In[38]:


title = driver.find_elements_by_tag_name("h1")
subhead = driver.find_elements_by_tag_name("h3")
byline = driver.find_elements_by_tag_name("p")


# In[39]:


for item in title:
    print(item.text.strip())
for item in subhead:
    print(item.text.strip())
for item in byline:
    print(item.text.strip())


# ## Part 3: Scraping using a single tag
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-list.html, printing out the title, subhead, and byline.
# 
# > **This will be important for the next few:** if you scrape multiples, you have a list. Even though it's Seleninum, you can use things like `[0]`, `[1]`, `[-1]` etc just like you would for a normal list.

# In[43]:


driver.get("http://jonathansoma.com/lede/static/by-list.html")


# In[46]:


all_content = driver.find_elements_by_tag_name("p")
for item in all_content:
    print(item.text.strip())


# ## Part 4: Scraping a single table row
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, printing out the title, subhead, and byline.

# In[80]:


driver.get("http://jonathansoma.com/lede/static/single-table-row.html")


# In[55]:


all_content = driver.find_elements_by_tag_name("tr")
for item in all_content:
    print(item.text.strip())


# ## Part 5: Saving into a dictionary
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, saving the title, subhead, and byline into a single dictionary called `book`.
# 
# > Don't use pandas for this one!

# In[50]:


driver.get("http://jonathansoma.com/lede/static/single-table-row.html")


# In[59]:


book = {}
all_content = driver.find_elements_by_tag_name("td")
book['title'] = all_content[0].text.strip()
book['subhead'] = all_content[1].text.strip()
book['byline'] = all_content[2].text.strip()
book


# ## Part 6: Scraping multiple table rows
# 
# Scrape the content at http://jonathansoma.com/lede/static/multiple-table-rows.html, printing out each title, subhead, and byline.
# 
# > You won't use pandas for this one, either!

# In[60]:


driver.get("http://jonathansoma.com/lede/static/multiple-table-rows.html")


# In[66]:


all_content = driver.find_elements_by_tag_name("tbody")
for item in all_content:
    print(item.text.strip())


# ## Part 7: Scraping an actual table
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a list of dictionaries.
# 
# > Don't use pandas here, either!

# In[83]:


driver.get("http://jonathansoma.com/lede/static/the-actual-table.html")


# In[97]:


dict_1 = {}
dict_2 = {}
dict_3 = {}
all_content = driver.find_elements_by_tag_name("td")

dict_1['title'] = all_content[0].text.strip()
dict_1['subhead'] = all_content[1].text.strip()
dict_1['byline'] = all_content[2].text.strip()
dict_2['title'] = all_content[3].text.strip()
dict_2['subhead'] = all_content[4].text.strip()
dict_2['byline'] = all_content[5].text.strip()
dict_3['title'] = all_content[6].text.strip()
dict_3['subhead'] = all_content[7].text.strip()
dict_3['byline'] = all_content[8].text.strip()

book_list = [dict_1, dict_2, dict_3]
book_list


# ## Part 8: Scraping multiple table rows into a list of dictionaries
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a pandas DataFrame.
# 
# > There are two ways to do this one! One uses just pandas, the other one uses the result from Part 7.

# In[98]:


driver.get("http://jonathansoma.com/lede/static/the-actual-table.html")


# In[102]:


df = pd.DataFrame(book_list)
df.head()


# ## Part 9: Scraping into a file
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html and save it as `output.csv`

# In[103]:


driver.get("http://jonathansoma.com/lede/static/the-actual-table.html")


# In[104]:


df.to_csv('/Users/ALukpat/Documents/Columbia/Fall_2020/Basic_Computing/week_six/10-homework/output.csv')

