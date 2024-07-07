
# Сравниваем вакансии программистов

В данном проекте реализован сбор данных вакансий с помощью API [hh.ru](https://api.hh.ru/) и [superjob.ru](https://api.superjob.ru/)

Данные собираются для города Москва по 10 языкам программирования:  

 * JavaScript
 * TypeScript
 * Swift
 * Go
 * C++
 * C#
 * PHP
 * Ruby
 * Python
 * Java

### Как установить

Python3 должен быть установлен. 
Используйте `pip` для установки зависимостей:
```
pip install -r requirements.txt
```

Также, для взаимодействия с API [superjob.ru](https://api.superjob.ru/) необходим ключ приложения. Получить ключ можно, ознакомившись с первым абзацем в Getting Started [в данной инструкции](https://api.superjob.ru/)

После получения ключа необходимо создать в корневой папке проекта файл .env и добавить значение 

`SUPERJOB_API_KEY = 'Ваш ключ'`

Пример ключа:

`v3.r.133468321.84f2909f015gr4t47654ad7e5edd18190700b3d9.456i7r12za1vqfeg8da83f4eag212342567093e1`

Запустить скрипт можно выполнив команду

`python3 main.py`

### Пример вывода скрипта

![image](https://github.com/e13q/WA_lesson5/assets/110967581/cb7eed73-c321-46e5-8378-7a1b80c19ce6)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
