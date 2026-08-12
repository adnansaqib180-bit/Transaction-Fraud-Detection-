from lightgbm import LGBMClassifier
import joblib 
from UTILS import feature_engineering , load_data, preprocessor
from imblearn.over_sampling import SMOTE


final_df = load_data('DATA/processed data/processed_balanced_data.csv')

final_df = feature_engineering(final_df)

final_df = preprocessor(final_df , 'gender')

print(final_df.head())

print('\n =============== df is ready =============')

X_train = final_df.drop(columns=['is_fraud'])
Y_train = final_df['is_fraud']
smote = SMOTE()
X , Y = smote.fit_resample(X_train,Y_train)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)
print('\n ======== start training ========')
model = LGBMClassifier(
    colsample_bytree=0.6, learning_rate=0.05,
    min_child_samples=50, n_estimators=800, num_leaves=15,
    random_state=42, reg_alpha=1, reg_lambda=0.1, subsample=0.8,
    verbosity=-1,is_unbalance = True
)
print(Y.value_counts())
trained_model = model.fit(X,Y)


# --------------------------------------------------------------------



from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, confusion_matrix

df = load_data('DATA/raw data/Test_data.csv')

df = feature_engineering(df)

df = preprocessor(df , 'gender')
print('\n =============== df is ready =============')
print()
print(df.head())


x = df.drop(columns=['is_fraud'])
y = df['is_fraud']

x = scaler.fit_transform(x)

print('======= testing is start =========')

y_pred = trained_model.predict_proba(x)
for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    y_pred_threshold = (y_pred[:,1] >= threshold).astype(int)
    print(f"Threshold: {threshold}")
    print(f"Accuracy: {accuracy_score(y, y_pred_threshold)}")
    print(f"Precision: {precision_score(y, y_pred_threshold)}")
    print(f"Recall: {recall_score(y, y_pred_threshold)}")
    print(f"F1 Score: {f1_score(y, y_pred_threshold)}")
    print(f"Confusion Matrix:\n{confusion_matrix(y, y_pred_threshold)}\n")


import pandas as pd

importance_df = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
})

importance_df = importance_df.sort_values(
    by='importance',
    ascending=False
)

print(importance_df.head(20))