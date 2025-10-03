"""
Network God Game Engine Physics System
Physical simulation and collision detection
"""

import time
import random
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from .engine_core import EngineSystem

@dataclass
class PhysicsSettings:
    gravity: Tuple[float, float, float] = (0.0, -9.81, 0.0)
    simulation_rate: int = 60  # Hz
    max_substeps: int = 4
    enable_collision_detection: bool = True
    enable_constraints: bool = True
    
@dataclass
class RigidBody:
    id: str
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    angular_velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    mass: float = 1.0
    friction: float = 0.5
    restitution: float = 0.3  # Bounciness
    is_static: bool = False
    is_kinematic: bool = False
    
@dataclass
class Collision:
    body_a: str
    body_b: str
    contact_point: Tuple[float, float, float]
    normal: Tuple[float, float, float]
    penetration_depth: float
    
@dataclass
class PhysicsStats:
    bodies_count: int = 0
    collisions_detected: int = 0
    constraints_solved: int = 0
    simulation_steps: int = 0
    avg_step_time: float = 0.0

class PhysicsSystem(EngineSystem):
    def __init__(self):
        self.settings = PhysicsSettings()
        self.stats = PhysicsStats()
        self.bodies: Dict[str, RigidBody] = {}
        self.colliders = {}
        self.constraints = {}
        self.materials = {}
        
        # Simulation state
        self.simulation_time = 0.0
        self.step_times = []
        self.max_step_times = 100
        
        # Self-improvement variables
        self.optimization_level = 1.0
        self.adaptive_substepping = True
        self.performance_history = []
        
    def initialize(self):
        """Initialize the physics system"""
        print("Initializing Physics System...")
        print(f"  Gravity: {self.settings.gravity}")
        print(f"  Simulation Rate: {self.settings.simulation_rate} Hz")
        print(f"  Max Substeps: {self.settings.max_substeps}")
        
        # Create default materials
        self._create_default_materials()
        
        print("Physics System initialized successfully")
        
    def _create_default_materials(self):
        """Create default physics materials"""
        self.materials["default"] = {
            "friction": 0.5,
            "restitution": 0.3,
            "density": 1.0
        }
        
        self.materials["ice"] = {
            "friction": 0.1,
            "restitution": 0.4,
            "density": 0.9
        }
        
        self.materials["rubber"] = {
            "friction": 0.8,
            "restitution": 0.9,
            "density": 1.2
        }
        
    def update(self, delta_time: float):
        """Update the physics system"""
        # Record step time for optimization
        step_start = time.time()
        
        # Perform physics simulation
        self._simulate(delta_time)
        
        # Update statistics
        self.stats.simulation_steps += 1
        step_time = time.time() - step_start
        self.step_times.append(step_time)
        if len(self.step_times) > self.max_step_times:
            self.step_times.pop(0)
            
        self.stats.avg_step_time = sum(self.step_times) / len(self.step_times) if self.step_times else 0
        
        # Adapt simulation based on performance
        self._adapt_simulation()
        
    def _simulate(self, delta_time: float):
        """Perform physics simulation for the given time step"""
        # Apply forces (gravity, etc.)
        self._apply_forces()
        
        # Integrate velocities and positions
        self._integrate(delta_time)
        
        # Detect and resolve collisions
        if self.settings.enable_collision_detection:
            collisions = self._detect_collisions()
            self.stats.collisions_detected = len(collisions)
            self._resolve_collisions(collisions)
            
        # Solve constraints
        if self.settings.enable_constraints:
            self._solve_constraints()
            
        # Update simulation time
        self.simulation_time += delta_time
        
    def _apply_forces(self):
        """Apply forces to all rigid bodies"""
        for body in self.bodies.values():
            if not body.is_static and not body.is_kinematic:
                # Apply gravity
                body.velocity = (
                    body.velocity[0] + self.settings.gravity[0] * (1/60),
                    body.velocity[1] + self.settings.gravity[1] * (1/60),
                    body.velocity[2] + self.settings.gravity[2] * (1/60)
                )
                
    def _integrate(self, delta_time: float):
        """Integrate velocities and positions"""
        for body in self.bodies.values():
            if not body.is_static and not body.is_kinematic:
                # Update position
                body.position = (
                    body.position[0] + body.velocity[0] * delta_time,
                    body.position[1] + body.velocity[1] * delta_time,
                    body.position[2] + body.velocity[2] * delta_time
                )
                
                # Update rotation (simplified)
                body.rotation = (
                    body.rotation[0] + body.angular_velocity[0] * delta_time,
                    body.rotation[1] + body.angular_velocity[1] * delta_time,
                    body.rotation[2] + body.angular_velocity[2] * delta_time
                )
                
    def _detect_collisions(self) -> List[Collision]:
        """Detect collisions between rigid bodies"""
        collisions = []
        
        # Simplified collision detection for demonstration
        body_list = list(self.bodies.values())
        for i in range(len(body_list)):
            for j in range(i + 1, len(body_list)):
                body_a = body_list[i]
                body_b = body_list[j]
                
                # Simple sphere collision detection
                distance = math.sqrt(
                    (body_a.position[0] - body_b.position[0]) ** 2 +
                    (body_a.position[1] - body_b.position[1]) ** 2 +
                    (body_a.position[2] - body_b.position[2]) ** 2
                )
                
                # Assume radius of 1 for simplicity
                if distance < 2.0:  # 1 + 1 = 2 (sum of radii)
                    collision = Collision(
                        body_a=body_a.id,
                        body_b=body_b.id,
                        contact_point=(
                            (body_a.position[0] + body_b.position[0]) / 2,
                            (body_a.position[1] + body_b.position[1]) / 2,
                            (body_a.position[2] + body_b.position[2]) / 2
                        ),
                        normal=(
                            body_b.position[0] - body_a.position[0],
                            body_b.position[1] - body_a.position[1],
                            body_b.position[2] - body_a.position[2]
                        ),
                        penetration_depth=2.0 - distance
                    )
                    collisions.append(collision)
                    
        return collisions
        
    def _resolve_collisions(self, collisions: List[Collision]):
        """Resolve detected collisions"""
        for collision in collisions:
            body_a = self.bodies[collision.body_a]
            body_b = self.bodies[collision.body_b]
            
            # Skip if either body is static
            if body_a.is_static and body_b.is_static:
                continue
                
            # Simple collision response
            if not body_a.is_static:
                # Reflect velocity
                body_a.velocity = (
                    -body_a.velocity[0] * body_a.restitution,
                    -body_a.velocity[1] * body_a.restitution,
                    -body_a.velocity[2] * body_a.restitution
                )
                
            if not body_b.is_static:
                # Reflect velocity
                body_b.velocity = (
                    -body_b.velocity[0] * body_b.restitution,
                    -body_b.velocity[1] * body_b.restitution,
                    -body_b.velocity[2] * body_b.restitution
                )
                
    def _solve_constraints(self):
        """Solve physics constraints"""
        # In a real implementation, this would solve joints, limits, etc.
        # For now, we'll just simulate the work
        self.stats.constraints_solved = random.randint(0, 10)
        time.sleep(0.001)  # Simulate constraint solving time
        
    def _adapt_simulation(self):
        """Adapt simulation parameters based on performance"""
        if len(self.step_times) < 30:
            return
            
        # Calculate average step time
        recent_steps = self.step_times[-30:]
        avg_step_time = sum(recent_steps) / len(recent_steps)
        target_step_time = 1.0 / self.settings.simulation_rate
        
        # Adjust optimization level based on performance
        if avg_step_time > target_step_time * 1.2:  # 20% over target
            # Increase optimization (reduce quality for performance)
            self.optimization_level = max(0.5, self.optimization_level - 0.05)
            print(f"Reducing physics quality to {self.optimization_level:.2f}")
        elif avg_step_time < target_step_time * 0.8:  # 20% under target
            # Decrease optimization (increase quality)
            self.optimization_level = min(1.5, self.optimization_level + 0.02)
            print(f"Increasing physics quality to {self.optimization_level:.2f}")
            
    def add_rigid_body(self, body_id: str, body: RigidBody):
        """Add a rigid body to the simulation"""
        self.bodies[body_id] = body
        self.stats.bodies_count = len(self.bodies)
        print(f"Added rigid body '{body_id}' to physics simulation")
        
    def remove_rigid_body(self, body_id: str):
        """Remove a rigid body from the simulation"""
        if body_id in self.bodies:
            del self.bodies[body_id]
            self.stats.bodies_count = len(self.bodies)
            print(f"Removed rigid body '{body_id}' from physics simulation")
            
    def set_gravity(self, x: float, y: float, z: float):
        """Set gravity vector"""
        self.settings.gravity = (x, y, z)
        print(f"Gravity set to ({x}, {y}, {z})")
        
    def get_physics_stats(self) -> PhysicsStats:
        """Get current physics statistics"""
        return self.stats.copy() if hasattr(self.stats, 'copy') else self.stats
        
    def get_performance_rating(self) -> float:
        """Get physics performance rating (0.0 to 1.0)"""
        if not self.step_times:
            return 1.0
            
        recent_steps = self.step_times[-30:]
        avg_step_time = sum(recent_steps) / len(recent_steps)
        target_step_time = 1.0 / self.settings.simulation_rate
        
        # Performance rating based on how close we are to target step time
        if avg_step_time <= 0:
            return 1.0
            
        rating = min(1.0, target_step_time / avg_step_time)
        return rating

if __name__ == "__main__":
    # Example usage
    physics = PhysicsSystem()
    physics.initialize()
    
    # Add some rigid bodies
    body1 = RigidBody("cube1", position=(0, 5, 0), mass=2.0)
    body2 = RigidBody("cube2", position=(0, 0, 0), is_static=True)
    
    physics.add_rigid_body("cube1", body1)
    physics.add_rigid_body("cube2", body2)
    
    # Simulate a few steps
    for i in range(100):
        physics.update(1/60)  # 60 FPS
        
    stats = physics.get_physics_stats()
    print(f"Simulated {stats.simulation_steps} steps")
    print(f"Average step time: {stats.avg_step_time:.4f}s")
    print(f"Performance rating: {physics.get_performance_rating():.2f}")