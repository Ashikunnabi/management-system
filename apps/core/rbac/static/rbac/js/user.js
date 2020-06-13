class User {
    constructor() {
        this._helper = new Helper();
        this._api = '/api/v1/';
    }
    
    user_list(){
        let url = this._api+'user/?format=datatables';
        let table = $('#user_table').DataTable({
            "processing": true,
            // "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            // "dom": '<"mb-3"B>flrtip',
            "searchPanes":true,            
            "searchPanes":{
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
                    title: 'USERS',
                    messageTop: '<h5 class="text-center">User List</h5>',
                    messageBottom: null
                }
            ],
            "lengthMenu": [ 10, 25, 50, 75, 100 ],
            "ajax": url,
            "columns": [
                { "data": "" },
                { "data": "username" },
                { "data": "first_name" },
                { "data": "last_name" },
                { "data": "email" },
                { "data": "position" },
                { "data": "is_active" },
            ], 
            "columnDefs": [            
                {
                    searchPanes:{
                        show: true,
                    },
                    targets: [5, 6],
                },
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                {
                    "targets": [ 1 ],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) { 
                        return data;
                    },
                },
                {
                    "targets": [ 6 ],
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
    
    user_list_row_select(){
        $('#user_table tbody').on( 'click', 'tr', function () {
            // deselect a selected row
            if ($(this).hasClass('selected')){
                $(this).toggleClass('selected');
                $('#edit_user, #delete_user').addClass('disabled');
            } else {
                // deselected all row
                $('#user_table tbody').children().removeClass('selected');
                // selecting clicked row
                $(this).toggleClass('selected');
                $('#edit_user, #delete_user').removeClass('disabled');
            }
        });     
    }
    
    redirect_to_user_add_page(){
        let self = this;
        $('#add_user').on( 'click', '', function () {
            let url = '/user/add/';
            window.open(url, "");
        });     
    }
    
    redirect_to_user_edit_page(){
        let self = this;
        $('#edit_user').on( 'click', '', function () {
            if ($(this).hasClass('disabled')){
                // button is disabled that means not table row selected, so do nothing
            }else{
                var table = $('#user_table').DataTable();
                console.log(table.row('.selected').data())
                let url = self._api + 'user/' + table.row('.selected').data().id;
                window.open(url, "_blank");
            }
        });     
    }
    
    user_delete(){
        let self = this;
        $('#delete_user').on( 'click', '', function () {
            if ($(this).hasClass('disabled')){
                // button is disabled that means not table row selected, so do nothing
            }else{
                var table = $('#user_table').DataTable();
				let selected_row_data = table.row('.selected').data();
                console.log(selected_row_data)
                swal({
                    title: "Are you sure?",
                    text: "User can not be deleted. This will make the user inactive! You are going to inactive user: '"+selected_row_data.username+"'",
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                })
                .then((willDelete) => {
                    if (willDelete) {
                        swal("Poof! User: '"+selected_row_data.username+"' has been inactive!", {
                            icon: "success",
                        });
                    } else {
                        swal("User: '"+selected_row_data.username+"' is safe and active!", {
                            icon: "error",
                        });
                    }
                });
            }
        });
    }
		
    user_add(){
        let self = this;
		let user_add_form = $('#user_add_form');
        user_add_form.on( 'submit', '', function (e) {
			e.preventDefault();
			let data_parsley = user_add_form.parsley();
            if (!data_parsley.isValid()){
                // button is disabled that means not table row selected, so do nothing
            }else{
				let data = self._helper.getFormDataToJson(user_add_form);
				console.log(data.account_status)
				if (data.account_status === undefined) data.account_status = '0';
				console.log(data);
				
				let url = self._api+'user/';
				var promise = self._helper.httpRequest(url, 'POST', JSON.stringify(data));
				promise.done(function (response) {
					// redirect to dashboard
					window.location.replace("/");
				});
				promise.fail(function (response) {
					// send back to login page with an error notification
					$.each(response, function(i, v){
						$.each(v, function(j, w){
							$.growl(w, { type: 'danger' });
						});
					});
					
				});
            }
        });
    }
}

let user = new User();

// getting all users
$(document).ready(function(e){
    user.user_list();
    user.user_list_row_select();
    user.redirect_to_user_add_page();
    user.redirect_to_user_edit_page();
    user.user_delete();
    user.user_add();  // rbac/user_add.html
});


	