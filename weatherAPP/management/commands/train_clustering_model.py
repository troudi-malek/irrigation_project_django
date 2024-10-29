from sklearn.cluster import KMeans
import joblib
from weatherAPP.data_processing import get_weather_data_for_clustering  

data = get_weather_data_for_clustering()

features = data[["temperature", "humidity", "precipitation", "irrigation_need"]]

kmeans = KMeans(n_clusters=3, random_state=42)

kmeans.fit(features)

joblib.dump(kmeans, "kmeans_climate_model.pkl")
