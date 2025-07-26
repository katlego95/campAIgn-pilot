<?php
// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

$plugin = new CampaignPilotAgent();
$dashboard_data = $plugin->get_dashboard_data();
?>

<div class="wrap">
    <h1>
        <span class="dashicons dashicons-chart-line"></span>
        Campaign Pilot Agent Dashboard
    </h1>
    
    <div class="cpa-container">
        <!-- Settings Section -->
        <div class="cpa-settings-section">
            <div class="cpa-card">
                <h2>🤖 Multi-Agent Flow Settings</h2>
                <p class="description">Configure your AI agents to automatically monitor inventory and launch targeted campaigns</p>
                
                <form id="cpa-agent-form">
                    <div class="cpa-form-row">
                        <div class="cpa-form-group">
                            <label for="campaign_length">
                                <strong>Default Campaign Length</strong>
                                <span class="description">How long should campaigns run?</span>
                            </label>
                            <select id="campaign_length" name="campaign_length" required>
                                <option value="3">3 days</option>
                                <option value="7" selected>7 days</option>
                                <option value="14">14 days</option>
                                <option value="30">30 days</option>
                            </select>
                        </div>
                        
                        <div class="cpa-form-group">
                            <label for="campaign_budget">
                                <strong>Default Campaign Budget</strong>
                                <span class="description">Budget per campaign in USD</span>
                            </label>
                            <input type="number" id="campaign_budget" name="campaign_budget" 
                                   value="20" min="5" max="1000" step="5" required>
                        </div>
                    </div>
                    
                    <div class="cpa-form-group">
                        <label for="campaign_copy">
                            <strong>Campaign Copy Template (Optional)</strong>
                            <span class="description">Default copy for your campaigns. Use {product_name} for dynamic insertion.</span>
                        </label>
                        <textarea id="campaign_copy" name="campaign_copy" rows="3" 
                                  placeholder="Discover our amazing {product_name}! Limited time offer with free shipping."></textarea>
                    </div>
                    
                    <div class="cpa-button-group">
                        <button type="submit" id="run-agent-btn" class="button button-primary button-large">
                            <span class="dashicons dashicons-performance"></span>
                            Launch Multi-Agent Flow
                        </button>
                        <div id="agent-status" class="cpa-status hidden"></div>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Dashboard Section -->
        <div class="cpa-dashboard-section">
            <div class="cpa-card">
                <div class="cpa-dashboard-header">
                    <h2>📊 Real-time Campaign Performance</h2>
                    <div class="cpa-dashboard-controls">
                        <div class="cpa-status-indicator">
                            <span class="cpa-status-dot active"></span>
                            <span>AI Agents Active</span>
                        </div>
                        <button type="button" id="refresh-dashboard-btn" class="button button-secondary">
                            <span class="dashicons dashicons-update"></span>
                            Refresh Data
                        </button>
                    </div>
                </div>
                
                <div class="cpa-metrics-overview">
                    <div class="cpa-metric-card">
                        <div class="cpa-metric-value" id="total-campaigns"><?php echo count($dashboard_data); ?></div>
                        <div class="cpa-metric-label">Active Campaigns</div>
                    </div>
                    <div class="cpa-metric-card">
                        <div class="cpa-metric-value" id="total-views">
                            <?php 
                            $total_views = array_sum(array_column($dashboard_data, 'page_views'));
                            echo number_format($total_views);
                            ?>
                        </div>
                        <div class="cpa-metric-label">Total Page Views</div>
                    </div>
                    <div class="cpa-metric-card">
                        <div class="cpa-metric-value" id="total-sales">
                            <?php 
                            $total_sales = array_sum(array_column($dashboard_data, 'sales'));
                            echo number_format($total_sales);
                            ?>
                        </div>
                        <div class="cpa-metric-label">Total Sales</div>
                    </div>
                    <div class="cpa-metric-card">
                        <div class="cpa-metric-value" id="avg-roas">4.2x</div>
                        <div class="cpa-metric-label">Avg ROAS</div>
                    </div>
                </div>
                
                <div class="cpa-table-container">
                    <table class="cpa-dashboard-table">
                        <thead>
                            <tr>
                                <th>Campaign ID</th>
                                <th>Product</th>
                                <th>Status</th>
                                <th>Page Views</th>
                                <th>Sales</th>
                                <th>Views Change</th>
                                <th>Sales Change</th>
                                <th>Budget</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="dashboard-table-body">
                            <?php foreach ($dashboard_data as $campaign): ?>
                            <tr>
                                <td class="campaign-id"><?php echo esc_html($campaign->campaign_id ?? $campaign['campaign_id']); ?></td>
                                <td class="product-name">
                                    <strong><?php echo esc_html($campaign->product_name ?? $campaign['product_name']); ?></strong>
                                    <span class="product-id">ID: <?php echo esc_html($campaign->product_id ?? $campaign['product_id']); ?></span>
                                </td>
                                <td>
                                    <span class="status-badge <?php echo esc_attr($campaign->campaign_status ?? $campaign['campaign_status']); ?>">
                                        <?php echo ucfirst(esc_html($campaign->campaign_status ?? $campaign['campaign_status'])); ?>
                                    </span>
                                </td>
                                <td class="metric-value"><?php echo number_format($campaign->page_views ?? $campaign['page_views']); ?></td>
                                <td class="metric-value"><?php echo number_format($campaign->sales ?? $campaign['sales']); ?></td>
                                <td>
                                    <?php 
                                    $views_change = $campaign->views_increase ?? $campaign['views_increase'];
                                    $class = $views_change >= 0 ? 'positive' : 'negative';
                                    $icon = $views_change >= 0 ? '↗' : '↘';
                                    ?>
                                    <span class="change-value <?php echo $class; ?>">
                                        <?php echo $icon . abs($views_change) . '%'; ?>
                                    </span>
                                </td>
                                <td>
                                    <?php 
                                    $sales_change = $campaign->sales_increase ?? $campaign['sales_increase'];
                                    $class = $sales_change >= 0 ? 'positive' : 'negative';
                                    $icon = $sales_change >= 0 ? '↗' : '↘';
                                    ?>
                                    <span class="change-value <?php echo $class; ?>">
                                        <?php echo $icon . abs($sales_change) . '%'; ?>
                                    </span>
                                </td>
                                <td class="budget-value">$<?php echo number_format($campaign->budget ?? $campaign['budget'], 2); ?></td>
                                <td>
                                    <button class="button button-small view-details" data-campaign="<?php echo esc_attr($campaign->campaign_id ?? $campaign['campaign_id']); ?>">
                                        View Details
                                    </button>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                
                <?php if (empty($dashboard_data)): ?>
                <div class="cpa-empty-state">
                    <div class="cpa-empty-icon">📈</div>
                    <h3>No active campaigns yet</h3>
                    <p>Launch your first multi-agent flow to start seeing campaign data here.</p>
                </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</div>

<!-- Loading Overlay -->
<div id="cpa-loading-overlay" class="cpa-loading-overlay hidden">
    <div class="cpa-loading-content">
        <div class="cpa-spinner"></div>
        <p>AI Agents are analyzing your inventory and launching campaigns...</p>
    </div>
</div> 