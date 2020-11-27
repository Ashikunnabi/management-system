import uuid
from apps.core.rbac.models import ActivityLog


def json_parameter_validation(json_data, required_params):
    """ Check parameter is available in json or not
        parameter:
        ---------
            json_data: dict, required
                A dictionary that should be validate by pramas are available or not
            required_params: list, required
                Those list of params that must be available on json_data
        return:
        ------
            required_params: list
                If required parameter is not in json_data then return that parameter name othrewise None
    """
    for param in required_params:
        if json_data.get(param) is None:
            return param
            

def get_user_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
            

def get_user_browser_details(request):    
    return request.headers.get('User-Agent')


def random_hex_code(length: int = 8) -> str:
    """
        To create a new random hex code of dynamic length.

        :parameter
            length (int): set how many character of hex code will generate. Default is 8 character.

        :return
            random hex code with dynamic length.
    """
    return uuid.uuid4().hex[:length]


def store_user_activity(request, store_json='', description='') -> None:
    """
        Store user activity into ActivityLog table for future reference

        :parameter
            request (obj): django request object
            store_json (str): dumps json for request/response data
            description (str): basic description to represent userside view
    :return:
    """
    ActivityLog.objects.create(store_json=store_json,
                               description=description,
                               ip_address=get_user_ip_address(request),
                               browser_details=get_user_browser_details(request)
                               )


