from UTILS import feature_engineering , load_data, preprocessor, load_model
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, confusion_matrix

final_df = load_data('DATA/raw data/Test_data.csv')

final_df = feature_engineering(final_df)

final_df = preprocessor(final_df , 'gender')
print('\n =============== df is ready =============')
print()
print(final_df.head())


X = final_df.drop(columns=['is_fraud'])
Y = final_df['is_fraud']
print()
print('========= loaded model =======')

model = load_model()

print('======= testing is start =========')

predictions = model.predict(X)

print('====== model performance ========')

print('Accuracy : ', accuracy_score(Y, predictions))
print('Precision : ', precision_score(Y, predictions))  
print('Recall : ', recall_score(Y, predictions))
print('F1 Score : ', f1_score(Y, predictions))
print('Confusion Matrix : \n', confusion_matrix(Y, predictions))

