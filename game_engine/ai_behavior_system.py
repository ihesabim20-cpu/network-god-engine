"""
Network God Game Engine AI Behavior System
NPC and entity AI behaviors with self-improvement capabilities
"""

import time
import random
import math
from typing import Dict, List, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from .engine_core import EngineSystem

class BehaviorState(Enum):
    IDLE = 1
    PATROL = 2
    CHASE = 3
    ATTACK = 4
    FLEE = 5
    INTERACT = 6
    DEAD = 7

class BehaviorType(Enum):
    PASSIVE = 1
    AGGRESSIVE = 2
    DEFENSIVE = 3
    SOCIAL = 4
    INTELLECTUAL = 5

@dataclass
class BehaviorSettings:
    update_rate: float = 0.1  # Seconds between behavior updates
    perception_range: float = 20.0  # How far entities can perceive
    communication_range: float = 10.0  # How far entities can communicate
    learning_rate: float = 0.01  # Rate of behavior adaptation
    enable_group_behavior: bool = True
    enable_emotional_states: bool = True

@dataclass
class EntityState:
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    health: float = 100.0
    energy: float = 100.0
    mood: str = "neutral"
    last_action: str = "idle"
    action_cooldown: float = 0.0

@dataclass
class BehaviorProfile:
    behavior_type: BehaviorType
    aggression: float = 0.5  # 0.0 to 1.0
    intelligence: float = 0.5  # 0.0 to 1.0
    sociality: float = 0.5  # 0.0 to 1.0
    curiosity: float = 0.5  # 0.0 to 1.0
    fear: float = 0.3  # 0.0 to 1.0
    memory: Dict[str, float] = field(default_factory=dict)  # Experience memory
    preferences: Dict[str, float] = field(default_factory=dict)  # Action preferences

@dataclass
class Entity:
    id: str
    state: EntityState
    behavior: BehaviorProfile
    faction: str = "neutral"
    goals: List[str] = field(default_factory=list)
    relationships: Dict[str, float] = field(default_factory=dict)  # Entity ID to relationship value

@dataclass
class BehaviorStats:
    entities_count: int = 0
    active_behaviors: int = 0
    learning_cycles: int = 0
    avg_response_time: float = 0.0
    successful_interactions: int = 0
    failed_interactions: int = 0

