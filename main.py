from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import json


# === Приложение и окно ===
app = QApplication([])              # Приложение
win = QWidget()                     # Окно
win.setWindowTitle('Умные заметки')
win.resize(900, 600)

# === Создание виджетов ===
# Для заметок
button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

# Для тегов
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')

# Списки и поля ввода
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
list_tags = QListWidget()
list_notes = QListWidget()
list_tags_label = QLabel('Список тегов')
list_notes_label = QLabel('Список заметок')

# === Расположение по линиям ===
main_line = QHBoxLayout()
main_col = QVBoxLayout()
row_1 = QHBoxLayout()
row_2 = QHBoxLayout()

main_col.addWidget(list_notes_label, alignment=Qt.AlignLeft)
main_col.addWidget(list_notes)

row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
main_col.addLayout(row_1)

main_col.addWidget(button_note_save)
main_col.addWidget(list_tags_label, alignment=Qt.AlignLeft)
main_col.addWidget(list_tags)
main_col.addWidget(field_tag)

row_2.addWidget(button_tag_add)
row_2.addWidget(button_tag_del)
main_col.addLayout(row_2)
main_col.addWidget(button_tag_search)

main_line.addWidget(field_text)
main_line.addLayout(main_col)
win.setLayout(main_line)


# === Функции ===
def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def add_note():
    name, ok = QInputDialog.getText(win, "Добавить заметку", "Введите название заметки:")
    if ok and len(name) > 0:
        notes[name] = {"текст": "", "теги": []}
        list_notes.addItem(name)

def save_note():
    keys = list_notes.selectedItems()
    if len(keys) > 0:
        key = keys[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes.json", "w", encoding="UTF-8") as file:
            json.dump(notes, file)

def delete_note():
    keys = list_notes.selectedItems()
    if len(keys) > 0:
        key = keys[0].text()
        notes.pop(key)
        list_notes.clear()
        list_notes.addItems(notes)
        list_tags.clear()
        field_text.clear()
        with open("notes.json", "w", encoding="UTF-8") as file:
            json.dump(notes, file)

def add_tag():
    keys = list_notes.selectedItems()
    if len(keys) > 0:
        key = keys[0].text()
        tag_text = field_tag.text() # Получить текст из QLineEdit с помощью метода text()
        list_tags.addItem(tag_text) # Добавить тег в список тегов (QListWidget)
        notes[key]["теги"].append(tag_text) # Добавить тег в список тегов (в словарь notes)
        field_tag.clear()           # Очистить QLineEdit с помощью метода clear()

        # Сохранить заметки
        with open("notes.json", "w", encoding="UTF-8") as file:
            json.dump(notes, file)

# Подключение к виджетам
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(delete_note)
button_tag_add.clicked.connect(add_tag)

# === Чтение заметок из файла ===
with open("notes.json", "r", encoding="UTF-8") as file:
    notes = json.load(file)
list_notes.addItems(notes)

# === Запуск приложения ===
win.show()
app.exec()
