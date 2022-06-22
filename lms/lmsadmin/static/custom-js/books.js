AjaxDatatableViewUtils.initialize_table(
    $(".table"),
    datatable_url,
    {
        processing: false,
        autoWidth: false,
        full_row_select: false,
        fixedHeader: true,
        "scrollX": true,
        "scrollY": "310px",
        "scrollCollapse": true,
        paging: true,
    },
    {
    }
);

$(document).on('click','.edit-books',function(){
    book_id = this.closest('tr').id.substr(4);
    window.location = '../edit-book/'+book_id;
});

function reload_datatable()
{
    $('.table').DataTable().ajax.reload();
}

$(document).on('change','#id_book_image',function(){
    readURL(this);
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#preview_book_image').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]); 
    }
}

