$(document).ready(function () {
    glass_insert_show.click(function () {
        glass_show()
    });
    glass_insert_hide.click(function () {
        glass_hide()
    });
    glass_insert_btn.click(function () {
        content = glass_insert.serializeJsonStr()
        order.push(content)
        order_content(content)
        glass_hide()
        console.log(order)
    });

    function glass_show() {
        /*
        点击添加镜片按钮执行以下操作 id = glass_insert_show
        显示添加镜片表格 id = glass_table
        显示取消添加按钮 id = glass_insert_hide
        隐藏添加镜片按钮 id = glass_insert_show
        清空品牌选择栏并填入空白值
         */
        glass_table.show()
        glass_insert_hide.show()
        glass_insert_show.hide()
        // framework_insert_hide.click()
    }

    function glass_hide() {
        /*
        点击取消添加按钮
        隐藏添加镜片表格 id = glass_table
        隐藏取消添加按钮 id = glass_insert_hide
        显示添加镜片按钮 id = glass_insert_show
         */
        glass_insert_hide.hide()
        glass_insert_show.show()
        glass_table.hide()
    }

    function order_content(content) {
        content = jQuery.parseJSON(content)
        html = ''
        html += '<tr>'
        html += '<td><span>' + content.brand + '</span></td>'
        html += '<td><span>' + content.model + '</span></td>'
        html += '<td><span>' + content.INDEX + '</span></td>'
        html += '<td><span>' + content.Around + '</span></td>'
        html += '<td><span>' + content.SPH + '</span></td>'
        html += '<td><span>' + content.CYL + '</span></td>'
        html += '<td><span>' + content.AX + '</span></td>'
        html += '<td><span>' + content.Add + '</span></td>'
        html += '<td><span>' + content.pd + '</span></td>'
        html += '</tr>'
        $('#order_content').append(html)
        $("#order_banner").show()
    }

    $.fn.serializeJsonStr = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return JSON.stringify(o);
    }
})
