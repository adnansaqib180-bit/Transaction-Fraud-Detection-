from lightgbm import LGBMClassifier
import joblib 
from UTILS import feature_engineering , load_data, preprocessor
from imblearn.over_sampling import SMOTE


final_df = load_data('DATA/processed data/processed_balanced_data.csv')

final_df = feature_engineering(final_df)

final_df = preprocessor(final_df , 'gender')

print(final_df.head())

print('\n =============== df is ready =============')
print(final_df.columns)

X_train = final_df.drop(columns=['is_fraud'])
Y_train = final_df['is_fraud']
smote = SMOTE(random_state=42)
X , Y = smote.fit_resample(X_train,Y_train)

print('\n ======== start training ========')
model = LGBMClassifier(
    colsample_bytree=0.6, learning_rate=0.05,
    min_child_samples=50, n_estimators=800, num_leaves=15,
    random_state=42, reg_alpha=1, reg_lambda=0.1, subsample=0.8,
    verbosity=-1,is_unbalance = True
)
print(Y.value_counts())
trained_model = model.fit(X,Y)


joblib.dump(trained_model,'trained_model.pkl')