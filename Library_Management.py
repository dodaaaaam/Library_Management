import sqlite3
import random
from faker import Faker
from itertools import cycle
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(24)

with sqlite3.connect("cau-db-practice.db") as connection:
  cursor = connection.cursor()
  
  #BOOK ENTITY
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS book(
      book_id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      author TEXT NOT NULL,
      publisher TEXT NOT NULL,
      total_copies INTEGER,
      category TEXT NOT NULL,
      remaining_copies INTEGER);
  ''')

  #LIBRARIAN ENTITY
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS librarian(
      librarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      phone TEXT NOT NULL,
      email TEXT NOT NULL);
  ''')

  #LIB_BOOKS
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS lib_books(
      librarian_id INTEGER,
      book_id INTEGER,

      PRIMARY KEY (librarian_id, book_id),
      FOREIGN KEY (librarian_id) REFERENCES librarian(librarian_id)
        ON DELETE CASCADE  ON UPDATE CASCADE,
      FOREIGN KEY (book_id) REFERENCES book(book_id)
        ON DELETE CASCADE  ON UPDATE CASCADE
      );
  ''')

  #USER ENTITY
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      phone TEXT NOT NULL,
      email TEXT NOT NULL,
      UNIQUE(phone));
  ''')

  #BOOK_LOAN ENTITY
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS book_loan(
      loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      return_date TEXT,
      loan_date TEXT,
      FOREIGN KEY(user_id) REFERENCES user(user_id)
        ON DELETE CASCADE  ON UPDATE CASCADE);
  ''')

  #MATCH_BOOKS
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS match_books(
      loan_id INTEGER NOT NULL,
      book_id INTEGER NOT NULL,
      PRIMARY KEY (loan_id, book_id),
      FOREIGN KEY(loan_id) REFERENCES loan(loan_id)
        ON DELETE CASCADE  ON UPDATE CASCADE,
      FOREIGN KEY(book_id) REFERENCES book(book_id)
        ON DELETE CASCADE  ON UPDATE CASCADE);
  ''')

  #ROOM ENTITY
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS room(
      room_id INTEGER NOT NULL,
      librarian_id INTEGER NOT NULL,
      room_name TEXT NOT NULL,
      PRIMARY KEY (room_id),
      FOREIGN KEY(librarian_id) REFERENCES librarian(librarian_id)
        ON DELETE CASCADE  ON UPDATE CASCADE);
  ''')

  #BOOKSHELF ENTITY
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookshelf(
      bookshelf_id INTEGER PRIMARY KEY AUTOINCREMENT,
      category TEXT NOT NULL,
      num_books INTEGER NOT NULL);
  ''')
  
  #ROOM_BOOKSHELVES
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS room_bookshelves(
      room_id INTEGER NOT NULL,
      bookshelf_id INTEGER NOT NULL,
      PRIMARY KEY (room_id, bookshelf_id),
      FOREIGN KEY(bookshelf_id) REFERENCES bookshelf(bookshelf_id)
        ON DELETE CASCADE  ON UPDATE CASCADE);
  ''')

  #BOOKSHELVES_BOOKS
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookshelves_books(
      bookshelf_id INTEGER NOT NULL,
      book_id INTEGER NOT NULL,
      PRIMARY KEY (bookshelf_id, book_id),
      FOREIGN KEY(book_id) REFERENCES book(book_id)
        ON DELETE CASCADE  ON UPDATE CASCADE);
  ''')

  # Insert BOOK records
  num_book_records = 100
  categories = ["Fiction", "Non-fiction", "Science", "History", "Biography", "Fantasy"]
  publishers = ["Penguin", "HarperCollins", "Oxford Press", "Simon & Schuster", "Random House"]

  for _ in range(num_book_records):
      title = fake.sentence(nb_words=3)  # Generate a random book title
      author = fake.name()  # Generate a random author name
      publisher = random.choice(publishers)  # Randomly select a publisher
      category = random.choice(categories)  # Randomly select a category
      total_copies = random.randint(1, 50)  # Randomly generate total copies
      remaining_copies = total_copies  

      cursor.execute('''
        INSERT INTO book (title, author, publisher, category, remaining_copies, total_copies)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, author, publisher, category, remaining_copies, total_copies))

 # Commit changes
  connection.commit()

  #print(f"{num_book_records} book records inserted successfully\n")

  # Insert LIBRARIAN records
  num_lib_records = 3

  for _ in range(num_lib_records):
      name = fake.name() 
      phone = fake.phone_number()
      email = fake.email()

      cursor.execute('''
        INSERT INTO librarian (name, phone, email)
        VALUES (?, ?, ?)
        ''', (name, phone, email))

  # Commit changes
  connection.commit()
  #print(f"{num_lib_records} librarian records inserted successfully\n")

  # Distribute books evenly among librarians
  cursor.execute('SELECT librarian_id FROM librarian')
  librarian_ids = [row[0] for row in cursor.fetchall()]  # Get a list of all librarian IDs

  cursor.execute('SELECT book_id FROM book')
  book_ids = [row[0] for row in cursor.fetchall()]  # Get a list of all book IDs

  librarian_cycle = cycle(librarian_ids)  # Create a repeating cycle of librarian IDs
  lib_books_records = []

  for book_id in book_ids:
      assigned_librarian = next(librarian_cycle)  # Assign librarians in a round-robin fashion
      lib_books_records.append((assigned_librarian, book_id))

  # Insert records into LIB_BOOKS table
  for librarian_id, book_id in lib_books_records:
      cursor.execute(''' 
        SELECT 1 FROM lib_books WHERE librarian_id = ? AND book_id = ?
        ''', (librarian_id, book_id))
    
      # Check if the record already exists
      if cursor.fetchone() is None:  # If record doesn't exist
            cursor.execute('''
                INSERT INTO lib_books (librarian_id, book_id)
                VALUES (?, ?)
                ''', (librarian_id, book_id))
      else:
            print(f"Record for librarian {librarian_id} and book {book_id} already exists.")

  # Commit changes
  connection.commit()

  #print(f"{len(lib_books_records)} records inserted into LIB_BOOKS successfully.\n")

  # Insert ROOM records
  num_room_records = 3
  room_names = ["101호", "201호", "301호"]

  for _ in range(num_room_records):
      room_name = random.choice(room_names)
      librarian_id = random.choice(librarian_ids)
    
      cursor.execute('''
        INSERT INTO room (room_name, librarian_id)
        VALUES (?, ?)
        ''', (room_name, librarian_id))

  # Commit changes
  connection.commit()
  #print(f"{num_room_records} room records inserted successfully\n")

  # Insert BOOKSHELVES_BOOKS records                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ``  ``````````````````````````````````````  
  cursor.execute('SELECT DISTINCT category FROM book')
  categories = [row[0] for row in cursor.fetchall()]  # Get a list of all unique categories

  bookshelf_records = []
  for category in categories:
      num_books_in_category = cursor.execute('SELECT COUNT(*) FROM book WHERE category = ?', (category,)).fetchone()[0]
      cursor.execute('''
          INSERT INTO bookshelf (category, num_books)
          VALUES (?, ?)
      ''', (category, num_books_in_category))
      bookshelf_id = cursor.lastrowid  # Get the ID of the newly inserted bookshelf
      bookshelf_records.append((bookshelf_id, category))

  # Commit changes
  connection.commit()
  #print(f"{len(bookshelf_records)} bookshelf records inserted successfully\n")

  # Map BOOKSHELVES_BOOKS records (책을 책장에 매핑)
  for bookshelf_id, category in bookshelf_records:
      cursor.execute('SELECT book_id FROM book WHERE category = ?', (category,))
      book_ids_in_category = [row[0] for row in cursor.fetchall()]
      for book_id in book_ids_in_category:
          cursor.execute('''
              INSERT INTO bookshelves_books (bookshelf_id, book_id)
              VALUES (?, ?)
          ''', (bookshelf_id, book_id))

  # Commit changes
  connection.commit()
  #print("bookshelf records inserted successfully\n")

  # Distribute bookshelves evenly among rooms
  cursor.execute('SELECT room_id FROM room')
  room_ids = [row[0] for row in cursor.fetchall()]

  cursor.execute('SELECT bookshelf_id FROM bookshelf')
  bookshelf_ids = [row[0] for row in cursor.fetchall()]

  room_cycle = cycle(room_ids) 
  room_books_records = []

  for bookshelf_id in bookshelf_ids:
      assigned_room = next(room_cycle)
      room_books_records.append((assigned_room, bookshelf_id))

  for room_id, bookshelf_id in room_books_records:
      cursor.execute('''
          INSERT INTO room_bookshelves (room_id, bookshelf_id)
          VALUES (?, ?)
      ''', (room_id, bookshelf_id))

  # Commit changes
  connection.commit()
  #print(f"{len(room_books_records)} records inserted into ROOM_BOOKSHELVES successfully.\n")

  '''
  new user register

  '''
  def new_user():
    u_name = input("name: ")
    u_phone = input("phone: ")
    u_email = input("email: ")

    cursor.execute('''
            INSERT INTO user (name, phone, email)
            VALUES (?, ?, ?)
            ''', (u_name, u_phone, u_email))
    connection.commit()
    print(f"New user registered successfully!\n")

  '''
  new book register
  '''
  def new_book():
    new_title = input("title: ")
    new_author = input("author: ")
    new_publisher = input("publisher: ")
    new_total_copies = input("total_copies: ")
    new_category = input("category: ")

    # 기존 책 제목 확인
    cursor.execute('SELECT title FROM book WHERE title = ?', (new_title,))
    existing_book = cursor.fetchone()

    if existing_book:
        new_total_copies = int(new_total_copies)
        # 기존 책이 있을 경우 `total_copies` 업데이트
        cursor.execute('''
            UPDATE book 
            SET total_copies = total_copies + ?, remaining_copies = remaining_copies + ?
            WHERE title = ?
        ''', (new_total_copies, new_total_copies, new_title))
        print(f"Existing book updated successfully! Total copies increased by {new_total_copies}.\n")
    else:
        # 새로운 책 등록
        cursor.execute('''
            INSERT INTO book (title, author, publisher, total_copies, category, remaining_copies)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (new_title, new_author, new_publisher, new_total_copies, new_category, new_total_copies))
        book_id = cursor.lastrowid

        cursor.execute('SELECT librarian_id FROM librarian')
        librarian = cursor.fetchall()
        librarian_id = random.choice([row[0] for row in librarian])
        cursor.execute('''
            INSERT INTO lib_books (librarian_id, book_id)
            VALUES (?, ?)
        ''', (librarian_id, book_id))

        cursor.execute('SELECT bookshelf_id FROM bookshelf WHERE category = ?', (new_category,))
        bookshelf = cursor.fetchone()
        bookshelf_id = bookshelf[0]
        cursor.execute('''
            INSERT INTO bookshelves_books (bookshelf_id, book_id)
            VALUES (?, ?)
        ''', (bookshelf_id, book_id))

        connection.commit()
        print(f"New book registered successfully!\n")


  '''
  book update 
  '''
  def update_book():
    book_title = input("Enter the title of the book to update: ")

    if not book_title:
        print("The title cannot be empty. Please enter a valid book title.\n")
        return

    # 해당 책이 존재하는지 확인
    cursor.execute('SELECT * FROM book WHERE title = ?', (book_title,))
    book = cursor.fetchone()

    if not book:
        print(f"The book '{book_title}' does not exist in the database.\n")
        return
    book_id = book[0]  # book_id를 가져옴

    # 사용자에게 업데이트할 항목 선택
    print("What would you like to update?")
    print("1. Title")
    print("2. Author")
    print("3. Publisher")
    print("4. Category")
    print("5. Total Copies")
    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        new_title = input("Enter the new title: ")
        cursor.execute('UPDATE book SET title = ? WHERE book_id = ?', (new_title, book_id))
    elif choice == '2':
        new_author = input("Enter the new author: ")
        cursor.execute('UPDATE book SET author = ? WHERE book_id = ?', (new_author, book_id))
    elif choice == '3':
        new_publisher = input("Enter the new publisher: ")
        cursor.execute('UPDATE book SET publisher = ? WHERE book_id = ?', (new_publisher, book_id))
    elif choice == '4':
        new_category = input("Enter the new category: ")
        cursor.execute('UPDATE book SET category = ? WHERE book_id = ?', (new_category, book_id))
        cursor.execute('SELECT bookshelf_id FROM bookshelf WHERE category = ?', (new_category,))
        bookshelf = cursor.fetchone()
        bookshelf_id = bookshelf[0]
        cursor.execute('UPDATE bookshelves_books SET bookshelf_id = ? WHERE book_id = ?', (bookshelf_id, book_id))
    elif choice == '5':
        new_total_copies = int(input("Enter the new total copies: "))
        # 총 복사본 수 변경 시 남은 복사본 수도 조정
        cursor.execute('''
            UPDATE book 
            SET total_copies = ?, 
                remaining_copies = remaining_copies + (? - total_copies)
            WHERE title = ?
        ''', (new_total_copies, new_total_copies, book_title))
    else:
        print("Invalid choice. No updates were made.\n")
        return

    # 변경 사항 저장
    connection.commit()
    print(f"The book '{book_title}' has been updated successfully!\n")


  '''
  book delete 
  '''
  def delete_book():
    book_title = input("Enter the title of the book to delete: ").strip()

    # 입력 유효성 검증
    if not book_title:
        print("The title cannot be empty. Please enter a valid book title.\n")
        return

    # 해당 책이 존재하는지 확인
    cursor.execute('SELECT * FROM book WHERE title = ?', (book_title,))
    book = cursor.fetchone()

    if not book:
        print(f"The book '{book_title}' does not exist in the database.\n")
        return
    
    book_id = book[0]  # book_id를 가져옴

    # 책 삭제 실행
    cursor.execute('DELETE FROM book WHERE book_id = ?', (book_id,))

    # 변경 사항 저장
    connection.commit()
    print(f"The book '{book_title}' has been deleted successfully!\n")


  '''
  book loan 
  '''
  def loan_book():
     # 사용자 입력 받기
    user_name = input("Enter the user name: ").strip()
    user_phone = input("Enter the user phone number: ").strip()
    user_email = input("Enter the user email: ").strip()
    
    # 사용자 존재 여부 확인
    cursor.execute('SELECT * FROM user WHERE name = ? AND phone = ? AND email = ?', (user_name, user_phone, user_email,))
    user = cursor.fetchone()

    if not user:
        print(f"User '{user_name}' does not exist.\n")
        return
    user_id = user[0]

    count = int(input("Enter the number of books: "))
    if count > 3:
        print("maximum 3")
        return
    
    for i in range(count):
        book_title = input("Enter the title of the book to loan: ").strip()

        # 책 존재 및 대출 가능 여부 확인
        cursor.execute('SELECT book_id, remaining_copies FROM book WHERE title = ?', (book_title,))
        book = cursor.fetchone()

        if not book:
            print(f"The book '{book_title}' does not exist in the database.\n")
            return

        book_id = book[0] 
        remaining_copies = book[1]

        if remaining_copies <= 0:
            print(f"The book '{book_title}' is currently not available for loan.\n")
            return

        # 대출 날짜 및 반납 날짜 생성
        loan_date = datetime.now().strftime('%Y-%m-%d')
        return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')

        # 대출 등록 (book_loan에 삽입)
        cursor.execute('''
            INSERT INTO book_loan (user_id, loan_date, return_date)
            VALUES (?, ?, ?)
        ''', (user_id, loan_date, return_date))
        # 변경 사항 커밋
        connection.commit()

        # 대출 ID 가져오기
        loan_id = cursor.lastrowid

        # 대출과 책 연결 (match_books에 삽입)
        cursor.execute('''
            INSERT INTO match_books (loan_id, book_id)
            VALUES (?, ?)
        ''', (loan_id, book_id))
        # 변경 사항 커밋
        connection.commit()

        # 잔여 복사본 감소
        cursor.execute('''
            UPDATE book
            SET remaining_copies = remaining_copies - 1
            WHERE book_id = ?
        ''', (book_id,))

        # 변경 사항 커밋
        connection.commit()

        print(f"The book '{book_title}' has been loaned to user ID '{user_id}' successfully!\n")


  '''
  book return 
  '''
  def return_book():
    # 사용자 입력 받기
    user_name = input("Enter the user name: ").strip()

    cursor.execute('SELECT user_id FROM user WHERE name = ?', (user_name,))
    user = cursor.fetchone()
    user_id = user[0]

    if not user:
        print(f"User with ID '{user_id}' does not exist.\n")
        return

    count = int(input("Enter the number of books: "))

    for i in range(count):
        book_title = input(f"Enter the title of the book {i+1} to return: ").strip()

        # 책 존재 여부 확인
        cursor.execute('SELECT book_id FROM book WHERE title = ?', (book_title,))
        book = cursor.fetchone()

        if not book:
            print(f"The book '{book_title}' does not exist in the database.\n")
            return
        
        book_id = book[0]  # 책의 ID

        # 책 대출 여부 확인
        cursor.execute('SELECT loan_id FROM match_books WHERE book_id = ?', (book_id,))
        loan = cursor.fetchone()

        if not loan:
            print(f"The book '{book_title}' is not loaned.\n")
            return

        loan_id = loan[0]
        
        # 대출된 책과 대출한 사용자가 맞는지 확인
        cursor.execute('SELECT user_id FROM book_loan WHERE loan_id = ?', (loan_id,))
        loan_user = cursor.fetchone()

        if not loan_user:
            print(f"No loan information found for the book '{book_title}'.\n")
            return
        
        if loan_user[0] != user_id:
            print(f"The user '{user_id}' did not loan the book '{book_title}'.\n")
            return

        # 대출 기록 삭제
        cursor.execute('DELETE FROM book_loan WHERE loan_id = ?', (loan_id,))
        cursor.execute('DELETE FROM match_books WHERE loan_id = ?', (loan_id,))

        # 잔여 복사본 증가
        cursor.execute('''
        UPDATE book
        SET remaining_copies = remaining_copies + 1
        WHERE book_id = ?
        ''', (book_id,))

        # 변경 사항 커밋
        connection.commit()

        print(f"The book '{book_title}' has been returned successfully!\n")

  print("Welcome to CAU Library Management System!\n")
  print("Please select the menu.\n\n")

  print("0. new user register\n")
  print("1. new book register\n")
  print("2. book update\n")
  print("3. book delete\n")
  print("4. new book loan\n")
  print("5. book loan return\n")

  #번호 입력
  a = input()
  while a != 'exit':
    if a=='0':
        new_user()
    elif a=='1':
        new_book()
    elif a=='2':
        update_book()
    elif a=='3':
        delete_book()
    elif a=='4':
        loan_book()
    elif a=='5':
        return_book()
    else:
        print("select correct number again")
        break
    print("Please select the menu.\n")
    a=input()

  connection.commit()
  cursor.close()