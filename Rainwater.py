import geopandas as gpd
import pandas as pd

rain=gpd.read_file(r"C:\Users\piyus\Downloads\rain_data.csv")
rain['ANNUAL'] = pd.to_numeric(rain['ANNUAL'], errors='coerce')

pd.set_option("display.max_rows", None)

coefficients = {
        "concrete": 0.85,
        "tiled": 0.75,
        "corrugated": 0.80,
        "thatched": 0.55,
        "asphalt": 0.70,
        "green": 0.50
    }


from flask import Flask, render_template,request

app=Flask(__name__)
@app.route("/")

def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])

def calculate():
   length=request.form.get('Length')
   width=request.form.get('Width')
   district=request.form.get('district')
   rooftype=request.form.get('roofType')

   try:
        area = float(length) * float(width)
   except (TypeError, ValueError):
        area = 0.0

   district_row = rain[rain['DISTRICT'].str.lower() == district.lower()]
   if not district_row.empty:
        rainfall = district_row.iloc[0]['ANNUAL']  # rainfall value from CSV
   else:
        rainfall = 1.2  # fallback default (meters annually)


   coeff = coefficients.get(rooftype, 0.75)
   harvest=area*rainfall*coeff   #in m^3
   harvest_L=harvest*1000  #in litres
   daily=harvest_L/365

   return render_template(
       'index.html',
       rainfall=f"{rainfall:.3f} m",
       area=f"{area: .2f} sq-m",
       harvest=f"{harvest_L: .3f} L",
       daily=f"{daily: .3f} L"
    )
if __name__ == "__main__":
    app.run(debug=True)
