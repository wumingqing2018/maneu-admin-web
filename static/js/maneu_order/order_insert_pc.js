$(document).ready(function () {
    var InputCount = 1;
    $("#AddMoreTextBox").click(function (e) {
        InputCount++;
        $("#Product_Orders_TABLE").append('    <div class="input-group input-group-sm mb-2">\n' +
            '        <input autocomplete="off" type="text" name="arg' + InputCount + '0" class="form-control" style="width: 12%" placeholder="类别">\n' +
            '        <input autocomplete="off" type="text" name="arg' + InputCount + '1" class="form-control" style="width: 12%" placeholder="品牌">\n' +
            '        <input autocomplete="off" type="text" name="arg' + InputCount + '2" class="form-control" style="width: 12%" placeholder="型号">\n' +
            '        <input autocomplete="off" type="text" name="arg' + InputCount + '3" class="form-control" style="width: 52%" placeholder="参数">\n' +
            '        <input autocomplete="off" type="text" name="arg' + InputCount + '4" class="form-control" style="width: 12%" placeholder="价格">\n' +
            '    </div>\n' +
            '</div>\n');
    });
    $('#DeleteTextBox').click(function (e) {
        if (InputCount > 1) {
            InputCount = InputCount - 1;
            $("#Product_Orders_TABLE>div").last().remove()
        }
    })
    $('#insert').click(function () {
        Product_Orders_json = $('#Product_Orders').serializeJsonStr();
        $('#Product_Orders_json').val(Product_Orders_json);
        Vision_Solutions_json = $('#Vision_Solutions').serializeJsonStr();
        $('#Vision_Solutions_json').val(Vision_Solutions_json);
        order_json = $('#order').serializeJsonStr();
        $('#order_json').val(order_json);
    })
    $('#Vision_Solutions_showbutton').click(function () {
            $('#Vision_Solutions_showbutton').attr('style', 'display: none')
            $('#Vision_Solutions_hidebutton').attr('style', 'display: block')
            $(".Vision_Solutions").attr('style', 'display: block')
        }
    )
    $('#Vision_Solutions_hidebutton').click(function () {
            $('#Vision_Solutions_hidebutton').attr('style', 'display: none');
            $('#Vision_Solutions_showbutton').attr('style', 'display: block');
            $(".Vision_Solutions").attr('style', 'display: none');
            $("#Vision_Solutions")[0].reset();
        }
    )
    $('#Store_showbutton').click(function () {
            $('#Store_showbutton').attr('style', 'display: none')
            $('#Store_hidebutton').attr('style', 'display: block')
            $(".Store").attr('style', 'display: block')
        }
    )
    $('#Store_hidebutton').click(function () {
            $('#Store_hidebutton').attr('style', 'display: none');
            $('#Store_showbutton').attr('style', 'display: block');
            $(".Store").attr('style', 'display: none');
            $("#Store")[0].reset();
        }
    )
});
