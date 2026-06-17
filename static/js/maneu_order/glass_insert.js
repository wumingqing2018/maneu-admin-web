$(document).ready(function () {
    $.ajax({
        url: api_glass_store_brand,
        type: 'GET',
        success: function (res) {
            if (res.code === 0) {
                for (i in res.data) {
                    data = res.data[i]
                    $('#brand_select').append('<option value="' + data + '">' + data + '</option>')
                }
            }
        }
    })
    $('#brand_select').change(function () {
        $.ajax({
            url: api_glass_store_model,
            type: 'GET',
            data: {'brand': $('#brand_select').val()},
            success: function (res) {
                console.log(res)
                if (res.code === 0) {
                    for (i in res.data) {
                        data = res.data[i]
                        $('#model_select').append('<option value="' + data + '">' + data + '</option>')
                    }
                }
            }
        })
    })
    $('#model_select').change(function () {
        $.ajax({
            url: api_glass_store_model,
            type: 'GET',
            data: {'brand': $('#brand_select').val()},
            success: function (res) {
                console.log(res)
                if (res.code === 0) {
                    for (i in res.data) {
                        data = res.data[i]
                        $('#model_select').append('<option value="' + data + '">' + data + '</option>')
                    }
                }
            }
        })
    })
    $('#ds_select').change(function () {
        $.ajax({
            url: api_glass_store_model,
            type: 'GET',
            data: {'brand': $('#brand_select').val()},
            success: function (res) {
                console.log(res)
                if (res.code === 0) {
                    for (i in res.data) {
                        data = res.data[i]
                        $('#model_select').append('<option value="' + data + '">' + data + '</option>')
                    }
                }
            }
        })
    })
})
