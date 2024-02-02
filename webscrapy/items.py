# items.py

import scrapy

class WebscrapyItem(scrapy.Item):
    # Define the fields for your item here like:
    # For parse_link1
    Country_Name = scrapy.Field()
    Country_Capital = scrapy.Field()
    Country_Population = scrapy.Field()
    Country_Area = scrapy.Field()

    # For parse_link2
    Team_Name = scrapy.Field()
    Year = scrapy.Field()
    Wins = scrapy.Field()
    Losses = scrapy.Field()
    OT_Losses = scrapy.Field()
    Win_Percentage = scrapy.Field()
    GF = scrapy.Field()
    GA = scrapy.Field()

    # For parse_link3
    Film_Year = scrapy.Field()
    Film_Title = scrapy.Field()
    Film_Nominations = scrapy.Field()
    Film_Awards = scrapy.Field()
    Film_Best_Picture = scrapy.Field()

    # For parse_link4
    Image_URL = scrapy.Field()
    Turtle_Family_Name = scrapy.Field()
    Learnmore_URL = scrapy.Field()

    # For parse_link5
    Link_Text = scrapy.Field()
