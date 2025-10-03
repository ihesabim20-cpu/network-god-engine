"""
Network God Game Engine Content Generator
Procedural content generation with self-improvement capabilities
"""

import time
import random
import math
import hashlib
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from .engine_core import EngineSystem

@dataclass
class GenerationSettings:
    seed: int = 42
    quality_level: int = 3  # 1-5, where 5 is highest quality
    complexity_factor: float = 1.0
    enable_adaptive_generation: bool = True
    max_generation_time: float = 5.0  # seconds
    cache_size: int = 100

@dataclass
class WorldParameters:
    size: Tuple[int, int, int] = (1000, 100, 1000)  # width, height, depth
    terrain_complexity: float = 0.5
    water_level: float = 0.3
    biome_count: int = 5
    cave_density: float = 0.2

@dataclass
class QuestParameters:
    difficulty_range: Tuple[int, int] = (1, 10)
    reward_variance: float = 0.3
    narrative_complexity: float = 0.5
    objective_types: List[str] = field(default_factory=lambda: [
        "retrieve", "defeat", "explore", "protect", "deliver"
    ])

@dataclass
class GenerationStats:
    worlds_generated: int = 0
    quests_generated: int = 0
    items_generated: int = 0
    avg_generation_time: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0

class ContentGenerator(EngineSystem):
    def __init__(self):
        self.settings = GenerationSettings()
        self.world_params = WorldParameters()
        self.quest_params = QuestParameters()
        self.stats = GenerationStats()
        
        # Generation caches
        self.world_cache = {}
        self.quest_cache = {}
        self.item_cache = {}
        
        # Self-improvement components
        self.generation_history = []
        self.performance_metrics = {}
        self.optimization_suggestions = []
        self.learning_rate = 0.01
        
        # Procedural generation algorithms
        self.noise_generators = {}
        self.fractal_functions = {}
        self.distribution_functions = {}
        
        # Initialize random seed
        random.seed(self.settings.seed)
        
    def initialize(self):
        """Initialize the content generator"""
        print("Initializing Content Generator...")
        print(f"  Seed: {self.settings.seed}")
        print(f"  Quality Level: {self.settings.quality_level}/5")
        print(f"  Adaptive Generation: {'Enabled' if self.settings.enable_adaptive_generation else 'Disabled'}")
        
        # Initialize generation algorithms
        self._initialize_algorithms()
        
        print("Content Generator initialized successfully")
        
    def _initialize_algorithms(self):
        """Initialize procedural generation algorithms"""
        # Simple noise generator (in a real implementation, this would be more complex)
        self.noise_generators["simplex"] = lambda x, y: random.uniform(-1, 1)
        self.noise_generators["perlin"] = lambda x, y: random.uniform(-1, 1)
        
        # Fractal functions
        self.fractal_functions["mountain"] = lambda x, y: abs(math.sin(x * 0.1) * math.cos(y * 0.1))
        self.fractal_functions["cave"] = lambda x, y: math.sin(x * 0.05) * math.cos(y * 0.05)
        
        # Distribution functions
        self.distribution_functions["uniform"] = lambda: random.uniform(0, 1)
        self.distribution_functions["gaussian"] = lambda: random.gauss(0.5, 0.2)
        
    def update(self, delta_time: float):
        """Update the content generator"""
        # Clean up old cache entries if needed
        self._manage_cache()
        
        # Adapt generation parameters based on performance
        if self.settings.enable_adaptive_generation:
            self._adapt_generation()
            
    def _manage_cache(self):
        """Manage generation caches to prevent memory issues"""
        caches = [self.world_cache, self.quest_cache, self.item_cache]
        
        for cache in caches:
            if len(cache) > self.settings.cache_size:
                # Remove oldest entries
                keys_to_remove = list(cache.keys())[:10]
                for key in keys_to_remove:
                    del cache[key]
                    
    def _adapt_generation(self):
        """Adapt generation parameters based on performance"""
        if len(self.generation_history) < 10:
            return
            
        # Calculate average generation time
        recent_generations = self.generation_history[-30:]
        avg_time = sum(g["time"] for g in recent_generations) / len(recent_generations)
        
        # Adjust complexity based on performance
        if avg_time > self.settings.max_generation_time * 0.8:
            # Reduce complexity
            self.settings.complexity_factor = max(0.1, self.settings.complexity_factor - 0.05)
            print(f"Reducing generation complexity to {self.settings.complexity_factor:.2f}")
        elif avg_time < self.settings.max_generation_time * 0.5:
            # Increase complexity
            self.settings.complexity_factor = min(2.0, self.settings.complexity_factor + 0.02)
            print(f"Increasing generation complexity to {self.settings.complexity_factor:.2f}")
            
    def generate_world(self, seed: int = None, params: WorldParameters = None) -> Dict[str, Any]:
        """Generate a procedural world"""
        start_time = time.time()
        
        # Use provided parameters or defaults
        if params is None:
            params = self.world_params
            
        # Use provided seed or generate one
        if seed is None:
            seed = random.randint(0, 1000000)
            
        # Check cache first
        cache_key = f"world_{seed}_{hash(str(params))}"
        if cache_key in self.world_cache:
            self.stats.cache_hits += 1
            return self.world_cache[cache_key]
            
        self.stats.cache_misses += 1
        
        # Generate world
        print(f"Generating world with seed {seed}...")
        
        world = {
            "seed": seed,
            "terrain": self._generate_terrain(params),
            "biomes": self._generate_biomes(params),
            "caves": self._generate_caves(params),
            "water_bodies": self._generate_water_bodies(params),
            "points_of_interest": self._generate_pois(params),
            "npc_spawns": self._generate_npc_spawns(params)
        }
        
        # Cache the result
        if len(self.world_cache) < self.settings.cache_size:
            self.world_cache[cache_key] = world
            
        # Update statistics
        generation_time = time.time() - start_time
        self.stats.worlds_generated += 1
        self.stats.avg_generation_time = (
            (self.stats.avg_generation_time * (self.stats.worlds_generated - 1) + generation_time) 
            / self.stats.worlds_generated
        )
        
        # Store in history
        self.generation_history.append({
            "type": "world",
            "time": generation_time,
            "seed": seed,
            "complexity": params.terrain_complexity
        })
        
        print(f"World generation completed in {generation_time:.2f}s")
        return world
        
    def _generate_terrain(self, params: WorldParameters) -> List[Dict]:
        """Generate terrain data"""
        terrain = []
        width, height, depth = params.size
        
        # Simplified terrain generation
        for x in range(0, width, 10):  # Reduced resolution for performance
            for z in range(0, depth, 10):
                # Generate height using noise
                noise_value = self.noise_generators["simplex"](x, z)
                base_height = noise_value * params.terrain_complexity * 50
                
                # Apply fractal functions for more interesting terrain
                mountain_factor = self.fractal_functions["mountain"](x, z)
                final_height = base_height + (mountain_factor * 20)
                
                terrain.append({
                    "position": (x, final_height, z),
                    "normal": (0, 1, 0),  # Simplified normal
                    "material": "grass" if final_height > params.water_level * 100 else "sand"
                })
                
        return terrain
        
    def _generate_biomes(self, params: WorldParameters) -> List[Dict]:
        """Generate biome data"""
        biomes = []
        
        for i in range(params.biome_count):
            biome = {
                "id": f"biome_{i}",
                "type": random.choice(["forest", "desert", "plains", "mountains", "swamp"]),
                "position": (
                    random.randint(0, params.size[0]),
                    0,
                    random.randint(0, params.size[2])
                ),
                "radius": random.randint(50, 200),
                "vegetation_density": random.uniform(0.1, 0.9),
                "temperature": random.uniform(-10, 35)
            }
            biomes.append(biome)
            
        return biomes
        
    def _generate_caves(self, params: WorldParameters) -> List[Dict]:
        """Generate cave systems"""
        caves = []
        
        cave_count = int(params.size[0] * params.size[2] * params.cave_density / 10000)
        
        for i in range(cave_count):
            cave = {
                "id": f"cave_{i}",
                "entrance": (
                    random.randint(0, params.size[0]),
                    random.randint(0, int(params.size[1] * 0.3)),
                    random.randint(0, params.size[2])
                ),
                "length": random.randint(20, 100),
                "complexity": random.uniform(0.1, 1.0),
                "treasure_chance": random.uniform(0.1, 0.5)
            }
            caves.append(cave)
            
        return caves
        
    def _generate_water_bodies(self, params: WorldParameters) -> List[Dict]:
        """Generate water bodies"""
        water_bodies = []
        
        # Generate a few lakes and rivers
        for i in range(random.randint(3, 8)):
            water_body = {
                "id": f"water_{i}",
                "type": random.choice(["lake", "river", "pond"]),
                "position": (
                    random.randint(0, params.size[0]),
                    params.water_level * params.size[1],
                    random.randint(0, params.size[2])
                ),
                "size": (
                    random.randint(10, 100),
                    5,
                    random.randint(10, 100)
                ),
                "freshwater": random.choice([True, False])
            }
            water_bodies.append(water_body)
            
        return water_bodies
        
    def _generate_pois(self, params: WorldParameters) -> List[Dict]:
        """Generate points of interest"""
        pois = []
        
        poi_types = ["tower", "ruins", "village", "dungeon", "cave_entrance", "landmark"]
        
        for i in range(random.randint(10, 30)):
            poi = {
                "id": f"poi_{i}",
                "type": random.choice(poi_types),
                "position": (
                    random.randint(0, params.size[0]),
                    random.randint(0, params.size[1]),
                    random.randint(0, params.size[2])
                ),
                "difficulty": random.randint(1, 10),
                "quest_marker": random.choice([True, False])
            }
            pois.append(poi)
            
        return pois
        
    def _generate_npc_spawns(self, params: WorldParameters) -> List[Dict]:
        """Generate NPC spawn points"""
        spawns = []
        
        npc_types = ["merchant", "guard", "quest_giver", "enemy", "animal"]
        
        for i in range(random.randint(20, 100)):
            spawn = {
                "id": f"spawn_{i}",
                "type": random.choice(npc_types),
                "position": (
                    random.randint(0, params.size[0]),
                    random.randint(0, params.size[1]),
                    random.randint(0, params.size[2])
                ),
                "respawn_time": random.randint(30, 300),  # seconds
                "aggro_radius": random.randint(10, 50) if "enemy" in npc_types else 0
            }
            spawns.append(spawn)
            
        return spawns
        
    def generate_quest(self, seed: int = None, params: QuestParameters = None) -> Dict[str, Any]:
        """Generate a procedural quest"""
        start_time = time.time()
        
        # Use provided parameters or defaults
        if params is None:
            params = self.quest_params
            
        # Use provided seed or generate one
        if seed is None:
            seed = random.randint(0, 1000000)
            
        # Check cache first
        cache_key = f"quest_{seed}_{hash(str(params))}"
        if cache_key in self.quest_cache:
            self.stats.cache_hits += 1
            return self.quest_cache[cache_key]
            
        self.stats.cache_misses += 1
        
        # Generate quest
        print(f"Generating quest with seed {seed}...")
        
        # Select objective type
        objective_type = random.choice(params.objective_types)
        
        # Generate quest based on objective type
        if objective_type == "retrieve":
            quest = self._generate_retrieve_quest(params)
        elif objective_type == "defeat":
            quest = self._generate_defeat_quest(params)
        elif objective_type == "explore":
            quest = self._generate_explore_quest(params)
        elif objective_type == "protect":
            quest = self._generate_protect_quest(params)
        elif objective_type == "deliver":
            quest = self._generate_deliver_quest(params)
        else:
            quest = self._generate_generic_quest(params)
            
        # Add common quest elements
        quest.update({
            "seed": seed,
            "difficulty": random.randint(*params.difficulty_range),
            "rewards": self._generate_rewards(params),
            "narrative": self._generate_narrative(params)
        })
        
        # Cache the result
        if len(self.quest_cache) < self.settings.cache_size:
            self.quest_cache[cache_key] = quest
            
        # Update statistics
        generation_time = time.time() - start_time
        self.stats.quests_generated += 1
        self.stats.avg_generation_time = (
            (self.stats.avg_generation_time * (self.stats.quests_generated - 1) + generation_time) 
            / self.stats.quests_generated
        )
        
        # Store in history
        self.generation_history.append({
            "type": "quest",
            "time": generation_time,
            "seed": seed,
            "difficulty": quest["difficulty"]
        })
        
        print(f"Quest generation completed in {generation_time:.2f}s")
        return quest
        
    def _generate_retrieve_quest(self, params: QuestParameters) -> Dict:
        """Generate a retrieve quest"""
        return {
            "type": "retrieve",
            "objective": f"Retrieve the {random.choice(['Ancient', 'Cursed', 'Blessed', 'Lost'])} {random.choice(['Artifact', 'Crystal', 'Relic', 'Gem'])}",
            "target_item": f"{random.choice(['Ancient', 'Cursed', 'Blessed', 'Lost'])} {random.choice(['Artifact', 'Crystal', 'Relic', 'Gem'])}",
            "location": f"{random.choice(['Cave', 'Ruins', 'Tower', 'Dungeon'])} of {random.choice(['Light', 'Darkness', 'Fire', 'Water', 'Earth', 'Air'])}",
            "required_quantity": random.randint(1, 5)
        }
        
    def _generate_defeat_quest(self, params: QuestParameters) -> Dict:
        """Generate a defeat quest"""
        return {
            "type": "defeat",
            "objective": f"Defeat the {random.choice(['Ancient', 'Cursed', 'Powerful', 'Mighty'])} {random.choice(['Dragon', 'Demon', 'Giant', 'Beast'])}",
            "target_enemy": f"{random.choice(['Ancient', 'Cursed', 'Powerful', 'Mighty'])} {random.choice(['Dragon', 'Demon', 'Giant', 'Beast'])}",
            "location": f"{random.choice(['Cave', 'Ruins', 'Tower', 'Dungeon'])} of {random.choice(['Light', 'Darkness', 'Fire', 'Water', 'Earth', 'Air'])}",
            "required_kills": random.randint(1, 3)
        }
        
    def _generate_explore_quest(self, params: QuestParameters) -> Dict:
        """Generate an explore quest"""
        return {
            "type": "explore",
            "objective": f"Explore the {random.choice(['Mysterious', 'Hidden', 'Forbidden', 'Ancient'])} {random.choice(['Cave', 'Ruins', 'Tower', 'Dungeon', 'Forest', 'Mountain'])}",
            "location": f"{random.choice(['Mysterious', 'Hidden', 'Forbidden', 'Ancient'])} {random.choice(['Cave', 'Ruins', 'Tower', 'Dungeon', 'Forest', 'Mountain'])}",
            "exploration_goals": random.randint(3, 8)
        }
        
    def _generate_protect_quest(self, params: QuestParameters) -> Dict:
        """Generate a protect quest"""
        return {
            "type": "protect",
            "objective": f"Protect the {random.choice(['Village', 'Caravan', 'Scholar', 'Merchant'])} from {random.choice(['Bandits', 'Monsters', 'Demons', 'Invaders'])}",
            "target_to_protect": f"{random.choice(['Village', 'Caravan', 'Scholar', 'Merchant'])}",
            "threat": f"{random.choice(['Bandits', 'Monsters', 'Demons', 'Invaders'])}",
            "duration": f"{random.randint(5, 30)} minutes"
        }
        
    def _generate_deliver_quest(self, params: QuestParameters) -> Dict:
        """Generate a deliver quest"""
        return {
            "type": "deliver",
            "objective": f"Deliver {random.choice(['Package', 'Letter', 'Gift', 'Supplies'])} to {random.choice(['Merchant', 'Scholar', 'Guard Captain', 'Village Elder'])}",
            "item": f"{random.choice(['Package', 'Letter', 'Gift', 'Supplies'])}",
            "recipient": f"{random.choice(['Merchant', 'Scholar', 'Guard Captain', 'Village Elder'])}",
            "destination": f"{random.choice(['Market District', 'Scholar\'s Tower', 'Guard Barracks', 'Village Center'])}"
        }
        
    def _generate_generic_quest(self, params: QuestParameters) -> Dict:
        """Generate a generic quest"""
        return {
            "type": "generic",
            "objective": f"Complete the {random.choice(['Mysterious', 'Challenging', 'Important'])} task",
            "description": f"A {random.choice(['simple', 'complex', 'urgent'])} task requiring {random.choice(['skill', 'courage', 'wisdom'])}"
        }
        
    def _generate_rewards(self, params: QuestParameters) -> Dict:
        """Generate quest rewards"""
        base_xp = random.randint(100, 1000)
        base_gold = random.randint(10, 100)
        
        # Apply variance
        xp = int(base_xp * random.uniform(1 - params.reward_variance, 1 + params.reward_variance))
        gold = int(base_gold * random.uniform(1 - params.reward_variance, 1 + params.reward_variance))
        
        # Chance for special rewards
        special_rewards = []
        if random.random() < 0.3:  # 30% chance
            special_rewards.append(f"{random.choice(['Rare', 'Magic', 'Ancient'])} {random.choice(['Weapon', 'Armor', 'Potion', 'Scroll'])}")
            
        return {
            "xp": xp,
            "gold": gold,
            "special_items": special_rewards
        }
        
    def _generate_narrative(self, params: QuestParameters) -> Dict:
        """Generate quest narrative"""
        return {
            "title": f"The {random.choice(['Lost', 'Cursed', 'Blessed', 'Ancient'])} {random.choice(['Quest', 'Journey', 'Adventure', 'Mission'])}",
            "description": f"{random.choice(['A long time ago', 'Recently', 'In the near future', 'In a distant land'])}, {random.choice(['a great hero', 'a wise scholar', 'a brave warrior', 'an ordinary person'])} {random.choice(['discovered', 'encountered', 'found', 'learned of'])} {random.choice(['a terrible secret', 'an ancient mystery', 'a powerful artifact', 'a dangerous threat'])}.",
            "npc_giver": f"{random.choice(['Old', 'Wise', 'Mysterious', 'Ancient'])} {random.choice(['Wizard', 'Knight', 'Scholar', 'Merchant'])}"
        }
        
    def generate_item(self, seed: int = None, item_type: str = None) -> Dict[str, Any]:
        """Generate a procedural item"""
        start_time = time.time()
        
        # Use provided seed or generate one
        if seed is None:
            seed = random.randint(0, 1000000)
            
        # Check cache first
        cache_key = f"item_{seed}_{item_type or 'generic'}"
        if cache_key in self.item_cache:
            self.stats.cache_hits += 1
            return self.item_cache[cache_key]
            
        self.stats.cache_misses += 1
        
        # Generate item
        print(f"Generating item with seed {seed}...")
        
        # Select item type if not provided
        if item_type is None:
            item_type = random.choice(["weapon", "armor", "consumable", "quest_item"])
            
        # Generate item based on type
        if item_type == "weapon":
            item = self._generate_weapon(seed)
        elif item_type == "armor":
            item = self._generate_armor(seed)
        elif item_type == "consumable":
            item = self._generate_consumable(seed)
        elif item_type == "quest_item":
            item = self._generate_quest_item(seed)
        else:
            item = self._generate_generic_item(seed)
            
        # Add common item elements
        item.update({
            "seed": seed,
            "rarity": random.choice(["common", "uncommon", "rare", "epic", "legendary"]),
            "value": random.randint(10, 1000)
        })
        
        # Cache the result
        if len(self.item_cache) < self.settings.cache_size:
            self.item_cache[cache_key] = item
            
        # Update statistics
        generation_time = time.time() - start_time
        self.stats.items_generated += 1
        self.stats.avg_generation_time = (
            (self.stats.avg_generation_time * (self.stats.items_generated - 1) + generation_time) 
            / self.stats.items_generated
        )
        
        # Store in history
        self.generation_history.append({
            "type": "item",
            "time": generation_time,
            "seed": seed,
            "rarity": item["rarity"]
        })
        
        print(f"Item generation completed in {generation_time:.2f}s")
        return item
        
    def _generate_weapon(self, seed: int) -> Dict:
        """Generate a weapon"""
        weapon_types = ["sword", "axe", "bow", "staff", "dagger"]
        weapon_type = random.choice(weapon_types)
        
        return {
            "type": "weapon",
            "subtype": weapon_type,
            "name": f"{random.choice(['Sharp', 'Heavy', 'Swift', 'Ancient', 'Cursed'])} {weapon_type.capitalize()}",
            "damage": random.randint(5, 50),
            "speed": random.uniform(0.5, 2.0),
            "special_effects": [f"{random.choice(['Fire', 'Ice', 'Lightning', 'Poison'])} Damage"] if random.random() < 0.3 else []
        }
        
    def _generate_armor(self, seed: int) -> Dict:
        """Generate armor"""
        armor_types = ["helmet", "chestplate", "leggings", "boots", "shield"]
        armor_type = random.choice(armor_types)
        
        return {
            "type": "armor",
            "subtype": armor_type,
            "name": f"{random.choice(['Sturdy', 'Reinforced', 'Enchanted', 'Ancient', 'Cursed'])} {armor_type.capitalize()}",
            "defense": random.randint(3, 30),
            "durability": random.randint(50, 200),
            "special_effects": [f"{random.choice(['Fire', 'Ice', 'Lightning', 'Poison'])} Resistance"] if random.random() < 0.3 else []
        }
        
    def _generate_consumable(self, seed: int) -> Dict:
        """Generate a consumable item"""
        return {
            "type": "consumable",
            "subtype": random.choice(["potion", "scroll", "food", "elixir"]),
            "name": f"{random.choice(['Healing', 'Mana', 'Strength', 'Speed', 'Invisibility'])} {random.choice(['Potion', 'Scroll', 'Elixir'])}",
            "effect": random.choice(["heal", "mana_restore", "buff", "debuff_remove"]),
            "potency": random.randint(1, 100),
            "duration": f"{random.randint(10, 300)} seconds" if random.random() < 0.7 else "instant"
        }
        
    def _generate_quest_item(self, seed: int) -> Dict:
        """Generate a quest item"""
        return {
            "type": "quest_item",
            "subtype": "artifact",
            "name": f"{random.choice(['Ancient', 'Cursed', 'Blessed', 'Lost'])} {random.choice(['Artifact', 'Relic', 'Crystal', 'Gem'])}",
            "description": f"A {random.choice(['powerful', 'mysterious', 'ancient', 'cursed'])} object of {random.choice(['great importance', 'unknown origin', 'immense power', 'historical significance'])}",
            "quest_required": True
        }
        
    def _generate_generic_item(self, seed: int) -> Dict:
        """Generate a generic item"""
        return {
            "type": "generic",
            "subtype": random.choice(["material", "tool", "junk", "misc"]),
            "name": f"{random.choice(['Common', 'Simple', 'Basic'])} {random.choice(['Material', 'Tool', 'Component'])}",
            "description": f"A {random.choice(['useful', 'common', 'simple'])} item"
        }
        
    def get_generation_stats(self) -> GenerationStats:
        """Get current generation statistics"""
        return self.stats.copy() if hasattr(self.stats, 'copy') else self.stats
        
    def get_performance_rating(self) -> float:
        """Get content generation performance rating (0.0 to 1.0)"""
        if self.stats.worlds_generated + self.stats.quests_generated + self.stats.items_generated == 0:
            return 1.0
            
        # Performance rating based on average generation time vs max allowed time
        if self.stats.avg_generation_time <= 0:
            return 1.0
            
        rating = max(0.0, min(1.0, 1.0 - (self.stats.avg_generation_time / self.settings.max_generation_time)))
        return rating
        
    def clear_cache(self):
        """Clear all generation caches"""
        self.world_cache.clear()
        self.quest_cache.clear()
        self.item_cache.clear()
        print("Content generation caches cleared")

if __name__ == "__main__":
    # Example usage
    generator = ContentGenerator()
    generator.initialize()
    
    # Generate some content
    print("Generating sample content...")
    
    # Generate a world
    world = generator.generate_world()
    print(f"Generated world with {len(world['terrain'])} terrain points")
    
    # Generate a quest
    quest = generator.generate_quest()
    print(f"Generated quest: {quest['narrative']['title']}")
    print(f"Objective: {quest['objective']}")
    
    # Generate an item
    item = generator.generate_item(item_type="weapon")
    print(f"Generated item: {item['name']} (Rarity: {item['rarity']})")
    
    # Show statistics
    stats = generator.get_generation_stats()
    print(f"\nGeneration Statistics:")
    print(f"  Worlds: {stats.worlds_generated}")
    print(f"  Quests: {stats.quests_generated}")
    print(f"  Items: {stats.items_generated}")
    print(f"  Average Generation Time: {stats.avg_generation_time:.4f}s")
    print(f"  Performance Rating: {generator.get_performance_rating():.2f}")