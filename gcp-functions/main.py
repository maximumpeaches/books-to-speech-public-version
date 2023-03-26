from book import Book

bsrs_cut_book = Book('building_secure_and_reliable_systems.txt',
                     ['Chapter 17. Crisis Management', 'Chapter 18. Recovery and Aftermath',
                      'Chapter 19. Case Study: Chrome Security Team',
                      'Chapter 20. Understanding Roles and Responsibilities'], ['ch17', 'ch18', 'ch19'], 'bsrs')

all_books = [bsrs_cut_book]


def write_nonexistent_books(request, context):
    for book in all_books:
        book.write_to_audio()


if __name__ == '__main__':
    write_nonexistent_books(None, None)
