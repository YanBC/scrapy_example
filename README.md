# Description
Scrapy example in using the default image pipeline

# Objective
collect all products on sale on the website

website url: http://books.toscrape.com/index.html

data to be collected:
1. book title
2. cover picture
3. price, tax included

# Run spider
```bash
scrapy crawl ProductSpider -o books.jl
```
