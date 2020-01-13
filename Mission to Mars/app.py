#import libraries for flask

from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo

# importing another python file to display the scraped data 
import scrape_mars

#create an instance of flask app

app = Flask(__name__)

#Setup Mongo db connection using flask pymongo

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

#con = "mongodb://localhost:27017"
#client = pymongo.MongoClient(con)

mars_collection = mongo.db.mars_db
#mars_collection.drop()

#mars_collection = client.mars_db

@app.route("/")
def first_page():

    # statement to find docs in the db
    mars_data = mars_collection.find()
    #print(mars_data)
    print("in first app: {}".format(mars_data))

    result = {}
    for doc in mars_data:
        result.update(doc)
    print(result)
    return render_template("index.html",html_mars_data = result)
    #return "Welcome"

@app.route("/scrape")
def scrape():



    # getting the data from "scrape_mars.py" - results from "scrape" function
    mars = scrape_mars.scrape()
    #mars = {'point1': "Media Get a Close-Up of NASA's Mars 2020 Rover", 'point2': "The clean room at NASA's Jet Propulsion Laboratory was open to the media to see NASA's next Mars explorer before it leaves for Florida in preparation for a summertime launch.", 'point3': 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA23634_hires.jpg', 'point4': None, 'point5': [{'title': 'Cerberus Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': 'Schiaparelli Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': 'Syrtis Major Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, {'title': 'Valles Marineris Hemisphere', 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]}
    #mars=[{'point1': "Media Get a Close-Up of NASA's Mars 2020 Rover"}, {'point2': "The clean room at NASA's Jet Propulsion Laboratory was open to the media to see NASA's next Mars explorer before it leaves for Florida in preparation for a summertime launch."}]
    #print(mars)
    print(type(mars))
    


    mars_collection.insert_many(mars)
    #mars_collection.update({}, mars, upsert=True)

    

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)





