import pandas as pd

# import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
import sklearn.tree as tree
from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import export_graphviz
# import graphviz


file = "archive/cardiovascular_risk_dataset.csv"

# dataset from kaggle: https://www.kaggle.com/datasets/vishardmehta/heart-risk-progression-dataset
# heart risk data set, used for ML usually but good here too

# Patient_ID  age   bmi  systolic_bp  diastolic_bp  cholesterol_mg_dl  ...  sleep_hours family_history_heart_disease  diet_quality_score  alcohol_units_per_week  heart_disease_risk_score  risk_categor│
df = pd.read_csv(file)
# print(df.head)
dfX = df[
    [
        "age",
        "bmi",
        "diastolic_bp",
        "cholesterol_mg_dl",
        "daily_steps",
        "stress_level",
        "physical_activity_hours_per_week",
        "sleep_hours",
        "diet_quality_score",
        "alcohol_units_per_week",
    ]
]
dfY = df["risk_category"]

X_train, X_test, y_train, y_test = train_test_split(dfX, dfY, test_size=0.30)

DT = tree.DecisionTreeClassifier()
DT.fit(X_train, y_train)

pred = DT.predict(X_test)

print("\nModel accuracy score:", accuracy_score(y_test, pred))
print("\nConfusion Matrix\n", confusion_matrix(y_test, pred))


knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

print("\nModel accuracy score:", accuracy_score(y_test, pred))
print("\nConfusion Matrix\n", confusion_matrix(y_test, pred))

model = GaussianNB().fit(X_train, y_train)
pred = model.predict(X_test)
print("\nModel accuracy score:", accuracy_score(y_test, pred))

model = MLPClassifier(max_iter=2500).fit(X_train, y_train)
pred = model.predict(X_test)

print("\nModel accuracy score:", accuracy_score(y_test, pred))

"""
Model Analyses
The Decision Tree model provides a breakdown of risk by identifying specific threshold values in features like BMI or cholesterol to categorize patients. Its confusion matrix shows it is particularly strong at identifying the second risk category, though it struggles with overlap between the first and third groups, which seems odd but the proof is in the pudding.

The KNN model classifies cardiovascular risk by grouping a patient with the five most similar individuals in the dataset based on their physical and lifestyle metrics. While it maintains a decent accuracy, the higher number of misclassifications in the confusion matrix suggests that some risk categories are not clearly separated in the feature space.

This model uses probability to determine risk, assuming that each health factor contributes independently to the likelihood of a specific risk category. With an accuracy of approximately 79.8%, it is the top-performing model, indicating that the health metrics follow a predictable distribution that fits probabilistic patterns well.

The Neural Network attempts to find complex, non-linear relationships between variables like alcohol consumption and sleep hours to predict heart disease risk. However, with an accuracy of only 61.7%, it is the weakest model, likely because the dataset is not large enough or the features are not complex enough to benefit from the multi-layer architecture.

The Gaussian Naive Bayes model significantly outperforms the other three, suggesting that a statistical, probabilistic approach is most effective for this specific cardiovascular dataset. In contrast, the Neural Network performs the worst, likely due to "overcomplicating" the data or requiring more intensive feature scaling than the tree or neighbor-based models. While the Decision Tree and KNN models show similar accuracy levels around 71-75%, the Decision Tree's confusion matrix reveals slightly better precision in isolating specific risk tiers. Overall, while the simpler statistical models excel here, the more complex algorithmic models like the MLP struggle to find a clear signal amidst the patient noise.
"""
