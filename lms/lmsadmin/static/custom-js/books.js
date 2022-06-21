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

$(document).on('click','.edit-state',function(){
    state_id = this.closest('tr').id.substr(4);
    window.location = '../state-list/'+state_id;
});

function reload_datatable()
{
    $('.table').DataTable().ajax.reload();
}

