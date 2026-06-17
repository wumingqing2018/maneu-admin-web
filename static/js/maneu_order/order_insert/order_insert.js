/*
提交订单JS
校验 c_name 是否符合输入要求
校验 c_phone 是否符合输入要求
*/
$(document).ready(function () {
    /*
     *  c_name 的值改变后, 判断 c_name 是否为空
     *  c_name 为空
     *      在username_error填充请输入姓名
     *  c_name 不为空
     *      清空username_error的值
     */
    $("#c_name").blur(function () {
        if ($('#c_name').val() === '') {
            $('#username_error').text('请输入姓名');
        } else {
            $('#username_error').text('');
            if (c_phone.val() === '') {
                $('#insert').hide()
            } else {
                $('#insert').show()
            }
        }
    });
    c_phone.change(function () {
        if (c_phone.val() === '') {
            $('#phone_error').text('请输入电话');
        } else if (isNaN(c_phone.val())) {
            $('#phone_error').text('电话由数字构成');
        } else if (c_phone.val().length < 11) {
            $('#phone_error').text('电话长度不足11位');
        } else if (c_phone.val().length > 11) {
            $('#phone_error').text('电话长度超过11位');
        } else {
            $('#phone_error').text('');
            if (c_name.val() === '') {
                $('#insert').hide()
            } else {
                $('#insert').show()
            }
        }
    });
    $('#insert').click(function () {
        $("#maneu_order").val('[' + order + ']');
        $.ajax({
            url: api_order_insert,
            type: 'POST',
            data: $('#order_insert').serialize(),
            success: function (res) {
                if (res.code === 0) {
                    alert("创建成功")
                } else if (res.code === 1) {
                    alert("请求出错 , 请刷新页面")
                } else if (res.code === 2) {
                    console.log(res.msg)
                } else if (res.code === 3) {
                    alert("创建失败")
                }
            }
        });
    });
});
