import smtplib, ssl
import sqlite3


def send_message(content, uuid):
    conn = sqlite3.connect('masterfish.db')
    cursor = conn.cursor()

    query = """
    SELECT email FROM users
    WHERE uuid = ?
    """
    receiver_email = cursor.execute(query, (uuid)).fetchone()
    #no peeking
    password = ''

    # For SSL
    port = 465
    smtp_server = 'friday.mxlogin.com'
    sender_email = 'notification@masterbait.fish'
    # Get message from file
    with open(content, 'r') as fp:
            # Create message
            msg = fp.read() + f" UUID: {uuid}"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)

    return

def claim_rig(email, uuid):
    conn = sqlite3.connect('masterfish.db')
    cursor = conn.cursor()
    """
    update priority, begin_date, and end date of a task
    :param email:
    :param uuid:
    """
    uuid = str(uuid["uuid"])
    data = (str(email),uuid)
    print(data)
    sql = ''' UPDATE users SET email = ? WHERE uuid = ? '''
    cursor.execute(sql,data)
    conn.commit()
