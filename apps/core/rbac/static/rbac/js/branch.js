// There are 6 types of permission
// 1. Add Branch 2. Edit/Change Branch 3. Delete Branch 4. Self View Branch
// 5. List View Branch 6. Detail View Branch
// To add a new branch, a role must have permission 1 & 5
// To delete an existing branch, a role must have permission 3 & 5
// To edit an existing branch (self), a role must have permission 2, 4 & 6
// To edit an existing branch (list), a role must have permission 2, 5 & 6


class Branch {
    constructor() {
        this._helper = new Helper();
        this.request_format = '?format=datatables'
        this._api = '/api/v1/';
        this.branch_list_url = this._api + 'branch/' + this.request_format;
        this.branch_add_url = '/branch/add/';
        this.user_permissions = request.user.permissions;
        this.current_editable_obj = null;
    }

    provide_permission_based_access() {
        // This function Check whether the user have the permissions to specific task
        let self = this;
        // If user_permissions array has not 'add.rbac_permission' or 'list_view.rbac_permission' then 'indexOf' will
        // return -1. That means user have not these permissions and the add branch button will be removed.
        if (!(self.user_permissions.indexOf("add.rbac_permission") > -1) || !(self.user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $('#add_branch').remove();
        }
        // If user_permissions array has not 'detail_view.rbac_permission' or 'change.rbac_permission' then 'indexOf' will
        // return -1. That means user have not these permissions and the edit branch button will be removed.
        if (!(self.user_permissions.indexOf("detail_view.rbac_permission") > -1) || !(self.user_permissions.indexOf("change.rbac_permission") > -1)) {
            $("#edit_branch").remove();
        }
        // If user_permissions array has not 'self_view.rbac_permission' or 'list_view.rbac_permission' then 'indexOf' will
        // return -1. That means user have not these permissions and the edit branch button will be removed.
        if (!(self.user_permissions.indexOf("self_view.rbac_permission") > -1) || !(self.user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $("#edit_branch").remove();
        }
        // If user_permissions array has not 'delete.rbac_permission' or 'list_view.rbac_permission' then 'indexOf' will
        // return -1. That means user have not these permissions and the delete branch button will be removed.
        if (!(self.user_permissions.indexOf("delete.rbac_permission") > -1) || !(self.user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $("#delete_branch").remove();
        }
    }

    branch_list() {
        // This function will show us the list of all branch
        let self = this;
        let url = self.branch_list_url;
        self._helper.blockUI();   // Calling the method for loading style
        // When the ajax request processing is done then ajaxStop() function will be called and unblock the window
        $(document).ajaxStop($.unblockUI);


        let table = $('#branch_table').DataTable({
            "processing": true,  // Enable or disable the display of a 'processing' indicator when the table is being processed (e.g. a sort).
            // "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            // "dom": '<"mb-3"B>flrtip',
            "searchPanes": {
                layout: 'columns-4'
            },
            "dom": 'P<"mb-3"B>flrtip',
            "buttons": [
                'colvis',
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
                {"data": "parent_human_readable"},
                {"data": "subbranches"},
                {"data": "user"},
                {"data": "is_active"},
                {"data": "address"},
            ],
            "columnDefs": [
                {
                    searchPanes: {
                        show: true,
                    },
                    targets: [2, 3, 4],
                },
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
                        if (data) return data;
                        else return 'Base Branch';
                    },
                },
                {
                    "targets": [3],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return data.length
                    },
                },
                {
                    "targets": [4],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return data.length
                    },
                },
                {
                    "targets": [5],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        if (data) return 'Active';
                        else return 'Inactive';
                    },
                },
                {
                    "targets": [6],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        return data;
                    },
                },
            ],
        });


    }

    branch_list_row_select() {
        $('#branch_table tbody').on('click', 'tr', function () {
            // Deselect a selected row
            if ($(this).hasClass('selected')) {
                $(this).toggleClass('selected');
                $('#edit_branch, #delete_branch').addClass('disabled');
            } else {
                // deselected all row
                $('#branch_table tbody').children().removeClass('selected');
                // Selecting clicked row
                $(this).toggleClass('selected');
                $('#edit_branch, #delete_branch').removeClass('disabled');
            }
        });
    }

    redirect_to_branch_add_page() {
        let self = this;
        $('#add_branch').on('click', '', function () {
            let url = self.branch_add_url;
            window.open(url, "_self");  // open the link in new tab=default is _blank
        });
    }

    redirect_to_branch_edit_page() {
        let self = this;
        $('#edit_branch').on('click', '', function () {
            if ($(this).hasClass('disabled')) {
                // button is disabled that means not table row selected, so do nothing
            } else {
                let table = $('#branch_table').DataTable();
                let url = '/branch/' + table.row('.selected').data().hashed_id;
                window.open(url, '_self');
            }
        });
    }


    set_parent_branch_in_dropdown() {
        let self = this;
        let url = self._api + 'branch/' + self.request_format;
        let branch_parent_dropdown = $('#branch');

        var promise = this._helper.httpRequest(url);
        promise.done(function (response) {
            let data = [];
            $.each(response.data, function (i, v) {
                data.push({
                    id: v.hashed_id,
                    text: v.name.concat(v.parent_human_readable !== null ? " (" + v.parent_human_readable + ")" : " (Base Branch)"),
                });
            });
            branch_parent_dropdown.select2({
                data: data
            });

            // if (window.location.pathname.match(/^\/branch\/([a-zA-Z0-9]){1,16}\/$/g)) {
            if (window.location.pathname !== self.branch_add_url) {
                // if the location is in branch edit then run below function.
                self.branch_edit_form_fillup();  // As this function take less time to complete response thats why we are
                // calling it here. to create a dependency.
            }

        });
        promise.fail(function (response) {
            alert(response.responseJSON.detail);
        });
    }

    set_group_in_dropdown() {
        let self = this;
        let url = self._api + 'group/' + self.request_format;
        let group_dropdown = $('#group');

        let promise = this._helper.httpRequest(url);
        promise.done(function (response) {
            let data = [];
            $.each(response.data, function (index, value) {
                data.push({
                    id: value.hashed_id,
                    text: value.name
                })
            });
            group_dropdown.select2({
                data: data
            });

            self.set_parent_branch_in_dropdown();
        });
        promise.fail(function (response) {
            alert(response.responseJSON.detail)
        });
    }

    set_user_in_dropdown() {
        let self = this;
        let url = self._api + 'user/' + self.request_format;
        let user_dropdown = $("#user");

        let promise = self._helper.httpRequest(url);
        promise.done(function (response) {
            let data = []
            $.each(response.data, function (index, value) {
                data.push({
                    id: value.id,
                    text: value.first_name
                });
            });
            user_dropdown.select2({
                data: data
            });
            self.set_group_in_dropdown();
        });
        promise.fail(function (response) {
            alert(response.responseJSON.detail);
        });
    }


    branch_add() {
        let self = this;
        let branch_add_form = $('#branch_add_form');
        self.set_user_in_dropdown();
        branch_add_form.submit(function (e) {
            e.preventDefault();
            let data_parsley = branch_add_form.parsley();
            if (!data_parsley.isValid()) {
                // Invalid Form Data
            } else {
                let data = {}

                data.name = $("input[name='name']").val();
                data.address = $("input[name='address']").val();
                // data.branch = $("select[name='branch']").val();
                data.group = $("select[name='group']").val();
                data.user = $("select[name='user']").val();
                data.is_active = $("input[name='is_active']").val();
                data.parent = $("select[name='branch']").val() === "" ? null : $("select[name='branch']").val();

                let url = self._api + 'branch/' + self.request_format;
                // self._helper.blockUI();
                // $(document).ajaxComplete($.unblockUI);

                let promise = self._helper.httpRequest(url, 'POST', JSON.stringify(data));
                promise.done(function (response) {
                    $.growl('Successfully branch added', {type: 'success'});
                    setTimeout(function () {
                        window.location.href = "/branch";
                    }, 1500);
                });

                promise.fail(function (response) {
                    if (response.status === 403) {
                        $.growl(response.responseJSON.detail, {type: 'danger'})
                    } else {
                        // $.unblockUI
                        $.each(response.responseJSON, function (key, v) {
                            if ($.isArray(response.responseJSON)) {
                                $.growl(v, {type: 'danger'});
                            } else {
                                $.each(v, function (j, w) {
                                    let message = w
                                    if (w.indexOf("The fields name, parent must make a unique set.") > -1) {
                                        message = "'Sub Branch' with this name already exists for this 'Base Branch'."
                                    }
                                    $.growl(message, {type: 'danger'});
                                });
                            }

                        });
                    }
                });
            }

        });
    }


    branch_edit_form_fillup() {
        let self = this;
        let branch_edit_form = $('#branch_edit_form');
        branch_edit_form.ready(function (e) {
            self._helper.blockUI();
            $(document).ajaxComplete($.unblockUI);
            let url = self._api + 'branch/' + branch_hashed_id + '/';
            let promise = self._helper.httpRequest(url, 'GET');
            promise.done(function (response) {
                function populate(formWillBeFilled, data) {
                    $.each(data, function (key, value) {
                        // console.log('key = ', key , 'value = ', value)
                        if (key === 'parent_hashed_id') $("[name='branch']", formWillBeFilled).val(value).select2();
                        else if (key === 'group_hashed_id') $('[name="group"]', formWillBeFilled).val(value).select2();
                        else if (key === 'user') $('[name=' + key + ']', formWillBeFilled).val(value).select2();
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else if (key === 'address') $('[name=' + key + ']', formWillBeFilled).val(value);
                        else $('[name=' + key + ']', formWillBeFilled).val(value);


                        // IF branch is base branch then add a option written with 'Base Branch'
                        if (key === 'parent' && data[key] === null) {
                            $("#branch_label").append('  (This is BASE BRANCH)')
                            $("#branch_label").css('color', 'blue')
                        }
                    });
                }

                populate(branch_edit_form, response);
                self.current_editable_obj = response;
            });

            promise.fail(function (response) {
                if (response.status === 403) {
                    $.growl(response.responseJSON.detail, {type: 'danger'});
                } else if (response.status === 404) {
                    $.growl('No branch found', {type: 'danger'});
                    setTimeout(function () {
                        window.location.href = "/branch";
                    }, 2000);
                } else {
                    $.each(response.responseJSON, function (index, value) {
                        $.each(value, function (j, w) {
                            let message = index + ": " + w
                            $.growl(message, {type: 'danger'});
                        });
                    });
                }
            });
        });
    }


    branch_edit() {
        let self = this;
        let branch_edit_form = $('#branch_edit_form');
        branch_edit_form.submit(function (e) {
            e.preventDefault();
            let data_parsley = branch_edit_form.parsley();
            if (!data_parsley.isValid()) {
                // Invalid Form Data
            } else {
                let data = {};
                if (self.current_editable_obj.name !== $("input[name='name']").val() ||
                    self.current_editable_obj.parent_hashed_id !== $("select[name='branch']").val()) {
                    data.name = $("input[name='name']").val();
                    data.parent = $("select[name='branch']").val() === "" ? null : $("select[name='branch']").val();
                }

                data.address = $("input[name='address']").val();
                // data.branch = $("select[name='branch']").val();
                data.group = $("select[name='group']").val();
                data.user = $("select[name='user']").val();
                data.is_active = $("input[name='is_active']").val();


                let url = self._api + 'branch/' + branch_hashed_id + '/';
                self._helper.blockUI();
                $(document).ajaxComplete($.unblockUI);

                let promise = self._helper.httpRequest(url, 'PATCH', JSON.stringify(data));
                promise.done(function (response) {
                    $.growl('Branch successfully updated', {type: 'success'});
                    setTimeout(function () {
                        window.location.href = '/branch';
                    }, 1500);
                });
                promise.fail(function (response) {
                    if (response.status === 403 || response.status === 404) {
                        $.growl(response.responseJSON.detail, {type: 'danger'});
                    } else {
                        $.each(response.responseJSON, function (key, value) {
                            if ($.isArray(response.responseJSON)) {
                                $.growl(value, {type: 'danger'});
                            } else {
                                $.each(value, function (i, w) {
                                    let message = w
                                    if (w.indexOf("The fields name, parent must make a unique set.") > -1) {
                                        message = "'Sub Branch' with this name already exists for this 'Base Branch'."
                                    }
                                    $.growl(message, {type: 'danger'});
                                });
                            }

                        });
                    }
                });
            }
        });
    }


    branch_delete() {
        let self = this;
        $('#delete_branch').on('click', '', function () {
            if ($(this).hasClass('disabled')) {
                // button is disabled that means no table row is selected, so do nothing
            } else {
                let table = $('#branch_table').DataTable();
                let selected_row_data = table.row('.selected').data();
                swal({
                    title: "Are you sure?",
                    text: "You are going to delete branch: '" + selected_row_data.name + "'.",
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                })
                    .then((willDelete) => {
                        if (willDelete) {
                            self._helper.blockUI();
                            $(document).ajaxComplete($.unblockUI);
                            let url = self._api + 'branch/' + selected_row_data.hashed_id + '/';
                            let promise = self._helper.httpRequest(url, 'DELETE');
                            promise.done(function (response) {
                                //
                                swal("Branch: '" + selected_row_data.name + "' has been deleted!", {icon: "success",});
                                setTimeout(function (e) {
                                    window.location.replace("/branch");
                                }, 1000);
                            });
                            promise.fail(function (response) {
                                // send back to login page with an error notification
                                $.each(response.responseJSON, function (index, value) {
                                    $.each(value, function (j, w) {
                                        let message = i + ": " + w
                                        $.growl(message, {type: 'danger'});
                                    });
                                });
                            });
                        } else {
                            swal("Branch: '" + selected_row_data.name + "' is safe and active!", {
                                icon: "error",
                            });
                        }
                    });
            }
        });
    }
}


