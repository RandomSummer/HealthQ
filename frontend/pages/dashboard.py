import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import datetime


with st.sidebar:
    st.info(f"Dashboard for monitoring the data. (Role) : {st.session_state.role}.")
        

a, b = st.columns(2)
c, d = st.columns(2)

a.metric(label="E-Dustbin", value="100", border=True)
b.metric(label="Location", value="20", border=True)

c.metric(label="Truck", value="8", border=True)
d.metric(label="Worker", value="24", border=True)



if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

uploaded_data = st.file_uploader("Choose a CSV file ...")

if uploaded_data is not None:
    # Load data
    if uploaded_data.name.endswith('csv'):
        data = pd.read_csv(uploaded_data)
    elif uploaded_data.name.endswith('xlsx'):
        data = pd.read_excel(uploaded_data, engine='openpyxl')

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Chart", "🗃 Data", "Activity", "Pickups", "Tasks", "Services"])

    data.dropna(inplace=True)

    columns = data.columns.tolist()

    # Convert string columns to integers
    for col in columns:
        if data[col].dtype == 'object':  # Check if column dtype is object (string)
            encoder = LabelEncoder()
            data[col] = encoder.fit_transform(data[col])

    selected_columns = ["fill_level", "temperature"]


    with tab1:
        col1,  col2 = st.columns(2)

        with col1:
            # tab1.subheader("A tab with a chart")
            if selected_columns:
                if len(selected_columns) >= 2:
                    scaler = StandardScaler()
                    scaled_data = scaler.fit_transform(data[selected_columns])

                    # Clustering
                    num_clusters = st.slider('Select number of clusters', 2, 10, 3)
                    kmeans = KMeans(n_clusters=num_clusters)
                    data['Cluster'] = kmeans.fit_predict(scaled_data)

                    # Visualize Clusters
                    if len(selected_columns) >= 2:
                        fig, ax = plt.subplots()
                        sns.scatterplot(x=data[selected_columns[0]], y=data[selected_columns[1]], hue=data['Cluster'], palette='viridis', ax=ax)
                        st.pyplot(fig)

        with col2:

            st.info("Linegraph using csv file \n Data psafljkasklfjaslkflkSFJLK rocessed")

            if 'location_lat' in data.columns and 'location_lon' in data.columns:
                            fig2, ax2 = plt.subplots()
                            sns.lineplot(
                                x=data['location_lat'],
                                y=data['location_lon'],
                                # hue=data['Cluster'],
                                palette='coolwarm',
                                ax=ax2
                            )
                            ax2.set_title("Clusters for latitude vs longitude")
                            st.pyplot(fig2)

    with tab2:
        tab2.subheader("A tab with the data")
        st.subheader('Raw data')
        st.write(data)
        # tab2.write(data)

    tab3.subheader("A tab with the Activity")
    d = tab3.date_input("Activities within ", value=None)
    # tab3.write("Filtered Date: ", d)

    tab4.subheader("A tab with the PickUp")
    tab4.write(data)

    with tab5:
        tab5.subheader("A tab with the Tasks")
        tab5.write(data)
       
        st.title("K-Means Clustering with Scatter Plots")

        # File uploader to load a CSV file
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

        if uploaded_file:
            # Read the uploaded CSV file
            data = pd.read_csv(uploaded_file)
            st.write("### Data Preview", data.head())

            # Allow user to select columns for clustering
            selected_columns = st.multiselect("Select columns for clustering", data.columns)

            if selected_columns:
                if len(selected_columns) >= 2:
                    # Scaling the selected data
                    scaler = StandardScaler()
                    scaled_data = scaler.fit_transform(data[selected_columns])

                    # Clustering
                    num_clusters = st.slider('Select number of clusters', 2, 10, 3, key="num_clusters_slider")
                    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
                    data['Cluster'] = kmeans.fit_predict(scaled_data)

                    # Scatter Plot 1: Based on selected columns
                    fig1, ax1 = plt.subplots()
                    sns.scatterplot(
                        x=data[selected_columns[0]],
                        y=data[selected_columns[1]],
                        hue=data['Cluster'],
                        palette='viridis',
                        ax=ax1
                    )
                    ax1.set_title(f"Clusters for {selected_columns[0]} vs {selected_columns[1]}")
                    st.pyplot(fig1)

                    # Scatter Plot 2: With fill_level and temperature
                    if 'fill_level' in data.columns and 'temperature' in data.columns:
                        fig2, ax2 = plt.subplots()
                        sns.scatterplot(
                            x=data['fill_level'],
                            y=data['temperature'],
                            hue=data['Cluster'],
                            palette='coolwarm',
                            ax=ax2
                        )
                        ax2.set_title("Clusters for Fill Level vs Temperature")
                        st.pyplot(fig2)
                else:
                    st.warning("Please select at least two columns for clustering.")
            else:
                st.info("Select columns to begin clustering.")
        else:
            st.info("Upload a CSV file to get started.")


    tab6.subheader("A tab with the Services")
    tab6.write(data)
