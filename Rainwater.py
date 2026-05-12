import geopandas as gpd
import pandas as pd

rain=gpd.read_file(r"C:\Users\piyus\Downloads\rain_data.csv")
rain['ANNUAL'] = pd.to_numeric(rain['ANNUAL'], errors='coerce')

rain['ANNUAL_MM']=rain['ANNUAL']*1000
pd.set_option("display.max_rows", None)




from flask import Flask, render_template,request

app=Flask(__name__)
@app.route("/",methods=["GET","POST"])

def home():
    
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
