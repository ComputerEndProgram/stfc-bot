import sqlite3
import os
from utils.db import get_connection, executeQuery

def createAllianceTables():
    """Create all necessary database tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Server table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Server (
            ServerID INTEGER PRIMARY KEY,
            AllianceName TEXT,
            ManualRegister INTEGER DEFAULT 0,
            CreateChannel INTEGER DEFAULT 0,
            ChannelCategory TEXT,
            WarPointsChannel TEXT,
            AllowAllyIntelAccess INTEGER DEFAULT 0
        )
    ''')
    
    # Alliance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Alliance (
            ServerID INTEGER,
            AllianceID TEXT,
            SubAlliance INTEGER DEFAULT 0,
            PRIMARY KEY (ServerID, AllianceID)
        )
    ''')
    
    # Alliance Role Permissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AllianceRolePermissions (
            ServerID INTEGER,
            Role TEXT,
            MemberRole INTEGER DEFAULT 0,
            AmbassadorRole INTEGER DEFAULT 0,
            AllyRole INTEGER DEFAULT 0,
            AdminRole INTEGER DEFAULT 0,
            AccessAmbassadorChannels INTEGER DEFAULT 0,
            PRIMARY KEY (ServerID, Role)
        )
    ''')
    
    # Alliance Member table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AllianceMember (
            ServerID INTEGER,
            AllianceID TEXT,
            PlayerID TEXT,
            PlayerName TEXT,
            KillCount INTEGER DEFAULT 0,
            PRIMARY KEY (ServerID, PlayerID)
        )
    ''')
    
    # Alliance Intelligence table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AllianceIntelligence (
            ServerID INTEGER,
            AllianceID TEXT,
            AoA INTEGER DEFAULT 0,
            COGNAP INTEGER DEFAULT 0,
            PlayerKos INTEGER DEFAULT 0,
            GalacticKos INTEGER DEFAULT 0,
            AllianceKos INTEGER DEFAULT 0,
            NAP INTEGER DEFAULT 0,
            War INTEGER DEFAULT 0,
            PRIMARY KEY (ServerID, AllianceID)
        )
    ''')
    
    # Player Intelligence table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PlayerIntelligence (
            ServerID INTEGER,
            PlayerName TEXT,
            PlayerAlliance TEXT,
            LastUpdate TEXT,
            PRIMARY KEY (ServerID, PlayerName)
        )
    ''')
    
    # General Alliance Info table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS GeneralAllianceInfo (
            ServerID INTEGER PRIMARY KEY,
            HomeInfo TEXT,
            RoeRules TEXT,
            AlliesInfo TEXT,
            NAPInfo TEXT,
            COGInfo TEXT,
            KosInfo TEXT,
            WarInfo TEXT
        )
    ''')
    
    # ROE (Rules of Engagement) table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ROE (
            ServerID INTEGER,
            AllianceID TEXT,
            PlayerName TEXT,
            Violations INTEGER DEFAULT 1,
            LastUpdated TEXT,
            PRIMARY KEY (ServerID, AllianceID, PlayerName)
        )
    ''')
    
    # Resources table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Resources (
            Resource TEXT,
            Tier INTEGER,
            System TEXT,
            Region TEXT,
            ReliabilityScore INTEGER DEFAULT 0,
            PRIMARY KEY (Resource, Tier, System)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database tables created successfully.")

def resetAllianceDatabase():
    """Reset/clear the alliance database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # List of tables to drop
    tables = [
        'Server', 'Alliance', 'AllianceRolePermissions', 'AllianceMember',
        'AllianceIntelligence', 'PlayerIntelligence', 'GeneralAllianceInfo', 
        'ROE', 'Resources'
    ]
    
    for table in tables:
        try:
            cursor.execute(f'DROP TABLE IF EXISTS {table}')
        except Exception as e:
            print(f"Error dropping table {table}: {e}")
    
    conn.commit()
    conn.close()
    print("Database reset completed.")

def deleteServerSettings(serverId):
    """Delete all settings for a specific server."""
    tables = ['Server', 'Alliance', 'AllianceRolePermissions', 'AllianceMember', 
              'AllianceIntelligence', 'PlayerIntelligence', 'GeneralAllianceInfo', 'ROE']
    
    conn = get_connection()
    cursor = conn.cursor()
    
    for table in tables:
        try:
            cursor.execute(f'DELETE FROM {table} WHERE ServerID = ?', (serverId,))
        except Exception as e:
            print(f"Error deleting from {table}: {e}")
    
    conn.commit()
    conn.close()
    print(f"Server {serverId} settings deleted successfully.")

def initializeDatabase():
    """Initialize the database with tables and sample data."""
    resetAllianceDatabase()
    createAllianceTables()
    loadSampleResources()

def loadSampleResources():
    """Load sample resource data into the database."""
    # Sample resource data for STFC
    sample_resources = [
        # Format: (resource, tier, system, region, reliability)
        ('crystal', 1, 'Sol', 'federation', 5),
        ('crystal', 2, 'Wolf 359', 'federation', 4),
        ('crystal', 3, 'Vulcan', 'federation', 3),
        ('crystal', 4, 'Andoria', 'federation', 2),
        ('ore', 1, 'Qo\'noS', 'klingon', 5),
        ('ore', 2, 'Kronos', 'klingon', 4),
        ('ore', 3, 'Rura Penthe', 'klingon', 3),
        ('ore', 4, 'Ketha', 'klingon', 2),
        ('gas', 1, 'Romulus', 'romulan', 5),
        ('gas', 2, 'Remus', 'romulan', 4),
        ('gas', 3, 'Reman', 'romulan', 3),
        ('gas', 4, 'Rator', 'romulan', 2),
        ('dilithium', 1, 'Deep Space', 'neutral', 5),
        ('dilithium', 2, 'Bajor', 'neutral', 4),
        ('dilithium', 3, 'Cardassia', 'neutral', 3),
        ('dilithium', 4, 'Terok Nor', 'neutral', 2),
    ]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    for resource_data in sample_resources:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO Resources (Resource, Tier, System, Region, ReliabilityScore)
                VALUES (?, ?, ?, ?, ?)
            ''', resource_data)
        except Exception as e:
            print(f"Error inserting resource data: {e}")
    
    conn.commit()
    conn.close()
    print("Sample resource data loaded successfully.")