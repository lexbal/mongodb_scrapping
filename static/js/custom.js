function loaderAjax(obj) {
    obj.html(
        '<div class="loader">'
        + '<i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>'
        + '<p>'
        + 'Veuillez attendre le chargement des données...'
        + '</p>'
        + '</div>'
    );
}

$(function () {
    $('.dataframe').DataTable();

    $('#filters').on('change', '#country-filter', function (e) {
        e.preventDefault();

        let _data = new FormData();
        let _div  = $("#content");

        _data.append('country', $(this).val());

        $.ajax({
            type: 'POST',
            url: '/filter/country',
            data: _data,
            processData: false,
            contentType: false,
            beforeSend: function () {
                loaderAjax(_div);
            }
        }).then(function (response) {
            _div.html(response);
        }).fail(function () {
            _div.html(
                '<div class="alert alert-danger">' +
                'Erreur !!!'  +
                '</div>'
            );
        });
    });
});
