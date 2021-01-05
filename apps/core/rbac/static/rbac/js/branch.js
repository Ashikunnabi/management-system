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
        this._api = '/api/v1/';
        this.branch_list_url = this._api + 'branch/';
        this.branch_add_url = '/branch/add/';
        this.user_permissions = request.user.permissions;
        this.current_editable_obj = null;

        this.Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 1300,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        })
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
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
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
                {"data": "branch_tree_view"},
                {"data": "subbranches"},
                {"data": "user"},
                {"data": "is_active"},
                {"data": "address"},
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
                        if (row.parent !== null) {
                            let splitText = data.split('/')
                            let lastPart = splitText.pop()
                            return splitText.join('/')
                        } else return 'Base Branch';
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
        let table = $('#branch_table').DataTable();

        $('#edit_branch').on('click', '', function () {
            if ($(this).hasClass('disabled')) {
                // button is disabled that means not table row selected, so do nothing
            } else if (table.row('.selected').data().is_active_parent !== null && !table.row('.selected').data().is_active_parent) {
                // branch can not be modified if it's parent is inactive
                self.Toast.fire({
                    icon: 'info',
                    title: "<p style='color: dark;'>Please active it's parent branch to edit <p>",
                    background: '#c2e7ff',
                    timer: 3000,
                })
            } else {
                let url = '/branch/' + table.row('.selected').data().hashed_id;
                window.open(url, '_self');
            }
        });
    }


    set_parent_branch_in_dropdown() {
        let self = this;
        let url = self._api + 'branch/';
        let branch_parent_dropdown = $('#branch');

        let promise = this._helper.httpRequest(url);
        promise.done(function (response) {
            let data = [];
            $.each(response, function (i, v) {
                if (window.location.pathname === self.branch_add_url) {
                    if (v.is_active) {
                        data.push({
                            id: v.hashed_id,
                            text: v.branch_tree_view,
                        });
                    }
                } else {
                    data.push({
                        id: v.hashed_id,
                        text: v.branch_tree_view,
                    });
                }
            });
            branch_parent_dropdown.select2({
                data: data
            });
            if (window.location.pathname !== self.branch_add_url) {
                // if the location is in branch edit then run below function.
                self.branch_edit_form_fillup();  // As this function take less time to complete response that's why we are
                // calling it here to create a dependency.
            }
        });

        promise.fail(function (response) {
            alert(response.responseJSON.detail);
        });
    }

    set_group_in_dropdown() {
        let self = this;
        let url = self._api + 'group/';
        let group_dropdown = $('#group');

        let promise = this._helper.httpRequest(url);
        promise.done(function (response) {
            let data = [];
            $.each(response, function (index, value) {
                if (value.is_active) {
                    data.push({
                        id: value.hashed_id,
                        text: value.name
                    })
                }
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
        let url = self._api + 'user/';
        let user_dropdown = $("#user");
        let promise = self._helper.httpRequest(url);

        promise.done(function (response) {
            let data = []
            $.each(response, function (index, value) {
                if (value.is_active) {
                    data.push({
                        id: value.id,
                        text: value.first_name
                    });
                }
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

                let url = self._api + 'branch/';
                self._helper.blockUI();
                $(document).ajaxComplete($.unblockUI);

                let promise = self._helper.httpRequest(url, 'POST', JSON.stringify(data));
                promise.done(function (response) {
                    self.Toast.fire({
                        icon: 'success',
                        title: "<p style='color: dark;'>Successfully branch added<p>",
                        background: '#c4ffda',
                    })
                    setTimeout(function () {
                        window.location.href = "/branch";
                    }, 1100);
                });

                promise.fail(function (response) {
                    if (response.status === 403) {
                        self.Toast.fire({
                            icon: 'error',
                            title: "<p style='color: dark;'>" + response.responseJSON.detail + "<p>",
                            background: '#ffabab',
                        });
                    } else {
                        $.each(response.responseJSON, function (key, v) {
                            if ($.isArray(response.responseJSON)) {
                                self.Toast.fire({
                                    icon: 'error',
                                    title: "<p style='color: dark;'>" + v + "<p>",
                                    background: '#ffabab',
                                });
                            } else {
                                $.each(v, function (j, w) {
                                    let message = w
                                    if (w.indexOf("The fields name, parent must make a unique set.") > -1) {
                                        message = "'Sub Branch' with this name already exists for this 'Base Branch'."
                                    }
                                    self.Toast.fire({
                                        icon: 'error',
                                        title: "<p style='color: dark;'>" + message + "<p>",
                                        background: '#ffabab',
                                    })

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

                    self.Toast.fire({
                        icon: 'error',
                        title: "<p style='color: dark;'>" + response.responseJSON.detail + "<p>",
                        background: '#ffabab',
                    });
                } else if (response.status === 404) {
                    self.Toast.fire({
                        icon: 'error',
                        title: "<p style='color: dark;'>No branch found<p>",
                        background: '#ffabab',
                    });
                    setTimeout(function () {
                        window.location.href = "/branch";
                    }, 2000);
                } else {
                    $.each(response.responseJSON, function (index, value) {
                        if ($.isArray(response.responseJSON)) {
                            self.Toast.fire({
                                icon: 'error',
                                title: "<p style='color: dark;'>" + value + "<p>",
                                background: '#ffabab',
                            });
                        } else {
                            $.each(value, function (j, w) {
                                let message = index + ": " + w
                                self.Toast.fire({
                                    icon: 'error',
                                    title: "<p style='color: dark;'>" + message + "<p>",
                                    background: '#ffabab',
                                });
                            });
                        }

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
                let parent = $("select[name='branch']").val() === "" ? null : $("select[name='branch']").val();
                if (self.current_editable_obj.name !== $("input[name='name']").val() || (
                    self.current_editable_obj.parent_hashed_id !== parent)) {
                    data.name = $("input[name='name']").val();
                    data.parent = parent;
                }

                data.address = $("input[name='address']").val();
                data.group = $("select[name='group']").val();
                data.user = $("select[name='user']").val();
                data.is_active = $("input[name='is_active']").val();

                let url = self._api + 'branch/' + branch_hashed_id + '/';
                self._helper.blockUI();
                $(document).ajaxComplete($.unblockUI);

                let promise = self._helper.httpRequest(url, 'PATCH', JSON.stringify(data));
                promise.done(function (response) {
                    self.Toast.fire({
                        icon: 'success',
                        title: "<p style='color: dark;'>Branch successfully updated<p>",
                        background: '#c4ffda',
                    });
                    setTimeout(function () {
                        window.location.href = '/branch';
                    }, 1500);
                });
                promise.fail(function (response) {
                    if (response.status === 403 || response.status === 404) {
                        self.Toast.fire({
                            icon: 'error',
                            title: "<p style='color: dark;'>" + response.responseJSON.detail + "<p>",
                            background: '#ffabab',
                        });
                    } else {
                        $.each(response.responseJSON, function (key, value) {
                            if ($.isArray(response.responseJSON)) {
                                self.Toast.fire({
                                    icon: 'error',
                                    title: "<p style='color: dark;'>" + value + "<p>",
                                    background: '#ffabab',
                                });
                            } else {
                                $.each(value, function (i, w) {
                                    let message = w
                                    if (w.indexOf("The fields name, parent must make a unique set.") > -1) {
                                        message = "'Sub Branch' with this name already exists for this 'Base Branch'."
                                    }
                                    self.Toast.fire({
                                        icon: 'error',
                                        title: "<p style='color: dark;'>" + message + "<p>",
                                        background: '#ffabab',
                                    });
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

                Swal.fire({
                    title: "Are you sure to delete branch '" + selected_row_data.name.toUpperCase() + "'?",
                    html: "Everything under this branch will be deleted.</br> <b style='background-color: yellow;'>You can't recover it again</b>",
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
                        let limit = 10
                        let progressBarTimer = setInterval(() => {
                            if (limit === 0) {
                                clearInterval(progressBarTimer);
                            }
                            $('#count_progress').val(limit * 10);
                            limit--;
                        }, 1000);
                        setTimeout(() => {
                            Swal.enableButtons();
                        }, 11000);
                    }

                })
                    .then((willDelete) => {
                        if (willDelete.isConfirmed) {
                            self._helper.blockUI();
                            $(document).ajaxComplete($.unblockUI);
                            let url = self._api + 'branch/' + selected_row_data.hashed_id + '/';
                            let promise = self._helper.httpRequest(url, 'DELETE');
                            promise.done(function (response) {
                                Swal.fire("Branch: '" + selected_row_data.name + "' has been deleted!", '', 'success');
                                setTimeout(function (e) {
                                    window.location.replace("/branch");
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
                            Swal.fire("Branch: '" + selected_row_data.name + "' is safe!", '', 'info');
                        }
                    });
            }
        });
    }
}


let _branch = new Branch();


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
            Swal.fire({
                title: "No Access",
                text: "Sorry! You do not have permission to view this page",
                icon: "warning",
                iconColor: "red",
            })

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
            Swal.fire({
                title: "No Access",
                text: "Sorry! You do not have permission to view this page",
                icon: "warning",
                iconColor: "red",
            })
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

        } else {
            $('.main-body').remove();
            Swal.fire({
                title: "No Access",
                text: "Sorry! You do not have permission to view this page",
                icon: "warning",
                iconColor: "red",
            })
        }
    }


});