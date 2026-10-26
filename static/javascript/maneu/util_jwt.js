/* =========================================================================
 * 全局公共 JS：认证、JWT 刷新、登出
 * 幂等设计：重复引入 / 重复执行不会造成重复绑定
 * ========================================================================= */
(function () {
    'use strict';

    // ---- 防重复初始化 ----
    if (window.__maneuCommonInited) return;
    window.__maneuCommonInited = true;

    // ---- 1. ajaxSetup：自动注入 Authorization ----
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if ((settings.url || '').indexOf('/refresh_token/') !== -1) return;
            var token = localStorage.getItem('access_token');
            if (token) xhr.setRequestHeader('Authorization', 'Bearer ' + token);
        }
    });

    // ---- 2. 刷新 Token ----
    window.refreshAccessToken = function () {
        var dfd = $.Deferred();
        var refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) { dfd.reject('No refresh token'); return dfd.promise(); }

        $.ajax({
            url: '/refresh_token/',
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({ refresh_token: refreshToken })
        }).done(function (res) {
            if (res && res.status === true && res.content && res.content.access_token) {
                dfd.resolve(res.content);
            } else {
                dfd.reject((res && res.message) || 'Invalid refresh response');
            }
        }).fail(function (xhr) { dfd.reject(xhr); });

        return dfd.promise();
    };

    // ---- 3. 401 拦截 + 刷新重放 ----
    var isRefreshing = false;
    var failedRequestsQueue = [];

    $(document).off('ajaxError.maneuAuth').on('ajaxError.maneuAuth', function (event, xhr, settings) {
        if (xhr.status !== 401) return;

        if ((settings.url || '').indexOf('/refresh_token/') !== -1) {
            localStorage.clear();
            window.location.href = '/login/';
            return;
        }

        failedRequestsQueue.push(function (newToken) {
            var opts = $.extend({}, settings);
            opts.headers = $.extend({}, settings.headers, {
                'Authorization': 'Bearer ' + newToken
            });
            return $.ajax(opts);
        });

        if (isRefreshing) return;
        isRefreshing = true;

        window.refreshAccessToken()
            .done(function (content) {
                localStorage.setItem('access_token', content.access_token);
                if (content.refresh_token) {
                    localStorage.setItem('refresh_token', content.refresh_token);
                }
                var queue = failedRequestsQueue.slice();
                failedRequestsQueue = [];
                queue.forEach(function (retry) { retry(content.access_token); });
            })
            .fail(function () {
                localStorage.clear();
                window.location.href = '/login/';
            })
            .always(function () { isRefreshing = false; });
    });

    // ---- 4. 登出 ----
    $(document).off('click.maneuLogout').on('click.maneuLogout', '.logoutBtn', function () {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
    });
})();