'use strict';

window.AjaxDatatableViewUtils = (function() {

    var _options = {};

    var _html_daterange_widget =
        'From: <input type="date" id="date_from" class="datepicker">' +
        'To: <input type="date" id="date_to" class="datepicker">';


    function init(options) {
        _options = options;

        if (!('language' in _options)) {
            _options.language = {};
        }
    }


    function _handle_column_filter(table, data, target) {
        var index = target.data('index');
        var value = target.val();

        var column = table.api().column(index);
        var old_value = column.search();
        console.log('Request to search value %o in column %o (current value: %o)', value, index, old_value);
        if (value != old_value) {
            console.log('searching ...');
            column.search(value).draw();
        }
        else {
            console.log('skipped');
        }
    };

    function getCookie(name) {
        var cookieValue = null;
        var value = '; ' + document.cookie,
            parts = value.split('; ' + name + '=');
        if (parts.length == 2) cookieValue = parts.pop().split(';').shift();
        return cookieValue;
    }

    function getCSRFToken() {
        var csrftoken = getCookie('csrftoken');
        if (csrftoken == null) {
            csrftoken = $('input[name=csrfmiddlewaretoken]').val();
        }
        return csrftoken;
    }

    function _setup_column_filters(table, data) {
		
        if (data.show_column_filters) {

            var filter_row = '<tr class="datatable-column-filter-row">';
            $.each(data.columns, function(index, item) {
                if (item.visible) {
                    if (item.searchable) {
                        var html = '';
                        if ('choices' in item && item.choices) {
           
                            var select = $('<select data-index="' + index.toString() + '"><option value=""></option></select>');
                            $(item.choices).each(function(index, choice) {
                                var option = $("<option>").attr('value', choice[0]).text(choice[1]);
                                if (choice[0] === item.initialSearchValue) {
                                    option.attr('selected', 'selected');
                                }
                                select.append(option);
                            });
                            html = $('<div>').append(select).html();
                        }
                        else {
                            var input = $('<input>')
                                .attr('type', 'text')
                                .attr('data-index', index)
                                .attr('placeholder', '...')
                                .attr('value', item.initialSearchValue ? item.initialSearchValue : '')
                            html = $('<div>').append(input).html();
                        }
                        if (item.className) {
                            filter_row += '<th class="' + item.className + '">' + html + '</th>';
                        }
                        else {
                            filter_row += '<th>' + html + '</th>';
                        }
                    }
                    else {
                        if (index == 0) {
                            var search_icon_html = _options.search_icon_html === undefined ? '' : _options.search_icon_html;
                            filter_row += '<th>' + search_icon_html + '</th>';
                        }
                        else {
                            filter_row += '<th></i>&nbsp;</th>';
                        }
                    }
                }
            });
            filter_row += '</tr>';

            var wrapper = table.closest('.dataTables_wrapper');
            $(filter_row).appendTo(
                wrapper.find('thead')
            );

            var column_filter_row = wrapper.find('.datatable-column-filter-row')
            column_filter_row.find('input,select').off().on('keyup change', function(event) {
                var target = $(event.target);
                _handle_column_filter(table, data, target);
            });
        }
    };


    function _bind_row_tools(table, url, options, extra_data)
    {
        if (options.full_row_select) {
            
            table.api().on('click', 'td', function(event) {
                var tr = $(this).closest('tr');
                
                if (tr.hasClass('details') && !$(event.target).hasClass('btn-close')) {
                    return;
                }

                var row = table.api().row(tr);
                if (row.child.isShown()) {
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {
                    table.find('tr').removeClass('shown');
                    table.api().rows().every(function( rowIdx, tableLoop, rowLoop) {
                        this.child.hide();
                    });
                    if (!tr.hasClass('details')) {
                        row.child(_load_row_details(row.data(), url, extra_data), 'details').show('slow');
                        tr.addClass('shown');
                    }
                }
            });

        } else {
            table.api().on('click', 'td.dataTables_row-tools .plus, td.dataTables_row-tools .minus', function(event) {
                event.preventDefault();
                var tr = $(this).closest('tr');
                var row = table.api().row(tr);
                if (row.child.isShown()) {
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {                    
                    var data = _load_row_details(row.data(), url, extra_data);
                    if (options.detail_callback) {
                        options.detail_callback(data, tr);
                    }
                    else {
                        row.child(data, 'details').show('slow');
                    }
                    tr.addClass('shown');
                }
            });
        }
    };

    function _load_row_details(rowData, url, extra_data) {

        var div = $('<div/>')
            .addClass('row-details-wrapper loading')
            .text('Loading...');

        if (rowData !== undefined) {

            var data = {
                action: 'details',
                pk: rowData['pk']
            };
            if (extra_data) {
                Object.assign(data, extra_data);
            }

            $.ajax({
                url: url,
                data: data,
                dataType: 'json',
                success: function(json) {
                    var parent_row_id = json['parent-row-id'];
                    if (parent_row_id !== undefined) {
                        div.attr('data-parent-row-id', parent_row_id);
                    }
                    div.html(json.html).removeClass('loading');
                }
            });
        }

        return div;
    };


    function adjust_table_columns() {
        $.fn.dataTable
            .tables({
                visible: true,
                api: true
            })
            .columns.adjust();
    };


    function _daterange_widget_initialize(table, data) {
        if (data.show_date_filters) {
            if (_options.fn_daterange_widget_initialize) {
                _options.fn_daterange_widget_initialize(table, data);
            }
            else {
                var wrapper = table.closest('.dataTables_wrapper');
                var toolbar = wrapper.find(".toolbar");
                toolbar.html(
                    '<div class="daterange" style="float: left; margin-right: 6px;">' +
                    '<span class="from"><label>From</label>: <input type="date" class="date_from datepicker"></span>' +
                    '<span class="to"><label>To</label>: <input type="date" class="date_to datepicker"></span>' +
                    '</div>'
                );
                toolbar.find('.date_from, .date_to').on('change', function(event) {
                    // Annotate table with values retrieved from date widgets
                    table.data('date_from', wrapper.find('.date_from').val());
                    table.data('date_to', wrapper.find('.date_to').val());
                    // Redraw table
                    table.api().draw();
                });
            }
        }
    }


    function after_table_initialization(table, data, url, options, extra_data) {
        _bind_row_tools(table, url, options, extra_data);
        //_setup_column_filters(table, data);
    }


    function _write_footer(table, html) {
        var wrapper = table.closest('.dataTables_wrapper');
        var footer = wrapper.find('.dataTables_extraFooter');
        if (footer.length <= 0) {
            $('<div class="dataTables_extraFooter"></div>').appendTo(wrapper);
            footer = wrapper.find('.dataTables_extraFooter');
        }
        footer.html(html);
    }

    function initialize_table(element, url, extra_options={}, extra_data={}) {

        var data = {action: 'initialize'};
        if (extra_data) {
            Object.assign(data, extra_data);
        }
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            dataType: 'json',
            headers: {'X-CSRFToken': getCSRFToken()}
        }).done(function(data, textStatus, jqXHR) {
            var options = {
                processing: true,
                serverSide: true,
                scrollX: true,
                autoWidth: true,
                dom: '<"toolbar">lrftip',
                language: _options.language,
                full_row_select: false,                
                ajax: function(data, callback, settings) {
                      var table = $(this);
                      data.date_from = table.data('date_from');
                      data.date_to = table.data('date_to');
                      if (extra_data) {
                          Object.assign(data, extra_data);
                      }                     
                      $.ajax({
                          type: 'POST',
                          url: url,
                          data: data,
                          dataType: 'json',
                          cache: false,
                          crossDomain: false,
                          headers: {'X-CSRFToken': getCSRFToken()}
                      }).done(function(data, textStatus, jqXHR) {                         
                          callback(data);

                          var footer_message = data.footer_message;
                          if (footer_message !== null) {
                              _write_footer(table, footer_message);
                          }

                      }).fail(function(jqXHR, textStatus, errorThrown) {
                          console.log('ERROR: ' + jqXHR.responseText);
                      });
                },
                columns: data.columns,
                searchCols: data.searchCols,
                lengthMenu: data.length_menu,
                order: data.order,
                initComplete: function() {
                    // HACK: wait 200 ms then adjust the column widths
                    // of all visible tables
                    setTimeout(function() {
                        AjaxDatatableViewUtils.adjust_table_columns();
                    }, 200);

                    // Notify subscribers
                    //console.log('Broadcast initComplete()');
                    table.trigger(
                        'initComplete', [table]
                    );
                },
                drawCallback: function(settings) {
                    // Notify subscribers
                    //console.log('Broadcast drawCallback()');
                    table.trigger(
                        'drawCallback', [table, settings]
                    );
                },
                rowCallback: function(row, data) {
                    // Notify subscribers
                    //console.log('Broadcast rowCallback()');
                    table.trigger(
                        'rowCallback', [table, row, data]
                    );
                },
                footerCallback: function (row, data, start, end, display) {
                    // Notify subscribers
                    //console.log('Broadcast footerCallback()');
                    table.trigger(
                        'footerCallback', [table, row, data, start, end, display]
                    );
                }
            }

            if (extra_options) {
                Object.assign(options, extra_options);
            }

            var table = element.dataTable(options);

            _daterange_widget_initialize(table, data);
            after_table_initialization(table, data, url, options, extra_data);
        })
    }


    function redraw_all_tables() {
        $.fn.dataTable.tables({
            api: true
        }).draw();
    }


    // Redraw table holding the current paging position
    function redraw_table(element) {
        var table = $(element).closest('table.dataTable');
        // console.log('element: %o', element);
        // console.log('table: %o', table);
        table.DataTable().ajax.reload(null, false);
    }


    return {
        init: init,
        initialize_table: initialize_table,
        adjust_table_columns: adjust_table_columns,
        redraw_all_tables: redraw_all_tables,
        redraw_table: redraw_table
    };

})();
