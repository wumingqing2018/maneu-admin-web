$(document).ready(function () {
    alert('1')
    detail_admin()
    $('#update').click(function () {
        $.ajax({
            url: admin_update,
            method: 'GET',
            data: {
                id: admin_id,
                phone: $('#phone').val(),
                nickname: $('#nickname').val(),
                location: $('#location').val(),
                content: $('#content').val()
            },
            success: function (res) {
                alert('修改成功')
            }
        })
    })

    function detail_admin() {
        $.ajax({
            url: admin_detail,
            method: 'GET',
            data: {
                id: admin_id,
            },
            success: function (res) {
                console.log(res)
                $('#time').val(res.content.time)
                $('#phone').val(res.content.phone)
                $('#nickname').val(res.content.nickname)
                $('#location').val(res.content.location)
                $('#content').val(res.content.content)
            }
        })
    }

    function update_admin() {
        $.ajax({
            url: admin_update,
            method: 'GET',
            data: {
                id: admin_id,
                phone: $('#phone').val(),
                nickname: $('#nickname').val(),
                location: $('#location').val(),
                content: $('#content').val()
            },
            success: function (res) {
                console.log(res)
            }
        })
    }
})
