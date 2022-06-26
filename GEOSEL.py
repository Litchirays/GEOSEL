#### **FYP Project - Streamlit (GEOSEL System)**
#### **Topic : GEOSPATIAL TEXT MINING FROM TWITTER FOR BUILDING CLASSIFICATION IN SELANGOR**
#### **Group : CS2596B**
#### **Course : CSP650 // Programme : CS259 // Semester : 6**
#### **SV : Dr Sofianita Mutalib**
#### **Lecturer : Dr Shamimi A. Halim**
#### **2019422984 - Irman Wafi Bin Rosli** 

# Import libraries

import streamlit as st 
import altair as alt
import plotly.express as px 
import pandas as pd 
import numpy as np 
import joblib
from streamlit_option_menu import option_menu
import time
import math

# Load Joblib for modelling in building classification system

pipe_lrbow = joblib.load(open("Modelling Label Building Classification.pkl","rb"))

# Define section

def predict_buildingslabel(tweets):
	results = pipe_lrbow.predict([tweets])
	return results[0]

def get_prediction_proba(tweets):
	results = pipe_lrbow.predict_proba([tweets])
	return results

# CSV Label meaning; Define for better understanding

labelmeaning = {0:"Residential",1:"Commercial"}
labelmeaningown = {0:"Residential",1:"Commercial"}

# Main System