class AIBehaviorSystem(EngineSystem):
    def __init__(self):
        self.settings = BehaviorSettings()
        self.stats = BehaviorStats()
        self.entities: Dict[str, Entity] = {}
        self.behavior_trees = {}
        self.stimuli = {}
        self.last_update_time = 0.0
        self.response_times = []
        self.max_response_times = 100
        
        # Self-improvement components
        self.learning_enabled = True
        self.adaptation_rate = 0.01
        self.performance_history = []
        self.behavior_models = {}  # Machine learning models for behavior prediction
        
    def initialize(self):
        """Initialize the AI behavior system"""
        print("Initializing AI Behavior System...")
        print(f"  Update Rate: {self.settings.update_rate}s")
        print(f"  Perception Range: {self.settings.perception_range}")
        print(f"  Learning Rate: {self.settings.learning_rate}")
        print(f"  Group Behavior: {'Enabled' if self.settings.enable_group_behavior else 'Disabled'}")
        
        # Create default behavior trees
        self._create_default_behavior_trees()
        
        print("AI Behavior System initialized successfully")
        
    def _create_default_behavior_trees(self):
        """Create default behavior tree templates"""
        self.behavior_trees["passive"] = {
            "root": "selector",
            "children": [
                {"name": "idle", "weight": 0.7},
                {"name": "wander", "weight": 0.3}
            ]
        }
        
        self.behavior_trees["aggressive"] = {
            "root": "selector",
            "children": [
                {"name": "attack_nearby_threats", "weight": 0.6},
                {"name": "patrol", "weight": 0.3},
                {"name": "idle", "weight": 0.1}
            ]
        }
        
        self.behavior_trees["social"] = {
            "root": "selector",
            "children": [
                {"name": "interact_with_nearby_entities", "weight": 0.5},
                {"name": "follow_friends", "weight": 0.3},
                {"name": "explore", "weight": 0.2}
            ]
        }
        
    def update(self, delta_time: float):
        """Update the AI behavior system"""
        current_time = time.time()
        
        # Only update at the specified rate
        if current_time - self.last_update_time < self.settings.update_rate:
            return
            
        update_start = time.time()
        
        # Update all entities
        self._update_entities(delta_time)
        
        # Process stimuli
        self._process_stimuli()
        
        # Adapt behaviors based on performance
        if self.learning_enabled:
            self._adapt_behaviors()
            
        # Update statistics
        self.last_update_time = current_time
        response_time = time.time() - update_start
        self.response_times.append(response_time)
        if len(self.response_times) > self.max_response_times:
            self.response_times.pop(0)
            
        self.stats.avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        self.stats.entities_count = len(self.entities)
        
    def _update_entities(self, delta_time: float):
        """Update all entities' behaviors"""
        for entity in self.entities.values():
            # Update entity state
            self._update_entity_state(entity, delta_time)
            
            # Select and execute behavior
            behavior = self._select_behavior(entity)
            self._execute_behavior(entity, behavior)
            
            # Update relationships and memory
            self._update_relationships(entity)
            self._update_memory(entity)
            
    def _update_entity_state(self, entity: Entity, delta_time: float):
        """Update entity state"""
        # Reduce action cooldown
        if entity.state.action_cooldown > 0:
            entity.state.action_cooldown = max(0, entity.state.action_cooldown - delta_time)
            
        # Regenerate energy and health slowly
        entity.state.energy = min(100.0, entity.state.energy + delta_time * 0.1)
        entity.state.health = min(100.0, entity.state.health + delta_time * 0.05)
        
    def _select_behavior(self, entity: Entity) -> str:
        """Select appropriate behavior for entity"""
        # Get nearby entities
        nearby_entities = self._get_nearby_entities(entity)
        
        # Check for threats
        threats = [e for e in nearby_entities if self._is_threat(entity, e)]
        
        # Check for friends
        friends = [e for e in nearby_entities if self._is_friend(entity, e)]
        
        # Behavior selection based on entity type and situation
        if entity.behavior.behavior_type == BehaviorType.AGGRESSIVE:
            if threats:
                return "attack"
            elif friends:
                return "patrol"
            else:
                return "wander"
        elif entity.behavior.behavior_type == BehaviorType.SOCIAL:
            if friends:
                return "interact"
            else:
                return "seek_social"
        elif entity.behavior.behavior_type == BehaviorType.DEFENSIVE:
            if threats:
                return "flee"
            else:
                return "patrol"
        else:  # PASSIVE or INTELLECTUAL
            return "explore"
            
    def _execute_behavior(self, entity: Entity, behavior: str):
        """Execute selected behavior"""
        if entity.state.action_cooldown > 0:
            return  # Still in cooldown period
            
        # Execute behavior with some randomness
        success = True
        execution_time = 0.0
        
        if behavior == "attack":
            success = self._execute_attack(entity)
            execution_time = 1.0
        elif behavior == "flee":
            success = self._execute_flee(entity)
            execution_time = 0.8
        elif behavior == "interact":
            success = self._execute_interaction(entity)
            execution_time = 1.5
        elif behavior == "patrol":
            success = self._execute_patrol(entity)
            execution_time = 2.0
        elif behavior == "wander":
            success = self._execute_wander(entity)
            execution_time = 1.2
        elif behavior == "explore":
            success = self._execute_explore(entity)
            execution_time = 2.5
        elif behavior == "seek_social":
            success = self._execute_seek_social(entity)
            execution_time = 1.8
            
        # Update statistics
        if success:
            self.stats.successful_interactions += 1
            entity.state.last_action = behavior
            entity.state.action_cooldown = execution_time
        else:
            self.stats.failed_interactions += 1
            
    def _execute_attack(self, entity: Entity) -> bool:
        """Execute attack behavior"""
        # Simulate attack action
        time.sleep(0.01)  # Simulate processing time
        entity.state.energy = max(0, entity.state.energy - 5.0)
        return True
        
    def _execute_flee(self, entity: Entity) -> bool:
        """Execute flee behavior"""
        # Simulate fleeing action
        time.sleep(0.005)  # Simulate processing time
        entity.state.energy = max(0, entity.state.energy - 2.0)
        return True
        
    def _execute_interaction(self, entity: Entity) -> bool:
        """Execute social interaction behavior"""
        # Simulate interaction
        time.sleep(0.02)  # Simulate processing time
        entity.state.energy = max(0, entity.state.energy - 1.0)
        return True
        
    def _execute_patrol(self, entity: Entity) -> bool:
        """Execute patrol behavior"""
        # Simulate patrolling
        time.sleep(0.01)  # Simulate processing time
        entity.state.energy = max(0, entity.state.energy - 1.5)
        return True
        
    def _execute_wander(self, entity: Entity) -> bool:
        """Execute wandering behavior"""
        # Simulate wandering
        time.sleep(0.005)  # Simulate processing time
        entity.state.energy = max(0, entity.state.energy - 0.5)
        return True
        
    def _execute_explore(self, entity: Entity) -> bool:
        """Execute exploration behavior"""
        # Simulate exploration
        time.sleep(0.015)  # Simulate processing time
        entity.state.energy = max(0, entity.state.energy - 2.0)
        return True
        
    def _execute_seek_social(self, entity: Entity) -> bool:
        """Execute social seeking behavior"""
        # Simulate seeking social interaction
        time.sleep(0.01)  # Simulate processing time
        entity.state.energy = max(0, entity.state.energy - 1.0)
        return True
        
    def _get_nearby_entities(self, entity: Entity) -> List[Entity]:
        """Get entities within perception range"""
        nearby = []
        for other_id, other_entity in self.entities.items():
            if other_id != entity.id:
                distance = math.sqrt(
                    (entity.state.position[0] - other_entity.state.position[0]) ** 2 +
                    (entity.state.position[1] - other_entity.state.position[1]) ** 2 +
                    (entity.state.position[2] - other_entity.state.position[2]) ** 2
                )
                if distance <= self.settings.perception_range:
                    nearby.append(other_entity)
        return nearby
        
    def _is_threat(self, entity: Entity, other: Entity) -> bool:
        """Check if another entity is a threat"""
        # Simple threat assessment
        faction_hostile = entity.faction != other.faction
        aggression_factor = other.behavior.aggression > 0.7
        return faction_hostile and aggression_factor
        
    def _is_friend(self, entity: Entity, other: Entity) -> bool:
        """Check if another entity is a friend"""
        # Simple friendship assessment
        faction_allied = entity.faction == other.faction
        relationship_positive = entity.relationships.get(other.id, 0) > 0
        return faction_allied or relationship_positive
        
    def _process_stimuli(self):
        """Process environmental stimuli"""
        # In a real implementation, this would process sounds, visual cues, etc.
        pass
        
    def _adapt_behaviors(self):
        """Adapt behaviors based on performance and experience"""
        # This is where the self-improvement happens
        self.stats.learning_cycles += 1
        
        # Adjust behavior preferences based on success rate
        success_rate = (
            self.stats.successful_interactions /
            max(1, self.stats.successful_interactions + self.stats.failed_interactions)
        )
        
        # If success rate is low, increase exploration of new behaviors
        if success_rate < 0.7:
            self.settings.learning_rate = min(0.1, self.settings.learning_rate + 0.001)
        elif success_rate > 0.9:
            self.settings.learning_rate = max(0.001, self.settings.learning_rate - 0.0005)
            
    def _update_relationships(self, entity: Entity):
        """Update relationships with other entities"""
        # Simple relationship update based on recent interactions
        pass
        
    def _update_memory(self, entity: Entity):
        """Update entity memory with recent experiences"""
        # Store successful actions in memory
        if entity.state.last_action not in entity.behavior.memory:
            entity.behavior.memory[entity.state.last_action] = 0
        entity.behavior.memory[entity.state.last_action] += 1
        
    def add_entity(self, entity_id: str, entity: Entity):
        """Add an entity to the behavior system"""
        self.entities[entity_id] = entity
        print(f"Added entity '{entity_id}' to AI behavior system")
        
    def remove_entity(self, entity_id: str):
        """Remove an entity from the behavior system"""
        if entity_id in self.entities:
            del self.entities[entity_id]
            print(f"Removed entity '{entity_id}' from AI behavior system")
            
    def set_behavior_type(self, entity_id: str, behavior_type: BehaviorType):
        """Set behavior type for an entity"""
        if entity_id in self.entities:
            self.entities[entity_id].behavior.behavior_type = behavior_type
            print(f"Set behavior type for '{entity_id}' to {behavior_type.name}")
            
    def get_behavior_stats(self) -> BehaviorStats:
        """Get current behavior statistics"""
        return self.stats.copy() if hasattr(self.stats, 'copy') else self.stats
        
    def get_performance_rating(self) -> float:
        """Get AI behavior performance rating (0.0 to 1.0)"""
        if not self.response_times:
            return 1.0
            
        recent_responses = self.response_times[-30:]
        avg_response_time = sum(recent_responses) / len(recent_responses)
        
        # Performance rating based on response time (target < 0.05s)
        rating = max(0.0, min(1.0, 1.0 - (avg_response_time / 0.05)))
        return rating

