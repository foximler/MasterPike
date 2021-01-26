import smtplib, ssl
import sqlite3


def send_message(content, uuid):
    # Sends message to use with current user email
    conn = sqlite3.connect('masterfish.db')
    cursor = conn.cursor()

    query = """
    SELECT email FROM users
    WHERE uuid = ?
    """

    data_received = cursor.execute(query, (uuid,)).fetchone()
    receiver_email = data_received[0]
    conn.commit()
    cursor.close()

    if receiver_email == None:
        return f"No receiver email: SQL error -- {receiver_email}"
    #no peeking
    password = ''

    # For SSL
    port = 465
    smtp_server = 'friday.mxlogin.com'
    sender_email = 'notification@masterbait.fish'

    msg = f"Fish On! UUID: {uuid}"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)

    return "Message Sent!"


def claim_rig(email, uuid):
    conn = sqlite3.connect('masterfish.db')
    cursor = conn.cursor()
    """
    update priority, begin_date, and end date of a task
    :param email:
    :param uuid:
    """
    uuid = str(uuid["uuid"])
    data = (str(email),uuid,)

    sql = ''' UPDATE users SET email = ? WHERE uuid = ? '''

    cursor.execute(sql,data)
    conn.commit()
    cursor.close()
