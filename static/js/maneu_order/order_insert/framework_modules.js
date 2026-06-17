/*
添加镜框相关js模块
 */
$(document).ready(function () {
    /**
     * 点击 id=framework_insert_show 按钮调用一下function
     * ajax 请求 api_framework_brand
     */
    framework_insert_show.click(function () {
        framework_show()
    });
    framework_insert_hide.click(function () {
        framework_hide()
    });
    framework_insert_btn.click(function () {
        /*
        点击framework_insert_btn按钮
        把添加镜框表单转换为json字符串并保存到order数组
        把表单内容显示到order_content的表格位置
         */
        content = framework_insert.serializeJsonStr()
        order.push(content);
        order_content(content)
        framework_hide()
    });

    function framework_show() {
        /*
        添加镜框表格 id=framework_table
        添加镜框按钮 id=framework_insert_show
        取消添加按钮 id=framework_insert_hide
        清空品牌选择栏并添加空白栏
        清空型号选择栏并添加空白栏
         */
        framework_table.show()
        framework_insert_show.hide()
        framework_insert_hide.show()
    }

    function framework_hide() {
        /*
        添加镜框表格 id=framework_table
        添加镜框按钮 id=framework_insert_show
        取消添加按钮 id=framework_insert_hide
         */
        framework_table.hide()
        framework_insert_show.show()
        framework_insert_hide.hide()
    }

    function order_content(content) {
        // 传入json字符串显示到id=order_content的表格位置
        content = jQuery.parseJSON(content)
        html = ''
        html += '<tr>'
        html += '<td><span>' + content.product + '</span></td>'
        html += '<td><span>' + content.brand + '</span></td>'
        html += '<td colspan="8"><span>' + content.model + '</span></td>'
        html += '</tr>'
        $('#order_content').append(html)
        $("#order_banner").show()
    }

    $.fn.serializeJsonStr = function () {
        // 把from表单内容转换为json字符串
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
