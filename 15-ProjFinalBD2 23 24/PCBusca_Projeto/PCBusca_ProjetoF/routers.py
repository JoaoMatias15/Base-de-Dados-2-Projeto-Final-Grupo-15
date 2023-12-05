# routers.py
class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'your_app':
            if 'PostgresModel' in model.__name__:
                return 'postgresql'
            elif 'MongoModel' in model.__name__:
                return 'mongodb'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'your_app' or obj2._meta.app_label == 'your_app':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'your_app':
            if db == 'postgresql' and 'MongoModel' in model_name:
                return False
            if db == 'mongodb' and 'PostgresModel' in model_name:
                return False
            return True
        return None