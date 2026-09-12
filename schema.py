from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class InventoryItem(BaseModel):
    subtype: str
    amount: int


class Observer(BaseModel):
    identityId: int
    steamId: int
    displayName: str


class World(BaseModel):
    serverId: str
    sessionName: str
    syncDistanceMeters: float


class PacketSource(BaseModel):
    entityId: int
    gridName: str
    blockName: str


class PacketPayload(BaseModel):
    grid: str
    entityId: int
    inventory: List[InventoryItem]


class Packet(BaseModel):
    tag: str
    source: PacketSource
    payload: PacketPayload


class TelemetryData(BaseModel):
    schemaVersion: str
    capturedAtUtc: datetime | None
    observer: Observer
    world: World
    packets: List[Packet]

