
// 将 "YYYY-MM-DD HH:MM:SS" 或类似格式转换为 datetime-local 可识别的 "YYYY-MM-DDTHH:MM"
function toDatetimeLocal(value) {
    if (!value) return '';
    if (value.includes('T')) return value.substring(0, 16);
    let parts = value.split(' ');
    if (parts.length >= 2) {
        return parts[0] + 'T' + parts[1].substring(0, 5);
    }
    return value.substring(0, 16);
}

// 通用错误提示（风格与订单管理页保持一致）
function showError(message) {
    alert(message || '操作失败，请稍后重试');
}

// ==================== 防重复提交控制 ====================
let isSubmitting = false;

function setSubmitting(btn, state, originalText = null) {
    isSubmitting = state;
    if (btn) {
        if (state) {
            btn.prop('disabled', true);
            btn.data('original-text', btn.html());
            btn.html('<span class="spinner-border spinner-border-sm me-1" role="status"></span> 处理中...');
        } else {
            btn.prop('disabled', false);
            if (btn.data('original-text')) {
                btn.html(btn.data('original-text'));
            }
        }
    }
}

// ==================== 数据加载与渲染 ====================
// 加载状态标签控制
function setLoadStatus($el, status, message) {
    $el.removeClass('status-empty status-loaded status-warning');
    if (status === 'loading') {
        $el.addClass('status-empty').text(message || '加载中...');
    } else if (status === 'success') {
        $el.addClass('status-loaded').text(message || '已加载');
    } else if (status === 'error') {
        $el.addClass('status-warning').text(message || '加载失败');
    }
}

// 渲染客户信息
function renderGuestDetail(guest) {
    if (guest?.status) {
        const g = guest.content;
        $('#time').val(toDatetimeLocal(g.time));
        $('#name').val(g.name || '');
        $('#phone').val(g.phone || '');
        $('#sex').val(g.sex || '');
        $('#age').val(g.age || '');
        $('#dfh').val(g.dfh || '');
        $('#em').val(g.em || '');
        $('#ot').val(g.ot || '');
        $('#remark').val(g.remark || '');
        setLoadStatus($('#guestLoadStatus'), 'success', '已加载');
    } else {
        setLoadStatus($('#guestLoadStatus'), 'error', '加载失败');
    }
}

// 渲染产品信息
function renderStoreDetail(store) {
    if (store?.status) {
        const storeData = store.content;
        // 兼容数组格式（如 [{key: val}…]）
        const obj = Array.isArray(storeData) ? (storeData[0] || {}) : storeData;
        let idx = 1;
        // 清空所有键值对输入框
        for (let i = 1; i <= 12; i++) {
            $(`#key${i}`).val('');
            $(`#val${i}`).val('');
        }
        for (const [key, value] of Object.entries(obj)) {
            if (idx <= 12) {
                $(`#key${idx}`).val(key);
                $(`#val${idx}`).val(value);
                idx++;
            }
        }
        setLoadStatus($('#storeLoadStatus'), 'success', '已加载');
    } else {
        setLoadStatus($('#storeLoadStatus'), 'error', '加载失败');
    }
}

// 主加载函数（带加载状态和请求取消）
let currentDetailRequest = null;
function loadDetail() {
    if (currentDetailRequest && currentDetailRequest.readyState !== 4) {
        currentDetailRequest.abort();
    }
    // 重置状态标签为“加载中”
    setLoadStatus($('#guestLoadStatus'), 'loading', '加载中...');
    setLoadStatus($('#storeLoadStatus'), 'loading', '加载中...');

    currentDetailRequest = $.ajax({
        url: STORE_API.detail,
        method: 'POST',
        data: { index_id: INDEX_ID },
        success: function(res) {
            if (!res?.status) {
                showError('加载详情失败：' + (res?.message || ''));
                setLoadStatus($('#guestLoadStatus'), 'error', '加载失败');
                setLoadStatus($('#storeLoadStatus'), 'error', '加载失败');
                return;
            }
            const { guest, store } = res.content;
            renderGuestDetail(guest);
            renderStoreDetail(store);
        },
        error: function(xhr) {
            if (xhr.statusText === 'abort') return;
            showError('网络错误，无法加载定制详情');
            setLoadStatus($('#guestLoadStatus'), 'error', '加载失败');
            setLoadStatus($('#storeLoadStatus'), 'error', '加载失败');
        }
    });
}

