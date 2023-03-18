// get todo starts
function get_post() {
    $.ajax({
        type: 'GET',
        url: '/get_post',
        success: successFn,
        error: errorFn
    })

    function successFn(result) {
        $(".create_post").html(result['remain'])
        $(".view_post").html(result['complete'])
    }

    function errorFn(xhr) {
        console.log('Error: ', xhr)
    }
}
// get todo ends
