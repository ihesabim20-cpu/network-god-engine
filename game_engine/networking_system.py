"""
Network God Game Engine Networking System
Multiplayer networking and blockchain integration
"""

import time
import json
import hashlib
import threading
import socket
import random
from typing import Dict, List, Tuple, Any, Callable
from dataclasses import dataclass, field
from .engine_core import EngineSystem

@dataclass
class NetworkSettings:
    server_port: int = 8080
    max_connections: int = 100
    packet_rate: int = 60  # packets per second
    enable_compression: bool = True
    enable_encryption: bool = True
    blockchain_sync_interval: float = 5.0  # seconds
    ping_interval: float = 1.0  # seconds

@dataclass
class ConnectionInfo:
    client_id: str
    address: Tuple[str, int]
    connected_time: float
    last_ping: float
    ping: float = 0.0
    packet_loss: float = 0.0
    bytes_sent: int = 0
    bytes_received: int = 0

@dataclass
class BlockchainConfig:
    rpc_endpoint: str = "http://localhost:8545"
    contract_addresses: Dict[str, str] = field(default_factory=dict)
    wallet_address: str = ""
    private_key: str = ""
    network_id: int = 1  # 1=mainnet, 3=ropsten, 4=rinkeby, etc.

@dataclass
class NetworkStats:
    active_connections: int = 0
    total_connections: int = 0
    packets_sent: int = 0
    packets_received: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    avg_latency: float = 0.0
    blockchain_syncs: int = 0

