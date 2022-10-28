# Test Task

*Скачанные результаты пробинга (два зип-файла с https://huggingface.co/datasets/bigscience/massive-probing-results/tree/main) я загрузила в папку data и поместила в один фолдер с файлом test_dashboard.py

Я построила дашборд из четырёх графиков:

* graph.1: отражает средние значения test-score каждой категории по всем слоям и языкам (например, есть категория Number, все text-score во всех слоях и языках, в которых она встречается, были сложены и поделены на количество вхождений) (по F1). По этому графику можно понять, какие категории даются модели хуже и лучше всего.
* graph.2: отражает средние значения всех слоев в целом для двух метрик. Поскольку разницы в значениях практически нет, все представленные графики были построены по F1, поскольку графики, построенные по accuracy, повторяли бы информацию.
* graph.3: отражает средние значения test-score по каждому языку (например, есть Английский язык, все его test-score всех слоев и всех категорий были сложены и поделены на количество вхождений) (по F1). По этому графику можно понять, какие языки даются модели хуже и лучше всего.
* graph.4: отражает средние значения test-score по каждому языку и для каждого слоя (например, есть Испанский язык, все его test-score в определенном слое для каждой категории были сложены и поделены на количество вхождений) (по F1). Так как слоев достаточно много, то для удобства лучше воспользоваться Zoom In и двигаться по осям. Можно выбрать две категории: Number и Mood (нормально и очень хорошо распознаваемые моделью категории, согласно graph.1; с такими параметрами две тепловые карты получаются совсем непохожими, что важнее для анализа, поэтому взяты такие параметры. Если брать категории с совсем низким F1, есть вероятность, что языков с такой категорией мало, по этой причине я, например, не брала NounClass, так как он представлен одним языком, тепловая карта пустая).

Поскольку объемы данных огромные, я воспользовалась модулем multiprocessing для python, который делает возможным одновременный запуск нескольких процессов, это ускорило работу моего кода. Также можно поискать более разумный способ, чтобы пробегаться по файлам, у меня в коде пока алгоритм проходится по файлам фолдера и применяет json.uploads(). 

Я пользовалась mathplotlibs, plotly, seaborn для визуализации данных. В прошлом году занималась проектом, который был посвящен Flask (https://github.com/AbinaKukanova/Organize-ur-life/blob/main/README.md). Использовала JS для активации темной/светлой темы веб-приложения, запуска таймера, на Питоне строила графики на основе информации из Базы данных.
