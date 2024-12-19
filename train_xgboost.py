import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# 读取CSV数据
df = pd.read_csv('D:/embeddings_with_labels_non_empty.csv')

# 提取特征和标签
features = df[[f'dim_{i}' for i in range(1, 1025)]].astype(float)
labels = df['分类标签']

# 设置K-Fold交叉验证参数
n_splits = 5
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# 初始化性能指标存储列表
accuracies = []
precisions = []
recalls = []
f1_scores = []
confusion_matrices = []

# XGBoost参数
xgb_params = {
    'n_estimators': 100,
    'max_depth': 6,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42
}

# 初始化最佳模型和最佳性能
best_model = None
best_f1_score = 0

# K-Fold交叉验证
for fold, (train_index, val_index) in enumerate(skf.split(features, labels), 1):
    # 分割数据
    X_train, X_val = features.iloc[train_index], features.iloc[val_index]
    y_train, y_val = labels.iloc[train_index], labels.iloc[val_index]

    # 初始化并训练模型
    clf = XGBClassifier(**xgb_params)
    clf.fit(X_train, y_train)

    # 预测
    y_pred = clf.predict(X_val)

    # 计算性能指标
    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred, average='weighted')
    recall = recall_score(y_val, y_pred, average='weighted')
    f1 = f1_score(y_val, y_pred, average='weighted')

    # 存储性能指标
    accuracies.append(accuracy)
    precisions.append(precision)
    recalls.append(recall)
    f1_scores.append(f1)
    confusion_matrices.append(confusion_matrix(y_val, y_pred))

    # 更新最佳模型
    if f1 > best_f1_score:
        best_f1_score = f1
        best_model = clf

    print(f"Fold {fold} Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}\n")

# 打印平均性能指标
print("Average Performance Metrics:")
print(f"Accuracy: {np.mean(accuracies):.4f} ± {np.std(accuracies):.4f}")
print(f"Precision: {np.mean(precisions):.4f} ± {np.std(precisions):.4f}")
print(f"Recall: {np.mean(recalls):.4f} ± {np.std(recalls):.4f}")
print(f"F1 Score: {np.mean(f1_scores):.4f} ± {np.std(f1_scores):.4f}")

# 保存最佳模型
if best_model is not None:
    # 保存整个模型
    joblib.dump(best_model, 'best_xgboost_model.joblib')

    # 也可以只保存模型权重
    best_model.save_model('best_xgboost_model.json')

    print("\n最佳模型已保存：")
    print("- joblib格式: best_xgboost_model.joblib")
    print("- JSON格式: best_xgboost_model.json")
    print(f"最佳模型的F1 Score: {best_f1_score:.4f}")