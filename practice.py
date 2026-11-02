import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

#load dataset
df=pd.read_csv("uber.csv")

print(df.info())
print(df.columns)
print(df.isnull().sum())

df["dropoff_longitude"]=df["dropoff_longitude"].fillna(df["dropoff_longitude"].mean())
df["dropoff_latitude"]=df["dropoff_latitude"].fillna(df["dropoff_latitude"].mean())

features=["pickup_longitude","pickup_latitude","dropoff_longitude","dropoff_latitude"]
x=df[features]
y=df["fare_amount"]

q1=y.quantile(0.25)
q3=y.quantile(0.75)
iqr=q3-q1

lower_limit=q1-1.5*iqr
upper_limit=q3+1.5*iqr

outliers=df[(df["fare_amount"]<lower_limit)|(df["fare_amount"]>upper_limit)]

print("out: ",len(outliers))

sns.boxplot(x=df["fare_amount"])
plt.show()

df=df[df["fare_amount"].between(lower_limit,upper_limit)]

x=df[features]
y=df["fare_amount"]

print("out: ",len(outliers))

sns.boxplot(x=df["fare_amount"])
plt.show()

corr=df[features+["fare_amount"]].corr()
print("corr: ",corr["fare_amount"])

plt.figure()
sns.heatmap(corr,annot=True,cmap="coolwarm",fmt=".2f")
plt.show()

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

lr=LinearRegression()
lr.fit(x_train,y_train)
y_pred_lr=lr.predict(x_test)

rf=RandomForestRegressor(n_estimators=100,random_state=42,n_jobs=-1)
rf.fit(x_train,y_train)
y_pred_rf=rf.predict(x_test)

r2_lr=r2_score(y_test,y_pred_lr)
r2_rf=r2_score(y_test,y_pred_rf)

rmse_lr=np.sqrt(mean_squared_error(y_test,y_pred_lr))
rmse_rf=np.sqrt(mean_squared_error(y_test,y_pred_rf))

results=pd.DataFrame({
    "models":["lr","rf"],
    "f2":[r2_lr,r2_rf],
    "rmse":[rmse_lr,rmse_rf]
})

results.set_index("models").plot(kind="bar")
plt.show()

input=pd.DataFrame([{
    "pickup_longitude":-74,
    "pickup_latitude":40.5,
    "dropoff_longitude":-73.5,
    "dropoff_latitude":41
}])

ans=lr.predict(input)
print(ans)

ans1=rf.predict(input)
print(ans1)