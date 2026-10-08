"""
Smart Agriculture Monitoring System
IoT-based crop health assessment, soil analysis, and weather tracking

This module simulates a comprehensive smart agriculture monitoring system that tracks
soil conditions, crop health, and weather parameters for precision farming.
"""

import random
import datetime
import json
import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import statistics
from enum import Enum


class CropHealthStatus(Enum):
    """Crop health status classification."""
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    CRITICAL = "CRITICAL"


class SoilQuality(Enum):
    """Soil quality classification."""
    OPTIMAL = "OPTIMAL"
    GOOD = "GOOD"
    ACCEPTABLE = "ACCEPTABLE"
    POOR = "POOR"


class WeatherCondition(Enum):
    """Weather condition classification."""
    FAVORABLE = "FAVORABLE"
    MODERATE = "MODERATE"
    UNFAVORABLE = "UNFAVORABLE"
    SEVERE = "SEVERE"


@dataclass
class AgriculturalReading:
    """Represents a single agricultural monitoring reading."""
    timestamp: str
    field_id: str
    soil_moisture: float              # Percentage (0-100%)
    soil_ph: float                    # pH value (0-14)
    soil_nitrogen: float              # mg/kg
    soil_phosphorus: float            # mg/kg
    soil_potassium: float             # mg/kg
    temperature: float                # Celsius
    humidity: float                   # Percentage
    rainfall: float                   # mm
    wind_speed: float                 # km/h
    crop_ndvi: float                  # Normalized Difference Vegetation Index (0-1)
    crop_health_status: str           # EXCELLENT, GOOD, FAIR, POOR, CRITICAL
    soil_quality_status: str          # OPTIMAL, GOOD, ACCEPTABLE, POOR
    weather_condition: str            # FAVORABLE, MODERATE, UNFAVORABLE, SEVERE
    irrigation_needed: bool
    fertilizer_recommendation: str
    alert_message: str


class SoilMoistureSensor:
    """Simulates a soil moisture sensor."""
    
    def __init__(self, baseline_moisture: float = 60.0):
        """
        Initialize the soil moisture sensor.
        
        Args:
            baseline_moisture: Baseline soil moisture percentage
        """
        self.baseline_moisture = baseline_moisture
        self.last_reading = None
    
    def read_moisture(self, rainfall: float = 0.0) -> float:
        """
        Read soil moisture level.
        
        Args:
            rainfall: Recent rainfall amount in mm
            
        Returns:
            Soil moisture percentage (0-100%)
        """
        if self.last_reading is None:
            reading = self.baseline_moisture + random.uniform(-10, 10)
        else:
            # Moisture decreases over time (evapotranspiration) but increases with rainfall
            reading = self.last_reading * 0.95 + self.baseline_moisture * 0.05
            reading += (rainfall * 2)  # Rainfall increases moisture
            reading += random.uniform(-3, 3)
        
        reading = max(10, min(100, reading))
        self.last_reading = reading
        return round(reading, 1)


class SoilPHSensor:
    """Simulates a soil pH sensor."""
    
    def __init__(self, baseline_ph: float = 7.0):
        """
        Initialize the soil pH sensor.
        
        Args:
            baseline_ph: Baseline soil pH
        """
        self.baseline_ph = baseline_ph
        self.last_reading = None
    
    def read_ph(self) -> float:
        """
        Read soil pH level.
        
        Returns:
            pH value (0-14)
        """
        if self.last_reading is None:
            reading = self.baseline_ph + random.uniform(-0.5, 0.5)
        else:
            reading = self.last_reading * 0.9 + self.baseline_ph * 0.1
            reading += random.uniform(-0.2, 0.2)
        
        reading = max(4.0, min(9.0, reading))
        self.last_reading = reading
        return round(reading, 1)


