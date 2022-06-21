let token = $("[name=csrfmiddlewaretoken]").val();

$(document).on("click", ".tgle-on", function () {
    let id = this.closest("tr").id.substr(4);
    let url = $(this).data('url')
    if (id) {
        swal({
            title: "Are you sure?",
            text: "Deactivate, this record!",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    headers: { "X-CSRFToken": token },
                    url: "/gopllay-admin/"+url,
                    method: "POST",
                    data: {
                        id: id,
                        status: "block",
                    },
                    datatype: "json",
                    success: function (data) {
                        reload_datatable()
                        swal("Record deactivated successfully!", {
                            icon: "success",
                        });
                    },
                });
            }
        });
    }
});

$(document).on("click", ".tgle-off", function () {
  let id = this.closest("tr").id.substr(4);
  let url = $(this).data('url')
  if (id) {
      swal({
          title: "Are you sure?",
          text: "Activate, this record!",
          icon: "warning",
          buttons: true,
          dangerMode: true,
      }).then((willDelete) => {
          if (willDelete) {
              $.ajax({
                  headers: { "X-CSRFToken": token },
                  url: "/gopllay-admin/"+url,
                  method: "POST",
                  data: {
                      id: id,
                      status: "active",
                  },
                  datatype: "json",
                  success: function (data) {
                      reload_datatable()
                      swal("Record activated successfully!", {
                          icon: "success",
                      });
                  },
              });
          }
      });
  }
});

$(document).on("click", ".del-record", function () {
  let id = this.closest("tr").id.substr(4);
  let url = $(this).data('url')
  if (id) {
      swal({
          title: "Are you sure?",
          text: "Delete, this record!",
          icon: "warning",
          buttons: true,
          dangerMode: true,
      }).then((willDelete) => {
          if (willDelete) {
              $.ajax({
                  headers: { "X-CSRFToken": token },
                  url: "/gopllay-admin/"+url,
                  method: "POST",
                  data: {
                      id: id,
                      status: "delete",
                  },
                  datatype: "json",
                  success: function (data) {
                      reload_datatable()
                      swal("Record deleted successfully!", {
                          icon: "success",
                      });
                  },
              });
          }
      });
  }
});
