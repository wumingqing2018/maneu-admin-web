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
            [$("#key10").val()] : $("#val10").val(),
            [$("#key20").val()] : $("#val20").val(),
            [$("#key30").val()] : $("#val30").val(),
            [$("#key40").val()] : $("#val40").val(),
            [$("#key50").val()] : $("#val50").val(),
            [$("#key60").val()] : $("#val60").val(),
            [$("#key70").val()] : $("#val70").val(),
            [$("#key80").val()] : $("#val80").val(),
            [$("#key90").val()] : $("#val90").val(),
            [$("#key00").val()] : $("#val00").val(),
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
                remark: $("#remark").val(),


                storeContent: JSON.stringify(data),
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
