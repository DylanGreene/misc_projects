# MLP for Regression
## Dylan Greene

### Train the Regression Model
Root-Mean-Square-Error achieved at epoch 1000:
* 0.34117494853093255

### Make Predictions Using the Regression Model and Evaluate
Root-Mean-Square-Error of predictions:
* 7.882993534108646

This result is really not very good. Looking at the actual predictions, there are clearly some which are not good.
However, based on the fact that running the prediction on the training data returns a much better RMSE, this is likely do to over-fitting.
As a result of the network over-fitting the training data, it does not generalize well and as such explains the observed behavior. 
