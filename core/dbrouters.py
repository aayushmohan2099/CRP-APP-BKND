# core/dbrouters.py
class MasterDBRouter:
    """
    Route:
      - app 'core' (master_* models) -> 'master' DB
      - everything else -> 'default' DB
    """
    route_app_labels = {'core'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'master'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'master'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = 'master' if obj1._meta.app_label in self.route_app_labels else 'default'
        db_obj2 = 'master' if obj2._meta.app_label in self.route_app_labels else 'default'
        return db_obj1 == db_obj2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # core app should NOT be migrated into default — it lives in 'master' (and is managed=False)
        if app_label in self.route_app_labels:
            return db == 'master'
        # all other apps (epSakhi, auth, background_task, etc.) should be in default
        return db == 'default'
