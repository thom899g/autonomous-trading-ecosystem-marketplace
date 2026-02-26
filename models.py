"""
Core data models for the Autonomous Trading Ecosystem Marketplace.
Using Firestore document structure with type-safe Python classes.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import uuid


class AgentStatus(str, Enum):
    """Status of trading agents in the ecosystem."""
    REGISTERED = "registered"
    VERIFIED = "verified"
    SUSPENDED = "suspended"
    RETIRED = "retired"


class StrategyType(str, Enum):
    """Types of trading strategies."""
    TECHNICAL = "technical"
    FUNDAMENTAL = "fundamental"
    QUANTITATIVE = "quantitative"
    ML_PREDICTIVE = "ml_predictive"
    ARBITRAGE = "arbitrage"
    MARKET_MAKING = "market_making"


class DataType(str, Enum):
    """Types of market data available for trading."""
    OHLCV = "ohlcv"
    ORDER_BOOK = "order_book"
    FUNDING_RATES = "funding_rates"
    SOCIAL_SENTIMENT = "social_sentiment"
    ON_CHAIN = "on_chain"
    NEWS = "news"


class TransactionStatus(str, Enum):
    """Status of marketplace transactions."""
    PENDING = "pending"
    ESCROW_HOLD = "escrow_hold"
    COMPLETED = "completed"
    FAILED = "failed"
    DISPUTED = "disputed"
    REFUNDED = "refunded"


@dataclass
class TradingAgent:
    """Represents an autonomous trading agent in the ecosystem."""
    agent_id: str = field(default_factory=lambda: f"agent_{uuid.uuid4().hex[:12]}")
    owner_wallet: str  # Blockchain wallet address
    name: str
    description: str
    status: AgentStatus = AgentStatus.REGISTERED
    registration_date: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    credit_balance: float = 0.0
    reputation_score: float = 100.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_firestore_dict(self) -> Dict[str, Any]:
        """Convert to Firestore-compatible dictionary."""
        data = asdict(self)
        data['registration_date'] = data['registration_date'].isoformat()
        data['last_active'] = data['last_active'].isoformat()
        return data
    
    @classmethod
    def from_firestore_dict(cls, data: Dict[str, Any]) -> 'TradingAgent':
        """Create from Firestore dictionary."""
        data['registration_date'] = datetime.fromisoformat(data['registration_date'])
        data['last_active'] = datetime.fromisoformat(data['last_active'])
        data['status'] = AgentStatus(data['status'])
        return cls(**data)


@dataclass
class TradingStrategy:
    """A trading strategy available for purchase/rent in the marketplace."""
    strategy_id: str = field(default_factory=lambda: f"strategy_{uuid.uuid4().hex[:12]}")
    creator_agent_id: str
    name: str
    description: str
    strategy_type: StrategyType
    price: float  # Credits required for purchase
    rental_price_per_hour: Optional[float] = None
    code_hash: str  # SHA-256 hash of strategy code
    storage_path: str  # Firebase Storage path to strategy code
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
    dependencies: List[str] = field(default_factory=list)
    performance_history: List[Dict[str, float]] = field(default_factory=list)
    total_sales: int = 0
    average_rating: float = 0.0
    is_active: bool = True
    validation_score: float = 0.0  # Score from validation engine
    
    def to_firestore_dict(self) -> Dict[str, Any]:
        """Convert to Firestore-compatible dictionary."""
        data = asdict(self)
        data['created_at'] = data['created_at'].isoformat()
        data['updated_at'] = data['updated_at'].isoformat()
        data['strategy_type'] = data['strategy_type'].value
        return data
    
    @classmethod
    def from_firestore_dict(cls, data: Dict[str, Any]) -> 'TradingStrategy':
        """Create from Firestore dictionary."""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        data['strategy_type'] = StrategyType(data['strategy_type'])
        return cls(**data)


@dataclass
class MarketDataProduct:
    """Market data product available for purchase."""
    data_id: str = field(default_factory=lambda: f"data_{uuid.uuid4().hex[:12]}")
    provider_agent_id: str
    name: str
    description: str
    data_type: DataType
    symbols: List[str]
    timeframe: str  # e.g., "1m", "1h", "1d"
    start_date: datetime
    end_date: datetime
    size_bytes: int
    price: float
    storage_path: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    compression_format