class SoilNutrientSensor:
    """Simulates soil nutrient sensors (N, P, K)."""
    
    def __init__(self, baseline_n: float = 40.0, baseline_p: float = 25.0, baseline_k: float = 200.0):
        """
        Initialize the soil nutrient sensor.
        
        Args:
            baseline_n: Baseline nitrogen level (mg/kg)
            baseline_p: Baseline phosphorus level (mg/kg)
            baseline_k: Baseline potassium level (mg/kg)
        """
        self.baseline_n = baseline_n
        self.baseline_p = baseline_p
        self.baseline_k = baseline_k
        self.last_n = None
        self.last_p = None
        self.last_k = None
    
    def read_nutrients(self) -> Tuple[float, float, float]:
        """
        Read soil nutrient levels.
        
        Returns:
            Tuple of (nitrogen, phosphorus, potassium) in mg/kg
        """
        # Nitrogen (decreases with crop uptake)
        if self.last_n is None:
            n = self.baseline_n + random.uniform(-5, 5)
        else:
            n = self.last_n * 0.98 + self.baseline_n * 0.02 + random.uniform(-2, 2)
        n = max(10, min(100, n))
        self.last_n = n
        
        # Phosphorus (relatively stable)
        if self.last_p is None:
            p = self.baseline_p + random.uniform(-3, 3)
        else:
            p = self.last_p * 0.95 + self.baseline_p * 0.05 + random.uniform(-1, 1)
        p = max(5, min(50, p))
        self.last_p = p
        
        # Potassium (decreases with crop uptake)
        if self.last_k is None:
            k = self.baseline_k + random.uniform(-20, 20)
        else:
            k = self.last_k * 0.97 + self.baseline_k * 0.03 + random.uniform(-10, 10)
        k = max(100, min(400, k))
        self.last_k = k
        
        return round(n, 1), round(p, 1), round(k, 1)


class TemperatureSensor:
    """Simulates a temperature sensor."""
    
    def __init__(self, baseline_temp: float = 25.0):
        """
        Initialize the temperature sensor.
        
        Args:
            baseline_temp: Baseline temperature in Celsius
        """
        self.baseline_temp = baseline_temp
        self.last_reading = None
    
    def read_temperature(self) -> float:
        """
        Read temperature with daily variations.
        
        Returns:
            Temperature in Celsius
        """
        if self.last_reading is None:
            reading = self.baseline_temp + random.uniform(-5, 5)
        else:
            reading = self.last_reading * 0.8 + self.baseline_temp * 0.2
            reading += random.uniform(-2, 2)
        
        reading = max(5, min(45, reading))
        self.last_reading = reading
        return round(reading, 1)


class HumiditySensor:
    """Simulates a humidity sensor."""
    
    def __init__(self, baseline_humidity: float = 60.0):
        """
        Initialize the humidity sensor.
        
        Args:
            baseline_humidity: Baseline humidity percentage
        """
        self.baseline_humidity = baseline_humidity
        self.last_reading = None
    
    def read_humidity(self) -> float:
        """
        Read humidity level.
        
        Returns:
            Humidity percentage (0-100%)
        """
        if self.last_reading is None:
            reading = self.baseline_humidity + random.uniform(-10, 10)
        else:
            reading = self.last_reading * 0.85 + self.baseline_humidity * 0.15
            reading += random.uniform(-5, 5)
        
        reading = max(20, min(95, reading))
        self.last_reading = reading
        return round(reading, 1)


class RainfallSensor:
    """Simulates a rainfall sensor."""
    
    def read_rainfall(self) -> float:
        """
        Read rainfall amount.
        
        Returns:
            Rainfall in mm
        """
        # 70% chance of no rain, 30% chance of rain
        if random.random() < 0.7:
            return 0.0
        else:
            # Rain amount between 2-50mm
            return round(random.uniform(2, 50), 1)


