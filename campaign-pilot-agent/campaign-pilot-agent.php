<?php
/**
 * Plugin Name: Campaign Pilot Agent
 * Plugin URI: https://example.com/campaign-pilot-agent
 * Description: Multi-agent flow dashboard for WooCommerce inventory monitoring and campaign management
 * Version: 1.0.0
 * Author: Campaign Pilot Team
 * License: GPL v2 or later
 * Text Domain: campaign-pilot-agent
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('CPA_PLUGIN_URL', plugin_dir_url(__FILE__));
define('CPA_PLUGIN_PATH', plugin_dir_path(__FILE__));
define('CPA_VERSION', '1.0.0');

class CampaignPilotAgent {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_scripts'));
        add_action('wp_ajax_cpa_run_agent', array($this, 'ajax_run_agent'));
        add_action('wp_ajax_cpa_refresh_dashboard', array($this, 'ajax_refresh_dashboard'));
        register_activation_hook(__FILE__, array($this, 'activate'));
    }
    
    public function init() {
        // Initialize plugin
    }
    
    public function activate() {
        // Create database tables if needed
        $this->create_tables();
    }
    
    private function create_tables() {
        global $wpdb;
        
        $table_name = $wpdb->prefix . 'cpa_campaigns';
        
        $charset_collate = $wpdb->get_charset_collate();
        
        $sql = "CREATE TABLE $table_name (
            id mediumint(9) NOT NULL AUTO_INCREMENT,
            campaign_id varchar(50) NOT NULL,
            product_id mediumint(9) NOT NULL,
            product_name varchar(255) NOT NULL,
            campaign_status varchar(20) DEFAULT 'active',
            page_views int(11) DEFAULT 0,
            sales int(11) DEFAULT 0,
            sales_increase decimal(5,2) DEFAULT 0.00,
            views_increase decimal(5,2) DEFAULT 0.00,
            budget decimal(10,2) DEFAULT 0.00,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        ) $charset_collate;";
        
        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql);
    }
    
    public function add_admin_menu() {
        add_menu_page(
            'Campaign Pilot Agent',
            'Campaign Pilot',
            'manage_options',
            'campaign-pilot-agent',
            array($this, 'admin_page'),
            'dashicons-chart-line',
            30
        );
    }
    
    public function enqueue_admin_scripts($hook) {
        if ($hook !== 'toplevel_page_campaign-pilot-agent') {
            return;
        }
        
        wp_enqueue_script(
            'cpa-admin-js',
            CPA_PLUGIN_URL . 'assets/admin.js',
            array('jquery'),
            CPA_VERSION,
            true
        );
        
        wp_enqueue_style(
            'cpa-admin-css',
            CPA_PLUGIN_URL . 'assets/admin.css',
            array(),
            CPA_VERSION
        );
        
        wp_localize_script('cpa-admin-js', 'cpa_ajax', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('cpa_nonce'),
        ));
    }
    
    public function admin_page() {
        include CPA_PLUGIN_PATH . 'templates/admin-page.php';
    }
    
    public function ajax_run_agent() {
        check_ajax_referer('cpa_nonce', 'nonce');
        
        $campaign_length = sanitize_text_field($_POST['campaign_length']);
        $campaign_budget = sanitize_text_field($_POST['campaign_budget']);
        $campaign_copy = sanitize_textarea_field($_POST['campaign_copy']);
        
        // Simulate API call to external multi-agent system
        $response = $this->simulate_agent_api_call($campaign_length, $campaign_budget, $campaign_copy);
        
        wp_send_json_success($response);
    }
    
    public function ajax_refresh_dashboard() {
        check_ajax_referer('cpa_nonce', 'nonce');
        
        $dashboard_data = $this->generate_mock_dashboard_data();
        
        wp_send_json_success($dashboard_data);
    }
    
    private function simulate_agent_api_call($length, $budget, $copy) {
        // Simulate external API call
        sleep(1); // Simulate network delay
        
        return array(
            'status' => 'success',
            'message' => 'Multi-agent flow initiated successfully',
            'agent_id' => 'agent_' . uniqid(),
            'campaigns_launched' => rand(3, 8)
        );
    }
    
    private function generate_mock_dashboard_data() {
        global $wpdb;
        
        // Clear existing mock data
        $table_name = $wpdb->prefix . 'cpa_campaigns';
        $wpdb->query("TRUNCATE TABLE $table_name");
        
        // Generate fresh mock data
        $products = array(
            array('name' => 'Wireless Bluetooth Headphones', 'base_views' => 2341, 'base_sales' => 23),
            array('name' => 'Organic Cotton T-Shirt', 'base_views' => 5672, 'base_sales' => 89),
            array('name' => 'Smart Water Bottle', 'base_views' => 8934, 'base_sales' => 234),
            array('name' => 'Premium Coffee Beans', 'base_views' => 1876, 'base_sales' => 34),
            array('name' => 'Yoga Mat Premium', 'base_views' => 3456, 'base_sales' => 67),
        );
        
        $campaigns = array();
        
        foreach ($products as $index => $product) {
            $campaign_id = 'camp_' . uniqid();
            $product_id = 100 + $index;
            $views_increase = rand(-20, 45);
            $sales_increase = rand(-15, 30);
            $new_views = $product['base_views'] + round($product['base_views'] * ($views_increase / 100));
            $new_sales = $product['base_sales'] + round($product['base_sales'] * ($sales_increase / 100));
            
            $wpdb->insert(
                $table_name,
                array(
                    'campaign_id' => $campaign_id,
                    'product_id' => $product_id,
                    'product_name' => $product['name'],
                    'campaign_status' => rand(0, 1) ? 'active' : 'paused',
                    'page_views' => $new_views,
                    'sales' => $new_sales,
                    'sales_increase' => $sales_increase,
                    'views_increase' => $views_increase,
                    'budget' => rand(15, 50)
                )
            );
            
            $campaigns[] = array(
                'campaign_id' => $campaign_id,
                'product_id' => $product_id,
                'product_name' => $product['name'],
                'campaign_status' => $wpdb->insert_id ? 'active' : 'paused',
                'page_views' => $new_views,
                'sales' => $new_sales,
                'sales_increase' => $sales_increase,
                'views_increase' => $views_increase,
                'budget' => rand(15, 50)
            );
        }
        
        return $campaigns;
    }
    
    public function get_dashboard_data() {
        global $wpdb;
        
        $table_name = $wpdb->prefix . 'cpa_campaigns';
        $results = $wpdb->get_results("SELECT * FROM $table_name ORDER BY created_at DESC");
        
        if (empty($results)) {
            return $this->generate_mock_dashboard_data();
        }
        
        return $results;
    }
}

// Initialize the plugin
new CampaignPilotAgent(); 