<h1>MoTeC visual analysis. Инструкция по запуску</h1>
<h2>Требования: docker, docker-compose, python3.9+, pip, JRE 8 или 11</h2>
<h3>Вариант 1: Docker compose</h3>

1) Запустите скрипт `./install`. Он сформирует `docker-compose.yml` в директорию `dist`, туда же запишет скрипт для инициализации базы данных и соберёт образ для PySpark.

2) `cd dist; docker-compose up`. Поднимутся три контейнера - *compute*, *store* (localhost:8769 для клиентов, 8767 для http) и *visualize* (http://localhost:3317)

3) Из отдельного терминала проинициализировать ClickHouse `./init-database.sh`. **База готова**.

4) Зайти в Grafana http://localhost:3317. Залогиниться как admin admin -> Skip.

5) http://localhost:3317/datasources/new -> ClickHouse -> URL http://store:8123/ -> Save & test. Должно быть сообщиение 'Data source is working'.
   
6) http://localhost:3317/dashboard/import -> Upload JSON -> корень репозитория -> dashboards -> 'Last upload.json'. Повторить для 'Comparison.json'. Визуализация готова.

7) Из корня запустить GUI клиента ./client

8) "Загрузить отрезок" -> example-data -> выбрать CSV файл -> 70 -> 3. Подождать обработку спарка и загрузку в базу (см. в консоль). Нажать "Обновить метаданные".

9) В Grafana открыть дашборд Last upload. Панели должны быть полными данных.

10) Повторите шаг 8 с другим csv из example-data и после нажмите "Создать сравнение". Выбранные галочкой в таблице заезды отобразятся в дашборде Comparison.

11) По завершении работы `docker-compose down` или `Ctlr+C` там, где был `up`.

12) Чтобы удалить их, вызовите `./distclean.sh`.

Note: Поскольку volumes созданы в dist, то на следующий `docker-compose up` данные останутся как в базе, так и в Grafana.

<h3>TODO Вариант 2: Amazon EC2 (in progress)</h3>