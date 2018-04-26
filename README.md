# scrapy-selenium-taobao
## 1 Preparation
This project is based on Python 3.6 and MongoDB <br>
This project is based on the following libs: scrapy v1.5.0, selenium v3.11.0, pymongo v3.4.0
## 2 Content
The purpose of this project is to scrap the commodity information from "taobao.com". The search KEYWORDS and MAX_PAGE can be modified in settings.py so that you can receive the information of items that you are interested in. The information of items is stored in MongoDB.
## 3 Tips
Selinum is used to directly scrap the information from the page source no matter what dynamic rendering technoloies the website use.<br>
To join selenium with scrapy, the key is to create a class named "SeleniumMiddleware" in middlewares.py and enable it.
