# api_yamdb
## О проекте
Проект YaMDb собирает отзывы пользователей на произведения. 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, 
в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», 
а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. 

Список категорий может быть расширен 
(например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

Произведению может быть присвоен жанр из списка предустановленных 
(например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы 
и ставят произведению оценку в диапазоне от одного до десяти (целое число); 
из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).
На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Как развернуть проект


Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:normalisht/api_yamdb.git
```
```bash
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv мenv
```
* Если у вас Linux/macOS
    ```bash
    source env/bin/activate
    ```
* Если у вас windows
    ```bash
    source env/scripts/activate
    ```
```bash
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python3 manage.py migrate
```
Запустить проект:
```bash
python3 manage.py runserver
```

### Импорт данных:
Для загрузки готовых объектов в БД, перейдите в директорию с файлом manage.py и воспользуйтесь этой командой в терминале 
(Имейте в виду, что если в БД уже были какие-то записи, то они будут удалены!)
```bash
cd api_yamdb
python manage.py load_data
```

## Авторы проекта
* https://github.com/Arin0451
* https://github.com/greengoblinalex
* https://github.com/normalisht