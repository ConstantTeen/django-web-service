# django-web-service

Есть разработчики моделей машинного обучения, а также люди, которые хотели бы пользоваться этими моделями, не имея при этом специальных знаний в области МЛ. 
На помощь приходит этот веб-сервис, который способен хранить модели разработчиков, а также предоставлять к ним доступ через http-запросы. 

## Из чего состоит проект?

Проект состоит из двух частей: 
* первая часть общается с клиентом: принимает от него xml-файл с входными данными, отправляет на вход модели и отправляет обратно предсказанные значения.
Также есть функционал приема исправленных экспертом предсказанных значений, с целью анализа ошибок модели.
* вторая часть позволяет разработчикам выложить готовую модель в веб-сервис

## Схема БД веб-сервиса

![BD schema](https://github.com/ConstantTeen/django-web-service/blob/master/additional_files/Relational_115_ind.png)

Часто модели, которые строят разработчики, решают схожие задачи, которые можно сгруппировать в проекты. Так например, может быть проект по классификации клиентов,
который распадается на две задачи: классификация юридических лиц и классификация физических лиц. Поэтому в БД хранится таблица Project (Проект), 
которое имеет внешний ключ на таблицу Task (Задача).


Сами модели хранятся в бинарном виде в таблице Model, вместе с данными автора модели, версией и прочим.

Все запросы к моделям со стороны клиентов отражены в таблице UserRequest (requests на диаграмме). Каждая запись в этой таблице хранит внешний ключ на модель и 
задачу, которая эта модель решает.

Полученные в результате запроса предсказания модели перед отправкой клиенту сохраняются в xml формате в таблице Result.

После получения клиентом ответа от сервиса, он может найти и исправить ошибки, которые допустила модель. Исправленные ошибки также можно отправить на сервис 
в xml формате. Такие акты фидбека хранятся в таблице Response и связаны с конкретными результатами работы какой-то модели.

## Формат входных данных
### Пример входных данных
```
<data project_id='228' task_id='2' option='request'>
  <row column0='rawdata' column1='anotherrawdata' column3='1337.7331'> </row>
  <row column0='dataraw' column1='rawanotherdata' column3='228.822'> </row>
  <row column0='rawdata' column1='anotherdataraw' column3='228.7331'> </row>
  <row column0='rawdata' column1='anorawtherdata' column3='1337.822'> </row>
  ...
</data>
```

На примере выше, атрибуты тега data содержат идентификаторы проекта и задачи, к которым относятся входные данные, а также флаг option, который служит для того, 
чтобы отличать запросы с целью предсказания значений и отправки исправлений ошибок модели. option принимает значения request и response.


Каждый атрибут тега row относится к своему признаку, на котором обучалась модель. Значение этих атрибутов - это значения соответствующего признака в записи. 
В данном примере, датасет состоит из признаков column0, column1 и column3. column0 и column1 - категориальные, а column3 - числовой признак.

### Пример ответа клиента
```
<data project_id='228' task_id='2' option='response' result_id='1337'>
  <row target='cat'> </row>
  <row target='dog'> </row>
  <row target='dog'> </row>
  <row target='cat'> </row>
  ...
</data>
```

На данном примере, у тега data появился еще один атрибут result_id. Это идентификатор записи в таблице Result БД, он служит для ассоциации ответа клиента
с предсказаниями, которые он получил и в которых нашел ошибки.


В таком же виде предсказания модели отправляются клиенту при первом запросе.


## Спецификация моделей

Каждая модель должна быть написана в виде "черного ящика". Такой ящик должен представлять собой сериализованный объект, сохраненный в бинарном виде в файл.
Методы сериализации и десериализации предоставляет библиотека cloudpickle.


### Пример использования cloudpickle:
Выгрузка модели в файл:
```
import cloudpickle as cp

# ...
# ...model training... 
# ...

with open('path/for/model', 'wb') as f:
    cp.dump(model, f)
```


Каждая модель должна содержать в себе метод ```make_prediction(self, X)```, который по входным данным ```X``` строит предсказания в человеко-читаемом формате.
Таким образом, работа с моделью будет производиться только через этот метод: 
```
import cloudpickle as cp

with open('path/for/model', 'rb') as f:
    loaded_model = cp.load(f)
    
# ...
# ...loading input data...
# ...

prediction = loaded_model.make_prediction(X)
print(prediction)
```

### Пример создания модели:
Импорт необходимых библиотек:
```
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import FunctionTransformer
import pandas as pd
```
Модель будет организованна в виде пайплайна. В качестве основы для модели выберем DecisionTreeClassifier
, и напишем последний слой пайплайна, который будет декодировать вывод классификатора в человеко-читаемый формат.

```
# dictionary describing classificator output
code2name = {
    0: 'cat',
    1: 'dog'
}

class DecisionTreeTransformer(DecisionTreeClassifier):
    def fit(self, X, y):
        self.X_columns = list(X.columns)
        self.y_columns = list(y.columns)

        return super().fit(X,y)
    
    def transform(self, X, y=None):
        y_pred = self.predict(X).reshape(-1,1)
        y_df = pd.DataFrame(y_pred, columns=self.y_columns)
        y_dec = y_df.applymap(lambda x: code2name[x])
        
        return pd.concat([X, y_dec], axis=0)
        
    def make_prediction(self, X, y=None):
        res = self.transform(X)
        
        return res[self.y_columns]
```
Опишем сам пайплайн:
```
pipe = Pipeline(
        [
            ('feature selection', FunctionTransformer(lambda df: df[['col1', 'col2', 'col3']])),
            ('classifier', DecisionTreeTransformer())
        ]
    )
    
pipe.fit(X_train, y_train)
pipe.predict(X_test)  # returns just codes
pipe.transform(X_test)  # returns human readable classes and input dataset
pipe.make_prediction(X_test)  # returns classes in desired format 
```
Важно что все промежуточные слои ```sklearn.pipeline.Pipeline``` должны содержать метод ```transform(self, X, y=None)``` 
и поэтому не получится использовать ```DecisionTreeClassifier``` в чистом виде.

