Title: Бесконечная загрузка сессии в GTA 5 Online
Date: 2020-07-22 21:00:00 +0500
Tags: Games
Summary: Всем играющим в GTA 5 Online известны проблемы с бесконечной загрузкой при смене сессии. Здесь описывается утилита, в некоторой мере их решающая.

Всем играющим в GTA 5 Online известны следующие проблемы:

  * Иногда нужна сессия без мешающих игроков, но с доступом к миссиям;
  * При выходе из миссии или при смене сессии по любой иной причине, сессия может грузиться бесконечно;
  * На сессии буянит очередной читер, заблокировав возможность вызова меню M (для переключения в пассивный режим) и Паузы (для смены сессии);
  * Rockstar ничего исправлять не желает.

Среди распространённых, более-менее работающих решений есть два:

  * Постановка процесса игры на паузу, секунд на 10.<br>
    Это приводит к отмене подключения к выбранной для вас игрой сессии и создании новой сессии с одним игроком.
    Требуется не стандартный Диспетер задач, предоставляющий возможность приостанавливать процессы.<br>
    Например, идущий в комплекте с Windows _resmon.exe_. Однако он запускается довольно-таки не быстро, а затем надо ещё нужный процесс найти в списке.
  * Отключение сетевого соединения.<br>
    Обычно выполняемое выдёргиванием кабеля Ethernet, но также можно запустить _ncpa.cpl_ и отключить сетевой адаптер через контекстное меню.<br>
    Это приводит к выбросу из сетевого в сюжетный режим.<br>
    Однако, при частом выдёргивании Ethernet кабеля, можно повредить коннекторы RJ-45. Что в свою очередь может привести к нестабильной работе сети.

Чтобы держать оба средства под рукой, написана программа, представленная [здесь](https://pauser.riuson.com/).

Функциональность представлена в интерфейсе тремя вкладками:

  * Network Adapters<br>
    Позволяет отключать и включать выбранные сетевые адаптеры одним нажатием кнопки.
    <span class="bg-warning .text-dark">Для управления сетевыми адаптерами программе требуются права администратора.</span>
  * Processes<br>
    Позволяет выбрать процессы, у которых в имени есть указанные строки, и остановить/продолжить их.
  * Batch<br>
    Здесь можно составить последовательность операций и запустить их на выполнение одной кнопкой. Список доступных операций следующий:
    * Приоставить подходищие под фильтр процессы;
    * Продолжить процессы;
    * Отключить выбранные сетевые адаптеры;
    * Включить сетевые адаптеры обратно;
    * Подождать указанное время (значение вводится в миллисекундах).

[<i class="fab fa-youtube"></i> Видеодемонстрация](https://www.youtube.com/watch?v=7AmPYQu1YdM)

![Adapters]({static}/images/posts/2020/07/20/adapters.png){ .img-fluid }
![Processes]({static}/images/posts/2020/07/20/processes.png){ .img-fluid }
![Batch]({static}/images/posts/2020/07/20/batch.png){ .img-fluid }
