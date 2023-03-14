import os
import docx
import numpy as np

from numpy import ndarray
from typing import List, Set, Dict, Union


def get_text(file_fp):
    doc = docx.Document(file_fp)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)


def split_crt(text) -> list[str]:
    # Import HMM-based tokenizer
    from kaznlp.tokenization.tokhmm import TokenizerHMM
    return [
        'Мусафирлер чокътан даркъалып кеттилер.',
        'Саат он эки бучукъ олгъаныны бильдириджи чанъ къакъты.'
    ]


def split_ru(text) -> list[str]:
    from razdel import sentenize
    return [
        'Гости давно разъехались.',
        'Часы пробили половину первого.'
    ]


def print_sentences_single(sentences, out_file_fp):
    with open(out_file_fp, 'w') as f:
        for s in sentences:
            f.write(s)
            f.write("\n")


def combine_sentences(sentences_a, sentences_b) -> list[str]:
    combined = []
    for i in range(len(sentences_a)):
        combined.append(sentences_a[i] + '\n' + sentences_b[i] + '\n')
    return combined


def main(file_crt_sp, file_ru_sp, sentences_combined_output_file_sp):
    dir_texts_split_sentences_combined = 'texts_pairs'
    assert os.path.exists(dir_texts_split_sentences_combined), \
        'Dir is absent: ' + dir_texts_split_sentences_combined

    file_crt_fp = os.path.join(dir_texts_split_sentences_combined, file_crt_sp)
    file_ru_fp = os.path.join(dir_texts_split_sentences_combined, file_ru_sp)
    print('*' * 100)
    print(f'Checking if file exits [{file_crt_fp}]', os.path.exists(file_crt_fp))
    print(f'Checking if file exits [{file_ru_fp}]', os.path.exists(file_ru_fp))

    print('Reading text from DOCX...')
    text_ct = get_text(file_crt_fp)
    print('Read OK. Total chars (CRT):', len(file_crt_fp))
    text_ru = get_text(file_ru_fp)
    print('Read OK. Total chars (RU):', len(file_ru_fp))

    sentences_ct = split_crt(text_ct)
    sentences_ru = split_ru(text_ru)

    sentences_crt_output_file_sp = file_crt_sp[:-5] + '.split' + '.txt'
    sentences_ru_output_file_sp = file_ru_sp[:-5] + '.split' + '.txt'

    dir_texts_split = 'texts_split'
    os.makedirs(dir_texts_split, exist_ok=True)
    sentences_crt_output_file_fp = os.path.join(dir_texts_split, sentences_crt_output_file_sp)
    sentences_ru_output_file_fp = os.path.join(dir_texts_split, sentences_ru_output_file_sp)

    print_sentences_single(sentences_ct, sentences_crt_output_file_fp)
    print_sentences_single(sentences_ru, sentences_ru_output_file_fp)

    sentences_combined = combine_sentences(sentences_ct, sentences_ru)
    # Hardcoded
    dir_texts_split_sentences_combined = 'texts_split_combined'
    os.makedirs(dir_texts_split_sentences_combined, exist_ok=True)
    sentences_combined_output_file_fp = os.path.join(
        dir_texts_split_sentences_combined,
        sentences_combined_output_file_sp
    )
    print_sentences_single(sentences_combined, sentences_combined_output_file_fp)


if __name__ == '__main__':
    file_crt_sp = 'Тургенев И.С. Биринджи севги.crt.docx'
    file_ru_sp = 'Тургенев И. С. Первая любовь.ru.docx'
    sentences_combined_output_file_sp = 'Тургенев И. С. Первая любовь. Биринджи севги.txt'

    main(file_crt_sp, file_ru_sp, sentences_combined_output_file_sp)
