#include <iostream>//подключили библиотеку
using namespace std;//стандартное пространство имен
//обозначили структуру двузначный циклич список
struct Node {//новая структура данных
    int value;//поле для хранение целого числа
    Node* next;//объяв указатель на след
    Node* prev;//указатель на предыдущ
};
//добавление элемента в конец
void pushBack(Node*& head, int val) {//объяв ф-ии которая не возвращает значение воид
    Node* newNode = new Node;//память для нового элемента
    newNode->value = val;//значение вал записывает в валуе
    newNode->next = newNode; // Замыкаем на себя
    newNode->prev = newNode;
    if (head == nullptr) {//проверка пустой ли список
        head = newNode;//у заголовка новый адрес элемента
        return;
    }
    //вставка к конец списка
    newNode->next = head;//новый элемент ссылается на первый
    newNode->prev = head->prev;//head->prev хранитадрес последнего элемента
    head->prev->next = newNode;//бывш последний теперь на новый как на следующий
    head->prev = newNode;//новый элемент последний 
}
//ввод с клавиатуры
void inputList(Node*& head, const string& listName) {//объявление ф-ии ввода
    int count;//переменная для хранения кол-ва элементов
    cout << "\n        List"<< listName <<"    \n";//заголовок секции ввода
    cout << "the number of numbers in the list? ";
    cin >> count;//считывание числа с клав в переменную count
    if (count <= 0) {//проверка на отрицательные числа
        cout << "list " << listName << " it will remain empty\n";
        return;
    }
    cout << "Enter " << count << " numbers separated by a space:\n";
    for (int i = 0; i < count; i++) 
    {                                 //запускаем цикл столько сколько count
        int val;//переменная для текущ числа
        cin >> val;//одно число с клав
        pushBack(head, val); //вызывает ф-ию добавления элемента в конец списка
    }
    cout << "List" << listName << " filled in \n";
}
//проверка наличия значения в списке
bool exists(Node* head, int val) {//объяв ф-ию возвращенную положит или отриц
    if (head == nullptr) return false;//если пустой список то сразу возвращает
    Node* p = head;//создание нового рабочего указателя и поставили его на голову
    do {
        if (p->value == val) return true;//сравнение текщ с искомым элементом
        p = p->next;//перемещает на следующий элемент
    } while (p != head);//проверка на возвращение к началу
    return false;
}
//разные числа списков (симметрическая разность)
Node* intersection(Node* list1, Node* list2) {//ф-ия возвращающая указатель на новый список
    Node* result = nullptr;//создание пустого заголовка для результ
    //если оба пустые то результат пустой
    if (list1 == nullptr && list2 == nullptr) return nullptr;
    
    //Проходим по первому списку: добавляем те, которых нет во втором
    if (list1 != nullptr) {
        Node* p1 = list1;//указатель для обхода первого списка
        do {
            int val = p1->value;//запомнили значение текущего элемента
            //если нет во втором и нет в результ
            if (!exists(list2, val) && !exists(result, val)) {//проверка двух условий: нет ли числа во втором списке? и нету ли его в результате?
                pushBack(result, val);//если все верно то добавляем
            }
            p1 = p1->next;//следующий элемент первого списка
        } while (p1 != list1);//повторяем пока не вернемся к началу
    }
    
    //Проходим по второму списку: добавляем те, которых нет в первом
    if (list2 != nullptr) {
        Node* p2 = list2;//указатель для обхода второго списка
        do {
            int val = p2->value;//запомнили значение текущего элемента
            //если нет в первом и нет в результ
            if (!exists(list1, val) && !exists(result, val)) {//проверка двух условий: нет ли числа в первом списке? и нету ли его в результате?
                pushBack(result, val);//если все верно то добавляем
            }
            p2 = p2->next;//следующий элемент второго списка
        } while (p2 != list2);//повторяем пока не вернемся к началу
    }
    
    return result;
}
//вывод списка
void printList(Node* head, const string& name) {//ф-ия вывода
    cout << name << ": ";//выводит список 
    if (head == nullptr) {//проверка на пустоту
        cout << "[ Empty]";//если пусто 
    } else {
        cout << "(";
        Node* p = head;//рабочий указатель для обхода
        do {
            cout << p->value << " ";//значения текущ элемента
            p = p->next;//переход к следующему
        } while (p != head);//пока не дойдем до начала
        cout << ")";
    }
    cout << endl;
}
//очистка памяти
void clearList(Node*& head) {//ф-ия удаление всех элементов
    if (head == nullptr) return;//если пуст то нечего
    Node* p = head;//начало с головы
    do {
        Node* temp = p;//сохранение адреса текущ элемента
        p = p->next;//переход к следующ до удаления
        delete temp;//освобождение памяти занятую элементом
    } while (p != head);//пока не дошли до головы
    head = nullptr;//обнуление заголовка
}
int main() {//вход в программу
    setlocale(LC_ALL, "Russian"); //для русского языка
    //объявление заголовка
    Node* listA = nullptr;
    Node* listB = nullptr;
    //пользователь вводит данные о списках
    inputList(listA, "No. 1");
    inputList(listB, "No. 2");
    //вывод изначальных списков 
    cout << "\n    INFORMATION ABOUT THE LISTS   \n";
    //показывает что было введено ранее
    printList(listA, "List No. 1");
    printList(listB, "List No. 2");
    Node* listResult = intersection(listA, listB);//вычислили разные числа между списками
    //вывели результат
    cout << "\n      result      \n";
    printList(listResult, "Different elements of list No. 1 and No. 2");
    // Очистка памяти
    clearList(listA);
    clearList(listB);
    clearList(listResult);
    cout << "\nThe memory is cleared, the program is completed\n";
    return 0;
}
