from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo
import logging
import os


app = Flask(__name__)




@app.route("/", methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route("/review", methods=['POST', 'GET'])
def mainpage():
  
    if request.method == 'POST':
        try:
            save_dir = 'images/'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }

            query = request.form['content'].replace(" ","")
            response = requests.get(
                f"https://www.google.com/search?q={query}&tbm=isch&sa=X&ved=2ahUKEwid6fvFlPT_AhWEwzgGHSWKDrQQ0pQJegQICRAB&biw=1536&bih=718&dpr=1.25")
            
            soup=bs(response.content,'html.parser')
            image_tags=soup.find_all('img')
            del image_tags[0]
            image_list=[]

            for i in image_tags:
                image_url=i['src']
                image_data=requests.get(image_url).content
                mydict={
                    'index': image_url,
                    'image': image_data
                }
                
                image_list.append(mydict)
                with open(os.path.join(save_dir,f"{query}_{image_tags.index(i)}.jpg"),"wb") as f:
                    f.write(image_data)
                    
            client=pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.bssvoyh.mongodb.net/?retryWrites=true&w=majority")
            db=client['image_scarp']
            coll_scrap=db['image_scarp']
            coll_scrap.insert_many(image_list)
            return 'image downloaded successfully'
            
            
        except:
         return "something went wrong"

    else:
        return render_template('index.html')

        

if __name__ == "__main__":
    
    app.run(debug=True)
    