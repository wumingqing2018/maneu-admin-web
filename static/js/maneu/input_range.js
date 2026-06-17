$(document).ready(
    /*
    sphere = 度数
    id = sphere 的滑动条改变后， 在id = sphere_msg显示sphere的值
     */
    $('#sphere').change(function () {
        $('#sphere_msg').html($('#sphere').val())
    }),
    /*
    astigmatic = 散光
    id = astigmatic 的滑动条改变后， 在id = astigmatic_msg显示astigmatic的值
     */
    $('#astigmatic').change(function () {
        $('#astigmatic_msg').html($('#astigmatic').val())
    }),
    /*
    count = 数量
    id = count 的滑动条改变后， 在id = count_msg显示count的值
     */
    $('#count').change(function () {
        $('#count_msg').html($('#count').val())
    }),
    /*
    refraction = 折射
    id = refraction 的滑动条改变后， 在id = refraction_msg显示refraction的值
     */
    $('#refraction').change(function () {
        $('#refraction_msg').html($('#refraction').val())
    }),
    /*
    pd = 瞳距
    id = pd 的滑动条改变后， 在id = pd_msg显示pd的值
     */
    $('#pd').change(function () {
        $('#pd_msg').html($('#pd').val())
    }),
    /*
    add = 渐进
    id = add 的滑动条改变后， 在id = add_msg显示add 的值
     */
    $("#add").change(function () {
        $('#add_msg').html($('#add').val())
    }),
    /*
    deviation = 偏位
    id = deviation 的滑动条改变后， 在id = deviation_msg显示deviation的值
     */
    $('#deviation').change(function () {
        $('#deviation_msg').html($('#deviation').val())
    }),
)
