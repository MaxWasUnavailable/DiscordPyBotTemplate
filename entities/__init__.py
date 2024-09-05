from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_or_create(session, model, filter_by: dict, defaults: dict):
    """
    Get or create a model.
    :param session: Session.
    :param model: Model.
    :param filter_by: Filter by.
    :param defaults: Defaults.
    :return: Instance.
    """
    instance = session.query(model).filter_by(**filter_by).first()
    if instance:
        return instance
    else:
        instance = model(**defaults)
        session.add(instance)
        session.commit()
        return instance


def get_or_create_simple(session, model, **kwargs):
    """
    Get or create a model. For simple models that don't need separate filter_by and defaults arguments.
    :param session: Session.
    :param model: Model.
    :param kwargs: Kwargs.
    :return: Instance.
    """
    return get_or_create(session, model, kwargs, kwargs)
