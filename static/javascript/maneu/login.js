// ========================================================================
// 1. 工具函数
// ========================================================================
function isValidPhone(phone) {
    return /^1[3-9]\d{9}$/.test(phone);
}

function showMessage(text, color = '#ff6b6b') {
    $('#msg').text(text).css('color', color);
}

function showLoginMessage(text, color = '#ff6b6b') {
    $('#login_msg').text(text).css('color', color);
}

// ========================================================================
// 3. 启动：先检查登录状态，再初始化登录页
// ========================================================================
$(document).ready(function () {
    checkLoginStatusThenInit();
});

function checkLoginStatusThenInit() {
    const refreshToken = localStorage.getItem('refresh_token');

    // 没有 refresh_token → 肯定未登录，直接显示表单
    if (!refreshToken) {
        $('#auth-check').hide();
        initLoginPage();
        return;
    }

    // 有 refresh_token → 向后端验证其有效性
    $.ajax({
        url: refreshUrl,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({refresh_token: refreshToken}),
        dataType: 'json',
        timeout: 8000
    }).done(function (res) {
        if (res && res.status === true && res.content && res.content.access_token) {
            // 验证成功 → 保存新 access_token → 跳转订单页
            localStorage.setItem('access_token', res.content.access_token);
            if (res.content.refresh_token) {
                localStorage.setItem('refresh_token', res.content.refresh_token);
            }
            window.location.replace(redirectUrl);
        } else {
            // 后端 200 但 status=false，视为无效
            clearAuthThenShowLogin();
        }
    }).fail(function (xhr) {
        if (xhr.status === 401) {
            // token 明确无效/过期 → 清除
            clearAuthThenShowLogin();
        } else {
            // 网络错误/超时 → 保留 token，仅显示登录表单
            $('#auth-check').hide();
            initLoginPage();
        }
    });
}

function clearAuthThenShowLogin() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    $('#auth-check').hide();
    initLoginPage();
}

// ========================================================================
// 4. 登录页主逻辑（原逻辑，仅调整外包装）
// ========================================================================
function initLoginPage() {
    const $call = $('#call');
    const $code = $('#code');
    const $sendsmsBtn = $('#sendsms-btn');
    const $waitBtn = $('#wait-btn');
    const $loginHold = $('#login-hold');
    const $loginBtn = $('#login-btn');

    let countdownTimer = null;
    let countdownSeconds = 0;

    // ---------- 登录按钮状态 ----------
    function toggleLoginButton() {
        if ($code.val().trim() === '') {
            $loginHold.show();
            $loginBtn.hide();
        } else {
            $loginHold.hide();
            $loginBtn.show();
        }
    }

    toggleLoginButton();
    $code.on('input', toggleLoginButton);

    // ---------- 验证码倒计时 ----------
    function startCountdown(seconds) {
        if (countdownTimer) clearInterval(countdownTimer);
        countdownSeconds = seconds;
        $sendsmsBtn.hide();
        $waitBtn.show().text(`${countdownSeconds}秒后可重试`);

        countdownTimer = setInterval(function () {
            countdownSeconds--;
            if (countdownSeconds <= 0) {
                clearInterval(countdownTimer);
                $waitBtn.hide();
                $sendsmsBtn.show().prop('disabled', false);
            } else {
                $waitBtn.text(`${countdownSeconds}秒后可重试`);
            }
        }, 1000);
    }

    // ---------- 发送验证码 ----------
    $sendsmsBtn.on('click', function () {
        const phone = $call.val().trim();

        if (!phone) {
            showMessage('请输入手机号码');
            return;
        }
        if (!isValidPhone(phone)) {
            showMessage('手机号格式不正确');
            return;
        }

        $sendsmsBtn.prop('disabled', true);

        $.ajax({
            url: sendsmsUrl,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({call: phone}),
            dataType: 'json',
            success: function (res) {
                if (res && res.status === true) {
                    showMessage('验证码已发送', '#4caf50');
                    startCountdown(60);
                } else {
                    showMessage((res && res.message) || '发送失败');
                    $sendsmsBtn.prop('disabled', false);
                }
            },
            error: function (xhr) {
                const errMsg = (xhr.responseJSON && xhr.responseJSON.message) || '网络错误，请稍后重试';
                showMessage(errMsg);
                $sendsmsBtn.prop('disabled', false);
            }
        });
    });

    // ---------- 登录 ----------
    $loginBtn.on('click', function () {
        const phone = $call.val().trim();
        const code = $code.val().trim();

        if (!phone || !code) {
            showMessage('请填写手机号和验证码');
            return;
        }
        if (!isValidPhone(phone)) {
            showMessage('手机号格式不正确');
            return;
        }

        $loginBtn.prop('disabled', true).text('登录中...');

        $.ajax({
            url: loginApiUrl,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({call: phone, code: code}),
            dataType: 'json',
            success: function (res) {
                if (res && res.status === true) {
                    const data = res.content || {};
                    if (data.access_token) localStorage.setItem('access_token', data.access_token);
                    if (data.refresh_token) localStorage.setItem('refresh_token', data.refresh_token);
                    window.location.replace(redirectUrl);
                } else {
                    showLoginMessage((res && res.message) || '登录失败');
                    $loginBtn.prop('disabled', false).text('登录');
                }
            },
            error: function (xhr) {
                let errMsg = '登录请求失败，请稍后重试';
                try {
                    const d = JSON.parse(xhr.responseText);
                    errMsg = d.message || errMsg;
                } catch (e) {
                }
                showLoginMessage(errMsg);
                $loginBtn.prop('disabled', false).text('登录');
            }
        });
    });
}
