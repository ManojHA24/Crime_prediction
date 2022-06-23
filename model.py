#!C:\Users\Lenovo\AppData\Local\Programs\Python\Python37-32\python.exe
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import warnings
import pickle
warnings.filterwarnings("ignore")
import pandas as pd
import sys
sys.path.append("C:\\Users\\Manoj H A\\OneDrive\Documents\\CPY_SAVES\\Forest-Fire-Prediction-Website-master\\")
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import converter as cv
import seaborn as sns
from sklearn.utils import resample # for upsampling
import util_script as us
import os

DATA_PATH = "C:\\Users\\Manoj H A\\OneDrive\Documents\\CPY_SAVES\\Forest-Fire-Prediction-Website-master\\data\\"

# Load the Dataset
test_files = ['crimes_2012.csv', 'crimes_2014.csv', 'crimes_2013.csv','crimes_2015.csv','crimes_2016.csv','crimes_2017.csv','crimes_2018.csv','crimes_2019.csv','crimes_2020.csv','crimes_2021.csv']
test_files = [DATA_PATH+x for x in test_files]
test_df = us.create_df(test_files)

# Drop missing values
test_df = test_df.dropna()

# Using apply() of pandas to apply time_convert on every row of the Date column
test_df['Date'] = test_df['Date'].apply(cv.time_convert)

# Feature Engineering our columns
test_df['Month'] = test_df['Date'].apply(cv.month_col)
test_df['Day'] = test_df['Date'].apply(cv.day_col)
test_df['Hour'] = test_df['Date'].apply(cv.hour_col)

top_10 = list(test_df['Primary Type'].value_counts().head(10).index)
# Compressing
df7 = cv.filter_top_10(test_df,top_10)
cri7 = df7.groupby(["Month", "Day", "District", "Hour"], as_index=False).agg({"Primary Type" : "count"})
cri7 = cri7.sort_values(by=["District"], ascending=False)
cri8 = cri7.rename(index=str, columns={"Primary Type" : "Crime_Count"})
cri8 = cri8[["Month", "Day", "District", "Hour", "Crime_Count"]]
cri8['Alarm'] = cri8['Crime_Count'].apply(cv.crime_rate_assign)
cri8 = cri8[['Month','Day','Hour','District','Crime_Count','Alarm']]    
print(cri8.head())
print("Class Imbalance\n")
print(cri8['Alarm'].value_counts())



# Set individual classes
cri8_low = cri8[cri8['Alarm']==0]
cri8_medium = cri8[cri8['Alarm']==1]
cri8_high = cri8[cri8['Alarm']==2]

# Upsample the minority classes to size of class 1 (medium)
cri8_low_upsampled = resample(cri8_low, 
                                 replace=True,     # sample with replacement
                                 n_samples=31355,    # to match majority class
                                 random_state=101) 

cri8_med_upsampled = resample(cri8_medium, 
                                 replace=True,     # sample with replacement
                                 n_samples=31355,    # to match majority class
                                 random_state=101)

# Combine majority class with upsampled minority class
cri8_upsampled = pd.concat([cri8_high, cri8_low_upsampled, cri8_med_upsampled])

X = cri8_upsampled.iloc[:,0:4].values
y = cri8_upsampled.iloc[:,5].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')

logreg.fit(X_train, y_train)

inputt=[int(x) for x in "3 4 23 18".split(' ')]
final=[np.array(inputt)]

b = logreg.predict(final)

pickle.dump(logreg,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))