class WindSpeedSensor:
    """Simulates a wind speed sensor."""
    
    def __init__(self, baseline_wind: float = 10.0):
        """
        Initialize the wind speed sensor.
        
        Args:
            baseline_wind: Baseline wind speed in km/h
        """
        self.baseline_wind = baseline_wind
        self.last_reading = None
    
    def read_wind_speed(self) -> float:
        """
        Read wind speed.
        
        Returns:
            Wind speed in km/h
        """
        if self.last_reading is None:
            reading = self.baseline_wind + random.uniform(-5, 5)
        else:
            reading = self.last_reading * 0.8 + self.baseline_wind * 0.2
            reading += random.uniform(-3, 3)
        
        reading = max(0, min(50, reading))
        self.last_reading = reading
        return round(reading, 1)


class CropHealthAnalyzer:
    """Analyzes crop health based on environmental and soil conditions."""
    
    def __init__(self):
        self.alert_history = []
    
    def calculate_ndvi(self, temperature: float, humidity: float, soil_moisture: float) -> float:
        """
        Calculate Normalized Difference Vegetation Index (NDVI).
        
        Returns:
            NDVI value (0-1)
        """
        # Simplified NDVI calculation based on environmental factors
        # Optimal conditions: temp 20-30°C, humidity 60-80%, moisture 50-70%
        temp_factor = 1.0 - abs(temperature - 25) / 30
        humidity_factor = 1.0 - abs(humidity - 70) / 70
        moisture_factor = 1.0 - abs(soil_moisture - 60) / 60
        
        ndvi = (temp_factor * 0.3 + humidity_factor * 0.3 + moisture_factor * 0.4) * 0.9
        return max(0.0, min(1.0, round(ndvi, 2)))
    
    def analyze_crop_health(self, ndvi: float, soil_moisture: float, temperature: float) -> Tuple[CropHealthStatus, str]:
        """
        Analyze crop health status.
        
        Returns:
            Tuple of (CropHealthStatus, alert_message)
        """
        alerts = []
        
        if ndvi < 0.3:
            alerts.append("CRITICAL: Very low vegetation index")
            status = CropHealthStatus.CRITICAL
        elif ndvi < 0.4:
            alerts.append("POOR: Low vegetation index")
            status = CropHealthStatus.POOR
        elif ndvi < 0.5:
            alerts.append("FAIR: Moderate vegetation index")
            status = CropHealthStatus.FAIR
        elif ndvi < 0.7:
            alerts.append("GOOD: Good vegetation index")
            status = CropHealthStatus.GOOD
        else:
            alerts.append("EXCELLENT: Excellent vegetation index")
            status = CropHealthStatus.EXCELLENT
        
        # Check soil moisture
        if soil_moisture < 20:
            alerts.append("CRITICAL: Severe drought stress")
            if status.value not in ["CRITICAL", "POOR"]:
                status = CropHealthStatus.POOR
        elif soil_moisture < 40:
            alerts.append("WARNING: Moderate drought stress")
        
        # Check temperature stress
        if temperature < 10 or temperature > 35:
            alerts.append("WARNING: Temperature stress detected")
        
        message = " | ".join(alerts)
        
        if status != CropHealthStatus.EXCELLENT:
            self.alert_history.append({
                'timestamp': datetime.datetime.now().isoformat(),
                'status': status.value,
                'message': message,
                'ndvi': ndvi,
                'soil_moisture': soil_moisture,
                'temperature': temperature
            })
        
        return status, message


