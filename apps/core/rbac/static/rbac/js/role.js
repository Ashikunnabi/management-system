// There are 6 types of permission
// 1. Add Role 2. Edit Role 3. Delete Role 4. Self View Role
// 5. List View Role 6. Detail View Role
// To add a new role, a role must have permission 1 & 5
// To delete an exixting role, a role must have permission 3 & 5
// To edit an exixting role (self), a role must have permission 2, 4 & 6
// To edit an exixting role (list), a role must have permission 2, 5 & 6


class Role {
    constructor() {
        this._helper = new Helper();
        this._api = '/api/v1/';
        this.role_list_url = this._api + 'role/';
        this.role_add_url = '/role/add/';
        this.user_permissions = request.user.permissions;
    }

    provide_permission_based_access() {
        let self = this;
        if (!(self.user_permissions.indexOf("add.rbac_role") > -1) || !(self.user_permissions.indexOf("list_view.rbac_role") > -1)) {
            $('#add_role').remove();
        }
        if (!(self.user_permissions.indexOf("detail_view.rbac_role") > -1) || !(self.user_permissions.indexOf("change.rbac_role") > -1)) {
            $('#edit_role').remove();
        }
        if (!(self.user_permissions.indexOf("self_view.rbac_role") > -1) && !(self.user_permissions.indexOf("list_view.rbac_role") > -1)) {
            $('#edit_role').remove();
        }
        if (!(self.user_permissions.indexOf("delete.rbac_role") > -1) || !(self.user_permissions.indexOf("list_view.rbac_role") > -1)) {
            $('#delete_role').remove();
        }
    }

