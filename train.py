import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# 读取训练数据
df_train = pd.read_csv('D:/embeddings_with_labels_non_empty.csv', encoding='utf-8-sig')

# 提取训练特征和标签
features_train = df_train[[f'dim_{i}' for i in range(1, 1025)]].astype(float)
labels_train = df_train['分类标签']

# 转换标签为整数
le = LabelEncoder()
labels_train = le.fit_transform(labels_train)

# 标准化特征
scaler = StandardScaler()
features_train_scaled = scaler.fit_transform(features_train)

# 定义模型列表
models = [
    ('SVM', SVC()),
    ('Random Forest', RandomForestClassifier())
]

# 训练模型并在训练数据上进行5折交叉验证
for name, model in models:
    scores = cross_val_score(model, features_train_scaled, labels_train, cv=5)
    print(f'{name} Cross-Validation Accuracy: {np.mean(scores)} (+/- {np.std(scores)})')

    # 训练模型
    model.fit(features_train_scaled, labels_train)

    # 读取测试数据
    df_test = pd.read_csv('D:/embeddings_with_labels_non_empty_guangfu2021.csv', encoding='utf-8-sig')

    # 提取测试特征和标签
    features_test = df_test[[f'dim_{i}' for i in range(1, 1025)]].astype(float)
    labels_test = df_test['分类标签']

    # 转换测试标签为整数
    labels_test = le.transform(labels_test)

    # 标准化测试特征
    features_test_scaled = scaler.transform(features_test)

    # 预测测试数据
    predictions = model.predict(features_test_scaled)

    # 计算准确率
    accuracy = accuracy_score(labels_test, predictions)
    print(f'{name} Test Accuracy: {accuracy}')

    # 输出分类报告
    print(f'{name} Classification Report:\n', classification_report(labels_test, predictions))