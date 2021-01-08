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
        console.log('inside set_category_in_jstree_div()');
        $('#jstree_div').jstree({
            'core': {
                'data': {
                    'headers': { 'Authorization': 'JWT '+self._helper.storage.getStorage('local', 'token').access },
                    'url': function (node) {
                        return node.id === '#' ?
                            self.category_list_url :
                            self.category_list_url;
                    },
                    'data': function (node) {
                        return {'id': node.id};
                    }
                }
            }
        });
    }
}


let _category = new Category();

$(document).ready(function (e) {
    _category.set_category_in_jstree_div()
});


