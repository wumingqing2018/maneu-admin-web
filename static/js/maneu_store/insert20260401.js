$(document).ready(function () {
    guest_hide()


    $('#guest_hide').click(function () {
        guest_hide()
    })
    $('#guest_show').click(function () {
        guest_show()
    })


    function guest_hide() {
        $("#guest_hide").hide()
        $("#guest_show").show()
        $("#guest_content").hide()
    }
    function guest_show() {
        $("#guest_hide").show()
        $("#guest_show").hide()
        $("#guest_content").show()
    }


    $('#insert').click(function () {
        data = [{
            'class': $("#class").val(),
            'brand': $("#brand").val(),
            'model': $("#model").val(),
            'price': $("#price").val(),
            'parameters': $("#parameters").val(),
            'arg00': $("#arg00").val(),
            'arg01': $("#arg01").val(),
            'arg10': $("#arg10").val(),
            'arg11': $("#arg11").val(),
            'arg20': $("#arg20").val(),
            'arg21': $("#arg21").val(),
            'arg30': $("#arg30").val(),
            'arg31': $("#arg31").val(),
            'arg40': $("#arg40").val(),
            'arg41': $("#arg41").val(),
            'arg50': $("#arg50").val(),
            'arg51': $("#arg51").val(),
            'arg60': $("#arg60").val(),
            'arg61': $("#arg61").val(),
            'arg70': $("#arg70").val(),
            'arg71': $("#arg71").val(),
            'arg80': $("#arg80").val(),
            'arg81': $("#arg81").val(),
            'arg90': $("#arg90").val(),
            'arg91': $("#arg91").val(),
        }];
        console.log(data)

        $.ajax({
            url: store_insert_api,
            method: 'GET',
            data: {
                time: $("#time").val(),
                name: $("#name").val(),
                phone: $("#phone").val(),


                age: $("#age").val(),
                sex: $("#sex").val(),
                dfh: $("#dfh").val(),
                ot: $("#ot").val(),
                em: $("#em").val(),
                guestRemark: $("#guestRemark").val(),


                storeContent: JSON.stringify(data),
                storeRemark: $("#storeRemark").val(),
            },

            success: function (res) {
                console.log(res)
                if (res.status === true){
                    alert('更新成功')
                }else {
                    alert('更新失败')
                }
            },

            error: function (res) {
                console.log(res)
                alert('网络错误')
            }
        })
    });

});
