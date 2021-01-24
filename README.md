# Новостная лента по акциям, выходящим на СПБ бирже

## Основная идея. 

Ввиду того, что США и Россия находятся в разных часовых поясах, часы работы Американских и Российских фондовых бирж 
отличаются. Так, если Американские фондовые биржи (NASDAQ, NYSE) открываются в 17-30 по Московскому времени, то 
Российские фондовые биржи (MOEX, SPBEX) открываются в 9-30. Иногда выходит так, что новости по американским компаниям, 
которые могут повлиять на котировки, выходят вне времени работы Американских бирж. Однако Российские биржи могут быть 
уже открыты. Потенциально, отслеживая важные новости, и входя в позиции этих компаний на Российских биржах, можно 
успеть на Американском пре-маркете получить прибыль.

## Описание приложения.

Приложение состоит из сайта на [Flask](https://flask.palletsprojects.com/en/1.1.x/) парсит новости с 
[новостной ленты](https://i.ibb.co/jZK4Jwn/menu.png) и телеграм-бота. 

**Сайт** имеет три вкладки:

![menu_with_news](https://i.postimg.cc/yd9sv3rZ/manu-with-news.png 'menu-image')

1. Все новости
2. Новости по акциям, торующимися на СПБ бирже
3. Тикеры всех акций, торгующихся на СПБ бирже

![tickers](https://i.postimg.cc/sXzNCBgS/tickers.png 'tickers-image')

Новости парсятся автоматически по заданному интервалу. Со второй и третьей вкладки можно перейти на отдельную страницу 
по каждой акции. На странице отображается:

1. График цены за 3 года
   <br/><br/>
   <img src="https://i.postimg.cc/GhTJzLc1/price-chart.png" width="800">
   <br/><br/>
   
2. Диаграмма перспективности компаний (за основу расчета взят алгоритм построения подобной диаграммы в приложении 
   [Simply Wall Street](https://simplywall.st/))
   <br /><br/>
   <img src="https://i.postimg.cc/RC6Ph5Wq/perspective-diagram.png" width="800">
   <br/><br/>

3. Описание расчета диаграммы со всеми коэффициентами
   <br/><br/>
   <img src="https://i.postimg.cc/h4L2T80q/perspective-checks.png" width="800">
   <br/><br/>

4. Рейтинг аналитиков
   <br/><br/>
   <img src="https://i.postimg.cc/X7v9q9HL/analysts.png" width="800">
   <br/><br/>

В footer есть ссылка на бот рассылки.
<br/><br/>

**Бот** позволяет пользователю подписаться на рассылку. Если пользователь подписан, ему приходят новости по компаниям, 
торгующимся на СПб бирже. Также через бот он может посмотреть рейтинг аналитиков, диаграмму перспективности и график 
цены.
   <br/><br/>
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://i.postimg.cc/3NqNd0Nf/bot.png" width="800">

## Установка

Скачайте проект с github.

```
git clone https://github.com/balancy/ProjectStocksNews.git
```

Создайте виртуальное окружение и установите зависимости:

```
pip install -r requirements.txt
```

Переименуйте файл `example.config.py` в `config.py`. Присвойте значения константам:
```
BOT_API_KEY - API ключ Вашего телеграм бота
BOT_API_LINK - Ссылка на Ваш бот
FINANCIAL_API_KEY - Ваш ключ на сайте FINANCIAL_BASE_URL
HOST_NAME - Имя Вашего хостинга
```

## Запуск программы

Для старта web-приложения запустите `flask app`. Для старта бота запустите `reading_bot.py`.