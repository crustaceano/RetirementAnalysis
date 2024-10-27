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
| SVM              | 0.3997         | 0.4571         | 0.4553         | 0.4562          |
| Random Forest     | 0.5865         | 0.5035         | 0.6000         | 0.4548          |
| CatBoost         | 0.6594         | 0.6457         | 0.6588         | 0.6522          |
| Logistic Regression | 0.6996       | 0.6901         | 0.6988         | 0.6944          |


### Мы сделали сайт, на котором вы можете потестировать работу нашего решения
### https://crustaceano-retirementanalysis-070d.twc1.net/
