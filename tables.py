# tag_table = """
#     CREATE TABLE IF NOT EXISTS tag (
#         name VARCHAR(20) NOT NULL PRIMARY KEY
#     );
# """

genre_table = """
    CREATE TABLE IF NOT EXISTS genre (
        name VARCHAR(20) PRIMARY KEY
    );
"""

actor_table = """
    CREATE TABLE IF NOT EXISTS actor (
        first_name VARCHAR(50) NOT NULL,
        middle_name VARCHAR(20),
        last_name VARCHAR(50) NOT NULL,
        PRIMARY KEY(first_name, last_name)
    );
"""

show_table = """
    CREATE TABLE IF NOT EXISTS tvshow (
        title VARCHAR(110) NOT NULL,
        view_rating VARCHAR(100),
        release_date DATE,
        summary TEXT,
        score DECIMAL(2, 1),
        votes INT,
        PRIMARY KEY(title)
    );
"""

show_genre_table = """
    CREATE TABLE IF NOT EXISTS show_genre (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        genre_name VARCHAR(20) NULL,
        tvshow_title VARCHAR(110) NOT NULL,
        FOREIGN KEY (genre_name) REFERENCES genre(name),
        FOREIGN KEY (tvshow_title) REFERENCES tvshow(title)
    );
"""

show_actor_table = """
    CREATE TABLE IF NOT EXISTS show_actor (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        actor_fn VARCHAR(50) NOT NULL,
        actor_ln VARCHAR(50) NOT NULL,
        tvshow_title VARCHAR(110) NOT NULL,
        FOREIGN KEY (actor_fn, actor_ln) REFERENCES actor(first_name, last_name),
        FOREIGN KEY (tvshow_title) REFERENCES tvshow(title)
    );
"""

tables = [
    genre_table, actor_table, show_table,
    show_genre_table, show_actor_table
]
