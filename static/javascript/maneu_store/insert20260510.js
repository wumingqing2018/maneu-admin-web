        // ==================== 全局配置与工具函数 ====================

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
                    btn.html('<span class="spinner-border spinner-border-sm me-1" role="status"></span> 提交中...');
                } else {
                    btn.prop('disabled', false);
                    if (btn.data('original-text')) {
                        btn.html(btn.data('original-text'));
                    }
                }
            }
        }

        // ==================== 表单验证 ====================
        function validateForm() {
            const name = $('#name').val().trim();
            const phone = $('#phone').val().trim();

            if (!name) {
                showError('请填写客户姓名');
                $('#name').focus();
                return false;
            }
            if (!phone) {
                showError('请填写联系电话');
                $('#phone').focus();
                return false;
            }
            // 简单手机号验证（可根据需要调整）
            const phoneRegex = /^1[3-9]\d{9}$|^\d{7,15}$/;
            if (!phoneRegex.test(phone)) {
                showError('请输入有效的联系电话');
                $('#phone').focus();
                return false;
            }
            return true;
        }

        // ==================== 收集产品参数 ====================
        function collectCustomData() {
            const keys = [];
            const customObj = {};
            for (let i = 1; i <= 12; i++) {
                const key = $(`#key${i}`).val().trim();
                const val = $(`#val${i}`).val().trim();
                if (key === '') continue;
                if (keys.includes(key)) {
                    showError(`产品参数名"${key}"重复，请修改后再提交。`);
                    return null;
                }
                keys.push(key);
                customObj[key] = val;
            }
            return [customObj];
        }

        // ==================== 提交订单 ====================
        function submitOrder() {
            // 防重复提交
            if (isSubmitting) return;

            // 表单验证
            if (!validateForm()) return;

            // 收集产品参数
            const storeData = collectCustomData();
            if (storeData === null) return;

            // 构建请求数据
            const requestData = {
                time: $('#time').val(),
                name: $('#name').val().trim(),
                phone: $('#phone').val().trim(),
                age: $('#age').val().trim(),
                sex: $('#sex').val().trim(),
                dfh: $('#dfh').val().trim(),
                ot: $('#ot').val().trim(),
                em: $('#em').val().trim(),
                remark: $('#remark').val().trim(),
                storeContent: JSON.stringify(storeData)
            };

            const $submitBtn = $('#submitOrderBtn');
            setSubmitting($submitBtn, true);

            $.ajax({
                url: STORE_INSERT_API,
                method: 'POST',      // 保持与原代码一致（后端接口为 GET）
                data: requestData,
                success: function(res) {
                    setSubmitting($submitBtn, false);
                    if (res.status === true) {
                        alert('记录提交成功');
                        // 可选：提交成功后重置表单（保留时间默认值）
                        $('#name, #phone, #remark, #age, #sex, #dfh, #ot, #em').val('');
                        for (let i = 1; i <= 12; i++) {
                            $(`#key${i}`).val('');
                            $(`#val${i}`).val('');
                        }
                        $('#name').focus();
                    } else {
                        showError('提交失败：' + (res.message || '未知错误'));
                    }
                },
                error: function(xhr) {
                    setSubmitting($submitBtn, false);
                    showError('网络错误，请稍后重试');
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

            // 绑定提交按钮事件
            $('#submitOrderBtn').on('click', submitOrder);

            // 可选：支持按回车键快速提交（在表单输入框内按回车）
            $('#guestSection input, #storeSection input').on('keypress', function(e) {
                if (e.which === 13) {
                    e.preventDefault();
                    submitOrder();
                }
            });
        });