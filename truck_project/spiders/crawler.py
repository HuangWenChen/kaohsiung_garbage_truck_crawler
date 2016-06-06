# -*-coding : utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
import re
from truck_project.items import TruckProjectItem


class Truckcrawler(scrapy.Spider):
    name = "truck"
    start_urls = ["http://waste.ksepb.gov.tw/index.php"]

    def parse(self, respone):
        domain = "http://waste.ksepb.gov.tw/services/get_area.php"
        res = BeautifulSoup(respone.body, "lxml")
        for district in res.select('select[name="s_D"] > option')[1:]:
            # print(district.text)
            yield scrapy.Request(domain+"?keyword="+district.text,
                                 callback=self.parse_village,
                                 meta={"s_D": district.text})

    def parse_village(self, respone):
        domain = "http://waste.ksepb.gov.tw/index.php"
        res = BeautifulSoup(respone.body, "lxml")
        # print(respone.meta["s_D"])
        for i in json.loads(res.text):
            yield scrapy.Request(domain+"?s_D="+respone.meta["s_D"]+"&s_E="+i[0]+"&s_F=",
                                 callback=self.parse_pages,
                                 meta={"s_D": respone.meta["s_D"],
                                       "s_E": i[0],
                                       "pages": 1})

    def parse_pages(self, respone):
        domain = "http://waste.ksepb.gov.tw/index.php"
        res = BeautifulSoup(respone.body, "lxml")
        pattern = re.compile("\d+$")
        number = int(pattern.search(list(res.select('tr.Caption > td[colspan="9"]'))[0].text).group())
        pages = ((number/25)+1) if number > 25 else 1
        for i in range(1, int(pages+1)):
            yield scrapy.Request(domain+"?s_D="+respone.meta["s_D"]+"&s_E="+respone.meta["s_E"]+"&carry_linePage="+str(i),
                                 callback=self.parse_detail,
                                 meta={"s_D": respone.meta["s_D"],
                                       "s_E": respone.meta["s_E"]})

    def parse_detail(self, respone):
        res = BeautifulSoup(respone.body, "lxml")
        itemResult = []
        for row in res.select("tr.Row"):
            item = TruckProjectItem()
            item["responsibility"] = row.select("td")[0].text.replace(u"\xa0", "")
            item["number"] = row.select("td")[1].text.replace(u"\xa0", "")
            item["stop_number"] = row.select("td")[2].text.replace(u"\xa0", "")
            item["district"] = row.select("td > a")[0].text.replace(u"\xa0", "")
            item["village"] = row.select("td > a")[1].text.replace(u"\xa0", "")
            item["stop_location"] = row.select("td")[5].text.replace(u"\xa0", "")
            item["stop_time"] = row.select("td")[6].text.replace(u"\xa0", "")
            item["recycle"] = row.select("td")[7].text.replace(u"\xa0", "")
            itemResult.append(item)
        return itemResult