def main():
	
	# GEOSEL website
	imageweb ="https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/2123321321.png"
	st.set_page_config(page_title='GEOSEL', page_icon = imageweb, layout = 'centered')

	# Logo

	image1="https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Element%201.png"
	st.image(image1, width=705)

	# Menu button

	selected = option_menu("",
		['Home', 'Dataset','QGIS','Model','Help'], icons=
		['house-fill', 'clipboard-data','pin-map-fill','cpu','gear-wide-connected'], default_index=0, orientation="horizontal")

	# Loading Bar Progress
	
	my_bar = st.progress(0)
	for percent_complete in range(100):
		time.sleep(0.000000000000000000000000000001)
		my_bar.progress(percent_complete + 1)

	# Main Menu option list

	if selected == 'Home':
		
		st.markdown(
        f"""<style>
		.stApp {{
			background: url("https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Background%20Main.png");
			background-size: cover;
         }}</style>""",unsafe_allow_html=True
		)

		st.subheader("GEOSEL System")
		st.subheader("Choose default tweets or type your own tweets.")

		default_or_own = st.radio("", ('Default tweets', 'My own tweets'))
		
		if default_or_own == 'Default tweets':

			st.subheader("Select default tweets to determine building type.")
			optiontweet = st.selectbox("",("Select one :",
			"I recently purchased a new house in Shah Alam.", 
			"In Petaling Jaya AEON Mall, I discovered several textile shop.",
			"I'm at Kuala Lumpur International Airport 2 (KLIA2).",
			"Lunch here today (@ Wizards in Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur)",
			"I'm at Sekolah Seri Puteri in Cyberjaya. Just posted a photo.",
			"I'm at Mitsui Shopping Park LaLaport - @lalafanlalaport in Kuala Lumpur.",
			"Some over-the-weekend raya open house photos.",
			"I'm at Padang Bolasepak Akedemi Merah Kuning in Sungai Buloh, Selangor.",
			"Buying a stock of some delicious coffee from @vnkopi.",
			"Alhamdulillah sampai juga. Lama tak solat sini (@ Masjid Diraja Tengku Ampuan Jemaah in Shah Alam, Selangor).",
			"I'm at Pusat Dagangan NSK (Trade City).",
			"Jom cari ikan di pasar tani sekitar rumah ini. Just posted a video @ Kampong Jenjarom, Selangor."))

			if optiontweet=="Select one :":
				st.subheader("Select one from the options.")

			check_tweetdef = optiontweet

			if check_tweetdef!="Select one :":
				prediction = predict_buildingslabel(optiontweet)
				probability = get_prediction_proba(optiontweet)

				# Output 1

				st.subheader("System Output")
				st.subheader("Your tweets :")
				st.info("{}".format(optiontweet))

				# Output 2

				st.subheader("Building type prediction :")
				building_icon = labelmeaning[prediction]
				st.info("Label {} : {} Area in Selangor".format(prediction,building_icon))

				if building_icon=='Residential':
			
					imageresident="https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Element%202.png"
					st.image(imageresident, width=705)

				if building_icon=='Commercial':
			
					imagecom="https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Element%203.png"
					st.image(imagecom, width=705)

				st.subheader("Building type probability score :")
				probabilitystatic = np.max(probability)
				probabilitystaticroundoff = format(probabilitystatic, '.4f')
				st.info("{} area score : {} / 1.0".format(building_icon,probabilitystaticroundoff))
			
				# Output 3

				st.subheader("Graph of prediction building type :")
				st.caption("( Label 0 = Residential, Label 1 = Commercial )")
				proba_df = pd.DataFrame(probability,columns=pipe_lrbow.classes_)
				proba_df_clean = proba_df.T.reset_index()
				proba_df_clean.columns = ["Building Type","Prediction score"]
				buildingchart = alt.Chart(proba_df_clean).mark_bar().encode(x='Building Type',y='Prediction score',color='Building Type')
				st.altair_chart(buildingchart,use_container_width=True)

		if default_or_own == 'My own tweets':

			st.subheader("Check your tweets to determine building type in Selangor.")
			with st.form(key='building_form'):
				raw_tweet = st.text_area("Type your tweets in the box.")
				check_tweet = st.form_submit_button(label='Predict Building Type')

			if check_tweet:
				prediction = predict_buildingslabel(raw_tweet)
				probability = get_prediction_proba(raw_tweet)

				# Output 1

				st.subheader("System Output")
				st.subheader("Your tweets :")
				st.info("{}".format(raw_tweet))

				# Output 2

				st.subheader("Building type prediction :")
				building_icon = labelmeaningown[prediction]
				st.info("Label {} : {} Area in Selangor".format(prediction,building_icon))

				if building_icon=='Residential':
			
					imageresident="https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Element%202.png"
					st.image(imageresident, width=705)

				if building_icon=='Commercial':
			
					imagecom="https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Element%203.png"
					st.image(imagecom, width=705)

				st.subheader("Building type probability score :")
				probabilitystatic = np.max(probability)
				probabilitystaticroundoff = format(probabilitystatic, '.4f')
				st.info("{} area score : {} / 1.0".format(building_icon,probabilitystaticroundoff))
			
				# Output 3

				st.subheader("Graph of prediction building type :")
				st.caption("( Label 0 = Residential, Label 1 = Commercial )")
				proba_df = pd.DataFrame(probability,columns=pipe_lrbow.classes_)
				proba_df_clean = proba_df.T.reset_index()
				proba_df_clean.columns = ["Building Type","Prediction score"]
				buildingchart = alt.Chart(proba_df_clean).mark_bar().encode(x='Building Type',y='Prediction score',color='Building Type')
				st.altair_chart(buildingchart,use_container_width=True)

	if selected == 'Dataset':
		
		# Background

		st.markdown(
         f"""<style>
		 .stApp {{
            background: url("https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Background%20Main%202.png");
            background-size: cover;
         }}</style>""",unsafe_allow_html=True
		)
		# Start

		datasetimg1="https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/1.png"
		datasetimg2=""
		datasetimg3=""
		datasetimg4=""
		datasetimg5=""
		datasetimg6=""
		datasetimg7=""
		datasetimg8=""
		datasetimg9=""
		datasetimg10=""

		st.image(datasetimg1, caption= 'Dataset CSV', width=705)

	if selected == 'QGIS':
		
		# Background

		st.markdown(
        f"""<style>
		.stApp {{
			background: url("https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Background%20Main%206.png");
			background-size: cover;
         }}</style>""",unsafe_allow_html=True
		)

		# Start

		QGISimg1=""
		QGISimg2=""
		QGISimg3=""
		QGISimg4=""
		QGISimg5=""
		QGISimg6=""
		QGISimg7=""
		QGISimg8=""
		QGISimg9=""
		QGISimg10=""

		#st.image(QGISimg1, caption= 'Dataset CSV', width=705)

	if selected == 'Model':
		
		# Background

		st.markdown(
        f"""<style>
		.stApp {{
			background: url("https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Background%20Main%203.png");
			background-size: cover;
         }}</style>""",unsafe_allow_html=True
		)

		# Start

		Modelimg1=""
		Modelimg2=""
		Modelimg3=""
		Modelimg4=""
		Modelimg5=""
		Modelimg6=""
		Modelimg7=""
		Modelimg8=""
		Modelimg9=""
		Modelimg10=""

		#st.image(Modelimg1, caption= 'Dataset CSV', width=705)

	if selected == 'Help':
		
		# Background

		st.markdown(
        f"""<style>
		.stApp {{
			background: url("https://raw.githubusercontent.com/Litchirays/Irman-FYP-Web-App/main/Images/Background%20Main%204.png");
			background-size: cover;
         }}</style>""",unsafe_allow_html=True
		)

		# Start

		Helpimg1=""
		Helpimg2=""
		Helpimg3=""
		Helpimg4=""
		Helpimg5=""
		Helpimg6=""
		Helpimg7=""
		Helpimg8=""
		Helpimg9=""
		Helpimg10=""

		#st.image(Helpimg1, caption= 'Dataset CSV', width=705)

if __name__ == '__main__':
	main()
