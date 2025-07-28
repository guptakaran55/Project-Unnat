from prometheus_client import Counter, Histogram, Gauge, generate_latest
import logging
from datetime import datetime


class ApplicationMonitoring:
    def __init__(self):
        # Prometheus metrics
        self.optimization_counter = Counter(
            'building_optimizations_total',
            'Total number of building optimizations'
        )

        self.optimization_duration = Histogram(
            'building_optimization_duration_seconds',
            'Time spent on building optimization'
        )

        self.active_sessions = Gauge(
            'active_design_sessions',
            'Number of active design sessions'
        )

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('building_optimizer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def track_optimization(self, lat, lng, building_type, duration, success):
        """Track optimization metrics"""
        self.optimization_counter.inc()
        self.optimization_duration.observe(duration)

        self.logger.info(f"Optimization completed: {lat}, {lng}, {building_type}, "
                         f"Duration: {duration}s, Success: {success}")

    def track_user_behavior(self, user_id, action, parameters):
        """Track user interactions for analytics"""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'action': action,
            'parameters': parameters
        }

        # Store in analytics database
        self.store_analytics_event(event)