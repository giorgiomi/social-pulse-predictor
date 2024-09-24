## To do


# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# from sklearn.model_selection import train_test_split

# data = pd.read_csv("../../data/processed/grouped_date_mun_hour.csv").drop(['class', 'Unnamed: 0'], axis=1)

# # Assuming 'data' is your full dataset with columns:
# # 'date', 'municipality.name', 'hour_category', 'temperature', 'minTemperature',
# # 'maxTemperature', 'precipitation', 'wind_speed', 'tweet_count'

# # 1. Split data into training set (before 2013-12-31) and the test set for 2013-12-31
# train_data = data[data['date'] < '2013-12-31']  # Training data up to 2013-12-30
# test_data = data[data['date'] == '2013-12-31']  # Test data for 2013-12-31

# # 2. Prepare features (X) and target (y) for training
# X_train = train_data[['municipality.name', 
#                       'hour_category', 
#                       'temperature', 
#                       'minTemperature', 
#                       'maxTemperature', 
#                       'precipitation',
#                       'wind_speed',
#                       'wind_dir',
#                       'curr_cell',
#                       'curr_site']]

# y_train = train_data['tweet_count']  # Target: Tweet count on past days

# # 3. Prepare features for prediction (without target 'tweet_count' for the test data)
# X_test = test_data[['date',
#                     'municipality.name', 
#                     'hour_category', 
#                     'temperature', 
#                     'minTemperature', 
#                     'maxTemperature', 
#                     'precipitation',
#                     'wind_speed',
#                     'wind_dir',
#                     'curr_cell',
#                     'curr_site']]

# # Encode categorical features
# le = LabelEncoder()
# for feat in categorical_features:
#     X[feat] = le.fit_transform(X[feat])

# # Drop original categorical columns
# X_train = X_train.drop(columns=['municipality.name', 'hour_category', 'date'])
# X_test = X_test.drop(columns=['municipality.name', 'hour_category', 'date'])

# # 5. Scale the numerical features
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# # 6. Train the Random Forest Regressor
# rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
# rf_regressor.fit(X_train_scaled, y_train)

# # 7. Predict the tweet counts for 2013-12-31
# y_pred_2013_12_31 = rf_regressor.predict(X_test_scaled)

# # Add the predictions to the test data
# test_data['predicted_tweet_count'] = y_pred_2013_12_31

# # 8. Display predictions for each municipality and timeslot
# print(test_data[['date', 'municipality.name', 'hour_category', 'predicted_tweet_count']])
