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
| SVM              | 0.9997         | 0.9971         | 0.9953         | 0.9962          |
| Random Forest     | 0.9965         | 0.9135         | 1.0000         | 0.9548          |
| CatBoost         | 0.9994         | 0.9857         | 0.9988         | 0.9922          |
| Logistic Regression | 0.9996       | 0.9901         | 0.9988         | 0.9944          |


### Мы сделали сайт, на котором вы можете потестировать работу нашего решения
### https://crustaceano-retirementanalysis-070d.twc1.net/
