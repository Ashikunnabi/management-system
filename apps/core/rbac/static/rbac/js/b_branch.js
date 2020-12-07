// There are 6 types of permission
// 1. Add Branch 2. Edit Branch 3. Delete Branch 4. Self View Branch
// 5. List View Branch 6. Detail View Branch
// To add a new branch, a role must have permission 1 & 5
// To delete an existing branch, a role must have permission 3 & 5
// To edit an existing branch (self), a role must have permission 2, 4 & 6
// To edit an existing branch (list), a role must have permission 2, 5 & 6


class Branch {
    constructor() {
        this._helper = new Helper();
        this._api = '/api/v1/';
        this.branch_list_url = this._api + 'branch/?format=datatables';
        this.branch_add_url = '/branch/add/';
        this.user_permissions = request.user.permissions;
    }

    provide_permission_based_access() {
        let self = this;
        // If user_permissions array has not 'add.rbac_permission' or 'list_view.rbac_permission' then 'indexOf' will
        // return -1. That means user have not these permissions and the add branch button will be removed.
        if (!(self.user_permissions.indexOf("add.rbac_permission") > -1) || !(self.user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $('#add_branch').remove();
        }
        // If user_permissions array has not 'detail_view.rbac_permission' or 'change.rbac_permission' then 'indexOf' will
        // return -1. That means user have not these permissions and the edit branch button will be removed.
        if (!(self.user_permissions.indexOf("detail_view.rbac_permission") > -1) || !(self.user_permissions.indexOf("change.rbac_permission") > -1)) {
            $('#edit_branch').remove();
        }
        // If user_permissions array has not 'self_view.rbac_permission' or 'list_view.rbac_permission' then 'indexOf' will
        // return -1. That means user have not these permissions and the edit branch button will be removed.
        if (!(self.user_permissions.indexOf("self_view.rbac_permission") > -1) && !(self.user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $('#edit_branch').remove();
        }
        // If user_permissions array has not 'delete.rbac_permission' or 'list_view.rbac_permission' then 'indexOf' will
        // return -1. That means user have not these permissions and the delete branch button will be removed.
        if (!(self.user_permissions.indexOf("delete.rbac_permission") > -1) || !(self.user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $('#delete_branch').remove();
        }
    }

    branch_list() {
        let self = this;
        let url = self.branch_list_url;
        // calling self.set_feature_in_dropdown() method for features that will store in session storage
        self.set_feature_in_dropdown();
        self._helper.blockUI();  // Calling the method for loading style
        // When the ajax request processing is done then this function will be called and unblock the window
        $(document).ajaxStop($.unblockUI);

        let table = $('#branch_table').DataTable({
            "processing": true,
            // "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            // "dom": '<"mb-3"B>flrtip',
            "searchPanes": {
                layout: 'columns-4'
            },
            "dom": 'P<"mb-3"B>flrtip',
            "buttons": [
                'copy',
                'excel',
                'pdf',
                'csv',
                {
                    extend: 'print',
                    title: 'Branches',
                    messageTop: '<h5 class="text-center">Branch List</h5>',
                    messageBottom: null
                }
            ],
            "lengthMenu": [10, 20, 50, 100],
            "ajax": {
                'url': url,
                'type': 'GET',
                'headers': {'Authorization': 'JWT ' + self._helper.storage.getStorage('local', 'token').access},
                'error': function (x, status, error) {
                    console.log(status, x, error, '---------')
                    if (x.status === 401) {
                        if (error === "Unauthorized") {
                            $(document).ajaxComplete($.unblockUI);  // After complete the ajax request then unblock the window
                            window.location.href = "/logout/";
                        }
                    }
                },
            },
            "columns": [
                {"data": ""},
                {"data": "name"},
                {"data": "parent"},
                {"data": "is_active"},
            ],
            "columnDefs": [
                {
                    searchPanes: {
                        show: true,
                    },
                    targets: [2, 3],
                },
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        // console.log(data, 'type=', type, 'row=', row, 'meta=', meta)
                        // console.log('-----------', table.page.info(), table.page.info()['start'] +meta['row'])
                        console.log(data)
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                {
                    "targets": [1],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        console.log('data=', data, '============')
                        return data;
                    },
                },
                {
                    "targets": [2],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let title = '';
                        $.map(self._helper._storage.getStorage('session', 'parent'), function (v, i) {
                            if (v.id === data) title = v.text
                        });
                        console.log(title, '============================00000')
                        return title;
                    },
                },
                {
                    "targets": [3],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        if (data) return 'Active';
                        else return 'Inactive';
                    },
                },
            ],
        });
    }