class SoilAnalyzer:
    """Analyzes soil conditions."""
    
    def analyze_soil_quality(self, ph: float, nitrogen: float, phosphorus: float, potassium: float) -> Tuple[SoilQuality, str]:
        """
        Analyze soil quality.
        
        Returns:
            Tuple of (SoilQuality, recommendation)
        """
        quality_score = 0
        recommendations = []
        
        # pH analysis (optimal 6.0-7.5)
        if 6.0 <= ph <= 7.5:
            quality_score += 25
        elif 5.5 <= ph <= 8.0:
            quality_score += 15
            recommendations.append("pH slightly outside optimal range")
        else:
            recommendations.append("pH requires adjustment")
        
        # Nitrogen analysis (optimal 30-50 mg/kg)
        if 30 <= nitrogen <= 50:
            quality_score += 25
        elif 20 <= nitrogen <= 60:
            quality_score += 15
            recommendations.append("Nitrogen levels slightly low")
        else:
            recommendations.append("Nitrogen fertilizer recommended")
        
        # Phosphorus analysis (optimal 15-30 mg/kg)
        if 15 <= phosphorus <= 30:
            quality_score += 25
        elif 10 <= phosphorus <= 40:
            quality_score += 15
            recommendations.append("Phosphorus levels acceptable")
        else:
            recommendations.append("Phosphorus fertilizer needed")
        
        # Potassium analysis (optimal 150-250 mg/kg)
        if 150 <= potassium <= 250:
            quality_score += 25
        elif 100 <= potassium <= 300:
            quality_score += 15
            recommendations.append("Potassium levels acceptable")
        else:
            recommendations.append("Potassium fertilizer recommended")
        
        # Determine soil quality
        if quality_score >= 90:
            quality = SoilQuality.OPTIMAL
        elif quality_score >= 70:
            quality = SoilQuality.GOOD
        elif quality_score >= 50:
            quality = SoilQuality.ACCEPTABLE
        else:
            quality = SoilQuality.POOR
        
        recommendation = " | ".join(recommendations) if recommendations else "Soil conditions are optimal"
        return quality, recommendation


class WeatherAnalyzer:
    """Analyzes weather conditions."""
    
    def analyze_weather(self, temperature: float, humidity: float, rainfall: float, wind_speed: float) -> Tuple[WeatherCondition, str]:
        """
        Analyze weather conditions.
        
        Returns:
            Tuple of (WeatherCondition, description)
        """
        alerts = []
        severity = 0
        
        # Temperature analysis
        if 15 <= temperature <= 30:
            alerts.append("Temperature favorable")
        elif 10 <= temperature <= 35:
            alerts.append("Temperature acceptable")
            severity += 1
        else:
            alerts.append("Temperature extreme")
            severity += 2
        
        # Humidity analysis
        if 40 <= humidity <= 80:
            alerts.append("Humidity favorable")
        elif 30 <= humidity <= 90:
            alerts.append("Humidity acceptable")
            severity += 1
        else:
            alerts.append("Humidity extreme")
            severity += 2
        
        # Wind analysis
        if wind_speed <= 20:
            alerts.append("Wind speed normal")
        elif wind_speed <= 35:
            alerts.append("Wind speed elevated")
            severity += 1
        else:
            alerts.append("High wind warning")
            severity += 2
        
        # Rainfall
        if rainfall > 0:
            alerts.append(f"Rainfall: {rainfall}mm")
        
        # Determine weather condition
        if severity == 0:
            condition = WeatherCondition.FAVORABLE
        elif severity <= 2:
            condition = WeatherCondition.MODERATE
        elif severity <= 4:
            condition = WeatherCondition.UNFAVORABLE
        else:
            condition = WeatherCondition.SEVERE
        
        description = " | ".join(alerts)
        return condition, description


class IrrigationRecommender:
    """Recommends irrigation based on soil conditions."""
    
    def recommend_irrigation(self, soil_moisture: float, rainfall: float, temperature: float) -> bool:
        """
        Recommend irrigation.
        
        Returns:
            True if irrigation is needed
        """
        # If recent rainfall, no irrigation needed
        if rainfall > 10:
            return False
        
        # If soil moisture is low and temperature is high, irrigation needed
        if soil_moisture < 40 and temperature > 25:
            return True
        
        # If soil moisture is critically low, irrigation needed
        if soil_moisture < 30:
            return True
        
        return False


