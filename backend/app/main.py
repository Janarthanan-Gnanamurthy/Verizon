from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import groq
import json
import time
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Education Platform")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY", "")
groq_client = groq.Client(api_key=groq_api_key)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        # Stores active WebSocket connections: {room_id: {user_id: WebSocket}}
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        # Stores user metadata: {room_id: {user_id: {info}}}
        self.user_info: Dict[str, Dict[str, Any]] = {}
        # Lock for thread-safe access to shared dictionaries
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        """Accepts a new WebSocket connection, stores it, and notifies the room."""
        
        # Print when a user enters the room
        print(f"User {user_id} has entered room {room_id}")

        async with self.lock:
            # Initialize room if it doesn't exist
            if room_id not in self.active_connections:
                self.active_connections[room_id] = {}
                self.user_info[room_id] = {}

            # Check if user_id already connected in this room (optional: decide policy - allow/reject/replace)
            if user_id in self.active_connections.get(room_id, {}):
                 print(f"Warning: User {user_id} already connected to room {room_id}. Replacing connection.")
                 # Optional: Close the old connection first if needed
                 # old_ws = self.active_connections[room_id][user_id]
                 # await old_ws.close(code=1008, reason="New connection established")

            # Store connection and user info
            self.active_connections[room_id][user_id] = websocket
            self.user_info[room_id][user_id] = {
                "connected_at": time.time(),
                "last_activity": time.time()
            }

            # Get participants list while lock is held
            current_participants = list(self.user_info[room_id].keys())

        # Broadcast connection status (outside lock to avoid holding it during network IO)
        # Note: This system message might trigger the frontend 'join' handling we discussed
        await self.broadcast_system_message(
            room_id=room_id,
            message=f"User {user_id} has joined the room",
            exclude_user=None # Notify everyone, including the new user
        )

        # Return current participants (list captured inside lock)
        return current_participants

    async def disconnect(self, room_id: str, user_id: str):
        """Removes a user's WebSocket connection and notifies the room."""
        should_broadcast = False
        async with self.lock:
            if room_id in self.active_connections and user_id in self.active_connections[room_id]:
                # Remove user from connections and info
                del self.active_connections[room_id][user_id]
                if room_id in self.user_info and user_id in self.user_info[room_id]:
                    del self.user_info[room_id][user_id]

                should_broadcast = True

                # Clean up room if empty
                if not self.active_connections[room_id]: # Check if the user dict for the room is empty
                    del self.active_connections[room_id]
                    if room_id in self.user_info:
                        del self.user_info[room_id]
                    print(f"Room {room_id} is now empty and has been removed.")


        # Broadcast disconnection outside the lock
        if should_broadcast:
            print(f"User {user_id} disconnected from room {room_id}.")
            await self.broadcast_system_message(
                room_id=room_id,
                message=f"User {user_id} has left the room",
                exclude_user=None # Notify everyone remaining
            )
        # else:
            # print(f"Attempted to disconnect user {user_id} from {room_id}, but they were not found.")


    async def broadcast(self, message: Dict[str, Any], room_id: str, exclude_user: Optional[str] = None):
        """Broadcast a message to all active connections in a room, with optional exclusion."""
        connections_to_send: List[tuple[str, WebSocket]] = []
        async with self.lock:
            if room_id in self.active_connections:
                # Create a list of (user_id, websocket) tuples to iterate over outside the lock
                connections_to_send = list(self.active_connections[room_id].items())

        if not connections_to_send:
             # print(f"No active connections found in room {room_id} to broadcast.") # Optional log
             return

        # Prepare tasks for sending messages concurrently
        tasks = []
        for user_id, connection in connections_to_send:
            if exclude_user is None or user_id != exclude_user:
                # Create a task for each send operation
                tasks.append(self._send_message(connection, message, user_id, room_id))

        # Run send tasks concurrently
        if tasks:
            await asyncio.gather(*tasks)


    # --- NEW METHOD ---
    async def send_to_user(self, message: Dict[str, Any], room_id: str, target_user_id: str):
        """Send a message directly to a specific user in a room."""
        websocket_to_send: Optional[WebSocket] = None
        async with self.lock:
            # Safely get the target user's WebSocket connection
            room_connections = self.active_connections.get(room_id)
            if room_connections:
                websocket_to_send = room_connections.get(target_user_id)

        # Send the message outside the lock
        if websocket_to_send:
            # Use the helper send method for consistency in error handling
            await self._send_message(websocket_to_send, message, target_user_id, room_id)
        # else:
             # Optional: Log if the target user wasn't found or active
             # print(f"Target user '{target_user_id}' not found or not active in room '{room_id}'.")
    # --- END NEW METHOD ---


    # --- HELPER for sending safely ---
    async def _send_message(self, websocket: WebSocket, message: Dict[str, Any], user_id: str, room_id: str):
         """Internal helper to send JSON message with error handling."""
         try:
             await websocket.send_json(message)
             # print(f"Message sent to {user_id} in {room_id}") # Verbose logging if needed
         except Exception as e:
             # Handle potential errors like closed connections during send
             print(f"Error sending message to user {user_id} in room {room_id}: {str(e)}. Type: {type(e)}")
             # Consider disconnecting the user if send fails persistently
             # print(f"Disconnecting user {user_id} due to send error.")
             # await self.disconnect(room_id, user_id) # Careful with potential recursion/deadlocks if disconnect also sends messages
    # --- END HELPER ---


    async def broadcast_system_message(self, room_id: str, message: str, exclude_user: Optional[str] = None):
        """Helper to format and broadcast system messages."""
        system_message = {
            "type": "system",
            "content": message,
            "timestamp": int(time.time() * 1000)
        }
        await self.broadcast(system_message, room_id, exclude_user)


    async def get_active_participants(self, room_id: str) -> List[str]:
        """Get a list of user IDs for active participants in a room."""
        async with self.lock:
            if room_id in self.user_info:
                # Return a list of keys (user_ids) from the user_info dict for the room
                return list(self.user_info[room_id].keys())
            return [] # Return empty list if room doesn't exist in user_info

    async def update_activity(self, room_id: str, user_id: str):
        """Update the last activity timestamp for a user."""
        async with self.lock:
            # Check both dictionaries for safety, although they should be consistent
            if room_id in self.user_info and user_id in self.user_info[room_id]:
                self.user_info[room_id][user_id]["last_activity"] = time.time()

