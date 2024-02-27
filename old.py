from collections import Counter as Counter
import re

def see_word_count(df_col,split_delim = "[, ]+"):
  """
  Функция для оценки слов, которые можно выбрать для парсинга. Считает количество вхождений всех слов между делимитерами
  :df_col: - колонка датафрейма
  :split_delim: - по умолчанию '[, ]+' ,делит по 1 или более(если идут подряд) запятой и пробелу. Этот аргумент вставляется как паттерн регулярки для разделения строки
  """
  count_dict = Counter()
  df_col.apply(str).str.lower().apply(lambda row: re.split(f"{split_delim}",row)).apply(count_dict.update)
  return count_dict

def line_print_dict_by_value(some_dict):
  for word,count in sorted(some_dict.items(),key=lambda x : x[1],reverse=True):
    print(f"{word}:{count}")

if __name__ == "__main__":
    print("Колонка с фактической погодой:")
    # fact_weather_word_count = see_word_count(df["weather_fact"],split_delim=",")

    # line_print_dict_by_value(fact_weather_word_count)