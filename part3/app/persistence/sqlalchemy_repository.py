from app.persistence.repository import Repository


class SQLAlchemyRepository(Repository):
    """Generic repository implementation using SQLAlchemy"""

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        from app import db
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        from app import db
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        from app import db
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Return first object matching a given attribute"""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
