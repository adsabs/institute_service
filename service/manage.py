'''
Created on October 20, 2016

@author: ehenneken
'''
import sys
from flask.ext.script import Manager, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand
from sqlalchemy.orm.exc import NoResultFound
from models import db, Library
from app import create_app

app_ = create_app()

app_.config.from_pyfile('config.py')
try:
    app_.config.from_pyfile('local_config.py')
except IOError:
    pass

migrate = Migrate(app_, db)
manager = Manager(app_)

class CreateDatabase(Command):
    """
    Creates the database based on models.py
    """
    @staticmethod
    def run(app=app_):
        """
        Creates the database in the application context
        :return: no return
        """
        with app.app_context():
            db.create_all()
            db.session.commit()

class UpdateOpenUrlTable(Command):
    """
    Update the table with OpenURL servers
    """
    @staticmethod
    def run(app=app_):
        """
        Updates the table with OpenURL servers in the application context
        """
        with app.app_context():
            updates = []
            with open(app.config['INSTITUTE_OPENURL_DATA']) as fh:
                for line in fh:
                    try:
                        name, server, icon = line.strip().split('\t')
                    except:
                        # If it's just a number, it's that stupid first line
                        # otherwise report the problem
                        if not line.strip().isdigit():
                            sys.stderr.write('Found line with wrong number of tabs: %s\n'%line.strip())
                        continue
                    # We have valid data
                    # Let's see if we already know about this entry
                    try:
                        l = Library.query.filter(Library.libname == name).one()
                        # It's there, but check if the rest is the same
                        if l.iconurl != icon or l.libserver != server: 
                            l.iconurl = icon
                            l.libserver = server
                            sys.stderr.write('Updating OpenURL entry: %s\n'%l)
                            db.session.commit()
                    except NoResultFound:
                        # We have a new record
                        l = Library(libname = name, 
                                    iconurl = icon,
                                    libserver = server,
                                    institute = 0)
                        sys.stderr.write('Adding OpenURL entry: %s\n'%l)
                        db.session.add(l)
                        db.session.commit()

class DeleteStaleOpenUrlEntries(Command):
    """
    Remove stale entries from the table with OpenURL servers
    """
    @staticmethod
    def run(app=app_):
        """
        Updates the table by removing stale OpenURL servers in the application context
        """
        with app.app_context():
            # Get the entry names from master file
            names = []
            with open(app.config['INSTITUTE_OPENURL_DATA']) as fh:
                for line in fh:
                    try:
                        names.append(line.strip().split('\t')[0])
                    except:
                        continue
            # Get database records with a name not in the master list
            # session.query(Record).filter(Record.id.in_(seq)).all()
            # session.query(Post).filter(~Post.tags.any(Tag.name.in_(['dont', 'want', 'these'])))
            records = db.session.query(Library).filter(~Library.libname.in_(names)).all()
            for record in records:
                sys.stderr.write('Deleting stale OpenURL entry: %s\n'%record)
                Library.query.filter(Library.id == record.id).delete()
            db.session.commit()

manager.add_command('db', MigrateCommand)
manager.add_command('createdb', CreateDatabase())
manager.add_command('update_openurl', UpdateOpenUrlTable())
manager.add_command('delete_stale_openurl', DeleteStaleOpenUrlEntries())

@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app_.wsgi_app = ProfilerMiddleware(app_.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app_.run()

if __name__ == '__main__':
    manager.run()
