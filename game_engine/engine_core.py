"""
Network God Game Engine Core
Main game loop and system management
"""

import time
import threading
from typing import Dict, List, Callable
from dataclasses import dataclass
from enum import Enum

class EngineState(Enum):
    STOPPED = 0
    RUNNING = 1
    PAUSED = 2
    ERROR = 3

@dataclass
class SystemInfo:
    name: str
    version: str
    status: str
    performance: float  # 0.0 to 1.0

class GameEngine:
    def __init__(self):
        self.state = EngineState.STOPPED
        self.systems: Dict[str, object] = {}
        self.system_info: Dict[str, SystemInfo] = {}
        self.frame_rate = 60
        self.frame_time = 1.0 / self.frame_rate
        self.last_frame_time = 0
        self.current_frame = 0
        self.performance_metrics = {}
        
        # Self-improvement components
        self.improvement_modules = []
        self.learning_rate = 0.01
        self.adaptation_enabled = True
        
        print("Network God Game Engine initialized")
        
    def register_system(self, name: str, system: object, version: str = "1.0"):
        """Register a system with the engine"""
        self.systems[name] = system
        self.system_info[name] = SystemInfo(name, version, "initialized", 1.0)
        print(f"System '{name}' registered with engine")
        
    def initialize_systems(self):
        """Initialize all registered systems"""
        print("Initializing engine systems...")
        for name, system in self.systems.items():
            try:
                if hasattr(system, 'initialize'):
                    system.initialize()
                    self.system_info[name].status = "initialized"
                    print(f"  ✓ {name} initialized")
                else:
                    self.system_info[name].status = "ready"
            except Exception as e:
                self.system_info[name].status = "error"
                print(f"  ✗ {name} initialization failed: {e}")
                
    def start(self):
        """Start the game engine"""
        if self.state != EngineState.STOPPED:
            print("Engine is already running")
            return
            
        print("Starting Network God Game Engine...")
        self.state = EngineState.RUNNING
        self.last_frame_time = time.time()
        self.current_frame = 0
        
        # Start main loop in a separate thread
        self.engine_thread = threading.Thread(target=self._main_loop)
        self.engine_thread.daemon = True
        self.engine_thread.start()
        
    def stop(self):
        """Stop the game engine"""
        print("Stopping Network God Game Engine...")
        self.state = EngineState.STOPPED
        
    def pause(self):
        """Pause the game engine"""
        if self.state == EngineState.RUNNING:
            self.state = EngineState.PAUSED
            print("Engine paused")
            
    def resume(self):
        """Resume the game engine"""
        if self.state == EngineState.PAUSED:
            self.state = EngineState.RUNNING
            self.last_frame_time = time.time()
            print("Engine resumed")
            
    def _main_loop(self):
        """Main engine loop"""
        while self.state != EngineState.STOPPED:
            if self.state == EngineState.RUNNING:
                start_time = time.time()
                
                # Update all systems
                self._update_systems()
                
                # Self-improvement cycle
                if self.adaptation_enabled:
                    self._adapt_and_improve()
                
                # Calculate frame timing
                end_time = time.time()
                frame_duration = end_time - start_time
                self.current_frame += 1
                
                # Store performance metrics
                self.performance_metrics[self.current_frame] = {
                    "frame_time": frame_duration,
                    "fps": 1.0 / frame_duration if frame_duration > 0 else 0,
                    "frame_number": self.current_frame
                }
                
                # Maintain frame rate
                sleep_time = self.frame_time - frame_duration
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            else:
                time.sleep(0.01)  # Small sleep when paused
                
    def _update_systems(self):
        """Update all registered systems"""
        for name, system in self.systems.items():
            try:
                if hasattr(system, 'update'):
                    system.update(self.frame_time)
                    self.system_info[name].performance = min(1.0, 1.0 / (self.frame_time * 0.9))
            except Exception as e:
                self.system_info[name].status = "error"
                print(f"Error updating {name}: {e}")
                
    def _adapt_and_improve(self):
        """Run self-improvement algorithms"""
        # This is where the engine would adapt based on performance metrics
        # and player feedback
        if self.current_frame % 300 == 0:  # Every 5 seconds at 60 FPS
            self._analyze_performance()
            self._optimize_systems()
            
    def _analyze_performance(self):
        """Analyze engine performance and identify bottlenecks"""
        if len(self.performance_metrics) < 10:
            return
            
        # Calculate average frame time
        recent_frames = list(self.performance_metrics.values())[-300:]  # Last 5 seconds
        avg_frame_time = sum(f["frame_time"] for f in recent_frames) / len(recent_frames)
        avg_fps = sum(f["fps"] for f in recent_frames) / len(recent_frames)
        
        # Identify systems with poor performance
        slow_systems = []
        for name, info in self.system_info.items():
            if info.performance < 0.7:
                slow_systems.append((name, info.performance))
                
        if avg_fps < self.frame_rate * 0.8:  # Below 80% target FPS
            print(f"Performance issue detected: {avg_fps:.1f} FPS (target: {self.frame_rate})")
            if slow_systems:
                print(f"Slow systems: {', '.join([f'{name} ({perf:.2f})' for name, perf in slow_systems])}")
                
    def _optimize_systems(self):
        """Optimize systems based on performance analysis"""
        # In a real implementation, this would make actual optimizations
        # For now, we'll just simulate the process
        for name, info in self.system_info.items():
            if info.performance < 0.8 and self.adaptation_enabled:
                # Simulate optimization
                improvement = min(0.2, (1.0 - info.performance) * 0.5)
                info.performance = min(1.0, info.performance + improvement)
                
    def get_system_info(self) -> Dict[str, SystemInfo]:
        """Get information about all registered systems"""
        return self.system_info.copy()
        
    def get_performance_stats(self) -> Dict:
        """Get engine performance statistics"""
        if not self.performance_metrics:
            return {}
            
        recent_frames = list(self.performance_metrics.values())[-300:]
        avg_frame_time = sum(f["frame_time"] for f in recent_frames) / len(recent_frames)
        avg_fps = sum(f["fps"] for f in recent_frames) / len(recent_frames)
        
        return {
            "average_frame_time": avg_frame_time,
            "average_fps": avg_fps,
            "current_frame": self.current_frame,
            "engine_state": self.state.name
        }
        
    def add_improvement_module(self, module):
        """Add a self-improvement module to the engine"""
        self.improvement_modules.append(module)
        print(f"Improvement module added: {type(module).__name__}")

# Example system base class
class EngineSystem:
    def initialize(self):
        """Initialize the system"""
        pass
        
    def update(self, delta_time: float):
        """Update the system"""
        pass
        
    def shutdown(self):
        """Shutdown the system"""
        pass

if __name__ == "__main__":
    # Example usage
    engine = GameEngine()
    
    # Register some example systems
    class RenderSystem(EngineSystem):
        def initialize(self):
            print("Render system initialized")
            
        def update(self, delta_time: float):
            # Simulate rendering work
            time.sleep(0.001)  # 1ms of work
            
    class PhysicsSystem(EngineSystem):
        def initialize(self):
            print("Physics system initialized")
            
        def update(self, delta_time: float):
            # Simulate physics work
            time.sleep(0.002)  # 2ms of work
            
    # Register systems
    engine.register_system("renderer", RenderSystem())
    engine.register_system("physics", PhysicsSystem())
    
    # Initialize and start engine
    engine.initialize_systems()
    engine.start()
    
    # Run for a few seconds
    time.sleep(5)
    
    # Stop engine
    engine.stop()
    print("Engine test completed")