    role_list() {
        let self = this;
        let url = self.role_list_url;
        self._helper.blockUI();
        $(document).ajaxStop($.unblockUI);
        let table = $('#role_table').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                'copy',
                'excel',
                'pdf',
                'csv',
                {
                    extend: 'print',
                    title: 'Roles',
                    messageTop: '<h5 class="text-center">Role List</h5>',
                    messageBottom: null
                }
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": {
                'url': url,
                'type': 'GET',
                'headers': {'Authorization': 'JWT ' + self._helper.storage.getStorage('local', 'token').access},
                'error': function (x, status, error) {
                    if (x.status === 401) {
                        if (error === "Unauthorized") {
                            $(document).ajaxComplete($.unblockUI);
                            window.location.href = "/logout/";
                        }
                    }
                },
            },
            "columns": [
                {"data": ""},
                {"data": "name"},
                {"data": "is_active"},
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                {
                    "targets": [1],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return data;
                    },
                },
                {
                    "targets": [2],
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

    role_list_row_select() {
        $('#role_table tbody').on('click', 'tr', function () {
            // deselect a selected row
            if ($(this).hasClass('selected')) {
                $(this).toggleClass('selected');
                $('#edit_role, #delete_role').addClass('disabled');
            } else {
                // deselected all row
                $('#role_table tbody').children().removeClass('selected');
                // selecting clicked row
                $(this).toggleClass('selected');
                $('#edit_role, #delete_role').removeClass('disabled');
            }
        });
    }

    redirect_to_role_add_page() {
        let self = this;
        $('#add_role').on('click', '', function () {
            let url = self.role_add_url;
            window.open(url, "_self");
        });
    }

    redirect_to_role_edit_page() {
        let self = this;
        $('#edit_role').on('click', '', function () {
            if ($(this).hasClass('disabled')) {
                // button is disabled that means not table row selected, so do nothing
            } else {
                var table = $('#role_table').DataTable();
                let url = '/role/' + table.row('.selected').data().id;
                window.open(url, "_self");
            }
        });
    }

    role_delete() {
        let self = this;
        $('#delete_role').on('click', '', function () {
            if ($(this).hasClass('disabled')) {
                // button is disabled that means not table row selected, so do nothing
            } else {
                var table = $('#role_table').DataTable();
                let selected_row_data = table.row('.selected').data();

                let limit = 10
                let timer;  // timer is for clear the settimeout
                let progressBarTimer = setInterval(() => {
                    if (limit === 0) {
                        clearInterval(progressBarTimer);
                    }
                    $('#count_progress').val(limit * 10);
                    limit--;
                }, 1000);

                Swal.fire({
                    title: "Are you sure to delete role '" + selected_row_data.name.toUpperCase() + "'?",
                    html: "Everything under this role will be deleted.</br> <b style='background-color: yellow;'>You can't recover it again</b>",
                    icon: "warning",
                    iconColor: "red",
                    showDenyButton: true,
                    // showCancelButton: true,
                    confirmButtonText: `Yes, delete`,
                    denyButtonText: `No`,
                    footer: "<progress id='count_progress' value='100' max='100' style='width: 70%;'></progress>",
                    didOpen: function () {
                        $(".swal2-confirm").css('background-color', '#ff5d4f')
                        $(".swal2-deny").css('background-color', 'gray')
                        $(".swal2-deny").css('margin-left', '50px')
                        Swal.disableButtons();

                        timer = setTimeout(() => {
                            Swal.enableButtons();
                        }, 11000);
                    },
                    didClose: () => {
                        clearInterval(progressBarTimer)
                        clearTimeout(timer)
                    }
                })
                    .then((willDelete) => {
                        if (willDelete.isConfirmed) {
                            self._helper.blockUI();
                            $(document).ajaxComplete($.unblockUI);
                            let url = self._api + 'role/' + selected_row_data.id + '/';
                            let promise = self._helper.httpRequest(url, 'DELETE');
                            promise.done(function (response) {
                                Swal.fire("Role: '" + selected_row_data.name.toUpperCase() + "' has been deleted!", '', 'success');
                                setTimeout(function (e) {
                                    window.location.replace("/role");
                                }, 1000);
                            });
                            promise.fail(function (response) {
                                // send back to login page with an error notification
                                $.each(response.responseJSON, function (index, value) {
                                    if ($.isArray(response.responseJSON)) {
                                        self.Toast.fire({
                                            icon: 'error',
                                            title: "<p style='color: dark;'>" + value + "<p>",
                                            background: '#ffabab',
                                        });
                                    } else {
                                        $.each(value, function (j, w) {
                                            let message = i + ": " + w
                                            self.Toast.fire({
                                                icon: 'error',
                                                title: "<p style='color: dark;'>" + message + "<p>",
                                                background: '#ffabab',
                                            });
                                        });
                                    }
                                });
                            });
                        } else if (willDelete.isDenied) {
                            Swal.fire("Role: '" + selected_row_data.name.toUpperCase() + "' is safe!", '', 'info');
                        }
                    });
            }
        });
    }

    set_permission_in_dropdown() {
        let self = this;
        let url = self._api + 'permission/';
        let permission_dropdown = $('#permission');

        var promise = this._helper.httpRequest(url);
        promise.done(function (response) {
            let data = [];
            $.each(response, function (i, v) {
                if (v.is_active) {
                    data.push({
                        id: v.id,
                        text: v.name,
                    });
                }
            });
            permission_dropdown.select2({
                data: data
            });

            if (window.location.pathname !== self.role_add_url) {
                // if the location is in branch edit then run below function.

                // Calling 'role_edit_form_fillup' here because 'set_permission_in_dropdown' take time to set the
                // permissions in dropdown. If we don't call 'role_edit_form_fillup' here 'role_edit_form_fillup' will
                // try to fill the form before the permission is set into the dropdown as it take less time to
                //  complete response.
                self.role_edit_form_fillup();
            }
        });
        promise.fail(function (response) {
            alert(response.responseJSON.detail);
        });


    }

    role_add() {
        let self = this;
        let role_add_form = $('#role_add_form');
        role_add_form.submit(function (e) {
            e.preventDefault();
            let data_parsley = role_add_form.parsley();
            if (!data_parsley.isValid()) {
                // Invalid Form Data
            } else {
                let data = new FormData($(this)[0]);
                if (data.has('is_active') === false) data.append('is_active', '0');

                let url = self._api + 'role/';

                self._helper.blockUI();
                $(document).ajaxComplete($.unblockUI);

                $.ajax({
                    type: "post",
                    url: url,
                    data: data,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        $.growl('Successfully role added', {type: 'success'});
                        setTimeout(function () {
                            window.location.href = "/role";
                        }, 1500);

                    },
                    error: function (response) {
                        if (response.status === 403) {
                            $.growl(response.responseJSON.detail, {type: 'danger'});
                        } else {
                            $.each(response.responseJSON, function (i, v) {
                                $.each(v, function (j, w) {
                                    let message = i + ": " + w;
                                    $.growl(message, {type: 'danger'});
                                });
                            });
                        }
                    }
                });
            }
        });
    }

