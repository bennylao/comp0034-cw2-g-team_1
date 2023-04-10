from .models import Crayfish1, Crayfish2
from crayfish_analysis_app import ma
from .models import db


class Crayfish1Schema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class. Inherits all the attributes from the Crayfish1 class."""

    class Meta:
        model = Crayfish1
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = True

class Crayfish2Schema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class. Inherits all the attributes from the Crayfish2 class."""

    class Meta:
        model = Crayfish2
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = True
