<h1>MoTeC visual analysis. Инструкция по запуску</h1>
<h2>Требования: docker, docker-compose, python3.9+, pip</h2>
<h3>Вариант 0: Luckyone - если очень лень и хочется испытаться удачу</h3>

Запустите скрипт `luckyone.sh`. Если система соответствует требованиям, то по окончании его работы будет вывдено `DONE!`. Далее `cd dist; docker-compose up` и можно приступать к шагам 4-9 из **варианта 1**.

<h3>Вариант 1: Docker compose</h3>

1) Запустите скрипт `./install`. Он сформирует `docker-compose.yml` и прочие необходимости в директорию `dist` и вызовет `docker-compose build`. После этого мы получим готовую инфраструктуру с инициализированной пустой базой.

    *Note*: на случай особой необходимости пользоваться сторонними клиентами к ClickHouse или Grafana, переназначенные порты можете посмотреть в `docker-compose.yml_template`

2) `cd dist; docker-compose up`. Поднимутся три контейнера - *compute*, *store* и [*visualize*](http://localhost:3317)

3) В корне запустите `./initgrafana`. Через REST API он подключит ClickHouse и добавит визуализацию из `dashboards`.

4) Из корня запустить GUI клиента `./client`

5) "Загрузить отрезок" -> example-data -> выбрать CSV файл -> 70 -> 3. Подождать обработку спарка и загрузку в базу (см. в консоль). Нажать "Обновить метаданные".

6) В [Grafana](http://localhost:3317/dashboards) открыть дашборд Last upload. Панели должны быть полными данных.

7) Повторите шаг 5 с другим csv из example-data и после нажмите "Создать сравнение". Выбранные галочкой в таблице заезды отобразятся в дашборде Comparison.

8) По завершении работы `docker-compose down` или `Ctlr+C` там, где был `up`.

    *Note*: Поскольку volumes созданы в dist, то на следующий `docker-compose up` данные останутся как в базе, так и в Grafana.

9) Чтобы удалить созданные контейнеры (вместе с данными в них), вызовите `./distclean.sh`.

<h3>TODO Вариант 2: Amazon EC2 (in progress)</h3>

<h3>Возможные ошибки</h3>

1) Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?

Докер демон не поднят. На Linux с systemd вы можете попробовать его запустить командой `systemctl start docker`

2) Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/_ping": dial unix /var/run/docker.sock: connect: permission denied

https://docs.docker.com/engine/install/linux-postinstall/ - шаги 1-3 + перелогиниться