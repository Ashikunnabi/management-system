def mobile_validator() -> list:
    """
    This function return a list of regex code for bd mobile number and the message(description of the regex requirement).
    :return: [regex, message]
    """
    regex = '\+?(88)?01[3456789][0-9]{8}$'
    message = 'Mobile number must be a valid Bangladeshi number'
    return [regex, message]


def name_validator() -> list:
    """
    This function return a list of regex code for name and the message(description of the regex's requirement).
    :return: [regex, message]
    """
    regex = '[-a-zA-Z0-9_.\s]{2,100}$'
    message = 'Vendor contains alphanumeric, underscore, space and period(.). Length: 2 to 100'
    return [regex, message]