let _branch = new Branch();


// Getting all branches
$(document).ready(function (e) {
    let user_permissions = request.user.permissions;
    if (window.location.pathname === '/branch/') {
        if ((user_permissions.indexOf("self_view.rbac_permission") > -1) || (user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $('.main-body').css('display', 'block');    // do display block as permission has permission to view
            _branch.provide_permission_based_access();
            _branch.branch_list();
            _branch.branch_list_row_select();
            _branch.redirect_to_branch_add_page();
            _branch.branch_delete();
            _branch.redirect_to_branch_edit_page();

        } else {
            $('.main-body').remove();
            swal({
                title: "No Access",
                text: "Sorry! You do not have permission to view this pabe",
                icon: "error",
                dangerMode: true,
            });
        }

    } else if (window.location.pathname === '/branch/add/') {
        if ((user_permissions.indexOf("add.rbac_permission") > -1) && (user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $('.main-body').css('display', 'block');  // do display block as permission has permission to view

            // _branch.set_parent_branch_in_dropdown();
            // _branch.set_group_in_dropdown();
            // _branch.set_user_in_dropdown();
            _branch.branch_add();  // rbac/branch_add.html

        } else {
            $('.main-body').remove();
            swal({
                title: "No Access",
                text: "Sorry! you do not have permission to view this page",
                icon: "error",
                dangerMode: true,
            });
        }
    } else if (window.location.pathname.match(/^\/branch\/([a-zA-Z0-9]){1,16}\/$/g)) {
        if (user_permissions.indexOf("detail_view.rbac_permission") > -1 && (user_permissions.indexOf("change.rbac_permission") > -1) &&
            ((user_permissions.indexOf("self_view.rbac_permission") > -1) || (user_permissions.indexOf("list_view.rbac_permission") > -1))) {

            $('.main-body').css('display', 'block');   // do display block as user has permission to view.
            // _branch.set_parent_branch_in_dropdown();
            // _branch.set_group_in_dropdown();
            _branch.set_user_in_dropdown();
            // _branch.branch_edit_form_fillup();
            _branch.branch_edit();

        }
    }


});