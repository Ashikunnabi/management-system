import uuid


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
            
    