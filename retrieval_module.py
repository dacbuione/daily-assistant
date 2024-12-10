import sqlite3

def search_data(keyword):
    conn = sqlite3.connect('assistants.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM health_info WHERE content LIKE ?', ('%' + keyword + '%',))
    results = cursor.fetchall()
    conn.close()
    return results 