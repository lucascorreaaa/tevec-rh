# Loading useful libraries
import pandas as pd
import numpy as np; np.random.seed(0)
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.decomposition import PCA

# Loading input data file into variable 'data' as a Data Frame
data = pd.read_csv("artificial_binary_classification_data.csv", index_col=0)

# Setting 'X' (independent variables) and 'y' (dependent variable)
X = data.drop('Target',axis=1)
y = data.iloc[:,-1]

# Visualizing descriptive statistics of the features
X.describe()

# Looking for any missing value (there's none)
X.isnull().sum().sum()

# Plotting the heatmap of correlation between the features
corr = X.corr()
sns.heatmap(corr, vmin=-1, vmax=1, center=0, cmap=sns.diverging_palette(20, 220, n=200))
#plt.show()

# ----------------------------------------------------------------------
# Excluding features with absolute correlation value greater than 0.8
# ----------------------------------------------------------------------

# Gettin upper triangle of correlation matrix
corr_upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(np.bool))

# Identifying features (columns) to drop (corr value > 0.8)
columns_to_drop = [column for column in corr_upper.columns if any(corr_upper[column].abs() > 0.8)]

# Droping columns from X
X = X.drop(columns_to_drop, axis=1)

# Plotting the heatmap of correlation matrix without correlated features.
sns.heatmap(X.corr(), vmin=-1, vmax=1, center=0, cmap=sns.diverging_palette(20, 220, n=200))
#plt.show()

# ----------------------------------------------------------------------
# Applying Principal Components Analysis (PCA) for dimensionality reduction
# ----------------------------------------------------------------------

# Applying PCA over all features and getting sufficient components to explain 99,9% of variance
pca = PCA(n_components=0.999, svd_solver='full')

# Fitting PCA and transforming X set onto PCA components space (dimensionality reduction)
X_pca = pca.fit_transform(X)

# ----------------------------------------------------------------------
# Applying Extremely Randomized Trees Classifier (Extra Tree Classifier - ETC)
# ----------------------------------------------------------------------

# Spliting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2)

# Fitting RFC model
etc = ExtraTreesClassifier(n_estimators=100)
etc.fit(X_train, y_train)

# Classifing the test set
y_pred = etc.predict(X_test)

# Checking RFC model performance
rfc_performance = (y_pred == y_test).sum() / len(y_test)
print("Extra Trees Classifier performance:", rfc_performance*100, "%")