class SmartAgricultureMonitoringSystem:
    """Main system controller for smart agriculture monitoring."""
    
    def __init__(self, field_id: str = "FIELD_001"):
        """
        Initialize the smart agriculture monitoring system.
        
        Args:
            field_id: Unique field identifier
        """
        self.field_id = field_id
        
        # Initialize sensors
        self.soil_moisture_sensor = SoilMoistureSensor(baseline_moisture=60.0)
        self.soil_ph_sensor = SoilPHSensor(baseline_ph=7.0)
        self.soil_nutrient_sensor = SoilNutrientSensor()
        self.temperature_sensor = TemperatureSensor(baseline_temp=25.0)
        self.humidity_sensor = HumiditySensor(baseline_humidity=60.0)
        self.rainfall_sensor = RainfallSensor()
        self.wind_speed_sensor = WindSpeedSensor(baseline_wind=10.0)
        
        # Initialize analyzers
        self.crop_health_analyzer = CropHealthAnalyzer()
        self.soil_analyzer = SoilAnalyzer()
        self.weather_analyzer = WeatherAnalyzer()
        self.irrigation_recommender = IrrigationRecommender()
        
        # Data logging
        self.readings: List[AgriculturalReading] = []
        self.excellent_count = 0
        self.good_count = 0
        self.fair_count = 0
        self.poor_count = 0
        self.critical_count = 0
    
    def simulate_cycle(self) -> AgriculturalReading:
        """
        Simulate one complete monitoring cycle.
        
        Returns:
            AgriculturalReading object
        """
        # Read sensors
        rainfall = self.rainfall_sensor.read_rainfall()
        soil_moisture = self.soil_moisture_sensor.read_moisture(rainfall)
        soil_ph = self.soil_ph_sensor.read_ph()
        soil_n, soil_p, soil_k = self.soil_nutrient_sensor.read_nutrients()
        temperature = self.temperature_sensor.read_temperature()
        humidity = self.humidity_sensor.read_humidity()
        wind_speed = self.wind_speed_sensor.read_wind_speed()
        
        # Analyze crop health
        ndvi = self.crop_health_analyzer.calculate_ndvi(temperature, humidity, soil_moisture)
        crop_health, crop_alert = self.crop_health_analyzer.analyze_crop_health(ndvi, soil_moisture, temperature)
        
        # Analyze soil
        soil_quality, soil_recommendation = self.soil_analyzer.analyze_soil_quality(soil_ph, soil_n, soil_p, soil_k)
        
        # Analyze weather
        weather_condition, weather_description = self.weather_analyzer.analyze_weather(
            temperature, humidity, rainfall, wind_speed
        )
        
        # Recommend irrigation
        irrigation_needed = self.irrigation_recommender.recommend_irrigation(soil_moisture, rainfall, temperature)
        
        # Update counters
        if crop_health == CropHealthStatus.EXCELLENT:
            self.excellent_count += 1
        elif crop_health == CropHealthStatus.GOOD:
            self.good_count += 1
        elif crop_health == CropHealthStatus.FAIR:
            self.fair_count += 1
        elif crop_health == CropHealthStatus.POOR:
            self.poor_count += 1
        elif crop_health == CropHealthStatus.CRITICAL:
            self.critical_count += 1
        
        # Create reading record
        reading = AgriculturalReading(
            timestamp=datetime.datetime.now().isoformat(),
            field_id=self.field_id,
            soil_moisture=soil_moisture,
            soil_ph=soil_ph,
            soil_nitrogen=soil_n,
            soil_phosphorus=soil_p,
            soil_potassium=soil_k,
            temperature=temperature,
            humidity=humidity,
            rainfall=rainfall,
            wind_speed=wind_speed,
            crop_ndvi=ndvi,
            crop_health_status=crop_health.value,
            soil_quality_status=soil_quality.value,
            weather_condition=weather_condition.value,
            irrigation_needed=irrigation_needed,
            fertilizer_recommendation=soil_recommendation,
            alert_message=crop_alert
        )
        
        self.readings.append(reading)
        return reading
    
    def run_simulation(self, num_cycles: int = 1000) -> List[AgriculturalReading]:
        """
        Run the simulation for a specified number of cycles.
        
        Args:
            num_cycles: Number of monitoring cycles to simulate
            
        Returns:
            List of all agricultural readings
        """
        for _ in range(num_cycles):
            self.simulate_cycle()
        
        return self.readings
    
    def get_statistics(self) -> Dict:
        """
        Calculate statistics from collected readings.
        
        Returns:
            Dictionary containing various statistics
        """
        if not self.readings:
            return {}
        
        soil_moisture = [r.soil_moisture for r in self.readings]
        soil_ph = [r.soil_ph for r in self.readings]
        soil_nitrogen = [r.soil_nitrogen for r in self.readings]
        soil_phosphorus = [r.soil_phosphorus for r in self.readings]
        soil_potassium = [r.soil_potassium for r in self.readings]
        temperatures = [r.temperature for r in self.readings]
        humidities = [r.humidity for r in self.readings]
        rainfall_amounts = [r.rainfall for r in self.readings]
        wind_speeds = [r.wind_speed for r in self.readings]
        ndvi_values = [r.crop_ndvi for r in self.readings]
        
        irrigation_count = sum(1 for r in self.readings if r.irrigation_needed)
        
        return {
            'total_readings': len(self.readings),
            'total_cycles': len(self.readings),
            'field_id': self.field_id,
            'soil_moisture': {
                'avg': round(statistics.mean(soil_moisture), 2),
                'min': round(min(soil_moisture), 2),
                'max': round(max(soil_moisture), 2),
                'std': round(statistics.stdev(soil_moisture), 2) if len(soil_moisture) > 1 else 0
            },
            'soil_ph': {
                'avg': round(statistics.mean(soil_ph), 2),
                'min': round(min(soil_ph), 2),
                'max': round(max(soil_ph), 2),
                'std': round(statistics.stdev(soil_ph), 2) if len(soil_ph) > 1 else 0
            },
            'soil_nitrogen': {
                'avg': round(statistics.mean(soil_nitrogen), 2),
                'min': round(min(soil_nitrogen), 2),
                'max': round(max(soil_nitrogen), 2)
            },
            'soil_phosphorus': {
                'avg': round(statistics.mean(soil_phosphorus), 2),
                'min': round(min(soil_phosphorus), 2),
                'max': round(max(soil_phosphorus), 2)
            },
            'soil_potassium': {
                'avg': round(statistics.mean(soil_potassium), 2),
                'min': round(min(soil_potassium), 2),
                'max': round(max(soil_potassium), 2)
            },
            'temperature': {
                'avg': round(statistics.mean(temperatures), 2),
                'min': round(min(temperatures), 2),
                'max': round(max(temperatures), 2),
                'std': round(statistics.stdev(temperatures), 2) if len(temperatures) > 1 else 0
            },
            'humidity': {
                'avg': round(statistics.mean(humidities), 2),
                'min': round(min(humidities), 2),
                'max': round(max(humidities), 2),
                'std': round(statistics.stdev(humidities), 2) if len(humidities) > 1 else 0
            },
            'rainfall': {
                'total': round(sum(rainfall_amounts), 2),
                'avg': round(statistics.mean(rainfall_amounts), 2),
                'rainy_days': sum(1 for r in rainfall_amounts if r > 0)
            },
            'wind_speed': {
                'avg': round(statistics.mean(wind_speeds), 2),
                'min': round(min(wind_speeds), 2),
                'max': round(max(wind_speeds), 2)
            },
            'crop_ndvi': {
                'avg': round(statistics.mean(ndvi_values), 2),
                'min': round(min(ndvi_values), 2),
                'max': round(max(ndvi_values), 2)
            },
            'crop_health_distribution': {
                'excellent': self.excellent_count,
                'good': self.good_count,
                'fair': self.fair_count,
                'poor': self.poor_count,
                'critical': self.critical_count
            },
            'irrigation_events': irrigation_count,
            'irrigation_percentage': round((irrigation_count / len(self.readings)) * 100, 2)
        }
    
    def export_to_csv(self, filename: str):
        """Export readings to CSV file."""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'field_id', 'soil_moisture', 'soil_ph', 'soil_nitrogen',
                         'soil_phosphorus', 'soil_potassium', 'temperature', 'humidity', 'rainfall',
                         'wind_speed', 'crop_ndvi', 'crop_health_status', 'soil_quality_status',
                         'weather_condition', 'irrigation_needed', 'fertilizer_recommendation', 'alert_message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for reading in self.readings:
                writer.writerow(asdict(reading))
    
    def export_to_json(self, filename: str):
        """Export readings to JSON file."""
        data = {
            'field_id': self.field_id,
            'metadata': {
                'total_readings': len(self.readings),
                'total_cycles': len(self.readings),
                'monitoring_duration': 'Simulated continuous monitoring'
            },
            'statistics': self.get_statistics(),
            'alert_history': self.crop_health_analyzer.alert_history,
            'readings': [asdict(r) for r in self.readings]
        }
        
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)
    
    def export_alerts_to_csv(self, filename: str):
        """Export alert history to CSV file."""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'status', 'message', 'ndvi', 'soil_moisture', 'temperature']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for alert in self.crop_health_analyzer.alert_history:
                writer.writerow(alert)


