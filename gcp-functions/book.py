import os

from tts import convert_text_to_audio_snippets


def cut_text(text, start, end, include_end=False):
    """
    Returns the portion of text which starts at start and ends at end, inclusive of the text contained within start and end.
    """
    start_index = text.find(start)
    end_index = text.find(end)
    if include_end:
        return text[start_index:end_index + len(end)].strip()
    else:
        return text[start_index:end_index].strip()


def cut_book(book_filename, start, end, include_end=False):
    """
    Returns the content of book_filename from text matching start to text matching end, inclusive.
    """
    with open('books/' + book_filename, 'r') as book:
        return cut_text(book.read(), start, end, include_end)


class Book:
    def __init__(self, book_filename, delimiters, chapter_names, output_directory):
        """
        Parameters
        ----------
        book_filename : str
            The name of the file that contains the book.
        delimiters : list[str]
            The text that delimits each chapter.
            If the whole book is to be cut, then the first delimiter would be 
            the first sentence and the last delimiter would be the last text.
            This must be in the same order and one less than chapter_names.
        chapter_names : list[str]
            The names of each chapter. They must line up with the delimiters and one greater in length.
        output_directory : str
            The directory where the chapters will be printed, if write_all_chapters is called.
            A typical value for output_directory is a short name for the book.
            output_directory must not contain spaces or any characters that wouldn't work for a directory name.
        """
        self.book_filename = book_filename
        self.delimiters = delimiters
        self.chapter_names = chapter_names
        assert len(self.delimiters) == len(
            self.chapter_names) + 1, 'chapter_names must be element shorter than delimiters. chapter_names refers to the content between each delimiter.'
        self.output_directory = output_directory
        self.chapters_output_directory = os.path.join('chapters', self.output_directory)
        os.makedirs(self.chapters_output_directory, 0o777, True)

    def write_all_chapters(self, replace_output_even_if_it_exists=False):
        """Write all the chapters in the book to files.

        :param replace_output_even_if_it_exists: if True, the files will be overwritten even if they exist. If False, that chapter
        won't be written if a file with its name already exists.
        :return: None
        """
        all_chapters = self.cut_all_chapters()
        assert len(all_chapters) == len(self.chapter_names), 'Every chapter must have a name.'
        for i in range(len(self.chapter_names)):
            try:
                with open(os.path.join(self.chapters_output_directory, self.chapter_names[i] + '.txt'),
                          'w' if replace_output_even_if_it_exists else 'x') as f:
                    f.write(all_chapters[i])
            except FileExistsError:
                assert not replace_output_even_if_it_exists, 'We only expect this type of error when replace_output_even_if_it_exists is False.'
                print('Not writing chapter', self.chapter_names[i],
                      'because it already exists and replace_output_even_if_it_exists is',
                      replace_output_even_if_it_exists)

    def cut_all_chapters(self):
        all_chapters = []
        for start, end in zip(self.delimiters, self.delimiters[1:]):
            all_chapters.append(cut_book(self.book_filename, start, end))
        return all_chapters

    def write_to_audio(self):
        # Just write the first chapter for now. I can change this later. Likewise just using the first chapter name below.
        chapter = self.cut_all_chapters()[0]
        audio_contents = convert_text_to_audio_snippets(chapter)
        mp3_filename = os.path.join(self.chapters_output_directory, self.chapter_names[0] + '.mp3')
        # The response's audio_content is binary.
        with open(mp3_filename, "wb") as out:
            for audio_content in audio_contents:
                out.write(audio_content)
                print('Audio content written to file ', mp3_filename)
