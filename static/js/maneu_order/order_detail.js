$(document).ready(function () {
    upline = Object.keys(maneu_store).length / 5
    for (i = 1; i <= upline; i++) {
        $('#store_table').append("            <tr>\n" +
            "                <td colspan='2'>\n" +
            "                    <span>" + maneu_store['arg' + i + '0'] + "</span>\n" +
            "                </td>\n" +
            "                <td colspan='2'>\n" +
            "                    <span>" + maneu_store['arg' + i + '1'] + "</span>\n" +
            "                </td>\n" +
            "                <td colspan='2'>\n" +
            "                    <span>" + maneu_store['arg' + i + '2'] + "</span>\n" +
            "                </td>\n" +
            "                <td colspan='2'>\n" +
            "                    <span>" + maneu_store['arg' + i + '3'] + "</span>\n" +
            "                </td>\n" +
            "                <td>\n" +
            "                    <span>" + maneu_store['arg' + i + '4'] + "</span>\n" +
            "                </td>\n" +
            "            </tr>\n")
    }
})
