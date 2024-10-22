import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from model.generate_vector import get_judge_list

def get_judge_result():
    # 读取数据
    data = pd.read_csv('model/judge/m.csv', header=None)

    # 将最后一列设为标签
    data.columns = list(range(data.shape[1]-1)) + ['label']

    # 特征和标签
    X = data.drop('label', axis=1)
    y = data['label']

    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    # 处理不平衡数据，使用SMOTE
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    # 创建随机森林分类器
    clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

    # 训练模型
    clf.fit(X_train_resampled, y_train_resampled)

    # 预测
    y_pred = clf.predict(X_test)

    # 评估模型
    #print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
    #print(classification_report(y_test, y_pred))

    # 使用交叉验证评估模型
    cv_scores = cross_val_score(clf, X_scaled, y, cv=5)
    #print(f'Cross-validation scores: {cv_scores}')
    #print(f'Mean CV score: {cv_scores.mean()}')

    # 输入数据
    vector = get_judge_list()
    new_data = np.array([vector])

    # 标准化输入数据
    new_data_scaled = scaler.transform(new_data)

    # 进行预测
    new_prediction = clf.predict(new_data_scaled)

    # 输出预测结果
    return new_prediction[0]