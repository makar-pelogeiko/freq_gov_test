# Комплекс утилит для поизведения тестирования различных DVFS регуляторов OS Android на предмет энергопотребления процессора

Технологии:
- Python 3.10+
- Android debug bridge

## Работа с проектом

### Скачивание и установка
```shell
git clone ...
cd ...
pip install -r requirements.txt
```

### Конфигурация
Конфигурационные константы расположены в файле `config.py`.

### Запуск проекта

```shell
python "utilname"
```

Например:
```shell
python conduct_all_test_govs.py
```

### Назначение утилит

#### ChangeFrequeGovernor (`change_freq_governor.py`)
Утилита меняющяя для всех ядер текущий DVFS-регулятор на переданный как аргумент. Конфигурируется параметрами из `config.py`.

Пример вызова:
```shell
python change_freq_governor.py <governor_name>
```
Аргументы:
 - governor_name - название регулятора
 
####  FrequeGovernorTest (`freq_gov_test.py`)
Утилита исполняющаяя заранее сконфигурированный набор тестов для текущего регулятора. Конфигурируется параметрами из `config.py`.

Пример вызова:
```shell
python freq_gov_test.py
```

#### PlotResults (`plot_results.py`)
Утилита выполняющая построение графиков по собранным в ходе тестирования данным. Конфигурируется параметрами из `config.py`.

Пример вызова:
```shell
python plot_results.py
```

####  TestGovernors (`test_govs.py`)
Утилита, выполняющяя тестирование выбранных регуляторов. Конфигурируется параметрами из `config.py`.

Пример вызова:
```shell
python test_govs.py
```

### Внесение изменений в проект

### Структура репозитория

```text
.
├── 
├── 
├── 
├── 
└── 
```

### Контакты

Макар Андреевич Пелогейка