class SystemPerformanceAnalyzer:
    """Analyzes system performance and efficiency metrics."""
    
    @staticmethod
    def calculate_crop_health_score(excellent: int, good: int, fair: int, poor: int, critical: int, total: int) -> float:
        """
        Calculate overall crop health score.
        
        Returns:
            Health score (0-100)
        """
        if total == 0:
            return 100.0
        score = ((excellent * 100 + good * 80 + fair * 60 + poor * 40 + critical * 0) / (total * 100)) * 100
        return round(score, 2)
    
    @staticmethod
    def calculate_soil_quality_score(avg_ph: float, avg_n: float, avg_p: float, avg_k: float) -> float:
        """
        Calculate soil quality score.
        
        Returns:
            Quality score (0-100)
        """
        ph_score = 100 - abs(avg_ph - 7.0) * 10
        n_score = 100 if 30 <= avg_n <= 50 else 70
        p_score = 100 if 15 <= avg_p <= 30 else 70
        k_score = 100 if 150 <= avg_k <= 250 else 70
        
        overall = (ph_score + n_score + p_score + k_score) / 4
        return round(max(0, min(100, overall)), 2)
    
    @staticmethod
    def calculate_environmental_favorability(avg_temp: float, avg_humidity: float, avg_wind: float) -> float:
        """
        Calculate environmental favorability score.
        
        Returns:
            Favorability score (0-100)
        """
        temp_score = 100 if 15 <= avg_temp <= 30 else 70
        humidity_score = 100 if 40 <= avg_humidity <= 80 else 70
        wind_score = 100 if avg_wind <= 20 else 70
        
        overall = (temp_score + humidity_score + wind_score) / 3
        return round(overall, 2)


