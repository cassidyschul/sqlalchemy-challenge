# sqlalchemy-challenge
Module 10 Challenge

In this assignment, I created a Python script to perform basic climate analysis and data exploration using a climate database. I used SQLAlchemy ORM to perform database queries, Pandas for data processing, and Matplotlib for creating visualizations.

I retrieved the last twelve months of precipitation data through SQLAlchemy, then loaded the results into a Pandas DataFrame to create a plot of precipitation over time.

![Tweleve_Month_Precipitation_Data.png](https://github.com/cassidyschul/sqlalchemy-challenge/blob/main/Figures/Tweleve_Month_Precipitation_Data.png?raw=true)

Next, I designed a query to identify the most active weather station in the database and calculated its minimum, maximum, and average temperatures. I then queried the temperature observation (TOBS) data from this most active station and used a histogram to visualize the temperature distribution.

![Twelve_Month_Temp_Data_Most_Active_Station.png](https://github.com/cassidyschul/sqlalchemy-challenge/blob/main/Figures/Twelve_Month_Temp_Data_Most_Active_Station.png?raw=true)

Finally, I built a Flask API to share these queries and results.


## Usage
Launch Jupyter Notebook and navigate to climate_script.ipynb
