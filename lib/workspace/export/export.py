import io
from ftplib import *
from io import StringIO
from sqlalchemy import create_engine


def to_db(data, engine=None, table_name=None,
          db_driver=None, db_host=None, db_port=None,
          db_user=None, db_pass=None, db_name=None):
    """
    Export pandas dataframe to target database
    :return:
    """
    # fill port arg if needed
    if db_port:
        db_port = ':' + db_port
    else:
        db_port = ':'
    # init connection if empty engine
    if not engine:
        engine = create_engine(f'{db_driver}://{db_user}:{db_pass}@{db_host}{db_port}/{db_name}')
    # transfer data to db
    data.to_sql(table_name, con=engine, if_exists='append')
    # save db engine connection
    return engine


def to_ftp(data, ftp_host, ftp_login, ftp_pass, ftp_path='/'):
    """
    Export pandas dataframe to target ftp folder
    :param ftp_host: target ftp host
    :param ftp_login: target ftp login
    :param ftp_pass:
    :param ftp_path:
    :param data:
    :return:
    """
    # TODO: add ability for append data to existed target remote ftp file
    ftp = FTP(ftp_host)
    ftp.login(ftp_login, ftp_pass)
    ftp.cwd(ftp_path)
    buffer = StringIO()
    data.to_csv(buffer)
    text = buffer.getvalue()
    bio = io.BytesIO(str.encode(text))
    # store file
    ftp.storbinary('STOR filename.csv', bio)
