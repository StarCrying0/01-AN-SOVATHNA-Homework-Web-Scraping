from bs4 import BeautifulSoup;
import json
import requests

response = requests.get("https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/")

soup = BeautifulSoup(response.text, 'html.parser')


pickup_lines = [];

titles = [];

title = soup.findAll('h2', class_="body-h2 css-j5a4ys emt9r7s1")
contents = soup.find(class_="article-body-content article-body standard-body-content css-4oaay7 et2g3wt6")

title = contents.findAll('h2', class_="body-h2 css-j5a4ys emt9r7s1")

for i in title:
    titles.append(i.text)

pickupLines = contents.findAll('ul',class_="css-1r2vahp emevuu60")
for i in pickupLines:
    if i.text == "": continue
    new = i.select("li")
    line = []
    for j in range(len(new)):
        if "RELATED: " in new[j].text: 
            new[j] = new[j].text.split("RELATED: ")[0]
            line.append(new[j])
            continue
        line.append(new[j].text)
    pickup_lines.append(line)

full_pickup_lines = []
for i in range(len(titles)):
    pickUpLine = {
        'title': titles[i],
        'lines': pickup_lines[i]
    }
    full_pickup_lines.append(pickUpLine)

data = json.dumps(full_pickup_lines,indent=4,ensure_ascii=False)

with open('womansday.json', 'a', encoding='utf-8') as file:
    file.write(data)