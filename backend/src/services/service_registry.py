class ServiceRegistry:
    def __init__(self):
        self.services = {}
    
    def register(self, name, service):
        """Register a service for health checking"""
        self.services[name] = service
        return service
    
    def check_service(self, service_name=None):
        """Check internal state of services"""
        results = {}
        
        if service_name:
            if service_name in self.services:
                service = self.services[service_name]
                if hasattr(service, 'check_internal'):
                    results[service_name] = service.check_internal()
                else:
                    results[service_name] = {"status": "unknown", "details": "No health check implemented"}
            else:
                results[service_name] = {"status": "not_found", "details": "Service not registered"}
        else:
            # Check all services
            for name, service in self.services.items():
                if hasattr(service, 'check_internal'):
                    results[name] = service.check_internal()
                else:
                    results[name] = {"status": "unknown", "details": "No health check implemented"}
                    
        return results