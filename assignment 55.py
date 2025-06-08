pip install scikit-learn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

#from sklearn.datasets import datasets
dir(datasets)
#from sklearn.datasets import datasets
breast_cancer =datasets.load_breast_cancer()
print (breast_cancer)

#to view columns
print("\n to view features_names______________")
print(breast_cancer.feature_names)

# Features and target
print("\n  Features and target__________________________")
x = pd.DataFrame(breast_cancer.data, columns=breast_cancer.feature_names)
y = pd.Series(breast_cancer.target)

# Class labels: 0 = malignant, 1 = benign
print(breast_cancer.target_names)

#standardise features with scale- centering the data(mean=0) and scaling date- standard deviation =1
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)


# to visualize features before scaling
plt.scatter(x['mean radius'], x['mean texture'], alpha=0.7)
plt.xlabel('Mean Radius (raw)')
plt.ylabel('Mean Texture (raw)')
plt.title('Before Scaling')
plt.grid(True)
plt.show()

# to visualise features after scaling
plt.scatter(x_scaled[:,0], x_scaled[:,1], alpha=0.7)
plt.xlabel('Mean Texture (scaled)')
plt.ylabel('Mean Radius (scaled)')
plt.title('After Scaling')
plt.grid(True)
plt.show()

# to reduce or summarise dataset into 2 variables
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)

# Convert to DataFrame for visualization
df_pca = pd.DataFrame(x_pca, columns=['PC1', 'PC2'])
df_pca['target'] = y

#visualise the result
plt.figure(figsize=(8,6))
scatter = plt.scatter(df_pca['PC1'], df_pca['PC2'], c=df_pca['target'], cmap='cividis', alpha=0.7)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of Breast Cancer Dataset')
handles, _ = scatter.legend_elements()
plt.legend(handles=handles, labels=list(breast_cancer.target_names[:len(handles)]))
plt.grid(True)
plt.show()

print("\n logistic Regression on reduced data_______________________________")
# Split data into 2 parts 80% train and 20% test
x_train, x_test, y_train, y_test = train_test_split(x_pca, y, test_size=0.2, random_state=42)

# Fit logistic regression
logreg = LogisticRegression()
logreg.fit(x_train, y_train)

# Use model to predict unseen test data
y_pred = logreg.predict(x_test)

#	Measure model accuracy and performance
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=breast_cancer.target_names))
