# -*- coding: windows-1251 -*-
import tkinter as tk
import re
import csv
import random
from bisect import bisect_left, bisect_right
import itertools
from pathlib import Path


class Anagrams:

    def __init__(self, dict):
        self.dict = dict
        self.col1 = []
        self.col2 = []
        self.len_dict = 0

        reader = csv.reader(self.dict)
        for row in reader:
            row = row[0].split(';')
            self.col1.append(row[0])
            self.col2.append(''.join(sorted(row[0])))
            self.len_dict += 1
        self.sort_dictionary()

        self.anagrams_col1 = []
        self.anagrams_col2 = []
        self.len_anagrams_dict = 0
        self.build_anagram_list()

        self.set_words = set(self.col1)

    def build_anagram_list(self):
        self.anagrams_col1 = []
        self.anagrams_col2 = []
        self.len_anagrams_dict = 0
        el = 0
        while el != self.len_dict:
            left = bisect_left(self.col2, self.col2[el])
            right = bisect_right(self.col2, self.col2[el])
            if right - left > 1:
                for i in range(left, right):
                    self.anagrams_col1.append(self.col1[i])
                    self.anagrams_col2.append(self.col2[i])
                    self.len_anagrams_dict += 1
            el = right


    def sort_dictionary(self):
        combined = list(zip(self.col2, self.col1))
        combined.sort(key=lambda x: x[0])
        self.col2, self.col1 = zip(*combined)
        self.col2 = list(self.col2)
        self.col1 = list(self.col1)


    def get_anagrams(self,word):
        word = word.strip().lower()
        if word in self.set_words:
            sorted_word = ''.join(sorted(word))
            list_of_anagrams = [word]
            left = bisect_left(self.anagrams_col2,sorted_word)
            right = bisect_right(self.anagrams_col2,sorted_word)
            for el in range(left,right):
                if self.anagrams_col1[el] != word:
                    list_of_anagrams.append(self.anagrams_col1[el])
            return list_of_anagrams
        else: return []


    def random_anagram_group(self):
        randind = random.randint(0,self.len_anagrams_dict-1)
        word = self.anagrams_col1[randind]
        anagrams = [word]
        sorted_word = self.anagrams_col2[randind]

        left = bisect_left(self.anagrams_col2, sorted_word)
        right = bisect_right(self.anagrams_col2, sorted_word)
        for i in range(left,right):
            if self.anagrams_col1[i] != word:
                anagrams.append(self.anagrams_col1[i])
        return anagrams

    def add_word(self,word):
        word = word.strip().lower()
        if word not in self.set_words:
            srtd_word = ''.join(sorted(word))
            i = bisect_left(self.col2,srtd_word)
            self.col1.insert(i,word)
            self.col2.insert(i,srtd_word)
            self.build_anagram_list()
            self.len_dict += 1
            self.set_words.add(word)
            return True
        else: return False

    def add_words_from_file(self, file):
        with open(file, 'r') as f:
            for word in f:
                word = word.strip().lower()
                if word not in self.set_words:
                    self.col1.append(word)
                    self.col2.append(''.join(sorted(word)))
                    self.len_dict += 1
        self.set_words = set(self.col1)
        self.sort_dictionary()
        self.build_anagram_list()


    def get_number_anagrams(self, number):
        s = str(number).strip()
        if s.startswith('-'):
            return []
        if not s.isdigit():
            return []
        digits = list(s)
        original = s
        uniq = set()
        for p in itertools.permutations(digits):
            uniq.add(''.join(p))

        res = [original]
        for x in sorted(uniq):
            if x != original:
                res.append(x)
        return res

    def random_number_anagram_group(self, length):
        length = int(length)
        if length <= 0:
            return []

        num = random.randint(int('1'+'0'*(length-1)),int('9'*length))

        return self.get_number_anagrams(num)


def letters_only(word):
    return bool(re.fullmatch(r"[А-Яа-яЁё]+", word))

