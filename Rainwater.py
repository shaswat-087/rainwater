import geopandas as gpd
import pandas as pd
from flask import Flask, render_template,request

rain = gpd.read_file("Rain_Data.csv")
rain['ANNUAL'] = pd.to_numeric(rain['ANNUAL'], errors='coerce')

pd.set_option("display.max_rows", None)

coefficients = {                                          #stores run-off coefficients for every root-top surface
    "concrete" : 0.8475,
    "tiled" : 0.7620,
    "corrugated" : 0.8125,
    "thatched" : 0.5480,
    "asphalt" : 0.7015,
    "green" : 0.5035
}

#flask part
app = Flask(__name__)
@app.route("/")

def index():
    return render_template('index.html', rainfall = None)
@app.route('/modular')
def modular():
    return render_template('modular.html')
@app.route('/rooftop')
def rooftop():
    return render_template('rooftop.html')
@app.route('/groundwater')
def groundwater():
    return render_template('groundwater.html')
@app.route('/calculate', methods = ['POST'])

def calculate():
   length = request.form.get('Length')
   width = request.form.get('Width')
   district = request.form.get('district')
   rooftype = request.form.get('roofType')

   try:
    area = float(length) * float(width)
    if area <= 0:
        return render_template(
            'index.html',
            error="Invalid dimensions"
        )
    except (TypeError, ValueError):
            return render_template(
                'index.html',
                error="Please enter valid numeric values"
            )

   district_row = rain[rain['DISTRICT'].str.lower() == district.lower()]
   if not district_row.empty:
        rainfall = float(district_row.iloc[0]['ANNUAL'])  # rainfall value from source file (CSV)
   else:
        rainfall = 1200  # fallback default (mm annually)


   coeff = coefficients.get(rooftype, 0.75)
   harvest_L = area * rainfall * coeff   #in litres
   daily = harvest_L / 365

   return render_template(
       'index.html',
       rainfall = rainfall,
       area = f"{area: .2f} sq-m",
       harvest = f"{harvest_L: .3f} L",
       daily = f"{daily: .3f} L"
    )
if __name__ == "__main__":
    app.run(debug = True)
