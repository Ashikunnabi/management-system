class User {
    constructor() {
        this._helper = new Helper();
        this._api = '/api/v1/';
        this.user_list_url = this._api+'user/?format=datatables';;
        this.user_add_url = '/user/add/';
    }
    
    user_list(){
        let self = this;
        let url = self.user_list_url;
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
            let url = self.user_add_url;
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
                let url = '/user/' + table.row('.selected').data().id;
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
                swal({
                    title: "Are you sure?",
                    text: "User can not be deleted. This will make the user inactive! You are going to inactive user: '"+selected_row_data.username+"'",
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                })
                .then((willDelete) => {
                    if (willDelete) {
                        let url = self._api+'user/' + selected_row_data.id + '/';
                        var promise = self._helper.httpRequest(url, 'DELETE');
                        promise.done(function (response) {
                            // redirect to dashboard
                            swal("Poof! User: '"+selected_row_data.username+"' has been inactive!", {
                                icon: "success",
                            });
                            setTimeout(function(e){window.location.replace("/user");}, 1000);                            
                        });
                        promise.fail(function (response) {
                            // send back to login page with an error notification
                            $.each(response.responseJSON, function(i, v){
                                $.each(v, function(j, w){
                                    let message = i +": " + w
                                    $.growl(message, { type: 'danger' });
                                });
                            });                            
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
    
    set_role_in_dropdown(){        
        let self = this;
        let url = self._api + 'role/';
        let role_dropdown = $('#role');        
        
        var promise = this._helper.httpRequest(url);
        promise.done(function (response) {
            let data = [];
            $.each(response.results, function(i, v){
                data.push({
                    id: v.id,
                    text: v.name,
                });
            });
            role_dropdown.select2({
                data: data
            });
        });
        promise.fail(function (response) {
            alert(response.responseJSON.detail);
        });
    }
    
    set_country_in_dropdown(){        
        let self = this;
        // let url = self._api + 'role/';
        // let url = 'https://restcountries.eu/rest/v2/all';
        let country_dropdown = $('#country');        
        
        // var promise = this._helper.httpRequest(url);
        // promise.done(function (response) {
            let data = [];
            $.each(countries, function(i, v){
                data.push({
                    id: i,
                    text: v.name,
                });
            });
            country_dropdown.select2({
                data: data
            });
        // });
        // promise.fail(function (response) {
            // alert(response.responseJSON.detail);
        // });
    }
	
    image_capture_upload(){        
        // Image upload from system
        $(document).on('click', '#profile_picture_upload, #signature_upload', function () {
            // profile picture upload from system
            if ($(this).attr("id") === 'profile_picture_upload'){
                $('#file_profile_picture').trigger('click');
                imageupload('profile_picture_preview', 'file_profile_picture');        
            }
            // signature upload from system
            if ($(this).attr("id") === 'signature_upload'){
                $('#file_signature').trigger('click');
                imageupload('signature_preview', 'file_signature');       
            }
        });

        // image capture using camera
        $(document).on('click', '#profile_picture_capture, #signature_capture', function () {
            // profile picture capture using camera
            if ($(this).attr("id") === 'profile_picture_capture'){
                imageCapture('profile_picture_preview', 'file_profile_picture');
            }
            // signature capture using camera
            if ($(this).attr("id") === 'signature_capture'){
                imageCapture('signature_preview', 'file_signature');
            }
        });
    }
	
    user_add(){
        let self = this;
		let user_add_form = $('#user_add_form');
        user_add_form.submit(function (e) {
			e.preventDefault();
			let data_parsley = user_add_form.parsley();
            if (!data_parsley.isValid()){
                // Invalid Form Data
            }else{
				let data = new FormData($(this)[0]);
				if (data.has('account_status') === false) data.append('account_status', '0');
				
				let url = self._api+'user/';
                
                $.ajax({
                    type: "post",
                    url: url,
                    data: data,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        $.growl('Successfully user added', { type: 'success' });
                        setTimeout(function () {
                            window.location.href("/user");
                        }, 1500);

                    },
                    error: function (response) {
                        if(response.status == 403){
                            $.growl(response.responseJSON.detail, { type: 'danger' });
                        }else{
                            $.each(response.responseJSON, function(i, v){
                                $.each(v, function(j, w){
                                    let message = i +": " + w
                                    $.growl(message, { type: 'danger' });
                                });
                            });
                        }
                    }
                });
            }
        });                
    }	
        
    user_edit_form_fillup(){
        let self = this;
		let user_edit_form = $('#user_edit_form');
        user_edit_form.ready(function (e) {
            let url = self._api+'user/' + user_id + '/';
            var promise = self._helper.httpRequest(url, 'GET');
            promise.done(function (response) { 
                function populate(frm, data) {
                  $.each(data, function(key, value){
                      if(key == 'country' || key == 'role') $('[name='+key+']', frm).val(value).select2();
                      else if(key == 'gender') $('[name='+key+'][value=' + value + ']', frm).attr('checked', 'checked');
                      else $('[name='+key+']', frm).val(value);
                  });
                }
                populate(user_edit_form, response);
            });
            promise.fail(function (response) {
                if(response.status == 403){
                    $.growl(response.responseJSON.detail, { type: 'danger' });
                }else{
                    $.each(response.responseJSON, function(i, v){
                        $.each(v, function(j, w){
                            let message = i +": " + w
                            $.growl(message, { type: 'danger' });
                        });
                    });
                }
            });
        });       
    }
      
    user_edit(){
        let self = this;
		let user_edit_form = $('#user_edit_form');
        user_edit_form.submit(function (e) {
			e.preventDefault();
			let data_parsley = user_edit_form.parsley();
            if (!data_parsley.isValid()){
                // Invalid Form Data
            }else{
				let data = new FormData($(this)[0]);
				if (data.has('account_status') === false) data.append('account_status', '0');
				if (data.has('gender')) data.append('gender', $("input[name='gender']:checked").val());
				
				let url = self._api+'user/' + user_id + '/';
               
                $.ajax({
                    type: "patch",
                    url: url,
                    data: data,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        $.growl('Successfully user updated', { type: 'success' });
                        setTimeout(function () {
                            window.location.href = "/user";
                        }, 1500);

                    },
                    error: function (response) {
                        if(response.status == 403){
                            $.growl(response.responseJSON.detail, { type: 'danger' });
                        }else{
                            $.each(response.responseJSON, function(i, v){
                                $.each(v, function(j, w){
                                    let message = i +": " + w
                                    $.growl(message, { type: 'danger' });
                                });
                            });
                        }
                    }
                });
            }
        });        
    }
}




let user = new User();

// getting all users
$(document).ready(function(e){
    if(window.location.pathname == '/user/'){
        user.user_list();
        user.user_list_row_select();
        user.redirect_to_user_add_page();
        user.redirect_to_user_edit_page();
        user.user_delete();        
    }
    if(window.location.pathname == '/user/add/'){
        user.image_capture_upload();
        user.set_role_in_dropdown();
        user.set_country_in_dropdown();
        user.user_add();  // rbac/user_add.html        
    }
    else if(window.location.pathname.match(/[\/user\/\d\/]/g)){
        user.image_capture_upload();
        user.set_role_in_dropdown();
        user.set_country_in_dropdown();
        user.user_edit_form_fillup();  // rbac/user_edit.html
        user.user_edit();  // rbac/user_edit.html
    }
});


	