manager = ConnectionManager()

# AI processing functions
async def process_transcription(text: str, background_tasks: BackgroundTasks = None) -> str:
    """Process text using Groq for transcription summarization"""
    if not groq_api_key:
        return "Groq API key not configured"
    
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an educational assistant. Summarize this transcription, highlighting key points, important concepts, and any questions that need addressing. Format your response with bullet points for clarity."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            model="llama3-8b-8192",
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = f"Error processing with Groq: {str(e)}"
        print(error_msg)
        return error_msg

# API endpoints
@app.get("/")
async def root():
    return {"message": "Education Platform API is running"}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, background_tasks: BackgroundTasks):
    await websocket.accept()
    user_id = None

    print(f"Websocket endpoint called for room {room_id}")  
    
    try:
        # First message must be a join request with user_id
        data = await websocket.receive_text()
        message = json.loads(data)
        
        if message["type"] != "signal" or not message.get("user") or message.get("content", {}).get("type") != "join":
            await websocket.close(4000, "First message must be a join signal")
            return
        
        user_id = message["user"]
        
        # Connect to the room
        participants = await manager.connect(websocket, room_id, user_id)
        print(f"Participants: {participants}")
        # Send current participants list
        await websocket.send_json({
            "type": "room_info",
            "participants": participants,
            "room_id": room_id,
            "timestamp": int(time.time() * 1000)
        })
        
        # Main message loop
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Update last activity time
            await manager.update_activity(room_id, user_id)
            
            # Handle different message types
            if message["type"] == "chat":
                # Broadcast chat message to all participants
                await manager.broadcast({
                    "type": "chat",
                    "user": message["user"],
                    "content": message["content"],
                    "timestamp": message["timestamp"]
                }, room_id, exclude_user=message["user"])
            
            elif message["type"] == "transcription":
                # Process transcription with AI
                summary = await process_transcription(message["content"], background_tasks)
                
                # Broadcast the summary
                await manager.broadcast({
                    "type": "ai_summary",
                    "content": summary,
                    "timestamp": message["timestamp"]
                }, room_id)
                
                # Add the transcription to the room history
                await manager.broadcast({
                    "type": "transcription_entry",
                    "user": message["user"],
                    "content": message["content"],
                    "timestamp": message["timestamp"]
                }, room_id)
            
            # Inside the websocket_endpoint function in main.py, replace the signal block

            elif message["type"] == "signal":
                sender_user_id = message.get("user")
                content = message.get("content", {})
                signal_type = content.get("type")
                target_user_id = content.get("target") # Get the target user

                if not sender_user_id:
                    print("Signal received without user ID.")
                    continue # Or handle error

                # Check if it's a targeted signal (offer, answer, ice-candidate)
                if signal_type in ["offer", "answer", "ice-candidate"] and target_user_id:
                    # Prepare the message to forward (keeping original sender info)
                    forward_message = {
                        "type": "signal",
                        "user": sender_user_id,
                        "content": content
                    }
                    # Send ONLY to the target user
                    await manager.send_to_user(forward_message, room_id, target_user_id)

                # Handle the initial 'join' signal - Broadcast this so others know to connect
                elif signal_type == "join":
                    # You might want to exclude the sender from this broadcast
                    # Or just let the frontend handle ignoring its own join signal
                    print(f"Broadcasting join signal to room {room_id} from {sender_user_id}")
                    await manager.broadcast({
                        "type": "signal",
                        "user": sender_user_id,
                        "content": content # Forward the original content
                    }, room_id, exclude_user=None) # Or exclude_user=sender_user_id
                    # Also broadcast a system message like before (handled in manager.connect)

                else:
                    # Handle other signal types or log unknown ones
                    print(f"Received unknown or non-targeted signal type: {signal_type} from {sender_user_id}")
                    # You could potentially still broadcast non-targeted signals if needed
                    # await manager.broadcast(message, room_id, exclude_user=sender_user_id)
                
    except WebSocketDisconnect:
        if user_id:
            await manager.disconnect(room_id, user_id)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        if user_id:
            await manager.disconnect(room_id, user_id)

