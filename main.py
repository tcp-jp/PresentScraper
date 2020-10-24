#!/bin/python3
import csv
import smtplib
from requests import get
from bs4 import BeautifulSoup as bs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep


EMAIL="example@example"
PASSWORD="example@example"

class Item: 
    def __init__(self, url, desired_price):
        self.url=url;
        self.desired_price=desired_price;
    def get_page(self):
        page = get(self.url);
        return page

    def get_id(self):
        if self.url.find("ebay") != -1:
            return "ebay";
        elif self.url.find("depop") != -1:
            return "depop";
        else:
            return print("No ID found");
        pass

    def send_email(self):
        server=smtplib.SMTP( "smtp.gmail.com", 587);
        server.starttls();
        server.login(EMAIL, PASSWORD);
        #server.sendmail("Joe Paterson", EMAIL + " " + "<" + EMAIL + ">", "Item price is lower than desired price", self.url)
        message=MIMEMultipart()
        message['From']=EMAIL
        message['To']=EMAIL
        message['Subject']="An Item You Are Watching Is Now At Your Desired Price"
        message.attach(MIMEText("Item price is lower than desired price" + " " + self.url, 'plain'))
        text=message.as_string()
        server.sendmail(EMAIL,EMAIL, text)



    def parse_data(self,page):
        html = bs(page.content, 'html.parser');
        search=self.get_id();
        if search == "ebay":
            price_span=html.find(id="prcIsum");
            price=price_span.attrs["content"];
        if search == "depop":
            price_span=html.find_all(class_="Pricestyles__FullPrice-sc-1vj3zjr-0 fvDOul");
            price=price_span[0].getText().strip('£').strip('$')
        if float(price) <= float(self.desired_price):
            # TODO 
            # Make this send a email
            print("ITS LOWER BABYYYY");
            self.send_email()


def get_sites(sitelist):
    with open(sitelist, mode="r") as sites:
        data = csv.DictReader(sites);
        lines=0;
        arr=[];
        for row in data:
            if lines == 0:
                pass
            else:
                line = Item(row["url"], row["desired_price"]);
                arr.append(line);
            lines += 1;
    return arr

def main():
    arr=get_sites("sites.txt");
    pages=[]
    line = 0;
    for site in arr:
        page=site.get_page();
        site.parse_data(page);
        line += 1;
    sleep(6000)


if __name__=="__main__":
    main()

        

