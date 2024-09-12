from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Result(Base):
    __tablename__ = 'slt_ws_result'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ECID = Column(String(255), nullable=False)
    Serial = Column(String(255), nullable=False)
    PartId = Column(String(255), nullable=False)
    LotNumber = Column(String(255), nullable=False)
    Cores = Column(String(255), nullable=True)
    Frequency = Column(String(255), nullable=True)
    AVS = Column(String(255), nullable=True)
    TDP = Column(String(255), nullable=True)
    TesterNumber = Column(String(255), nullable=False)
    ScreeningMode = Column(String(255), nullable=False)
    TestCase = Column(String(255), nullable=False)
    Operator = Column(String(255), nullable=True)
    BoardSerial = Column(String(255), nullable=True)
    SocketSerial = Column(String(255), nullable=True)
    Environments = Column(String, nullable=True)  # Changed to String
    StartTime = Column(DateTime(6), nullable=True)
    RunTime = Column(Integer, nullable=True)
    Result = Column(Integer, nullable=True)  # Changed to Integer
    BinLabel = Column(String(255), nullable=True)
    HBin = Column(String(255), nullable=True)
    SBin = Column(String(255), nullable=True)
    LogFile = Column(String, nullable=True)  # Changed to String
    ReportFile = Column(String, nullable=True)  # Changed to String
    SummaryFile = Column(String, nullable=True)  # Changed to String
    LastModified = Column(DateTime(6), nullable=True)
    CpuType = Column(String(255), nullable=False)
    HandlerID = Column(String(255), nullable=True)
    TestStep = Column(String(255), nullable=True)
    COM_ECID = Column(String(255), nullable=True)
    IO_ECID = Column(String(255), nullable=True)
    BinFailed = Column(JSON, nullable=True)
    FinalLogFile = Column(String, nullable=True)  # Changed to String