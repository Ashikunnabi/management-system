class Category {

    constructor() {
        this._helper = new Helper();
        this._api = '/inventory/api/v1/';
        this.category_list_url = this._api + 'js-tree-category/';
        this.user_permissions = request.user.permissions;
    }

    // fill jstree div
    set_category_in_jstree_div() {
        let self = this;
        $('#jstree_div').jstree({
            'core': {
                "animation": 0,
                "check_callback": true,
                "themes": {"stripes": true},
                'data': {
                    'headers': {'Authorization': 'JWT ' + self._helper.storage.getStorage('local', 'token').access},
                    'url': function (node) {
                        return node.id === '#' ?
                            self.category_list_url :
                            self.category_list_url;
                    },
                    'data': function (node) {
                        return {'id': node.id};
                    }
                }
            },
            "types": {
                "#": {
                    "max_children": -1,
                    "max_depth": -1,
                    "valid_children": ["root"]
                },
                "root": {
                    "icon": "fas fa-large fa-folder",
                    "valid_children": ["default"]
                },
                "default": {
                    "icon": "fas fa-large fa-folder",
                    "valid_children": ["default", "file"]
                },
                "file": {
                    "icon": "fas fa-large fa-folder",
                    "valid_children": []
                }
            },
            "plugins": [
                "contextmenu", "dnd", "search",
                "state", "types", "wholerow"
            ]
        });
    }
}


let _category = new Category();

$(document).ready(function (e) {
    _category.set_category_in_jstree_div()
});


