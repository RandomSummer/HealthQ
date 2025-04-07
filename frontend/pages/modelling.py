import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import time

st.title("Waste Segmentation App")

with st.sidebar:
    st.info(f"Role : {st.session_state.role}.")

def prediction():
    msg = st.toast('Preprocessing Date...')
    time.sleep(1)
    msg.toast('Analysing...')
    time.sleep(1)
    msg.toast('Done', icon = "✔")

uploaded_file = st.file_uploader("Choose a CSV file ...")
prediction()

# if st.button('Press to use Example Dataset'):
#     # Load the example file directly
#     example_file = 'simulated_waste_bins.csv'  # Ensure the file is in the same directory
#     uploaded_file = open(example_file, 'r')  # Open the file as a binary read
#     prediction()

if uploaded_file is not None:
    # Load data
    if uploaded_file.name.endswith('csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('xlsx'):
        data = pd.read_excel(uploaded_file, engine='openpyxl')

    # Handling missing values
    st.subheader('Handling Missing Values')
    st.write("Original data shape:", data.shape)
    st.write("Number of missing values before handling:", data.isnull().sum().sum())
    
    # Drop rows with any NaN values
    data.dropna(inplace=True)

    # Verify data integrity post handling missing values
    st.write("Number of missing values after handling:", data.isnull().sum().sum())

    # Display Data
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    # Data Preprocessing
    st.subheader('Data Preprocessing')
    columns = data.columns.tolist()

    # Convert string columns to integers
    for col in columns:
        if data[col].dtype == 'object':  # Check if column dtype is object (string)
            encoder = LabelEncoder()
            data[col] = encoder.fit_transform(data[col])

    selected_columns = st.multiselect('Select columns for clustering', columns)

    if selected_columns:
        st.write(f"Selected columns for clustering: {selected_columns}")
        if len(selected_columns) >= 2:
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data[selected_columns])

            # Clustering
            st.subheader('Clustering')
            num_clusters = st.slider('Select number of clusters', 2, 10, 3)
            kmeans = KMeans(n_clusters=num_clusters)
            data['Cluster'] = kmeans.fit_predict(scaled_data)

            # Visualize Clusters
            st.subheader('Cluster Visualization')
            if len(selected_columns) >= 2:
                fig, ax = plt.subplots()
                sns.scatterplot(x=data[selected_columns[0]], y=data[selected_columns[1]], hue=data['Cluster'], palette='viridis', ax=ax)
                st.pyplot(fig)
            else:
                st.write("Please select at least two columns for clustering visualization.")
        else:
            st.write("Please select at least two columns for clustering visualization.")
    else:
        st.write("Please select columns for clustering.")