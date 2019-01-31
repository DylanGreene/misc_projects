# Supervised Learning and Open Set Recognition
## Dylan Greene

## Baseline Accuracy (Closed Set):
Accuracy = 94.46% (9446/10000) (classification)

## Open Set (Trained using only 0-5):
Baseline: Accuracy = 58.47% (5847/10000) (classification)
### Improved approach:
First, train a new model using the -b flag set to 1. This flag trains a regression model which allows for probability estimates. This will allow prediction based on probabilities rather than just multi-class classification. Since this is an open set, it is important to be able to predict that the output is unknown rather than taking just the largest probability of known classes.
Baseline for probability based prediction: Accuracy = 58.52% (5852/10000) (classification)
However, now that the probabilities of each known class are available, we can determine if we are confident enough to actually predict that a sample fits one of the known classes.
This can be done using a simple script to see if any of the predicted classes surpass a certain threshold of confidence for the prediction. This has been implemented in `proba_predict.py`.
Based on some analysis of what confidence probability would be a good break point, it turned out 0.95 was around the sweet spot. As such, if the highest predicted probability is less than 0.95, we will predict it is unknown (-1). On the other hand, if it is greater than or equal to 0.95, we will predict the class of that probability.
Based on these changes, I was able to classify 8315 of the 10000 correctly. Thus the improved method resulted in an accuracy of 83.15% for the open set data compared to the baseline of just 58.52%.
To run this improved version:
  * `./svm-train -b 1 mnist_openset.scale mnist_openset.scale.model_proba`
  * `./svm-predict -b 1 mnist_openset.scale.t mnist_openset.scale.model_proba mnist_openset.scale.output_proba`
  * `python proba_predict.py mnist_openset.scale.t mnist_openset.scale.output_proba mnist_openset.scale.improved_output`
The predicted classes will be stored on each line of `mnist_openset.scale.improved_output`