# Model for creating a room
class RoomCreate(BaseModel):
    name: str
    host_id: str

# Participant model
class Participant(BaseModel):
    id: str
    name: str
    is_host: bool = False
    joined_at: int

# Room model
class Room(BaseModel):
    id: str
    name: str
    host_id: str
    created_at: int
    participants: List[Participant] = []

# Rooms storage (in-memory for simplicity)
rooms: Dict[str, Room] = {}
rooms_lock = asyncio.Lock()

@app.post("/rooms/")
async def create_room(room_data: RoomCreate):
    timestamp = int(time.time() * 1000)
    
    async with rooms_lock:
        room_id = f"room_{len(rooms) + 1}"
        new_room = Room(
            id=room_id,
            name=room_data.name,
            host_id=room_data.host_id,
            created_at=timestamp,
            participants=[]
        )
        rooms[room_id] = new_room
    
    return {"room_id": room_id}

@app.get("/rooms/")
async def list_rooms():
    active_rooms = []
    
    async with rooms_lock:
        room_items = list(rooms.items())

    for room_id, room in room_items:
        # Get participants count (already acquires ConnectionManager lock)
        participants_count = len(await manager.get_active_participants(room_id))
        
        active_rooms.append({
            "id": room.id,
            "name": room.name,
            "host_id": room.host_id,
            "participant_count": participants_count,
            "created_at": room.created_at
        })
    
    return {"rooms": active_rooms}

@app.get("/rooms/{room_id}")
async def get_room(room_id: str):
    async with rooms_lock:
        if room_id not in rooms:
            return {"error": "Room not found"}
        room = rooms[room_id]
        room_data = {
            "id": room.id,
            "name": room.name,
            "host_id": room.host_id,
            "created_at": room.created_at,
        }

    # Get active participants (already acquires ConnectionManager lock)
    active_participants = await manager.get_active_participants(room_id)
    
    # Combine data outside lock
    room_data["active_participants"] = active_participants
    room_data["participant_count"] = len(active_participants)
    
    return room_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 