// ==================== 更新操作（带防抖与刷新） ====================
// 通用更新方法（GET 请求，沿用后端现有风格）
function performUpdate(url, data, successMsg, $btn, onSuccess) {
    if (isSubmitting) return;
    if (!confirm('确定要更新这条记录吗？')) return;

    setSubmitting($btn, true);
    $.ajax({
        url: url,
        method: 'POST',
        data: data,
        success: function(res) {
            setSubmitting($btn, false);
            if (res && res.status) {
                alert(successMsg);
                // 更新成功后重新加载详情，保持界面最新
                loadDetail();
                if (onSuccess) onSuccess(res);
            } else {
                showError('更新失败：' + (res?.message || '未知错误'));
            }
        },
        error: function(xhr) {
            setSubmitting($btn, false);
            showError('网络错误，请稍后重试');
        }
    });
}

// 更新客户信息
function updateGuest() {
    const data = {
        index_id: INDEX_ID,
        time: $('#time').val(),
        name: $('#name').val(),
        phone: $('#phone').val(),
        age: $('#age').val(),
        sex: $('#sex').val(),
        dfh: $('#dfh').val(),
        ot: $('#ot').val(),
        em: $('#em').val(),
        guestRemark: $('#remark').val()
    };
    performUpdate(STORE_API.guestUpdate, data, '客户信息更新成功', $('#guestUpdate'));
}

// 收集12组产品键值对
function collectStoreData() {
    const obj = {};
    const keysSeen = [];
    for (let i = 1; i <= 12; i++) {
        const key = $(`#key${i}`).val().trim();
        const val = $(`#val${i}`).val().trim();
        if (key === '') continue;
        if (keysSeen.includes(key)) {
            showError(`产品参数名"${key}"重复，请修改后再提交。`);
            return null;
        }
        keysSeen.push(key);
        obj[key] = val;
    }
    return obj;
}

// 更新产品信息
function updateStore() {
    const storeObj = collectStoreData();
    if (storeObj === null) return;
    const data = {
        index_id: INDEX_ID,
        storeContent: JSON.stringify([storeObj])
    };
    performUpdate(STORE_API.update, data, '产品信息更新成功', $('#storeUpdate'));
}

// ==================== 删除操作 ====================
function deleteOrder() {
    if (!confirm('确定要删除这条记录吗？此操作不可恢复。')) return;
    const $deleteBtn = $('#deleteOrder');
    setSubmitting($deleteBtn, true);
    $.ajax({
        url: STORE_API.delete,
        method: 'POST',
        data: { index_id: INDEX_ID },
        success: function(res) {
            setSubmitting($deleteBtn, false);
            if (res?.status) {
                alert('删除成功');
                location.replace("{% url 'maneu_store:index' %}");
            } else {
                showError('删除失败：' + (res?.message || ''));
            }
        },
        error: function() {
            setSubmitting($deleteBtn, false);
            showError('网络错误，删除失败');
        }
    });
}

// ==================== 二维码下载 ====================
function downloadQRCode() {
    $.ajax({
        url: STORE_API.qrcode,
        method: 'POST',
        data: { index_id: INDEX_ID },
        xhrFields: { responseType: 'blob' },
        success: function(blob) {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = INDEX_ID + '.png';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        },
        error: function() {
            showError('二维码生成失败，请稍后重试');
        }
    });
}

// ==================== 折叠面板切换 ====================
function setupToggle(triggerId, panelId) {
    $(triggerId).on('click', function() {
        const $panel = $(panelId);
        $panel.slideToggle(200);
        $(this).find('i').toggleClass('bi-chevron-down bi-chevron-up');
    });
}

// ==================== 页面初始化 ====================
$(function() {
    // 初始化折叠面板
    setupToggle('#toggleGuest', '#guestExtra');
    setupToggle('#toggleProduct', '#productExtra');

    // 绑定所有操作按钮
    $('#guestUpdate').on('click', updateGuest);
    $('#storeUpdate').on('click', updateStore);
    $('#deleteOrder').on('click', deleteOrder);
    $('#generateQrCode').on('click', downloadQRCode);

    // 加载详情数据
    loadDetail();
});