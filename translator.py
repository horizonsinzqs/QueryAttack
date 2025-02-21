from nltk.tokenize import word_tokenize
import os
import argparse
import csv
from trans_llms import trans_sentence_llms
from split_sentence_llms import split_sentence_llms as split_sentence_using_llms
from all_template import C_plusplus_template, C_template, C_sharp_template, Python_template, Go_template, SQL_template, Java_template, JavaScript_template, URL_template

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='path to original csv file', default='data/harmful_behaviors.csv')
    parser.add_argument('--store_path', type=str, help='path to store translated csv file', default='data')
    parser.add_argument('--target_language', type=str, help='target language,like C++, C, C#, Python, Go, SQL, Java, JavaScript, URL', default='ALL')
    parser.add_argument('--trans_verify', type=bool, help='use llms to verify each translation or not', default=False)
    # Append a mark to the end of the filename when saving
    args = parser.parse_args()

    if args.target_language not in ['C++', 'C', 'C#', 'Python', 'Go', 'SQL', 'Java', 'JavaScript', 'URL', 'ALL']:
        print(f"Unsupported target language: {args.target_language}")
        # Exit the program
        exit(1)
    return args

def load_data(args):
    # Read the csv file from the path, with each line being a sentence
    try:
        with open(args.path, 'r', encoding='utf-8') as file:
            # Use list comprehension to read each line and remove the newline character at the end of each line
            data = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {args.path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    return data

def process_words(words, args):
    args = parse_args()
    # Reassemble words into a sentence
    sentence = ' '.join(words)
    # Process using llms
    Content, Modifier, Category = trans_sentence_llms(sentence, args)

    return Content, Modifier, Category

def sentence_split(sentence):
    args = parse_args()
    split_sentence = split_sentence_using_llms(sentence)
    return split_sentence

def translate(data, args):
    phrases_data = []  # Used to store extracted phrases

    for sentence_index, sentence in enumerate(data):
        words = word_tokenize(sentence)
        if len(words) > 13:
            split_sentences = sentence_split(sentence)
            for split_sentence in split_sentences:
                words = word_tokenize(split_sentence)
                Content, Modifier, Category = process_words(words, args)

                phrases_data.append({
                    'sentence_index': sentence_index,
                    'Content': Content,
                    'Modifier': Modifier,
                    'Category': Category
                })
            continue
        else:
            Content, Modifier, Category = process_words(words, args)

            phrases_data.append({
                'sentence_index': sentence_index,
                'Content': Content,
                'Modifier': Modifier,
                'Category': Category
            })
    return phrases_data

def store_data(target_data, args):
    if not os.path.exists(f'{args.store_path}/llms'):
        os.makedirs(f'{args.store_path}/llms')

    # Store the translated data in a csv file, with each sentence in target_data occupying one line in the csv file
    if args.target_language in ['C++', 'C', 'C#', 'Python', 'Go', 'SQL', 'Java', 'JavaScript', 'URL']:
        with open(f'{args.store_path}/llms/{args.target_language}_translated.csv', 'w', encoding='utf-8') as file:
            for sentence in target_data:
                file.write(sentence + '\n----\n')
    else:
        print(f"Unsupported target language: {args.target_language}")


def store_phrases(phrases_data, args):
    if not os.path.exists(f'{args.store_path}/llms'):
        os.makedirs(f'{args.store_path}/llms')

    with open(f'{args.store_path}/llms/phrases.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file,
                                fieldnames=['sentence_index', 'Content', 'Modifier', 'Category'])
        writer.writeheader()
        for phrase in phrases_data:
            writer.writerow(phrase)

def load_phrases(args):
    with open(f'{args.store_path}/llms/phrases.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        phrases_data = [row for row in reader]
    return phrases_data

def assemble_code(phrases_data, args):
    target_language = args.target_language
    target_data = []
    sentence_groups = {}

    # Group by sentence_index
    for phrase in phrases_data:
        sentence_index = int(phrase['sentence_index'])
        if sentence_index not in sentence_groups:
            sentence_groups[sentence_index] = []
        sentence_groups[sentence_index].append(phrase)

    if target_language == 'ALL':
        target_data_C_plusplus = []
        target_data_C = []
        target_data_C_sharp = []
        target_data_Python = []
        target_data_Go = []
        target_data_SQL = []
        target_data_Java = []
        target_data_JavaScript = []
        target_data_URL = []
        for sentence_index, phrases in sentence_groups.items():
            target_sentence_C_plusplus = ''
            target_sentence_C = ''
            target_sentence_C_sharp = ''
            target_sentence_Python = ''
            target_sentence_Go = ''
            target_sentence_SQL = ''
            target_sentence_Java = ''
            target_sentence_JavaScript = ''
            target_sentence_URL = ''
            for phrase in phrases:
                Content = phrase['Content']
                Category = phrase['Category']
                Modifier = phrase['Modifier']
                target_sentence_C_plusplus += C_plusplus_template.format(Category=Category, Content=Content, Modifier=Modifier)
                target_sentence_C += C_template.format(Category=Category, Content=Content, Modifier=Modifier)
                target_sentence_C_sharp += C_sharp_template.format(Category=Category, Content=Content, Modifier=Modifier)
                target_sentence_Python += Python_template.format(Category=Category, Content=Content, Modifier=Modifier)
                target_sentence_Go += Go_template.format(Category=Category, Content=Content, Modifier=Modifier)
                target_sentence_SQL += SQL_template.format(Category=Category, Content=Content, Modifier=Modifier)
                target_sentence_Java += Java_template.format(Category=Category, Content=Content, Modifier=Modifier)
                target_sentence_JavaScript += JavaScript_template.format(Category=Category, Content=Content, Modifier=Modifier)
                target_sentence_URL += URL_template.format(Category=Category, Content=Content, Modifier=Modifier)
            target_data_C_plusplus.append(target_sentence_C_plusplus)
            target_data_C.append(target_sentence_C)
            target_data_C_sharp.append(target_sentence_C_sharp)
            target_data_Python.append(target_sentence_Python)
            target_data_Go.append(target_sentence_Go)
            target_data_SQL.append(target_sentence_SQL)
            target_data_Java.append(target_sentence_Java)
            target_data_JavaScript.append(target_sentence_JavaScript)
            target_data_URL.append(target_sentence_URL)
            print(target_data_C_plusplus)
            print(target_data_C)
            print(target_data_C_sharp)
            print(target_data_Python)
            print(target_data_Go)
            print(target_data_SQL)
            print(target_data_Java)
            print(target_data_JavaScript)
            print(target_data_URL)
            print("\n\n")
        args.target_language = 'C++'
        store_data(target_data_C_plusplus, args)
        args.target_language = 'C'
        store_data(target_data_C, args)
        args.target_language = 'C#'
        store_data(target_data_C_sharp, args)
        args.target_language = 'Python'
        store_data(target_data_Python, args)
        args.target_language = 'Go'
        store_data(target_data_Go, args)
        args.target_language = 'SQL'
        store_data(target_data_SQL, args)
        args.target_language = 'Java'
        store_data(target_data_Java, args)
        args.target_language = 'JavaScript'
        store_data(target_data_JavaScript, args)
        args.target_language = 'URL'
        store_data(target_data_URL, args)
        args.target_language = 'ALL'

    if target_language == 'C++':
        for sentence_index, phrases in sentence_groups.items():
            target_sentence = ''
            for phrase in phrases:
                target_sentence += C_plusplus_template.format(**phrase)
            target_data.append(target_sentence)

    if target_language == 'C':
        for sentence_index, phrases in sentence_groups.items():
            target_sentence = ''
            for phrase in phrases:
                target_sentence += C_template.format(**phrase)
            target_data.append(target_sentence)
        store_data(target_data, args)

    if target_language == 'C#':
        for sentence_index, phrases in sentence_groups.items():
            target_sentence = ''
            for phrase in phrases:
                target_sentence += C_sharp_template.format(**phrase)
            target_data.append(target_sentence)
        store_data(target_data, args)

    if target_language == 'Python':
        for sentence_index, phrases in sentence_groups.items():
            target_sentence = ''
            for phrase in phrases:
                target_sentence += Python_template.format(**phrase)
            target_data.append(target_sentence)
        store_data(target_data, args)

    if target_language == 'Go':
        for sentence_index, phrases in sentence_groups.items():
            target_sentence = ''
            for phrase in phrases:
                target_sentence += Go_template.format(**phrase)
            target_data.append(target_sentence)
        store_data(target_data, args)

    if target_language == 'SQL':
        for sentence_index, phrases in sentence_groups.items():
            target_sentence = ''
            for phrase in phrases:
                target_sentence += SQL_template.format(**phrase)
            target_data.append(target_sentence)
        store_data(target_data, args)

    if target_language == 'Java':
        for sentence_index, phrases in sentence_groups.items():
            target_sentence = ''
            for phrase in phrases:
                target_sentence += Java_template.format(**phrase)
            target_data.append(target_sentence)
        store_data(target_data, args)

    if target_language == 'JavaScript':
        for sentence_index, phrases in sentence_groups.items():
            target_sentence = ''
            for phrase in phrases:
                target_sentence += JavaScript_template.format(**phrase)
            target_data.append(target_sentence)
        store_data(target_data, args)

    if target_language == 'URL':
        for sentence_index, phrases in sentence_groups.items():
            target_sentence = ''
            for phrase in phrases:
                target_sentence += URL_template.format(**phrase)
            target_data.append(target_sentence)
        store_data(target_data, args)

def main():
    args = parse_args()

    # Load data
    data = load_data(args)

    # Translate data
    phrases_data = translate(data, args)

    # Store data
    store_phrases(phrases_data, args)

    # Load phrases and assemble code
    phrases_data = load_phrases(args)
    assemble_code(phrases_data, args)

if __name__ == '__main__':
    main()
