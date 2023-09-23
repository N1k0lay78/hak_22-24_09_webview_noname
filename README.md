# hak_22-24_09_webview_noname

    Цифровой прорыв 2023: Сезон ИИ
    Распознавание деталей/узлов на участке
    Общество с ограниченной ответственностью «Управляющая компания Коблик Груп»

Сфера деятельности: Производство машин и оборудования для сельского и лесного хозяйства

Краткое описание кейса: Создание программного модуля видеоаналитики по определению вида детали после её покраски.

Постановка задачи: На основе видеопотока с камеры, с применением технологий искусственного интеллекта, создать программный модуль, который определяет вид покрашенной детали или узла по внешнему виду и известным характеристикам, с заданными требованиями вероятности и точности определения.

Проблематика: В производстве на участок окраски заходят идентифицированные детали и узлы, не окрашенные (с гравировкой или с бирками), на данном этапе можно с легкостью распознать где какая деталь или узел. Затем эти детали и узлы завешиваются на траверсу. Перед покраской бирки снимаются. После покраски гравировки не остается. В результате имеем траверсу неидентифицированных деталей или узлов. При достаточно плотной завеске траверсы деталями и узлами, на их идентификацию тратится очень много времени, что приводит к задержке окрасочного конвейера. Это сказывается на общем времени, затрачиваемом на выпуск окрашиваемой продукции конвейера, и, соответственно, на его эффективность. Требуется распознать деталь после её окрашивания, опираясь на характеристики её 3Д-модели и внешний вид.

Решение: Решение кейса представляет собой прототип системы распознавания окрашенных деталей и узлов при наведении камеры телефона, например. При оценке будет учитываться объективное качество модели, плюс к баллам можно получить, если можно будет также просмотреть характеристики детали/узла.

Стек технологии: Python, JS, Yolo8, matplotlib, torchvision, numpy, pandas, docker, и flask


