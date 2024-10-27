# ByteBusters

### RetirementAnalysis
Прогнозирование раннего выхода на пенсию.

Мы протестировали работу нескольких моделей на кросс валидации K_fold=5
* CatBoost
* Random Forest
* Logistic Regression
* Support Vector Machines

### Бенчмарк 

| Модель           | Accuracy        | Precision       | Recall          | F1 Score        |
|------------------|----------------|----------------|----------------|-----------------|
| SVM              | 0.6997         | 0.7571         | 0.7553         | 0.7562          |
| Random Forest     | 0.7865         | 0.7035         | 0.8000         | 0.6548          |
| CatBoost         | 0.8594         | 0.8457         | 0.8588         | 0.8522          |
| Logistic Regression | 0.8996       | 0.8901         | 0.8988         | 0.8944          |


### Мы сделали сайт, на котором вы можете потестировать работу нашего решения
### https://crustaceano-retirementanalysis-070d.twc1.net/
