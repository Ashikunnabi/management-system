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
        this.branch_list_url = this._api + 'branch/?format=datatables';
        this.branch_add_url = '/branch/add/';
        this.user_permissions = request.user.permissions;
    }

    provide_permission_based_access() {
        // This function Check whether the user have the permissions to specific task
        let self = this;
        // If user_permissions array has not 'add.rbac_permission' or 'list_view.rbac_permission' then 'indexOf' will
        // return -1. That means user have not these permissions and the add branch button will be removed.
        if (!(self.user_permissions.indexOf("add.rbac_permission") > -1) || !(self.user_permissions.indexOf("list_view.rbac_permission")) > -1) {
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
                {"data": "parent"},
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
                        else return '-';
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


}

let _branch = new Branch();


// Getting all branches
$(document).ready(function (e) {
    let user_permissions = request.user.permissions;
    // if (window.location.pathname ===  '/branch/') {
    //     if ((user_permissions.indexOf("self_view.rbac_permission") > -1) || (user_permissions.indexOf("list_view.rbac_permission") > -1)) {
    //         $('.main-body').css('display', 'block');    // do display block as permission has permission to view
    //         _branch.provide_permission_based_access();
    //         _branch.branch_list();
    //     } else {
    //         $('.main-body').remove();
    //         swal({
    //             title: "No Access",
    //             text: "Sorry! You do not have permission to view this pabe",
    //             icon: "error",
    //             dangerMode: true,
    //         });
    //     }
    //
    // }

    if (window.location.pathname === '/branch/') {
        if ((user_permissions.indexOf("self_view.rbac_permission") > -1) || (user_permissions.indexOf("list_view.rbac_permission") > -1)) {
            $('.main-body').css('display', 'block');  // do display block as permission has permission to view
            _branch.provide_permission_based_access();
            _branch.branch_list();
            // _branch.permission_list_row_select();
            // _branch.redirect_to_permission_add_page();
            // _branch.redirect_to_permission_edit_page();
            // _branch.permission_delete();
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