if __name__ == "__main__":
    # Example usage
    ai_system = AIBehaviorSystem()
    ai_system.initialize()
    
    # Create some entities
    entity1 = Entity(
        id="npc1",
        state=EntityState(position=(0, 0, 0)),
        behavior=BehaviorProfile(
            behavior_type=BehaviorType.SOCIAL,
            aggression=0.2,
            intelligence=0.8,
            sociality=0.9
        ),
        faction="allied"
    )
    
    entity2 = Entity(
        id="npc2",
        state=EntityState(position=(5, 0, 0)),
        behavior=BehaviorProfile(
            behavior_type=BehaviorType.AGGRESSIVE,
            aggression=0.8,
            intelligence=0.6,
            sociality=0.3
        ),
        faction="enemy"
    )
    
    # Add entities to system
    ai_system.add_entity("npc1", entity1)
    ai_system.add_entity("npc2", entity2)
    
    # Simulate a few updates
    for i in range(50):
        ai_system.update(0.1)  # 10 FPS updates
        
    stats = ai_system.get_behavior_stats()
    print(f"Managed {stats.entities_count} entities")
    print(f"Executed {stats.learning_cycles} learning cycles")
    print(f"Average response time: {stats.avg_response_time:.4f}s")
    print(f"Performance rating: {ai_system.get_performance_rating():.2f}")