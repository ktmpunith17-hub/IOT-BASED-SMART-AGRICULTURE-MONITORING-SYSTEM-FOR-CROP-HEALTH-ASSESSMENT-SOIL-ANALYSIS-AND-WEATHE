"""
Generate professional visualizations for the Smart Agriculture Monitoring System.
Creates 7 high-resolution charts suitable for inclusion in the internship report.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from datetime import datetime


def load_data():
    """Load simulation data from JSON file."""
    with open('/home/ubuntu/smart_agriculture_report/agricultural_readings.json', 'r') as f:
        data = json.load(f)
    return data


def create_chart_1_soil_conditions():
    """Create Chart 1: Soil Moisture, pH, and Nutrient Levels Trend."""
    data = load_data()
    readings = data['readings']
    
    # Extract data
    soil_moisture = [r['soil_moisture'] for r in readings]
    soil_ph = [r['soil_ph'] for r in readings]
    soil_nitrogen = [r['soil_nitrogen'] for r in readings]
    
    cycle_numbers = list(range(1, len(soil_moisture) + 1))
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle('Soil Conditions Monitoring - Moisture, pH, and Nitrogen Levels', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Soil Moisture
    axes[0].plot(cycle_numbers, soil_moisture, color='#1f77b4', linewidth=2, label='Soil Moisture')
    axes[0].axhline(y=60, color='green', linestyle='--', linewidth=1.5, label='Optimal Level (60%)')
    axes[0].axhline(y=40, color='orange', linestyle='--', linewidth=1.5, label='Warning Level (40%)')
    axes[0].fill_between(cycle_numbers, 40, 80, alpha=0.1, color='green', label='Optimal Range')
    axes[0].set_ylabel('Soil Moisture (%)', fontsize=11, fontweight='bold')
    axes[0].set_ylim(0, 105)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='best', fontsize=9)
    axes[0].set_title('Soil Moisture Level Trend', fontsize=12, fontweight='bold', pad=10)
    
    # Soil pH
    axes[1].plot(cycle_numbers, soil_ph, color='#ff7f0e', linewidth=2, label='Soil pH')
    axes[1].axhline(y=7.0, color='green', linestyle='--', linewidth=1.5, label='Optimal pH (7.0)')
    axes[1].fill_between(cycle_numbers, 6.0, 7.5, alpha=0.1, color='green', label='Optimal Range')
    axes[1].set_ylabel('Soil pH', fontsize=11, fontweight='bold')
    axes[1].set_ylim(4, 9)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='best', fontsize=9)
    axes[1].set_title('Soil pH Level Trend', fontsize=12, fontweight='bold', pad=10)
    
    # Soil Nitrogen
    axes[2].plot(cycle_numbers, soil_nitrogen, color='#2ca02c', linewidth=2, label='Nitrogen Level')
    axes[2].axhline(y=40, color='green', linestyle='--', linewidth=1.5, label='Optimal Level (40 mg/kg)')
    axes[2].fill_between(cycle_numbers, 30, 50, alpha=0.1, color='green', label='Optimal Range')
    axes[2].set_ylabel('Nitrogen (mg/kg)', fontsize=11, fontweight='bold')
    axes[2].set_xlabel('Monitoring Cycle', fontsize=11, fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend(loc='best', fontsize=9)
    axes[2].set_title('Soil Nitrogen Level Trend', fontsize=12, fontweight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/smart_agriculture_report/chart_01_soil_conditions.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 1: Soil Conditions - Created")


def create_chart_2_weather_analysis():
    """Create Chart 2: Temperature, Humidity, and Rainfall Analysis."""
    data = load_data()
    readings = data['readings']
    
    # Extract data
    temperature = [r['temperature'] for r in readings]
    humidity = [r['humidity'] for r in readings]
    rainfall = [r['rainfall'] for r in readings]
    
    cycle_numbers = list(range(1, len(temperature) + 1))
    
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    fig.suptitle('Weather Conditions Monitoring - Temperature, Humidity, and Rainfall', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Temperature Trend
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(cycle_numbers, temperature, color='#d62728', linewidth=2, label='Temperature')
    ax1.axhline(y=25, color='green', linestyle='--', linewidth=1.5, label='Optimal (25°C)')
    ax1.fill_between(cycle_numbers, 15, 30, alpha=0.1, color='green', label='Favorable Range')
    ax1.set_ylabel('Temperature (°C)', fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 40)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best', fontsize=9)
    ax1.set_title('Temperature Trend', fontsize=12, fontweight='bold', pad=10)
    
    # Humidity Trend
    ax2 = fig.add_subplot(gs[1, :])
    ax2.plot(cycle_numbers, humidity, color='#9467bd', linewidth=2, label='Humidity')
    ax2.axhline(y=60, color='green', linestyle='--', linewidth=1.5, label='Optimal (60%)')
    ax2.fill_between(cycle_numbers, 40, 80, alpha=0.1, color='green', label='Favorable Range')
    ax2.set_ylabel('Humidity (%)', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='best', fontsize=9)
    ax2.set_title('Humidity Trend', fontsize=12, fontweight='bold', pad=10)
    
    # Rainfall Distribution
    ax3 = fig.add_subplot(gs[2, :])
    rainy_days = [r for r in rainfall if r > 0]
    ax3.bar(range(len(rainfall)), rainfall, color=['#1f77b4' if r > 0 else '#d3d3d3' for r in rainfall], 
            width=1.0, edgecolor='none', alpha=0.7)
    ax3.set_ylabel('Rainfall (mm)', fontsize=11, fontweight='bold')
    ax3.set_xlabel('Monitoring Cycle', fontsize=11, fontweight='bold')
    ax3.set_title(f'Rainfall Distribution ({len(rainy_days)} rainy days out of {len(rainfall)})', 
                  fontsize=12, fontweight='bold', pad=10)
    ax3.grid(True, alpha=0.3, axis='y')
    
    plt.savefig('/home/ubuntu/smart_agriculture_report/chart_02_weather_analysis.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 2: Weather Analysis - Created")


def create_chart_3_crop_health():
    """Create Chart 3: Crop Health NDVI and Status Distribution."""
    data = load_data()
    readings = data['readings']
    stats = data['statistics']
    
    # Extract data
    ndvi = [r['crop_ndvi'] for r in readings]
    crop_health_status = [r['crop_health_status'] for r in readings]
    
    cycle_numbers = list(range(1, len(ndvi) + 1))
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle('Crop Health Assessment - NDVI and Health Status Distribution', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # NDVI Trend
    axes[0].plot(cycle_numbers, ndvi, color='#2ca02c', linewidth=2, label='NDVI')
    axes[0].axhline(y=0.7, color='green', linestyle='--', linewidth=1.5, label='Excellent Threshold (0.7)')
    axes[0].axhline(y=0.5, color='orange', linestyle='--', linewidth=1.5, label='Good Threshold (0.5)')
    axes[0].fill_between(cycle_numbers, 0.7, 1.0, alpha=0.1, color='green', label='Excellent Range')
    axes[0].fill_between(cycle_numbers, 0.5, 0.7, alpha=0.1, color='yellow')
    axes[0].set_ylabel('NDVI (Normalized Difference Vegetation Index)', fontsize=11, fontweight='bold')
    axes[0].set_ylim(0, 1.0)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='best', fontsize=9)
    axes[0].set_title('Crop NDVI Trend', fontsize=12, fontweight='bold', pad=10)
    
    # Health Status Distribution
    dist = stats['crop_health_distribution']
    statuses = ['Excellent', 'Good', 'Fair', 'Poor', 'Critical']
    counts = [dist['excellent'], dist['good'], dist['fair'], dist['poor'], dist['critical']]
    colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728', '#8b0000']
    
    bars = axes[1].bar(statuses, counts, color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)
    axes[1].set_ylabel('Number of Readings', fontsize=11, fontweight='bold')
    axes[1].set_xlabel('Crop Health Status', fontsize=11, fontweight='bold')
    axes[1].set_title('Crop Health Status Distribution', fontsize=12, fontweight='bold', pad=10)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            axes[1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}\n({height/sum(counts)*100:.1f}%)',
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/smart_agriculture_report/chart_03_crop_health.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 3: Crop Health - Created")


def create_chart_4_nutrient_analysis():
    """Create Chart 4: Soil Nutrient Levels (N, P, K) Analysis."""
    data = load_data()
    readings = data['readings']
    stats = data['statistics']
    
    # Extract data
    nitrogen = [r['soil_nitrogen'] for r in readings]
    phosphorus = [r['soil_phosphorus'] for r in readings]
    potassium = [r['soil_potassium'] for r in readings]
    
    cycle_numbers = list(range(1, len(nitrogen) + 1))
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle('Soil Nutrient Analysis - Nitrogen, Phosphorus, and Potassium Levels', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Nitrogen
    axes[0].plot(cycle_numbers, nitrogen, color='#1f77b4', linewidth=2, label='Nitrogen')
    axes[0].axhline(y=40, color='green', linestyle='--', linewidth=1.5, label='Optimal (40 mg/kg)')
    axes[0].fill_between(cycle_numbers, 30, 50, alpha=0.1, color='green', label='Optimal Range')
    axes[0].set_ylabel('Nitrogen (mg/kg)', fontsize=11, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='best', fontsize=9)
    axes[0].set_title('Nitrogen Level Trend', fontsize=12, fontweight='bold', pad=10)
    
    # Phosphorus
    axes[1].plot(cycle_numbers, phosphorus, color='#ff7f0e', linewidth=2, label='Phosphorus')
    axes[1].axhline(y=22.5, color='green', linestyle='--', linewidth=1.5, label='Optimal (22.5 mg/kg)')
    axes[1].fill_between(cycle_numbers, 15, 30, alpha=0.1, color='green', label='Optimal Range')
    axes[1].set_ylabel('Phosphorus (mg/kg)', fontsize=11, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='best', fontsize=9)
    axes[1].set_title('Phosphorus Level Trend', fontsize=12, fontweight='bold', pad=10)
    
    # Potassium
    axes[2].plot(cycle_numbers, potassium, color='#2ca02c', linewidth=2, label='Potassium')
    axes[2].axhline(y=200, color='green', linestyle='--', linewidth=1.5, label='Optimal (200 mg/kg)')
    axes[2].fill_between(cycle_numbers, 150, 250, alpha=0.1, color='green', label='Optimal Range')
    axes[2].set_ylabel('Potassium (mg/kg)', fontsize=11, fontweight='bold')
    axes[2].set_xlabel('Monitoring Cycle', fontsize=11, fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend(loc='best', fontsize=9)
    axes[2].set_title('Potassium Level Trend', fontsize=12, fontweight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/smart_agriculture_report/chart_04_nutrient_analysis.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 4: Nutrient Analysis - Created")


def create_chart_5_irrigation_recommendations():
    """Create Chart 5: Irrigation Recommendations and Soil Moisture."""
    data = load_data()
    readings = data['readings']
    stats = data['statistics']
    
    # Extract data
    soil_moisture = [r['soil_moisture'] for r in readings]
    irrigation_needed = [r['irrigation_needed'] for r in readings]
    
    cycle_numbers = list(range(1, len(soil_moisture) + 1))
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle('Irrigation Management - Soil Moisture and Irrigation Recommendations', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Soil Moisture with Irrigation Events
    axes[0].plot(cycle_numbers, soil_moisture, color='#1f77b4', linewidth=2, label='Soil Moisture')
    
    # Mark irrigation events
    irrigation_cycles = [i for i, needed in enumerate(irrigation_needed, 1) if needed]
    if irrigation_cycles:
        irrigation_moisture = [soil_moisture[i-1] for i in irrigation_cycles]
        axes[0].scatter(irrigation_cycles, irrigation_moisture, color='red', s=100, 
                       marker='v', label='Irrigation Event', zorder=5)
    
    axes[0].axhline(y=60, color='green', linestyle='--', linewidth=1.5, label='Optimal (60%)')
    axes[0].axhline(y=40, color='orange', linestyle='--', linewidth=1.5, label='Warning (40%)')
    axes[0].fill_between(cycle_numbers, 40, 80, alpha=0.1, color='green', label='Favorable Range')
    axes[0].set_ylabel('Soil Moisture (%)', fontsize=11, fontweight='bold')
    axes[0].set_ylim(0, 105)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='best', fontsize=9)
    axes[0].set_title('Soil Moisture with Irrigation Events', fontsize=12, fontweight='bold', pad=10)
    
    # Irrigation Statistics
    irrigation_count = stats['irrigation_events']
    irrigation_percentage = stats['irrigation_percentage']
    
    categories = ['Irrigation\nNeeded', 'No Irrigation\nNeeded']
    values = [irrigation_count, len(readings) - irrigation_count]
    colors_pie = ['#d62728', '#2ca02c']
    
    wedges, texts, autotexts = axes[1].pie(values, labels=categories, autopct='%1.1f%%',
                                             colors=colors_pie, startangle=90, textprops={'fontsize': 11})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    axes[1].set_title(f'Irrigation Requirement Distribution ({irrigation_count} events)', 
                     fontsize=12, fontweight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/smart_agriculture_report/chart_05_irrigation_recommendations.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 5: Irrigation Recommendations - Created")


def create_chart_6_performance_metrics():
    """Create Chart 6: System Performance Metrics Dashboard."""
    data = load_data()
    stats = data['statistics']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('System Performance Metrics Dashboard', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Crop Health Distribution
    dist = stats['crop_health_distribution']
    statuses = ['Excellent', 'Good', 'Fair', 'Poor', 'Critical']
    counts = [dist['excellent'], dist['good'], dist['fair'], dist['poor'], dist['critical']]
    colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728', '#8b0000']
    
    axes[0, 0].bar(statuses, counts, color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)
    axes[0, 0].set_ylabel('Count', fontsize=10, fontweight='bold')
    axes[0, 0].set_title('Crop Health Distribution', fontsize=11, fontweight='bold', pad=10)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Environmental Conditions
    temp_avg = stats['temperature']['avg']
    humidity_avg = stats['humidity']['avg']
    wind_avg = stats['wind_speed']['avg']
    
    env_categories = ['Temperature\n(°C)', 'Humidity\n(%)', 'Wind Speed\n(km/h)']
    env_values = [temp_avg, humidity_avg, wind_avg]
    env_colors = ['#d62728', '#9467bd', '#8c564b']
    
    axes[0, 1].bar(env_categories, env_values, color=env_colors, edgecolor='black', linewidth=1.5, alpha=0.8)
    axes[0, 1].set_ylabel('Value', fontsize=10, fontweight='bold')
    axes[0, 1].set_title('Average Environmental Conditions', fontsize=11, fontweight='bold', pad=10)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Soil Nutrient Levels
    soil_categories = ['Nitrogen\n(mg/kg)', 'Phosphorus\n(mg/kg)', 'Potassium\n(mg/kg)']
    soil_values = [stats['soil_nitrogen']['avg'], stats['soil_phosphorus']['avg'], stats['soil_potassium']['avg']]
    soil_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    axes[1, 0].bar(soil_categories, soil_values, color=soil_colors, edgecolor='black', linewidth=1.5, alpha=0.8)
    axes[1, 0].set_ylabel('Concentration (mg/kg)', fontsize=10, fontweight='bold')
    axes[1, 0].set_title('Average Soil Nutrient Levels', fontsize=11, fontweight='bold', pad=10)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Key Statistics
    axes[1, 1].axis('off')
    
    stats_text = f"""
    SYSTEM STATISTICS
    
    Total Monitoring Cycles: {stats['total_cycles']}
    Total Readings: {stats['total_readings']}
    Field ID: {stats['field_id']}
    
    SOIL QUALITY
    • Avg Moisture: {stats['soil_moisture']['avg']}%
    • Avg pH: {stats['soil_ph']['avg']}
    • Avg Nitrogen: {stats['soil_nitrogen']['avg']} mg/kg
    
    WEATHER
    • Avg Temperature: {stats['temperature']['avg']}°C
    • Avg Humidity: {stats['humidity']['avg']}%
    • Total Rainfall: {stats['rainfall']['total']} mm
    
    CROP HEALTH
    • Avg NDVI: {stats['crop_ndvi']['avg']}
    • Irrigation Events: {stats['irrigation_events']}
    • Irrigation %: {stats['irrigation_percentage']}%
    """
    
    axes[1, 1].text(0.1, 0.95, stats_text, transform=axes[1, 1].transAxes,
                   fontsize=10, verticalalignment='top', fontfamily='monospace',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/smart_agriculture_report/chart_06_performance_metrics.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 6: Performance Metrics - Created")


def create_chart_7_comprehensive_dashboard():
    """Create Chart 7: Comprehensive Agricultural Monitoring Dashboard."""
    data = load_data()
    readings = data['readings']
    stats = data['statistics']
    
    # Extract key data
    soil_moisture = [r['soil_moisture'] for r in readings]
    temperature = [r['temperature'] for r in readings]
    humidity = [r['humidity'] for r in readings]
    ndvi = [r['crop_ndvi'] for r in readings]
    
    cycle_numbers = list(range(1, len(soil_moisture) + 1))
    
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    fig.suptitle('Comprehensive Smart Agriculture Monitoring Dashboard', 
                 fontsize=18, fontweight='bold', y=0.995)
    
    # 1. Soil Moisture Trend
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(cycle_numbers, soil_moisture, color='#1f77b4', linewidth=1.5)
    ax1.fill_between(cycle_numbers, soil_moisture, alpha=0.3, color='#1f77b4')
    ax1.set_title('Soil Moisture', fontsize=10, fontweight='bold')
    ax1.set_ylabel('(%)', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 105)
    
    # 2. Temperature Trend
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(cycle_numbers, temperature, color='#d62728', linewidth=1.5)
    ax2.fill_between(cycle_numbers, temperature, alpha=0.3, color='#d62728')
    ax2.set_title('Temperature', fontsize=10, fontweight='bold')
    ax2.set_ylabel('(°C)', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # 3. Humidity Trend
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(cycle_numbers, humidity, color='#9467bd', linewidth=1.5)
    ax3.fill_between(cycle_numbers, humidity, alpha=0.3, color='#9467bd')
    ax3.set_title('Humidity', fontsize=10, fontweight='bold')
    ax3.set_ylabel('(%)', fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 100)
    
    # 4. NDVI Trend
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.plot(cycle_numbers, ndvi, color='#2ca02c', linewidth=1.5)
    ax4.fill_between(cycle_numbers, ndvi, alpha=0.3, color='#2ca02c')
    ax4.set_title('Crop NDVI', fontsize=10, fontweight='bold')
    ax4.set_ylabel('(Index)', fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 1.0)
    
    # 5. Crop Health Distribution
    ax5 = fig.add_subplot(gs[1, 1])
    dist = stats['crop_health_distribution']
    statuses = ['Excellent', 'Good', 'Fair', 'Poor', 'Critical']
    counts = [dist['excellent'], dist['good'], dist['fair'], dist['poor'], dist['critical']]
    colors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728', '#8b0000']
    ax5.barh(statuses, counts, color=colors, edgecolor='black', linewidth=1)
    ax5.set_title('Crop Health Status', fontsize=10, fontweight='bold')
    ax5.set_xlabel('Count', fontsize=9)
    ax5.grid(True, alpha=0.3, axis='x')
    
    # 6. Soil Quality Metrics
    ax6 = fig.add_subplot(gs[1, 2])
    soil_metrics = ['pH', 'Nitrogen', 'Phosphorus', 'Potassium']
    soil_values = [stats['soil_ph']['avg'], 
                   stats['soil_nitrogen']['avg']/10,  # Scale for visualization
                   stats['soil_phosphorus']['avg'],
                   stats['soil_potassium']['avg']/10]  # Scale for visualization
    ax6.bar(soil_metrics, soil_values, color=['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728'], 
            edgecolor='black', linewidth=1, alpha=0.8)
    ax6.set_title('Soil Quality Avg', fontsize=10, fontweight='bold')
    ax6.set_ylabel('Value', fontsize=9)
    ax6.grid(True, alpha=0.3, axis='y')
    ax6.tick_params(axis='x', rotation=45)
    
    # 7. Statistics Summary
    ax7 = fig.add_subplot(gs[2, :])
    ax7.axis('off')
    
    summary_text = f"""
    COMPREHENSIVE MONITORING SUMMARY

    SOIL CONDITIONS                          WEATHER CONDITIONS                    CROP HEALTH
    • Moisture: {stats['soil_moisture']['avg']}% (Range: {stats['soil_moisture']['min']}-{stats['soil_moisture']['max']}%)    • Temperature: {stats['temperature']['avg']}°C (Range: {stats['temperature']['min']}-{stats['temperature']['max']}°C)    • NDVI: {stats['crop_ndvi']['avg']} (Range: {stats['crop_ndvi']['min']}-{stats['crop_ndvi']['max']})
    • pH: {stats['soil_ph']['avg']} (Range: {stats['soil_ph']['min']}-{stats['soil_ph']['max']})           • Humidity: {stats['humidity']['avg']}% (Range: {stats['humidity']['min']}-{stats['humidity']['max']}%)       • Excellent: {dist['excellent']} | Good: {dist['good']} | Fair: {dist['fair']} | Poor: {dist['poor']} | Critical: {dist['critical']}
    • Nitrogen: {stats['soil_nitrogen']['avg']} mg/kg                • Rainfall: {stats['rainfall']['total']} mm ({stats['rainfall']['rainy_days']} rainy days)      • Irrigation Events: {stats['irrigation_events']} ({stats['irrigation_percentage']}%)
    • Phosphorus: {stats['soil_phosphorus']['avg']} mg/kg            • Wind Speed: {stats['wind_speed']['avg']} km/h (Range: {stats['wind_speed']['min']}-{stats['wind_speed']['max']})
    • Potassium: {stats['soil_potassium']['avg']} mg/kg

    MONITORING PERIOD: {stats['total_cycles']} continuous cycles | FIELD ID: {stats['field_id']} | TOTAL READINGS: {stats['total_readings']}
    """
    
    ax7.text(0.05, 0.95, summary_text, transform=ax7.transAxes,
            fontsize=9.5, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3, pad=1))
    
    plt.savefig('/home/ubuntu/smart_agriculture_report/chart_07_comprehensive_dashboard.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Chart 7: Comprehensive Dashboard - Created")


def main():
    """Generate all visualizations."""
    print("=" * 80)
    print("GENERATING PROFESSIONAL VISUALIZATIONS")
    print("Smart Agriculture Monitoring System")
    print("=" * 80)
    print()
    
    try:
        create_chart_1_soil_conditions()
        create_chart_2_weather_analysis()
        create_chart_3_crop_health()
        create_chart_4_nutrient_analysis()
        create_chart_5_irrigation_recommendations()
        create_chart_6_performance_metrics()
        create_chart_7_comprehensive_dashboard()
        
        print()
        print("=" * 80)
        print("✓ ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
        print("=" * 80)
        print()
        print("Generated files:")
        print("  1. chart_01_soil_conditions.png")
        print("  2. chart_02_weather_analysis.png")
        print("  3. chart_03_crop_health.png")
        print("  4. chart_04_nutrient_analysis.png")
        print("  5. chart_05_irrigation_recommendations.png")
        print("  6. chart_06_performance_metrics.png")
        print("  7. chart_07_comprehensive_dashboard.png")
        print()
        
    except Exception as e:
        print(f"Error generating visualizations: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
