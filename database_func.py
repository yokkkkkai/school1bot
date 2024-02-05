# -*- coding: utf-8 -*-

import pymysql
from config import host, user, password, db_name


def get_connection():
    return pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )


def allnick():
    usernames = []
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            insert_all_users = "SELECT username FROM user"
            cursor.execute(insert_all_users)
            rows = cursor.fetchall()
            for row in rows:
                usernames.append(row['username'])
    finally:
        connection.close()
    return usernames


def allids():
    chat_ids = []
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            insert_all_users = "SELECT chat_id FROM user"
            cursor.execute(insert_all_users)
            rows = cursor.fetchall()
            for row in rows:
                chat_ids.append(row['chat_id'])
    finally:
        connection.close()
    return chat_ids


def newuser(user_nickname, chat_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            insert_new_user = f"INSERT INTO user (username, chat_id) VALUES ('{user_nickname}', '{chat_id}')"
            cursor.execute(insert_new_user)
            connection.commit()
    finally:
        connection.close()