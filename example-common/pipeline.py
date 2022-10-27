from social_core.pipeline.partial import partial


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get("ajax") or user and user.email:
        return
    elif is_new and not details.get("email"):
        email = strategy.request_data().get("email")
        if email:
            details["email"] = email
        else:
            current_partial = kwargs.get("current_partial")
            return strategy.redirect(
                "/email?partial_token={0}".format(current_partial.token)
            )


@partial
def require_country(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get("ajax"):
        return
    elif is_new and not details.get("country"):
        country = strategy.request_data().get("country")
        if country:
            details["country"] = country
        else:
            current_partial = kwargs.get("current_partial")
            return strategy.redirect(
                "/country?partial_token={0}".format(current_partial.token)
            )


@partial
def require_city(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get("ajax"):
        return
    elif is_new and not details.get("city"):
        city = strategy.request_data().get("city")
        if city:
            details["city"] = city
        else:
            current_partial = kwargs.get("current_partial")
            return strategy.redirect(
                "/city?partial_token={0}".format(current_partial.token)
            )
