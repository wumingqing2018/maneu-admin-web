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

    // ---- 4. 统一请求入口（Promise + abort/readyState 兼容） ----

    /**
     * 发送一次请求，401 时刷新 token 并重放
     * 返回一个"增强 Promise"：
     *   - 保留 jQuery Promise 的 done / fail / always / then
     *   - 额外提供 abort()：取消当前请求（含重放阶段）
     *   - 额外提供 readyState：pending 时 0，settled 时 4
     */
    function sendWithRetry(opts) {
        var dfd       = $.Deferred();
        var currentXHR = null;
        var aborted   = false;

        function fire(retried) {
            if (aborted) return;

            currentXHR = $.ajax(opts);

            currentXHR.done(function (res) {
                dfd.resolve(res);
            }).fail(function (xhr, status, error) {
                if (aborted || status === 'abort') {
                    dfd.reject(xhr, 'abort', 'abort');
                    return;
                }
                if (!xhr || xhr.status !== 401 || retried) {
                    dfd.reject(xhr, status, error);
                    return;
                }
                refreshAccessToken().then(function () {
                    fire(true);
                }, function () {
                    redirectToLogin();
                    dfd.reject(xhr, status, error);
                });
            });
        }

        fire(false);

        var promise = dfd.promise();

        // ⭐ 关键修复：补上 abort()
        promise.abort = function () {
            aborted = true;
            if (currentXHR && typeof currentXHR.abort === 'function') {
                currentXHR.abort();   // 会触发 .fail(status='abort')，进而 reject dfd
            } else {
                dfd.reject(null, 'abort', 'abort');
            }
        };

        // ⭐ 关键修复：补上 readyState（供 if (readyState !== 4) 判断）
        try {
            Object.defineProperty(promise, 'readyState', {
                configurable: true,
                get: function () {
                    return dfd.state() === 'pending' ? 0 : 4;
                }
            });
        } catch (e) {
            // 某些老浏览器 defineProperty 不支持 getter，忽略
            promise.readyState = 4;
        }

        return promise;
    }

    /**
     * 统一请求入口（参数与 $.ajax 一致）
     */
    window.apiRequest = function (options) {
        if (!options || !options.url) {
            var bad = $.Deferred();
            bad.reject(null, 'error', new Error('apiRequest: url is required'));
            var badPromise = bad.promise();
            badPromise.abort = function () {};
            badPromise.readyState = 4;
            return badPromise;
        }

        var opts = $.extend({}, options);
        if (options.headers) opts.headers = $.extend({}, options.headers);

        return sendWithRetry(opts);
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