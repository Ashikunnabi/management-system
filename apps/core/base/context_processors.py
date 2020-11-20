import json
from apps.core.rbac.api.v1.serializers import FeatureSerializer
from apps.core.rbac.models import Feature


def left_sidebar(request):
    if request.user.is_authenticated:
        if request.user.role.code in ['super_admin']:
            queryset = Feature.objects.all()
        else:
            view_permissions = list(set(request.user.role.permission.filter(is_active=True, code__contains='view').values_list('feature_id', flat=True)))
            queryset = Feature.objects.filter(is_active=True, id__in=view_permissions)
            
        sidebar_options = json.dumps(FeatureSerializer(queryset.order_by('order_for_sidebar'), many=True).data)

        rearranged_list, rearranged_dict = [], dict()
        current_url = request.get_full_path()
        
        for value in json.loads(sidebar_options):
            if value["parent"] is None or value["parent"] == '':
                value["status"] = ''
                level_1 = []
                for v in json.loads(sidebar_options):
                    if v["parent"] == str(value["id"]):
                        v["status"] = ''
                        # print(current_url, v["url"])
                        # if current_url is not None and current_url == v["url"]:
                        if current_url is not None and v["url"] is not None:
                            if v["url"] in current_url:
                                v["status"] = 'active'
                                value["status"] = 'active pcoded-trigger'
                        level_1.append(v)
                value['level_1'] = level_1            
                if len(value['level_1']) == 0:
                    if current_url is not None and current_url == value["url"]:
                        value["status"] = 'active'
                rearranged_list.append(value)
        variables = {
          'SIDEBAR_OPTIONS': rearranged_list
        }
        return variables
    return ''