    permission_list_row_select() {
        $('#permission_table tbody').on('click', 'tr', function () {
            // deselect a selected row
            if ($(this).hasClass('selected')) {
                $(this).toggleClass('selected');
                $('#edit_permission, #delete_permission').addClass('disabled');
            } else {
                // deselected all row
                $('#permission_table tbody').children().removeClass('selected');
                // selecting clicked row
                $(this).toggleClass('selected');
                $('#edit_permission, #delete_permission').removeClass('disabled');
            }
        });
    }

    redirect_to_permission_add_page() {
        let self = this;
        $('#add_permission').on('click', '', function () {
            let url = self.permission_add_url;
            window.open(url, "");
        });
    }

    redirect_to_permission_edit_page() {
        let self = this;
        $('#edit_permission').on('click', '', function () {
            if ($(this).hasClass('disabled')) {
                // button is disabled that means not table row selected, so do nothing
            } else {
                var table = $('#permission_table').DataTable();
                let url = '/permission/' + table.row('.selected').data().id;
                window.open(url, "_blank");
            }
        });
    }

    permission_delete() {
        let self = this;
        $('#delete_permission').on('click', '', function () {
            if ($(this).hasClass('disabled')) {
                // button is disabled that means not table row selected, so do nothing
            } else {
                var table = $('#permission_table').DataTable();
                let selected_row_data = table.row('.selected').data();
                swal({
                    title: "Are you sure?",
                    text: "You are going to delete permission: '" + selected_row_data.name + "'",
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                })
                    .then((willDelete) => {
                        if (willDelete) {
                            self._helper.blockUI();
                            $(document).ajaxComplete($.unblockUI);
                            let url = self._api + 'permission/' + selected_row_data.id + '/';
                            var promise = self._helper.httpRequest(url, 'DELETE');
                            promise.done(function (response) {
                                // redirect to dashboard
                                swal("Poof! Permission: '" + selected_row_data.name + "' has been deleted!", {
                                    icon: "success",
                                });
                                setTimeout(function (e) {
                                    window.location.replace("/permission");
                                }, 1000);
                            });
                            promise.fail(function (response) {
                                // send back to login page with an error notification
                                $.each(response.responseJSON, function (i, v) {
                                    $.each(v, function (j, w) {
                                        let message = i + ": " + w
                                        $.growl(message, {type: 'danger'});
                                    });
                                });
                            });
                        } else {
                            swal("Permission: '" + selected_row_data.name + "' is safe and active!", {
                                icon: "error",
                            });
                        }
                    });
            }
        });
    }

    set_feature_in_dropdown() {
        let self = this;
        let url = self._api + 'feature/?format=datatables';
        let feature_dropdown = $('#feature');

        var promise = this._helper.httpRequest(url);
        promise.done(function (response) {
            let data = [];
            $.each(response.data, function (i, v) {
                data.push({
                    id: v.id,
                    text: v.title,
                });
            });
            feature_dropdown.select2({
                data: data
            });
            // storing features in session storage for further use
            self._helper._storage.saveStorage('session', 'feature', data);
        });
        promise.fail(function (response) {
            alert(response.responseJSON.detail);
        });
    }

