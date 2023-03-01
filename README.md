# Seattle Houses Analysis and Price Prediction
 Analysis of a dataset that contains house sale prices for King County, which includes Seattle. It includes homes sold between May 2014 and May 2015.
 
 
In this link you can see the dashboard created in streamlit : https://analytics-us-houses.herokuapp.com/
 

Note:
The .csv file used is on this link: https://www.kaggle.com/datasets/harlfoxem/housesalesprediction?select=kc_house_data.csv

## 1.0 The Context
 Business analysis of a fictional real estate company, in which the CEO is interested in maximize company profit by finding good deals in King County.
 
![image](https://user-images.githubusercontent.com/124091702/216186114-7d7a7dc9-558c-48b9-bcb1-a2bc062369de.png)




## 2.0 The Problem

  The CEO would like to access certain information, in an easy and interactive way, for some business strategy on his own cell phone. Such information as:
   
   - Property filters by one or several regions;
   - Choose one or more variables to view;
   - Observe a total number of properties, the average price, the average living room and also the average price per square meter in each of the zip codes;
   - Analyze each of the columns in a more descriptive way;
   - A map with portfolio density by region and also price density;
   - Check the distribution of properties by number of bathrooms and bedrooms.
  
  <br>
  
  ## 3.0 The Solution
  
  Build an iterative dashboard through streamlit and provide the access link through the Heroku platform.
  ![image](https://user-images.githubusercontent.com/124091702/216185715-8004d531-876f-4c79-bb24-83b86470222a.png)

### 3.1 Planning the Solution

   - Property filters by one or several regions.
 
    -Objective: View properties by zip code.
    
    -User Action: Enter one or more desired codes.

    -A view: A table with all attributes and filtered by postal code
    
   - Choose one or more variables to view
   
    -Objective: View characteristics of the property.
    
    -User Action: Enter the desired characteristics.
    
    -A view: A table with all attributes selected

   - Observe a total number of properties, the average price, the average living room and also the average price per square meter in each of the zip codes
   
    -Objective: View the averages of some metrics by region.
    
    -User Action: Enter the desired metrics.
    
    -A view: A table with all attributes selected.
    
   - Analyze each of the columns in a more descriptive way
   
    -Objective: View more descriptive reviews.
    
    -User Action: Enter the desired metrics.
    
    -A view: A table with descriptive metrics by selected attribute.
    
   - A map with portfolio density by region and also price density
   
    -Objective: View portfolio density on the map (number of properties by region and by price).
    
    -User Action: Zoom the map.
    
    -A view: A map with real estate density by region and by price created using geopandas and the folium library.
    
   - Check the distribution of properties by number of bathrooms and bedrooms
   
    -Objective: Observe the concentration of properties by bedrooms and bathrooms
    
    -User Action: Filter number of bedrooms and bathrooms
    
    -A view:  A histogram with each attribute defined.
    
  
  ### 3.2 Machine Learning Implementation
  ##### 3.2.1 Linear Regression
  
  This type of machine learning was implemented by analyzing the correlation coefficient of price with attributes.In addition, the multiple linear regression results were already satisfactory for the report and for the CEO's required understanding and analysis of pricing.

#### Heatmap with correction coefficients
     
![heatcoeficiente](https://user-images.githubusercontent.com/124091702/222221705-b0090b49-36b1-4488-a251-9995a2ccd84c.png)

With this analysis we chose the attributes: 'bedrooms', 'bathrooms', 'sqft_living',
       'sqft_lot', 'floors', 'waterfront', 'view', 'condition', 'grade',
       'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode',
       'lat'and'long' to be compared with the 'price'attribute.
       
##### Conclusion of the linear regression implementation
With this implementation, we achieved around 68.85% accuracy of the results with the validation base and an average error equal to 123888.44377486005.


    
