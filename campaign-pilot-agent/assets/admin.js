jQuery(document).ready(function($) {
    
    // Cache DOM elements
    const $agentForm = $('#cpa-agent-form');
    const $runAgentBtn = $('#run-agent-btn');
    const $refreshBtn = $('#refresh-dashboard-btn');
    const $agentStatus = $('#agent-status');
    const $loadingOverlay = $('#cpa-loading-overlay');
    const $tableBody = $('#dashboard-table-body');
    
    // Initialize
    init();
    
    function init() {
        bindEvents();
        // Auto-refresh every 30 seconds
        setInterval(refreshDashboard, 30000);
    }
    
    function bindEvents() {
        $agentForm.on('submit', handleAgentFormSubmit);
        $refreshBtn.on('click', handleRefreshClick);
        $(document).on('click', '.view-details', handleViewDetails);
    }
    
    function handleAgentFormSubmit(e) {
        e.preventDefault();
        
        const formData = {
            action: 'cpa_run_agent',
            nonce: cpa_ajax.nonce,
            campaign_length: $('#campaign_length').val(),
            campaign_budget: $('#campaign_budget').val(),
            campaign_copy: $('#campaign_copy').val()
        };
        
        showLoading(true);
        setButtonState($runAgentBtn, 'loading');
        
        $.ajax({
            url: cpa_ajax.ajax_url,
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    showStatus('success', `✅ ${response.data.message}! Launched ${response.data.campaigns_launched} campaigns.`);
                    
                    // Refresh dashboard after a short delay
                    setTimeout(function() {
                        refreshDashboard();
                    }, 2000);
                    
                } else {
                    showStatus('error', '❌ Failed to launch agent flow. Please try again.');
                }
            },
            error: function() {
                showStatus('error', '❌ Connection error. Please check your internet connection.');
            },
            complete: function() {
                showLoading(false);
                setButtonState($runAgentBtn, 'normal');
            }
        });
    }
    
    function handleRefreshClick(e) {
        e.preventDefault();
        refreshDashboard();
    }
    
    function refreshDashboard() {
        setButtonState($refreshBtn, 'loading');
        
        $.ajax({
            url: cpa_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'cpa_refresh_dashboard',
                nonce: cpa_ajax.nonce
            },
            success: function(response) {
                if (response.success) {
                    updateDashboardTable(response.data);
                    updateMetrics(response.data);
                    showNotification('Dashboard refreshed successfully!');
                } else {
                    showNotification('Failed to refresh dashboard data.', 'error');
                }
            },
            error: function() {
                showNotification('Connection error while refreshing data.', 'error');
            },
            complete: function() {
                setButtonState($refreshBtn, 'normal');
            }
        });
    }
    
    function updateDashboardTable(campaigns) {
        if (!campaigns || campaigns.length === 0) {
            $tableBody.html('<tr><td colspan="9" class="cpa-empty-state"><div class="cpa-empty-icon">📈</div><h3>No active campaigns yet</h3><p>Launch your first multi-agent flow to start seeing campaign data here.</p></td></tr>');
            return;
        }
        
        let html = '';
        campaigns.forEach(function(campaign) {
            const viewsClass = campaign.views_increase >= 0 ? 'positive' : 'negative';
            const salesClass = campaign.sales_increase >= 0 ? 'positive' : 'negative';
            const viewsIcon = campaign.views_increase >= 0 ? '↗' : '↘';
            const salesIcon = campaign.sales_increase >= 0 ? '↗' : '↘';
            
            html += `
                <tr class="campaign-row" data-campaign="${campaign.campaign_id}">
                    <td class="campaign-id">${escapeHtml(campaign.campaign_id)}</td>
                    <td class="product-name">
                        <strong>${escapeHtml(campaign.product_name)}</strong>
                        <span class="product-id">ID: ${campaign.product_id}</span>
                    </td>
                    <td>
                        <span class="status-badge ${campaign.campaign_status}">
                            ${capitalize(campaign.campaign_status)}
                        </span>
                    </td>
                    <td class="metric-value">${formatNumber(campaign.page_views)}</td>
                    <td class="metric-value">${formatNumber(campaign.sales)}</td>
                    <td>
                        <span class="change-value ${viewsClass}">
                            ${viewsIcon}${Math.abs(campaign.views_increase)}%
                        </span>
                    </td>
                    <td>
                        <span class="change-value ${salesClass}">
                            ${salesIcon}${Math.abs(campaign.sales_increase)}%
                        </span>
                    </td>
                    <td class="budget-value">$${formatCurrency(campaign.budget)}</td>
                    <td>
                        <button class="button button-small view-details" data-campaign="${campaign.campaign_id}">
                            View Details
                        </button>
                    </td>
                </tr>
            `;
        });
        
        $tableBody.html(html);
        
        // Add animation effect
        $('.campaign-row').hide().fadeIn(300);
    }
    
    function updateMetrics(campaigns) {
        if (!campaigns || campaigns.length === 0) return;
        
        const totalCampaigns = campaigns.length;
        const totalViews = campaigns.reduce((sum, c) => sum + parseInt(c.page_views), 0);
        const totalSales = campaigns.reduce((sum, c) => sum + parseInt(c.sales), 0);
        
        animateValue('#total-campaigns', parseInt($('#total-campaigns').text()) || 0, totalCampaigns);
        animateValue('#total-views', parseInt($('#total-views').text().replace(/,/g, '')) || 0, totalViews);
        animateValue('#total-sales', parseInt($('#total-sales').text().replace(/,/g, '')) || 0, totalSales);
    }
    
    function animateValue(selector, start, end) {
        const $element = $(selector);
        const duration = 1000;
        const startTime = performance.now();
        
        function updateValue(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = Math.floor(start + (end - start) * progress);
            $element.text(formatNumber(currentValue));
            
            if (progress < 1) {
                requestAnimationFrame(updateValue);
            }
        }
        
        requestAnimationFrame(updateValue);
    }
    
    function handleViewDetails(e) {
        const campaignId = $(e.target).data('campaign');
        
        // Mock detailed view - in real implementation, this would open a modal or navigate to detail page
        alert(`Campaign Details for: ${campaignId}\n\nThis would show detailed analytics, performance charts, and campaign settings in a real implementation.`);
    }
    
    function showLoading(show) {
        if (show) {
            $loadingOverlay.removeClass('hidden');
        } else {
            $loadingOverlay.addClass('hidden');
        }
    }
    
    function setButtonState($button, state) {
        const originalText = $button.data('original-text') || $button.html();
        $button.data('original-text', originalText);
        
        switch (state) {
            case 'loading':
                $button.prop('disabled', true);
                if ($button.is('#run-agent-btn')) {
                    $button.html('<span class="dashicons dashicons-update"></span> Launching Agents...');
                } else {
                    $button.html('<span class="dashicons dashicons-update"></span> Refreshing...');
                }
                break;
            case 'normal':
                $button.prop('disabled', false);
                $button.html(originalText);
                break;
        }
    }
    
    function showStatus(type, message) {
        $agentStatus.removeClass('hidden success error')
                   .addClass(type)
                   .text(message);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            $agentStatus.addClass('hidden');
        }, 5000);
    }
    
    function showNotification(message, type = 'success') {
        // Create temporary notification
        const $notification = $(`
            <div class="notice notice-${type} is-dismissible cpa-notification" style="margin: 10px 0;">
                <p>${message}</p>
            </div>
        `);
        
        $('.cpa-container').prepend($notification);
        
        // Auto-remove after 3 seconds
        setTimeout(function() {
            $notification.fadeOut(300, function() {
                $(this).remove();
            });
        }, 3000);
    }
    
    // Utility functions
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }
    
    function formatCurrency(num) {
        return parseFloat(num).toFixed(2);
    }
    
    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
    
    // Real-time status updates simulation
    function simulateRealTimeUpdates() {
        setInterval(function() {
            // Randomly update status dot to simulate agent activity
            const $statusDot = $('.cpa-status-dot');
            $statusDot.toggleClass('active');
            
            setTimeout(function() {
                $statusDot.addClass('active');
            }, 1000);
        }, 10000);
    }
    
    // Initialize real-time updates
    simulateRealTimeUpdates();
    
    // Handle form validation
    $agentForm.find('input, select, textarea').on('blur change', function() {
        validateForm();
    });
    
    function validateForm() {
        const campaignLength = $('#campaign_length').val();
        const campaignBudget = $('#campaign_budget').val();
        
        let isValid = true;
        
        if (!campaignLength) {
            isValid = false;
        }
        
        if (!campaignBudget || campaignBudget < 5 || campaignBudget > 1000) {
            isValid = false;
        }
        
        $runAgentBtn.prop('disabled', !isValid);
        
        return isValid;
    }
    
    // Initial validation
    validateForm();
    
    console.log('Campaign Pilot Agent Dashboard initialized successfully!');
}); 