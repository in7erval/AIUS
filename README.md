# Репозиторий для работ по АИУС (7 семестр)

<p align="left">
<img src="https://raster.shields.io/github/last-commit/in7erval/AIUS">
<img src="https://raster.shields.io/badge/made_by-in7erval-blue">
<img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg">
<img src="https://raster.shields.io/github/repo-size/in7erval/AIUS">
<a href="https://sonarcloud.io/dashboard?id=in7erval_AIUS"><img src="https://sonarcloud.io/api/project_badges/measure?project=in7erval_AIUS&metric=ncloc"></a>
<a href="https://sonarcloud.io/dashboard?id=in7erval_AIUS"><img src="https://sonarcloud.io/api/project_badges/measure?project=in7erval_AIUS&metric=reliability_rating"></a>
<a href="https://sonarcloud.io/dashboard?id=in7erval_AIUS"><img src="https://sonarcloud.io/api/project_badges/measure?project=in7erval_AIUS&metric=sqale_rating"></a>
</p>
                                                                              
**Посмотрел? Поставь :star: репозиторию `and use your brain, dude`!**
                                                                              
## Список работ:
1. [Игра "Змейка"](#1-игра-змейка)
2. [В ожидании...](#2-в-ожидании)

## 1. [Игра "Змейка"](https://github.com/in7erval/AIUS/tree/master/Snake). 
### Консольный режим. 
  * WASD/стрелки - управление головой змейки
  * Q - выход из игры в любой момент
  * R - сброс игры в любой момент

  **Usage:**
  >  * ```python main.py --cli``` 
  >
  >  или 
  >
  >  * ```python main.py --cli -S SIZE```, где SIZE - размер поля (по умолчанию равен 10)

<img src="https://github.com/in7erval/AIUS/blob/master/Snake/assets/console.gif" width="700" height="500"/>

### Графический режим.
  * WASD/стрелки - управление головой змейки
  * Q - выход из игры в любой момент
  * R - сброс игры в любой момент
  * Z - включение анимации цвета хвоста змейки
  * X - смена цвета фона
  * E - включение/отлючение показа команд
  * T - ускорение передвижения змейки
  * G - замедление передвижения змейки
  * F - включение/отключение режима одиночного нажатия *(змейка будет двигаться не постоянно, а по нажатию на клавиши)*
  * 1-5 - смена цветовой палитры хвоста змейки

**Usage:**
>
>  Для начала установить библиотеку *Pygame*:
>
>  * ```pip install pygame``` 
>  
>  После этого можно использовать команду
>  
>  * ```python main.py --gui``` 
>  
>  или
>  
>  * ```python main.py --gui -S SIZE -B BLOCKSIZE```, где BLOCKSIZE - размер одной клетки в пикселях (по умолчанию равен 50)

<img src="https://github.com/in7erval/AIUS/blob/develop/Snake/assets/graphical.gif" width="500" height="500"/>

### P.S.
1. Все команды выполняются из директории Snake
2. 🤫 Тсссс, говорят, если запустить игру с флагом ```-С```, будет активирован чит!!1!1!!!
3. Если после прочтения инструкции всё равно ничего не понял, используй
   * ```python main.py --help``` :+1:

[Назад к списку работ :arrow_up:](#список-работ)
## 2. В ожидании....

[Назад к списку работ :arrow_up:](#список-работ)
