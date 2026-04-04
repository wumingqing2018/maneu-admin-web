$(document).ready(function () {
    detail_store()
    guest_hide()


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


    function detail_store() {
        $.ajax({
            url: store_detail,
            data: {
                'index_id': index_id,
            },
            success: function (res) {
                if (res.status === true) {

                    guest = res.content.guest
                    if (guest.status === true) {
                        $('#guestRemark').val(guest.content.remark)
                        $('#phone').val(guest.content.phone)
                        $('#name').val(guest.content.name)
                        $('#time').val(guest.content.time)
                        $('#sex').val(guest.content.sex)
                        $('#age').val(guest.content.age)
                        $('#dfh').val(guest.content.dfh)
                        $('#em').val(guest.content.em)
                        $('#ot').val(guest.content.ot)
                    }


                    store = res.content.store
                    if (store.status === true) {
                                                $('#parameters').val(store.content[0].parameters)
                        $('#class').val(store.content[0].class)
                        $('#brand').val(store.content[0].brand)
                        $('#model').val(store.content[0].model)
                        $('#price').val(store.content[0].price)
                        $('#arg00').val(store.content[0].arg00)
                        $('#arg01').val(store.content[0].arg01)
                        $('#arg10').val(store.content[0].arg10)
                        $('#arg11').val(store.content[0].arg11)
                        $('#arg20').val(store.content[0].arg20)
                        $('#arg21').val(store.content[0].arg21)
                        $('#arg30').val(store.content[0].arg30)
                        $('#arg31').val(store.content[0].arg31)
                        $('#arg40').val(store.content[0].arg40)
                        $('#arg41').val(store.content[0].arg41)
                        $('#arg50').val(store.content[0].arg50)
                        $('#arg51').val(store.content[0].arg51)
                        $('#arg60').val(store.content[0].arg60)
                        $('#arg61').val(store.content[0].arg61)
                        $('#arg70').val(store.content[0].arg70)
                        $('#arg71').val(store.content[0].arg71)
                        $('#arg80').val(store.content[0].arg80)
                        $('#arg81').val(store.content[0].arg81)
                        $('#arg90').val(store.content[0].arg90)
                        $('#arg91').val(store.content[0].arg91)
                    }

                }
            }
        })
    }


    $('#guest_hide').click(function () {
        guest_hide()
    })


    $('#guest_show').click(function () {
        guest_show()
    })


    $('#delete').click(function () {
        if (confirm("确定要删除记录吗？")) {
            $.ajax({
                url: store_delete,
                data: {
                    'index_id': index_id,
                },
                success: function (res) {
                    console.log(res)
                    if (res.status === true) {
                        alert('删除成功')
                    } else {
                        alert('删除失败')
                    }
                },
                error: function (res) {
                    console.log(res)
                    alert('网络错误')
                }
            })
        } else {
            return false;
        }
    })


    $('#guestUpdate').click(function update_guest() {
        $.ajax({
            url: store_update_time,
            method: 'GET',
            data: {
                index_id: index_id,
                guestRemark: $("#guestRemark").val(),
                phone: $("#phone").val(),
                time: $("#time").val(),
                name: $("#name").val(),
                age: $("#age").val(),
                sex: $("#sex").val(),
                dfh: $("#dfh").val(),
                ot: $("#ot").val(),
                em: $("#em").val(),
            },
            success: function (res) {
                console.log(res)
                if (res.status === true) {
                    alert('更新成功')
                } else {
                    alert('更新失败')
                }
            },
            error: function (res) {
                console.log(res)
                alert('网络错误')
            }
        })
    })


    $('#storeUpdate').click(function update_order() {

        data = [{
                        'parameters': $("#parameters").val(),
            'class': $("#class").val(),
            'brand': $("#brand").val(),
            'model': $("#model").val(),
            'price': $("#price").val(),
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

        $.ajax({
            url: store_update_data,
            method: 'GET',
            data: {
                index_id: index_id,
                content: JSON.stringify(data),
            },

            success: function (res) {
                if (res.status === true){
                    alert('更新成功')
                }else {
                    alert('更新失败')
                }
            },

            error: function (res) {
                alert('网络错误')
            }

        })
    })


    $('#generate_qr_code').click(function () {
        $.ajax({
            url: store_QRcode,
            data: {
                'index_id': index_id,
            },
            method: 'GET',
            xhrFields: {
                responseType: 'blob'  // 关键：告诉 jQuery 将响应解析为 Blob
            },
            success: function (blob) {
                // 创建对象 URL
                const blobUrl = URL.createObjectURL(blob);

                // 创建临时 <a> 标签并触发下载
                const link = document.createElement('a');
                link.href = blobUrl;
                link.download = index_id;
                document.body.appendChild(link);
                link.click();

                // 清理
                document.body.removeChild(link);
                URL.revokeObjectURL(blobUrl);
            },
            error: function (xhr, status, error) {
                console.error('下载失败:', error);
            }
        });
    })


});