def btn_find_anagrams():
    word = entry_find_out.get().strip().lower()
    anagrams_listbox.delete(0, tk.END)
    if not word:
        label_anagrams.config(text="Введите слово перед добавлением")
        return
    if word.isdigit():
        label_anagrams.config(text=f"Список анаграмм для последовательности цифр '{word}':")
        list_of_anagrams = main.get_number_anagrams(word)
        if 1<len(list_of_anagrams)<10:
            for el in list_of_anagrams:
                anagrams_listbox.insert(tk.END, el)
        elif len(list_of_anagrams)>9:
            label_anagrams.config(text=f"Длина последовательности цифр {word} слишком велика")
        else:
            label_anagrams.config(text=f"У последовательности цифр {word} нет анаграмм")
    else:
        label_anagrams.config(text=f"Список анаграмм для слова '{word}':")
        list_of_anagrams = main.get_anagrams(word)
        if len(list_of_anagrams) >1:
            for el in list_of_anagrams[1:]:
                anagrams_listbox.insert(tk.END, el)
        elif len(list_of_anagrams) == 1:
            label_anagrams.config(text=f"У слова '{word}' нет анаграмм")
        else:
            label_anagrams.config(text=f"В словаре нет слова '{word}'. Вы можете добавить его")
    entry_find_out.delete(0, tk.END)

def btn_generate():
    anagrams_listbox.delete(0, tk.END)
    label_anagrams.config(text=f"Случайная группа анаграмм:")
    random_list_of_anagrams = main.random_anagram_group()
    for el in random_list_of_anagrams:
        anagrams_listbox.insert(tk.END, el)

def btn_num_generate():
    anagrams_listbox.delete(0, tk.END)
    label_anagrams.config(text=f"Случайная группа анаграмм:")
    length = entry_length.get()
    if not(2<=int(length)<=9): label_anagrams.config(text=f"Длина не может быть меньше 2 или больше 9")
    else:
        random_list_of_anagrams = []
        while len(random_list_of_anagrams)<2:
            random_list_of_anagrams = main.random_number_anagram_group(length)
        for el in random_list_of_anagrams:
            anagrams_listbox.insert(tk.END, el)

def btn_add():
    word = entry_add.get()
    if not word:
        label_add.config(text="Введите слово перед добавлением")
        return
    if ".txt" in word :
        word = ''.join(i for i in word if i != '"' and i != "'")
        try:
            added = main.add_words_from_file(word)
            label_add.config(text="Слова из файла успешно загружены")
        except:
            label_add.config(text="Возникла ошибка с открытием файла")

    else:
        word = word.strip().lower()
        if not letters_only(word):
            label_add.config(text="Некорректный тип данных")
        else:
            added = main.add_word(word)
            if added:
                label_add.config(text="Слово успешно добавлено")
            else:
                label_add.config(text="Слово уже есть в словаре")
    entry_add.delete(0, tk.END)
    screen.after(3000, lambda: label_add.config(text="Введите слово,\n либо абсолютный путь до текстового файла со списком слов,\n которые нужно добавить в словарь:"))

if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR / "data" / "nouns_dict1.csv"
    with csv_path.open() as f:
        main = Anagrams(f)


    screen = tk.Tk()
    screen.title("Анаграммы")
    screen.geometry("600x600")

    #Левая колонка/Поиск
    label_find_out = tk.Label(screen, text="Введите слово или последовательность цифр, анаграммы которых хотите узнать:")
    label_find_out.place(x=20, y=20)

    entry_find_out = tk.Entry(screen, width=30)
    entry_find_out.place(x=20, y=50)

    find_out_btn = tk.Button(screen,text="Отправить",command=btn_find_anagrams)
    find_out_btn.place(x=200, y=47)

    #Левая колонка/Список
    label_anagrams = tk.Label(screen, text="Список анаграм для слова или последовательности цифр ...:")
    label_anagrams.place(x=20, y=80)

    anagrams_listbox = tk.Listbox(screen, width=30, height=9)
    anagrams_listbox.place(x=20, y=100)

    #Левая колонка/Рандомайзер
    generator_btn = tk.Button(screen,text="Сгенерировать анаграммы слов",command=btn_generate)
    generator_btn.place(x=20, y=250)

    generator_num_btn = tk.Button(screen,text="Сгенерировать анаграммы последовательностей цифр длинной:",command=btn_num_generate)
    generator_num_btn.place(x=20, y=275)

    entry_length = tk.Entry(screen, width=10)
    entry_length.place(x=393, y=277)

    #Левая колонка/Добавление
    label_add = tk.Label(screen, text="Введите слово,\nлибо абсолютный путь до текстового файла со списком слов,\nкоторые нужно добавить в словарь:", justify="left",anchor="w")
    label_add.place(x=20, y=310)

    entry_add = tk.Entry(screen, width=30)
    entry_add.place(x=20, y=370)

    add_btn = tk.Button(screen,text="Добавить",command=btn_add)
    add_btn.place(x=200, y=367)


    screen.mainloop()