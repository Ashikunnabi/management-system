class LeftSidebar{
    constructor(){
        this._helper = new Helper();
        this._api_v1 = '/api/v1/';
    }
    
    sidebar_option_generation(sidebar){        
        var sidebase_html = '<li class="nav-item pcoded-hasmenu active pcoded-trigger">';
        $.each(sidebar, function(index, value){
            sidebase_html += '<a href="#!" class="nav-link"><span class="pcoded-micon">'+value.icon+'</span><span class="pcoded-mtext">'+value.title+'</span></a>';
            sidebase_html += '<ul class="pcoded-submenu">';
            $.each(value.level_1, function(i, v){
                sidebase_html += '<li class="active"><a href="" class="">'+ v.title+'</a></li>';     
            });
            sidebase_html += '</ul>';
            sidebase_html += '</li>';
        });
        $('.pcoded-inner-navbar').append(sidebase_html);        
    }
    
    request_for_sidebar(){ 
        let object = this;    
        // let url = object._api_v1 + 'feature/';
        let url = '/sidebar/';
        var promise = this._helper.httpRequest(url);
        promise.done(function (response) {
            object.sidebar_option_generation(response)
        });
        promise.fail(function (response) {
            // send back to registration page with an error notification
            alert(response.responseJSON.detail);
        });
    }
}

let left_sidebar = new LeftSidebar();

left_sidebar.request_for_sidebar();
