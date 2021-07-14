
actors = [
    'INSERT INTO actor (first_name, last_name) VALUES (%s, %s);', [
        ("actor1_fn", "actor1_ln",),
        ("actor2_fn", "actor2_ln",),
        ("actor3_fn", "actor3_ln",),
        ("actor4_fn", "actor4_ln",),
        ("actor5_fn", "actor5_ln",),
        ("actor6_fn", "actor6_ln",)
    ]
]

tags = [
    'INSERT INTO tag (name) VALUES (%s);', [
        ('tag1', ), ('tag2', ), ('tag3', ), ('tag4', ), ('tag5', )
    ]
]

genres = [
    'INSERT INTO genre (name) VALUES (%s);', [
        ('genre1', ), ('genre2', ), ('genre3', ), ('genre4', )
    ]
]

shows = [
    'INSERT INTO tvshow (title, view_rating, release_date, summary, score, votes) VALUES (%s, %s, %s, %s, %s, %s);', [
        ('show1', None, '2018-12-04', 'show 1 summary', 2.3, 3822),
        ('show2', 'PG', '2013-03-24', 'show 2 summary', 1.5, 17292),
        ('show3', 'PG', '2015-11-11', 'show 3 summary', 3.9, None),
        ('show4', 'G', '2020-7-22', 'show 4 summary', 4.2, 2111),
        ('show5', 'R', '2018-2-17', 'show 5 summary', 5.1, 19033),
        ('show6', 'PG', '2018-10-31', 'show 6 summary', 7.3, 47219),
        ('show7', None, '2017-6-23', 'show 7 summary', 1.8, 192),
        ('show8', 'PG-13', '2021-4-13', 'show 8 summary', 7.3, None),
        ('show9', None, '2019-9-25', 'show 9 summary', 6.7, 89921)
    ]
]

show_genres = [
    'INSERT INTO show_genre (id, genre_name, tvshow_title) VALUES (%s, %s, %s);', [
        (None, 'genre1', 'show3'),
        (None, 'genre1', 'show8'),
        (None, 'genre2', 'show2'),
        (None, 'genre2', 'show4'),
        (None, 'genre2', 'show8'),
        (None, 'genre3', 'show1'),
        (None, 'genre4', 'show2'),
        (None, 'genre4', 'show6'),
        (None, None, 'show7'),
        (None, 'genre4', 'show5'),
        (None, 'genre2', 'show1'),
        (None, 'genre4', 'show1'),
        (None, 'genre3', 'show3'),
        (None, 'genre4', 'show8')
    ]
]

show_actors = [
    'INSERT INTO show_actor (id, actor_fn, actor_ln, tvshow_title) VALUES (%s, %s, %s, %s);', [
        (None, 'actor2_fn', 'actor2_ln', 'show3'),
        (None, 'actor3_fn', 'actor3_ln', 'show4'),
        (None, 'actor1_fn', 'actor1_ln', 'show3'),
        (None, 'actor1_fn', 'actor1_ln', 'show1'),
        (None, 'actor1_fn', 'actor1_ln', 'show7'),
        (None, 'actor5_fn', 'actor5_ln', 'show5'),
        (None, 'actor5_fn', 'actor5_ln', 'show3'),
        (None, 'actor4_fn', 'actor4_ln', 'show6'),
        (None, 'actor6_fn', 'actor6_ln', 'show3'),
        (None, 'actor6_fn', 'actor6_ln', 'show2')
    ]
]

table_data = [actors, tags, genres, shows, show_genres, show_actors]