class NetworkingSystem(EngineSystem):
    def __init__(self):
        self.settings = NetworkSettings()
        self.blockchain_config = BlockchainConfig()
        self.stats = NetworkStats()
        
        # Connection management
        self.connections: Dict[str, ConnectionInfo] = {}
        self.client_callbacks: Dict[str, Callable] = {}
        
        # Server components
        self.server_socket = None
        self.server_running = False
        self.server_thread = None
        
        # Blockchain integration
        self.blockchain_connected = False
        self.contract_interfaces = {}
        self.pending_transactions = {}
        self.last_blockchain_sync = 0.0
        
        # Self-improvement components
        self.network_optimization_enabled = True
        self.adaptive_compression = True
        self.performance_history = []
        self.optimization_suggestions = []
        
        # Packet handling
        self.packet_handlers = {}
        self.packet_queue = []
        self.packet_processing_thread = None
        self.packet_processing_running = False
        
    def initialize(self):
        """Initialize the networking system"""
        print("Initializing Networking System...")
        print(f"  Server Port: {self.settings.server_port}")
        print(f"  Max Connections: {self.settings.max_connections}")
        print(f"  Packet Rate: {self.settings.packet_rate} Hz")
        print(f"  Compression: {'Enabled' if self.settings.enable_compression else 'Disabled'}")
        print(f"  Encryption: {'Enabled' if self.settings.enable_encryption else 'Disabled'}")
        
        # Register default packet handlers
        self._register_default_handlers()
        
        # Initialize blockchain connection
        self._initialize_blockchain()
        
        print("Networking System initialized successfully")
        
    def _register_default_handlers(self):
        """Register default packet handlers"""
        self.packet_handlers["ping"] = self._handle_ping
        self.packet_handlers["player_update"] = self._handle_player_update
        self.packet_handlers["chat_message"] = self._handle_chat_message
        self.packet_handlers["quest_progress"] = self._handle_quest_progress
        self.packet_handlers["transaction_request"] = self._handle_transaction_request
        
    def _initialize_blockchain(self):
        """Initialize blockchain connection"""
        try:
            # In a real implementation, this would connect to an actual blockchain
            print(f"Connecting to blockchain at {self.blockchain_config.rpc_endpoint}...")
            
            # Simulate blockchain connection
            time.sleep(0.1)
            self.blockchain_connected = True
            
            # Initialize contract interfaces
            self.contract_interfaces["ngt_token"] = "0xTokenContractAddress"
            self.contract_interfaces["staking"] = "0xStakingContractAddress"
            self.contract_interfaces["governance"] = "0xGovernanceContractAddress"
            self.contract_interfaces["nft"] = "0xNFTContractAddress"
            
            print("Blockchain connection established")
            
        except Exception as e:
            print(f"Failed to connect to blockchain: {e}")
            self.blockchain_connected = False
            
    def update(self, delta_time: float):
        """Update the networking system"""
        # Process packet queue
        self._process_packet_queue()
        
        # Update connection status
        self._update_connections(delta_time)
        
        # Sync with blockchain periodically
        if time.time() - self.last_blockchain_sync > self.settings.blockchain_sync_interval:
            self._sync_with_blockchain()
            
        # Adapt network parameters based on performance
        if self.network_optimization_enabled:
            self._adapt_network_parameters()
            
    def _process_packet_queue(self):
        """Process queued packets"""
        # In a real implementation, this would process network packets
        # For now, we'll just clear the queue
        processed_packets = min(10, len(self.packet_queue))
        for i in range(processed_packets):
            packet = self.packet_queue.pop(0)
            self.stats.packets_received += 1
            
    def _update_connections(self, delta_time: float):
        """Update connection status"""
        current_time = time.time()
        
        # Update connection info
        for conn_id, conn in list(self.connections.items()):
            # Check for timeout
            if current_time - conn.last_ping > 30.0:  # 30 second timeout
                print(f"Connection {conn_id} timed out")
                self._disconnect_client(conn_id)
                
        # Update statistics
        self.stats.active_connections = len(self.connections)
        
    def _sync_with_blockchain(self):
        """Sync with blockchain for player data"""
        if not self.blockchain_connected:
            return
            
        try:
            # In a real implementation, this would sync with actual blockchain
            print("Syncing with blockchain...")
            
            # Simulate blockchain operations
            time.sleep(0.05)
            self.stats.blockchain_syncs += 1
            self.last_blockchain_sync = time.time()
            
            print("Blockchain sync completed")
            
        except Exception as e:
            print(f"Blockchain sync failed: {e}")
            
    def _adapt_network_parameters(self):
        """Adapt network parameters based on performance"""
        # This is where the self-improvement happens
        if len(self.performance_history) < 10:
            return
            
        # Calculate average latency
        recent_latencies = [p["latency"] for p in self.performance_history[-30:]]
        avg_latency = sum(recent_latencies) / len(recent_latencies)
        
        # Adjust packet rate based on latency
        if avg_latency > 0.1:  # 100ms
            # Reduce packet rate to reduce network load
            self.settings.packet_rate = max(20, self.settings.packet_rate - 5)
            print(f"Reducing packet rate to {self.settings.packet_rate} Hz due to high latency")
        elif avg_latency < 0.02:  # 20ms
            # Increase packet rate for better responsiveness
            self.settings.packet_rate = min(120, self.settings.packet_rate + 5)
            print(f"Increasing packet rate to {self.settings.packet_rate} Hz due to low latency")
            
    def start_server(self):
        """Start the game server"""
        if self.server_running:
            print("Server is already running")
            return
            
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('localhost', self.settings.server_port))
            self.server_socket.listen(self.settings.max_connections)
            
            self.server_running = True
            self.server_thread = threading.Thread(target=self._server_loop)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            print(f"Game server started on port {self.settings.server_port}")
            
        except Exception as e:
            print(f"Failed to start server: {e}")
            
    def stop_server(self):
        """Stop the game server"""
        print("Stopping game server...")
        self.server_running = False
        
        if self.server_socket:
            self.server_socket.close()
            
        # Disconnect all clients
        for client_id in list(self.connections.keys()):
            self._disconnect_client(client_id)
            
        print("Game server stopped")
        
    def _server_loop(self):
        """Main server loop"""
        while self.server_running:
            try:
                # Accept new connections
                client_socket, address = self.server_socket.accept()
                
                # Create new client connection
                client_id = f"client_{hashlib.md5(str(address).encode()).hexdigest()[:8]}"
                conn_info = ConnectionInfo(
                    client_id=client_id,
                    address=address,
                    connected_time=time.time(),
                    last_ping=time.time()
                )
                
                self.connections[client_id] = conn_info
                self.stats.total_connections += 1
                
                print(f"New client connected: {client_id} from {address}")
                
                # Start client handler thread
                client_thread = threading.Thread(target=self._handle_client, args=(client_socket, client_id))
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.server_running:
                    print(f"Error accepting client connection: {e}")
                    
    def _handle_client(self, client_socket, client_id: str):
        """Handle client communication"""
        try:
            while client_id in self.connections and self.server_running:
                # Receive data from client
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                        
                    self.stats.bytes_received += len(data)
                    
                    # Process received data
                    self._process_client_data(client_id, data)
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error receiving data from {client_id}: {e}")
                    break
                    
        except Exception as e:
            print(f"Error handling client {client_id}: {e}")
        finally:
            # Clean up connection
            self._disconnect_client(client_id)
            client_socket.close()
            
    def _process_client_data(self, client_id: str, data: bytes):
        """Process data received from client"""
        try:
            # Decode JSON data
            message = json.loads(data.decode('utf-8'))
            
            # Handle packet based on type
            packet_type = message.get("type", "unknown")
            if packet_type in self.packet_handlers:
                self.packet_handlers[packet_type](client_id, message)
            else:
                print(f"Unknown packet type from {client_id}: {packet_type}")
                
        except json.JSONDecodeError:
            print(f"Invalid JSON data from {client_id}")
        except Exception as e:
            print(f"Error processing client data from {client_id}: {e}")
            
    def _handle_ping(self, client_id: str, message: Dict):
        """Handle ping packet"""
        # Update connection info
        if client_id in self.connections:
            self.connections[client_id].last_ping = time.time()
            self.connections[client_id].ping = message.get("ping_time", 0)
            
        # Send pong response
        response = {
            "type": "pong",
            "timestamp": time.time()
        }
        self.send_packet(client_id, response)
        
    def _handle_player_update(self, client_id: str, message: Dict):
        """Handle player update packet"""
        # Process player state update
        player_data = message.get("player_data", {})
        
        # In a real implementation, this would update the player's state in the game world
        # For now, we'll just acknowledge receipt
        response = {
            "type": "player_update_ack",
            "player_id": player_data.get("id"),
            "timestamp": time.time()
        }
        self.send_packet(client_id, response)
        
    def _handle_chat_message(self, client_id: str, message: Dict):
        """Handle chat message packet"""
        chat_data = message.get("chat_data", {})
        
        # Broadcast message to all connected clients
        broadcast_message = {
            "type": "chat_broadcast",
            "chat_data": chat_data,
            "sender": client_id
        }
        
        for conn_id in self.connections:
            self.send_packet(conn_id, broadcast_message)
            
    def _handle_quest_progress(self, client_id: str, message: Dict):
        """Handle quest progress packet"""
        quest_data = message.get("quest_data", {})
        
        # In a real implementation, this would update quest progress
        # For now, we'll just acknowledge receipt
        response = {
            "type": "quest_progress_ack",
            "quest_id": quest_data.get("id"),
            "progress": quest_data.get("progress"),
            "timestamp": time.time()
        }
        self.send_packet(client_id, response)
        
    def _handle_transaction_request(self, client_id: str, message: Dict):
        """Handle blockchain transaction request"""
        tx_data = message.get("transaction_data", {})
        
        # Process blockchain transaction
        if self.blockchain_connected:
            # In a real implementation, this would send a transaction to the blockchain
            # For now, we'll simulate the process
            tx_id = f"tx_{random.randint(100000, 999999)}"
            
            # Store pending transaction
            self.pending_transactions[tx_id] = {
                "client_id": client_id,
                "data": tx_data,
                "timestamp": time.time()
            }
            
            # Send transaction confirmation
            response = {
                "type": "transaction_confirmed",
                "transaction_id": tx_id,
                "status": "pending",
                "timestamp": time.time()
            }
            self.send_packet(client_id, response)
        else:
            # Send error response
            response = {
                "type": "transaction_error",
                "error": "Blockchain not connected",
                "timestamp": time.time()
            }
            self.send_packet(client_id, response)
            
    def send_packet(self, client_id: str, packet: Dict):
        """Send packet to client"""
        if client_id not in self.connections:
            return
            
        try:
            # Encode packet as JSON
            data = json.dumps(packet).encode('utf-8')
            
            # In a real implementation, this would send data through the socket
            # For now, we'll just update statistics
            self.stats.packets_sent += 1
            self.stats.bytes_sent += len(data)
            
        except Exception as e:
            print(f"Error sending packet to {client_id}: {e}")
            
    def _disconnect_client(self, client_id: str):
        """Disconnect client"""
        if client_id in self.connections:
            print(f"Client {client_id} disconnected")
            del self.connections[client_id]
            
    def register_client_callback(self, event_type: str, callback: Callable):
        """Register callback for client events"""
        self.client_callbacks[event_type] = callback
        
    def get_network_stats(self) -> NetworkStats:
        """Get current network statistics"""
        return self.stats.copy() if hasattr(self.stats, 'copy') else self.stats
        
    def get_performance_rating(self) -> float:
        """Get networking performance rating (0.0 to 1.0)"""
        # Performance rating based on latency and packet loss
        if self.stats.packets_sent == 0:
            return 1.0
            
        # Calculate packet loss percentage
        packet_loss = 0.0
        if self.stats.packets_sent > 0:
            packet_loss = min(1.0, self.stats.packets_received / max(1, self.stats.packets_sent))
            
        # Calculate latency rating (target < 50ms)
        latency_rating = max(0.0, min(1.0, 1.0 - (self.stats.avg_latency / 0.05)))
        
        # Combine ratings
        performance_rating = (latency_rating * 0.7) + (packet_loss * 0.3)
        return performance_rating
        
    def set_blockchain_config(self, config: BlockchainConfig):
        """Set blockchain configuration"""
        self.blockchain_config = config
        print("Blockchain configuration updated")
        
        # Reinitialize blockchain connection
        self._initialize_blockchain()
        
    def get_connection_info(self, client_id: str) -> ConnectionInfo:
        """Get connection information for a client"""
        return self.connections.get(client_id)

if __name__ == "__main__":
    # Example usage
    networking = NetworkingSystem()
    networking.initialize()
    
    # Start server
    networking.start_server()
    
    # Simulate some network activity
    time.sleep(2)
    
    # Show statistics
    stats = networking.get_network_stats()
    print(f"Network Statistics:")
    print(f"  Active Connections: {stats.active_connections}")
    print(f"  Total Connections: {stats.total_connections}")
    print(f"  Packets Sent: {stats.packets_sent}")
    print(f"  Packets Received: {stats.packets_received}")
    print(f"  Performance Rating: {networking.get_performance_rating():.2f}")
    
    # Stop server
    networking.stop_server()
    print("Networking system test completed")