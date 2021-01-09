#!/usr/bin/env python
import sys
import csv
import json
import pprint
from isbntools.app import *

# Service to get book detals from
# 'goob' = Google Books Service
# 'wiki' = Wikipedia.org
# 'openl' = OpenLibrary.org
SERVICE = 'openl'

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def json2csv(in_file, out_file):

    # Opening JSON file and loading the data
    # into the variable data
    with open(in_file) as json_file:
        book_data = json.load(json_file)

    # now we will open a file for writing
    data_file = open(out_file, 'w')

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0

    for book in book_data:
        if count == 0:

            # Writing headers of CSV file
            header = book.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(book.values())

    data_file.close()


def process(in_file, out_file):
    global SERVICE

    books = []
    processed = 0
    first = True

    with open(in_file) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            processed += 1
            if first:
                first = False

                # csv_writer.writerow(['ISBN_10', 'ISBN_13', 'Title', 'Authors',
                #                      'Description', 'Thumbnail', 'Small Thumbnail',
                #                      'Publisher', 'Year'])

            title = row["Title"].strip()
            author = row["Author"].strip()
            isbn = isbn_from_words(f"{title} {author}")
            isbn_10 = to_isbn10(isbn),
            publisher = ''
            year = ''
            description = ''
            thumbnail = ''
            small_thumbnail = ''
            isbn_editions = []
            if isbn_10:
                isbn_10 = isbn_10[0]
            try:
                data = meta(isbn, service=SERVICE)
            except:
                data = meta(isbn, service='goob')

            try:
                title = data['Title']
                author = ', '.join(data['Authors']),
                publisher = data['Publisher']
                year = data['Year']
                isbn_editions = editions(isbn)
                isbn_editions = ', '.join(isbn_editions)
                description = desc(isbn)
                thumbnails = cover(isbn)
                if thumbnails:
                    thumbnail = thumbnails['thumbnail']
                    small_thumbnail = thumbnails['smallThumbnail']

                # pprint.pprint(list(data.keys()))
            except:
                eprint(f"Error: {isbn}, {row['Title']}")

            print(f"{processed} {row['Title']}")
            books.append({
                "isbn": isbn,
                "isbn_10": isbn_10,
                "title": title,
                "authors": author,
                "description": description,
                "thumbnail": thumbnail,
                "small_thumbnail": small_thumbnail,
                "publisher": publisher,
                "year": year,
                "editions": isbn_editions
                })

            # csv_writer.writerow([
            #     isbn,
            #     isbn_10,
            #     title,
            #     author,
            #     description,
            #     thumbnail,
            #     small_thumbnail,
            #     publisher,
            #     year])

    with open(out_file, mode="w") as write_file:
        json.dump(books, write_file)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("USAGE: isbn.py <in_file> <out_file>")
        sys.exit()

    if sys.argv[1] == 'csv':
        json2csv(sys.argv[2], sys.argv[3])
    else:
        process(sys.argv[1], sys.argv[2])