    role_edit_form_fillup() {
        let self = this;
        let role_edit_form = $('#role_edit_form');
        role_edit_form.ready(function (e) {
            self._helper.blockUI();
            $(document).ajaxComplete($.unblockUI);
            let url = self._api + 'role/' + role_id + '/';
            var promise = self._helper.httpRequest(url, 'GET');
            promise.done(function (response) {
                function populate(frm, data) {
                    $.each(data, function (key, value) {
                        if (key === 'permission') $('[name=' + key + ']', frm).val(value).select2();
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', frm).val(value);
                    });
                }

                populate(role_edit_form, response);
            });
            promise.fail(function (response) {
                if (response.status === 403) {
                    $.growl(response.responseJSON.detail, {type: 'danger'});
                } else if (response.status === 404) {
                    $.growl('No role found', {type: 'danger'});
                    setTimeout(function () {
                        window.location.href = "/role";
                    }, 2000);
                } else {
                    $.each(response.responseJSON, function (i, v) {
                        $.each(v, function (j, w) {
                            let message = i + ": " + w;
                            $.growl(message, {type: 'danger'});
                        });
                    });
                }
            });
        });
    }

    role_edit() {
        let self = this;
        let role_edit_form = $('#role_edit_form');
        role_edit_form.submit(function (e) {
            e.preventDefault();
            let data_parsley = role_edit_form.parsley();
            if (!data_parsley.isValid()) {
                // Invalid Form Data
            } else {
                let data = new FormData($(this)[0]);
                if (data.has('is_active') === false) data.append('is_active', '0');

                let url = self._api + 'role/' + role_id + '/';

                self._helper.blockUI();
                $(document).ajaxStop($.unblockUI);
                $.ajax({
                    type: "patch",
                    url: url,
                    data: data,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        $.growl('Successfully role updated', {type: 'success'});
                        window.location.href = '/role';
                    },
                    error: function (response) {
                        $('body').unblock();
                        if (response.status === 403 || response.status === 404) {
                            $.growl(response.responseJSON.detail, {type: 'danger'});
                        } else {
                            $.each(response.responseJSON, function (i, v) {
                                $.each(v, function (j, w) {
                                    let message = i + ": " + w;
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


let _role = new Role();

// getting all roles
$(document).ready(function (e) {
    let user_permissions = request.user.permissions;
    if (window.location.pathname === '/role/') {
        if ((user_permissions.indexOf("self_view.rbac_role") > -1) || (user_permissions.indexOf("list_view.rbac_role") > -1)) {
            $('.main-body').css('display', 'block');  // do display block as role has role to view
            _role.provide_permission_based_access();
            _role.role_list();
            _role.role_list_row_select();
            _role.redirect_to_role_add_page();
            _role.redirect_to_role_edit_page();
            _role.role_delete();
        } else {
            $('.main-body').remove();
            swal({
                title: "No Access",
                text: "Sorry! you do not have permission to view this page",
                icon: "error",
                dangerMode: true,
            });
        }
    } else if (window.location.pathname === '/role/add/') {
        if ((user_permissions.indexOf("add.rbac_role") > -1) && (user_permissions.indexOf("list_view.rbac_role") > -1)) {
            $('.main-body').css('display', 'block');  // do display block as role has role to view
            _role.set_permission_in_dropdown();
            _role.role_add();  // rbac/role_add.html 
        } else {
            $('.main-body').remove();
            swal({
                title: "No Access",
                text: "Sorry! you do not have permission to view this page",
                icon: "error",
                dangerMode: true,
            });
        }
    } else if (window.location.pathname.match(/[\/role\/\d\/]/g)) {
        if ((user_permissions.indexOf("detail_view.rbac_role") > -1) && (user_permissions.indexOf("change.rbac_role") > -1) &&
            ((user_permissions.indexOf("self_view.rbac_role") > -1) || (user_permissions.indexOf("list_view.rbac_role") > -1))) {
            $('.main-body').css('display', 'block');  // do display block as role has role to view
            _role.set_permission_in_dropdown();
            // _role.role_edit_form_fillup();  // rbac/role_edit.html
            _role.role_edit();  // rbac/role_edit.html
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


