from lightgbm import LGBMClassifier
import joblib 
from UTILS import feature_engineering , load_data, preprocessor
from imblearn.over_sampling import SMOTE


final_df = load_data('DATA/raw data/fraudTrain.csv')

final_df = feature_engineering(final_df)

final_df = preprocessor(final_df , 'gender')

print(final_df.head())

print('\n =============== df is ready =============')
print(final_df.columns)

X = final_df.drop(columns=['is_fraud'])
Y = final_df['is_fraud']


print('\n ======== start training ========')
model = LGBMClassifier(
    colsample_bytree=0.6, learning_rate=0.05,
    min_child_samples=50, n_estimators=800, num_leaves=15,
    random_state=42, reg_alpha=1, reg_lambda=0.1, subsample=0.8,
    verbosity=-1,class_weight='balanced',scale_pos_weight=2000
)
print(Y.value_counts())
trained_model = model.fit(X,Y)


joblib.dump(trained_model,'trained_model.pkl')