    permission_add() {
        let self = this;
        let permission_add_form = $('#permission_add_form');
        permission_add_form.submit(function (e) {
            e.preventDefault();
            let data_parsley = permission_add_form.parsley();
            if (!data_parsley.isValid()) {
                // Invalid Form Data
            } else {
                let data = new FormData($(this)[0]);
                if (data.has('is_active') === false) data.append('is_active', '0');

                let url = self._api + 'permission/';

                self._helper.blockUI();
                $(document).ajaxComplete($.unblockUI);

                $.ajax({
                    type: "post",
                    url: url,
                    data: data,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        $.growl('Successfully permission added', {type: 'success'});
                        setTimeout(function () {
                            window.location.href = "/permission";
                        }, 1500);

                    },
                    error: function (response) {
                        if (response.status == 403) {
                            $.growl(response.responseJSON.detail, {type: 'danger'});
                        } else {
                            $.each(response.responseJSON, function (i, v) {
                                $.each(v, function (j, w) {
                                    let message = i + ": " + w
                                    $.growl(message, {type: 'danger'});
                                });
                            });
                        }
                    }
                });
            }
        });
    }

    permission_edit_form_fillup() {
        let self = this;
        let permission_edit_form = $('#permission_edit_form');
        permission_edit_form.ready(function (e) {
            self._helper.blockUI();
            $(document).ajaxComplete($.unblockUI);
            let url = self._api + 'permission/' + permission_id + '/';
            var promise = self._helper.httpRequest(url, 'GET');
            promise.done(function (response) {
                function populate(frm, data) {
                    $.each(data, function (key, value) {
                        if (key == 'feature') $('[name=' + key + ']', frm).val(value).select2();
                        else if (key == 'is_active') (value == true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', frm).val(value);
                    });
                }

                populate(permission_edit_form, response);
            });
            promise.fail(function (response) {
                if (response.status == 403) {
                    $.growl(response.responseJSON.detail, {type: 'danger'});
                } else if (response.status == 404) {
                    $.growl('No permission found', {type: 'danger'});
                    setTimeout(function () {
                        window.location.href = "/permission";
                    }, 2000);
                } else {
                    $.each(response.responseJSON, function (i, v) {
                        $.each(v, function (j, w) {
                            let message = i + ": " + w
                            $.growl(message, {type: 'danger'});
                        });
                    });
                }
            });
        });
    }

    permission_edit() {
        let self = this;
        let permission_edit_form = $('#permission_edit_form');
        permission_edit_form.submit(function (e) {
            e.preventDefault();
            let data_parsley = permission_edit_form.parsley();
            if (!data_parsley.isValid()) {
                // Invalid Form Data
            } else {
                let data = new FormData($(this)[0]);
                if (data.has('is_active') === false) data.append('is_active', '0');

                let url = self._api + 'permission/' + permission_id + '/';

                self._helper.blockUI();
                $(document).ajaxStop($.unblockUI);
                $.ajax({
                    type: "patch",
                    url: url,
                    data: data,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        $.growl('Successfully permission updated', {type: 'success'});
                    },
                    error: function (response) {
                        $('body').unblock();
                        if (response.status == 403 || response.status == 404) {
                            $.growl(response.responseJSON.detail, {type: 'danger'});
                        } else {
                            $.each(response.responseJSON, function (i, v) {
                                $.each(v, function (j, w) {
                                    let message = i + ": " + w
                                    $.growl(message, {type: 'danger'});
                                });
                            });
                        }
                    }
                });
            }
        });
    }
}


let _branch = new Branch();

// getting all permissions
$(document).ready(function (e) {
    let user_permissions = request.user.permissions;
    if (window.location.pathname === '/branch/') {
        if ((user_permissions.indexOf("self_view.rbac_permission") > -1) || (user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $('.main-body').css('display', 'block');  // do display block as permission has permission to view
            _branch.provide_permission_based_access();
            _branch.branch_list();
            // _branch.permission_list_row_select();
            // _branch.redirect_to_permission_add_page();
            // _branch.redirect_to_permission_edit_page();
            // _branch.permission_delete();
        }
        else {
            $('.main-body').remove();
            swal({
                title: "No Access",
                text: "Sorry! you do not have permission to view this page",
                icon: "error",
                dangerMode: true,
            });
        }
    }
    else if (window.location.pathname == '/permission/add/') {
        if ((user_permissions.indexOf("add.rbac_permission") > -1) && (user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $('.main-body').css('display', 'block');  // do display block as permission has permission to view
            _permission.set_feature_in_dropdown();
            _permission.permission_add();  // rbac/permission_add.html
        } else {
            $('.main-body').remove();
            swal({
                title: "No Access",
                text: "Sorry! you do not have permission to view this page",
                icon: "error",
                dangerMode: true,
            });
        }
    } else if (window.location.pathname.match(/[\/permission\/\d\/]/g)) {
        if ((user_permissions.indexOf("detail_view.rbac_permission") > -1) && (user_permissions.indexOf("change.rbac_permission") > -1) &&
            ((user_permissions.indexOf("self_view.rbac_permission") > -1) || (user_permissions.indexOf("list_view.rbac_permission") > -1))) {
            $('.main-body').css('display', 'block');  // do display block as permission has permission to view
            _permission.set_feature_in_dropdown();
            _permission.permission_edit_form_fillup();  // rbac/permission_edit.html
            _permission.permission_edit();  // rbac/permission_edit.html
        } else {
            $('.main-body').remove();
            swal({
                title: "No Access",
                text: "Sorry! you do not have permission to view this page",
                icon: "error",
                dangerMode: true,
            });
        }
    }
});