def main():
    """Main function to run the simulation."""
    print("=" * 80)
    print("IOT-BASED SMART AGRICULTURE MONITORING SYSTEM")
    print("Crop Health Assessment, Soil Analysis, and Weather Tracking")
    print("=" * 80)
    print()
    
    # Initialize system
    system = SmartAgricultureMonitoringSystem(field_id="FIELD_001")
    
    print("Starting simulation with 1000 monitoring cycles...")
    print("(Continuous agricultural field monitoring with real-time analysis)")
    print()
    
    # Run simulation
    readings = system.run_simulation(num_cycles=1000)
    
    # Get statistics
    stats = system.get_statistics()
    
    # Export data
    system.export_to_csv('/home/ubuntu/smart_agriculture_report/agricultural_readings.csv')
    system.export_to_json('/home/ubuntu/smart_agriculture_report/agricultural_readings.json')
    system.export_alerts_to_csv('/home/ubuntu/smart_agriculture_report/crop_health_alerts.csv')
    
    # Display results
    print("SIMULATION RESULTS")
    print("-" * 80)
    print(f"Total Monitoring Cycles: {stats['total_cycles']}")
    print(f"Total Readings: {stats['total_readings']}")
    print(f"Field ID: {stats['field_id']}")
    print()
    
    print("CROP HEALTH DISTRIBUTION")
    print("-" * 80)
    dist = stats['crop_health_distribution']
    print(f"Excellent: {dist['excellent']} ({(dist['excellent']/stats['total_readings']*100):.1f}%)")
    print(f"Good: {dist['good']} ({(dist['good']/stats['total_readings']*100):.1f}%)")
    print(f"Fair: {dist['fair']} ({(dist['fair']/stats['total_readings']*100):.1f}%)")
    print(f"Poor: {dist['poor']} ({(dist['poor']/stats['total_readings']*100):.1f}%)")
    print(f"Critical: {dist['critical']} ({(dist['critical']/stats['total_readings']*100):.1f}%)")
    print()
    
    print("SOIL CONDITIONS STATISTICS")
    print("-" * 80)
    print(f"Soil Moisture: {stats['soil_moisture']['avg']}% (Range: {stats['soil_moisture']['min']}-{stats['soil_moisture']['max']}%)")
    print(f"Soil pH: {stats['soil_ph']['avg']} (Range: {stats['soil_ph']['min']}-{stats['soil_ph']['max']})")
    print(f"Nitrogen: {stats['soil_nitrogen']['avg']} mg/kg (Range: {stats['soil_nitrogen']['min']}-{stats['soil_nitrogen']['max']})")
    print(f"Phosphorus: {stats['soil_phosphorus']['avg']} mg/kg (Range: {stats['soil_phosphorus']['min']}-{stats['soil_phosphorus']['max']})")
    print(f"Potassium: {stats['soil_potassium']['avg']} mg/kg (Range: {stats['soil_potassium']['min']}-{stats['soil_potassium']['max']})")
    print()
    
    print("WEATHER STATISTICS")
    print("-" * 80)
    print(f"Temperature: {stats['temperature']['avg']}°C (Range: {stats['temperature']['min']}-{stats['temperature']['max']}°C)")
    print(f"Humidity: {stats['humidity']['avg']}% (Range: {stats['humidity']['min']}-{stats['humidity']['max']}%)")
    print(f"Total Rainfall: {stats['rainfall']['total']} mm ({stats['rainfall']['rainy_days']} rainy days)")
    print(f"Wind Speed: {stats['wind_speed']['avg']} km/h (Range: {stats['wind_speed']['min']}-{stats['wind_speed']['max']})")
    print()
    
    print("CROP MONITORING STATISTICS")
    print("-" * 80)
    print(f"Average NDVI: {stats['crop_ndvi']['avg']} (Range: {stats['crop_ndvi']['min']}-{stats['crop_ndvi']['max']})")
    print(f"Irrigation Events: {stats['irrigation_events']} ({stats['irrigation_percentage']}%)")
    print()
    
    # Performance analysis
    analyzer = SystemPerformanceAnalyzer()
    health_score = analyzer.calculate_crop_health_score(
        dist['excellent'], dist['good'], dist['fair'], dist['poor'], dist['critical'],
        stats['total_readings']
    )
    soil_score = analyzer.calculate_soil_quality_score(
        stats['soil_ph']['avg'], stats['soil_nitrogen']['avg'],
        stats['soil_phosphorus']['avg'], stats['soil_potassium']['avg']
    )
    env_score = analyzer.calculate_environmental_favorability(
        stats['temperature']['avg'], stats['humidity']['avg'], stats['wind_speed']['avg']
    )
    
    print("SYSTEM PERFORMANCE METRICS")
    print("-" * 80)
    print(f"Crop Health Score: {health_score}/100")
    print(f"Soil Quality Score: {soil_score}/100")
    print(f"Environmental Favorability: {env_score}/100")
    print()
    
    print("Data exported to:")
    print("  - /home/ubuntu/smart_agriculture_report/agricultural_readings.csv")
    print("  - /home/ubuntu/smart_agriculture_report/agricultural_readings.json")
    print("  - /home/ubuntu/smart_agriculture_report/crop_health_alerts.csv")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
