#!/usr/bin/env python
# coding: utf-8

# ## Logging on
# 
# Use Selenium to visit https://webapps1.chicago.gov/buildingrecords/ and accept the agreement.
# 
# > Think about when you use `.find_element_...` and when you use `.find_elementSSS_...`

# In[1]:


import requests
from selenium import webdriver
driver = webdriver.Chrome()
import pandas as pd


# In[2]:


driver.get("https://webapps1.chicago.gov/buildingrecords/")


# In[3]:


# first, select cosmetologist from "license program type" dropdown menu
button = driver.find_element_by_xpath("/html/body/div/div[4]/form/div[1]/div[1]/input")
button.click()

# finally, submit
submit_button = driver.find_element_by_xpath("/html/body/div/div[4]/form/div[4]/div/button")
submit_button.click()


# ## Searching
# 
# Search for **400 E 41ST ST**.

# In[4]:


address_search = driver.find_element_by_xpath('/html/body/div/div[4]/form/div[1]/div/input')
address_search.send_keys("400 E 41ST ST")

submit_button2 = driver.find_element_by_xpath("/html/body/div/div[4]/form/div[2]/div/button")
submit_button2.click()


# ## Saving tables with pandas
# 
# Use pandas to save a CSV of all **permits** to `Permits - 400 E 41ST ST.csv`. Note that there are **different sections of the page**, not just one long permits table.

# In[17]:


get_ipython().system('pip install html5lib')


# In[19]:


data5 = pd.read_html(driver.page_source)


# In[34]:


type(data5)


# In[30]:


df5 = data5[0]
df5.head()


# In[32]:


df5.to_csv('Permits - 400 E 41ST ST.csv', index=False)
df6 = pd.read_csv("Permits - 400 E 41ST ST.csv")
df6.head()


# ## Saving tables the long way
# 
# Save a CSV of all DOB inspections to `Inspections - 400 E 41ST ST.csv`, but **you also need to save the URL to the inspection**. As a result, you won't be able to use pandas, you'll need to use a loop and create a list of dictionaries.
# 
# You can use Selenium (my recommendation) or you can feed the source to BeautifulSoup. You should have approximately 157 rows.
# 
# You'll probably need to find the table first, then the rows inside, then the cells inside of each row. You'll probably use lots of list indexing. I might recommend XPath for finding the table.
# 
# *Tip: If you get a "list index out of range" error, it's probably due to an issue involving `thead` vs `tbody` elements. What are they? What are they for? What's in them? There are a few ways to troubleshoot it.*

# In[12]:


inspections_table = driver.find_element_by_id('resultstable_inspections')
inspections_table2 = inspections_table.find_elements_by_tag_name('tr')


# In[13]:


inspections_list = []

for item in inspections_table2[1:]:
    number = item.find_elements_by_tag_name('td')[0].text.strip()
    url = item.find_element_by_tag_name('a').get_attribute('href')
    #url = item.find_element_by_xpath(f'/html/body/div/div[4]/div[10]/table/tbody/tr[{count}]/td[1]/a').text.strip()
    date = item.find_elements_by_tag_name('td')[1].text.strip()
    status = item.find_elements_by_tag_name('td')[2].text.strip()
    description = item.find_elements_by_tag_name('td')[3].text.strip()
    
    inspections_list.append({
        'Inspection_number': number,
        'URL': url,
        'Inspection_date': date,
        'Status': status,
        'Type_description': description
    })


# In[14]:


df3 = pd.DataFrame(inspections_list)
df3.head()


# In[15]:


df3.to_csv('Inspections - 400 E 41ST ST.csv', index=False)
df4 = pd.read_csv("Inspections - 400 E 41ST ST.csv")
df4.head()


# ### Loopity loops
# 
# > If you used Selenium for the last question, copy the code and use it as a starting point for what we're about to do!
# 
# If you click the inspection number, it'll open up a new window that shows you details of the violations from that visit. Count the number of violations for each visit and save it in a new column called **num_violations**.
# 
# Save this file as `Inspections - 400 E 41ST ST - with counts.csv`.
# 
# Since it opens in a new window, we have to say "Hey Selenium, pay attention to that new window!" We do that with `driver.switch_to.window(driver.window_handles[-1])` (each window gets a `window_handle`, and we're just asking the driver to switch to the last one.). A rough sketch of what your code will look like is here:
# 
# ```python
# # Click the link that opens the new window
# 
# # Switch to the new window/tab
# driver.switch_to.window(driver.window_handles[-1])
# 
# # Do your scraping in here
# 
# # Close the new window/tab
# driver.close()
# 
# # Switch back to the original window/tab
# driver.switch_to.window(driver.window_handles[0])
# ```
# 
# You'll want to play around with them individually before you try it with the whole set - the ones that pass are very different pages than the ones with violations! There are a few ways to get the number of violations, some easier than others.

# #### Getting individual violation count:

# In[ ]:


# count the number of rows when you click on each url


# In[6]:


# Click the link that opens the new window

# button = driver.find_element_by_tag_name('a').get_attribute('href')
button = inspections_table.find_elements_by_link_text("13175960")
button[0].click()

driver.switch_to.window(driver.window_handles[-1])


# In[8]:


# scraping for number of violations
get_table_body = driver.find_elements_by_tag_name('tbody')
get_table_body_rows = get_table_body[0].find_elements_by_tag_name('tr')
violation_num = len(get_table_body_rows)
violation_num


# In[9]:


# Close the new window/tab
driver.close()


# In[15]:


# Switch back to the original window/tab
driver.switch_to.window(driver.window_handles[0])


# #### Getting all violation counts:

# In[9]:


inspections_list[:3]


# In[13]:


inspections_table2[1].text.strip()


# In[23]:


flag = driver.find_elements_by_tag_name('h5')
len(flag)


# In[29]:


violations_list = []

for dictionary in inspections_list:
    if dictionary['Status'] == 'FAILED':
        button = inspections_table.find_elements_by_link_text((f"{dictionary['Inspection_number']}"))
        button[0].click()

        driver.switch_to.window(driver.window_handles[-1])
        
        # at least one of the violations is marked "FAILED" but the page doesn't show any violations
        flag = driver.find_elements_by_tag_name('h5')
        
        # if the page shows violations, flag will be an empty list
        if len(flag) == 0:
            get_table_body = driver.find_elements_by_tag_name('tbody')
            get_table_body_rows = get_table_body[0].find_elements_by_tag_name('tr')
            violation_num = len(get_table_body_rows)
            violations_list.append(violation_num)
        else:
            violations_list.append(0)
            
        driver.close()

        driver.switch_to.window(driver.window_handles[0])
    else:
        violations_list.append(0)


# In[31]:


df4['num_violations'] = violations_list


# In[32]:


df4.head()


# In[ ]:




