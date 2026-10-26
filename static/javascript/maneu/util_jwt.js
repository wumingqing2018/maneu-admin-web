// ================================================================
// 1. 全局 Ajax 设置：自动注入 Authorization，跳过刷新接口
// ================================================================
$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (settings.url.indexOf('/refresh_token/') !== -1) return;
            var token = localStorage.getItem('access_token');
            if (token) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + token);
            }
        }
    });
});

// ================================================================
// 2. 刷新 Token —— 改为 JSON 提交，适配新后端
//    请求: POST /refresh_token/  body: {"refresh_token": "..."}
//    响应: {status, message, content: {access_token}}
// ================================================================
function refreshAccessToken() {
    var dfd = $.Deferred();
    var refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
        dfd.reject('No refresh token');
        return dfd.promise();
    }

    $.ajax({
        url: '/refresh_token/',
        method: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({ refresh_token: refreshToken })
    }).done(function (res) {
        // 新后端返回 content.access_token
        if (res && res.status === true && res.content && res.content.access_token) {
            dfd.resolve(res.content);
        } else {
            dfd.reject((res && res.message) || 'Invalid refresh response');
        }
    }).fail(function (xhr) {
        dfd.reject(xhr);
    });

    return dfd.promise();
}

// ================================================================
// 3. 401 拦截 + 自动刷新重放
// ================================================================
var isRefreshing = false;
var failedRequestsQueue = [];

$(document).ajaxError(function (event, xhr, settings) {
    if (xhr.status !== 401) return;

    // 刷新接口自身 401 → 直接登出
    if (settings.url.indexOf('/refresh_token/') !== -1) {
        localStorage.clear();
        window.location.href = '/login/';
        return;
    }

    // 排队：重放时显式携带新 token，避免依赖 beforeSend 的隐式行为
    failedRequestsQueue.push(function (newToken) {
        var opts = $.extend({}, settings);
        opts.headers = $.extend({}, settings.headers, {
            'Authorization': 'Bearer ' + newToken
        });
        return $.ajax(opts);
    });

    if (isRefreshing) return;
    isRefreshing = true;

    refreshAccessToken()
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
        .always(function () {
            isRefreshing = false;
        });
});

// ================================================================
// 4. 登出
// ================================================================
$(".logoutBtn").click(function () {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/';
});

// ================================================================
// 5. 页面主逻辑
// ================================================================
(function () {
    'use strict';

    // ---------- 工具 ----------
    function val(id) {
        return ($('#' + id).val() || '').trim();
    }

    function getToken() {
        return localStorage.getItem('access_token') || '';
    }

    function showError(msg) {
        alert(msg || '操作失败，请稍后重试');
    }

    function getNowForDatetimeLocal() {
        var d = new Date();
        var pad = function (n) { return String(n).padStart(2, '0'); };
        return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) +
            'T' + pad(d.getHours()) + ':' + pad(d.getMinutes());
    }

    function setupToggle(btnId, panelId) {
        var $btn = $('#' + btnId);
        var $panel = $('#' + panelId);
        if (!$btn.length || !$panel.length) return;
        $btn.on('click', function () {
            $panel.slideToggle(200);
            $btn.find('i').toggleClass('bi-chevron-down bi-chevron-up');
        });
    }

    // ---------- 收集产品参数 ----------
    function collectStoreContent() {
        var keys = [];
        var obj = {};
        for (var i = 1; i <= 12; i++) {
            var key = val('key' + i);
            var v   = val('val' + i);
            if (!key) continue;
            if (keys.indexOf(key) !== -1) {
                showError('产品参数名「' + key + '」重复，请修改后再提交');
                return null;
            }
            keys.push(key);
            obj[key] = v;
        }
        if (keys.length === 0) {
            showError('请至少填写一组产品参数');
            return null;
        }
        return JSON.stringify([obj]);
    }

    // ---------- 提交 ----------
    var isSubmitting = false;

    function submitOrder() {
        if (isSubmitting) return;

        var storeContent = collectStoreContent();
        if (storeContent === null) return;

        var payload = {
            time:         $('#time').val(),
            name:         val('name'),
            phone:        val('phone'),
            remark:       val('remark'),
            storeContent: storeContent
        };

        var token = getToken();
        if (!token) {
            alert('请先登录');
            window.location.href = '/login/';
            return;
        }

        var $btn = $('#submitOrderBtn');
        var originalText = $btn.html();

        isSubmitting = true;
        $btn.prop('disabled', true)
            .html('<span class="spinner-border spinner-border-sm me-1"></span>提交中...');

        $.ajax({
            url: window.STORE_INSERT_API,
            method: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(payload),
            success: function (res) {
                if (!res || res.status !== true) {
                    showError((res && res.message) || '提交失败');
                    return;
                }

                // 兼容两种响应结构：
                // A) {status, message, content: {index_id, store, guest}}
                // B) {status, message, content: {}}
                var c = res.content || {};
                var storeStatus = (c.store && typeof c.store.status !== 'undefined') ? c.store.status : undefined;
                var guestStatus = (c.guest && typeof c.guest.status !== 'undefined') ? c.guest.status : undefined;

                if (storeStatus === undefined && guestStatus === undefined) {
                    alert('提交成功');
                    location.href = window.STORE_LIST_URL || '/';
                    return;
                }

                if (storeStatus && guestStatus) {
                    alert('提交成功');
                    location.href = window.STORE_LIST_URL || '/';
                    return;
                }

                var msgs = [];
                if (c.store && !c.store.status) msgs.push('产品：' + (c.store.message || '保存失败'));
                if (c.guest && !c.guest.status) msgs.push('客户：' + (c.guest.message || '保存失败'));
                showError(msgs.join('\n') || '提交失败');
            },
            error: function (xhr) {
                if (xhr.status === 401) return;   // 交给全局 ajaxError（刷新 + 重放）
                var msg = '网络错误，请稍后重试';
                try {
                    var data = JSON.parse(xhr.responseText);
                    msg = data.message || msg;
                } catch (e) {}
                showError(msg);
            },
            complete: function (xhr) {
                if (xhr.status === 401) return;   // 保持"提交中"，等重放结束
                isSubmitting = false;
                $btn.prop('disabled', false).html(originalText);
            }
        });
    }

    // ---------- 初始化 ----------
    $(function () {
        $('#time').val(getNowForDatetimeLocal());
        setupToggle('toggleProduct', 'productExtra');
        $('#submitOrderBtn').on('click', submitOrder);
        $('#guestSection input, #storeSection input').on('keypress', function (e) {
            if (e.which === 13) {
                e.preventDefault();
                submitOrder();
            }
        });
    });
})();