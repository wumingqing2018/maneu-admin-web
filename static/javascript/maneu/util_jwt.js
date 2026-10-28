/* =========================================================================
 * 全局公共 JS：认证、JWT 刷新、统一请求包装、登出
 * ========================================================================= */
(function () {
    'use strict';

    if (window.__maneuCommonInited) return;
    window.__maneuCommonInited = true;

    var TOKEN_KEY   = 'access_token';
    var REFRESH_KEY = 'refresh_token';
    var REFRESH_URL = '/refresh_token/';
    var LOGIN_URL   = '/login/';

    // ---- 1. 兜底：自动注入 Authorization ----
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (String(settings.url || '').indexOf(REFRESH_URL) !== -1) return;
            var token = localStorage.getItem(TOKEN_KEY);
            if (token) xhr.setRequestHeader('Authorization', 'Bearer ' + token);
        }
    });

    // ---- 2. 刷新 Token（单飞） ----
    var refreshPromise = null;

    function refreshAccessToken() {
        if (refreshPromise) return refreshPromise;

        var refreshToken = localStorage.getItem(REFRESH_KEY);
        if (!refreshToken) {
            return $.Deferred().reject('No refresh token').promise();
        }

        refreshPromise = $.ajax({
            url: REFRESH_URL,
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({ refresh_token: refreshToken })
        }).then(function (res) {
            if (res && res.status === true && res.content && res.content.access_token) {
                localStorage.setItem(TOKEN_KEY, res.content.access_token);
                if (res.content.refresh_token) {
                    localStorage.setItem(REFRESH_KEY, res.content.refresh_token);
                }
                return res.content.access_token;
            }
            return $.Deferred().reject((res && res.message) || 'Invalid refresh response');
        }, function (xhr) {
            return $.Deferred().reject(xhr);
        }).always(function () {
            refreshPromise = null;
        });

        return refreshPromise;
    }
    window.refreshAccessToken = refreshAccessToken;

    // ---- 3. 统一获取 access_token ----
    window.getAccessToken = function () {
        return localStorage.getItem(TOKEN_KEY) || '';
    };

    function redirectToLogin() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(REFRESH_KEY);
        window.location.href = LOGIN_URL;
    }

    // ---- 4. 401 刷新后重放 ----
    function sendWithRetry(opts, retried) {
        return $.ajax(opts).then(function (res) {
            return res;
        }, function (xhr, status, error) {
            if (!xhr || xhr.status !== 401 || retried) {
                return $.Deferred().reject(xhr, status, error).promise();
            }

            return refreshAccessToken().then(function () {
                return sendWithRetry(opts, true);
            }, function () {
                redirectToLogin();
                return $.Deferred().reject(xhr, status, error).promise();
            });
        });
    }

    /**
     * 统一请求入口（参数与 $.ajax 一致）
     */
    window.apiRequest = function (options) {
        if (!options || !options.url) {
            return $.Deferred().reject(null, 'error', new Error('apiRequest: url is required')).promise();
        }
        var opts = $.extend({}, options);
        if (options.headers) opts.headers = $.extend({}, options.headers);
        return sendWithRetry(opts, false);
    };

    /**
     * 统一 JSON POST 入口
     */
    window.requestJSON = function (url, payload) {
        return window.apiRequest({
            url: url,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(payload || {}),
            dataType: 'json'
        });
    };

    // ---- 5. 登出 ----
    $(document).off('click.maneuLogout').on('click.maneuLogout', '.logoutBtn', function () {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(REFRESH_KEY);
        window.location.href = '/';
    });
})();
