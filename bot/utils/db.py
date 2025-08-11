import sqlite3
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'stfc_bot.db')

def get_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)

def queryDatabase(sql):
    """Execute a SELECT query and return results."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Database query error: {e}")
        return []

def executeQuery(sql, params=None):
    """Execute an INSERT, UPDATE, or DELETE query."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database execute error: {e}")
        return False

# Alliance and Server management functions
def saveAlliance(serverId, allianceId, subAlliance=0):
    """Save alliance information."""
    sql = '''
        INSERT OR REPLACE INTO Alliance (ServerID, AllianceID, SubAlliance)
        VALUES (?, ?, ?)
    '''
    return executeQuery(sql, (serverId, allianceId, subAlliance))

def saveSettings(serverId, allianceName, manualRegister, createChannel, channelCategory, allowAllyIntelAccess=0):
    """Save server settings."""
    sql = '''
        INSERT OR REPLACE INTO Server (ServerID, AllianceName, ManualRegister, CreateChannel, ChannelCategory, AllowAllyIntelAccess)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    return executeQuery(sql, (serverId, allianceName, manualRegister, createChannel, channelCategory, allowAllyIntelAccess))

def saveGeneralInfo(serverId, homeInfo='', roeRules='', alliesInfo='', napInfo='', cogInfo='', kosInfo='', warInfo=''):
    """Save general alliance information."""
    sql = '''
        INSERT OR REPLACE INTO GeneralAllianceInfo (ServerID, HomeInfo, RoeRules, AlliesInfo, NAPInfo, COGInfo, KosInfo, WarInfo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    return executeQuery(sql, (serverId, homeInfo, roeRules, alliesInfo, napInfo, cogInfo, kosInfo, warInfo))

def setNewMaster(serverId, allianceId):
    """Set a new master alliance."""
    # First, set all alliances as sub-alliances
    sql1 = '''UPDATE Alliance SET SubAlliance = 1 WHERE ServerID = ?'''
    executeQuery(sql1, (serverId,))
    
    # Then set the specified alliance as master
    sql2 = '''UPDATE Alliance SET SubAlliance = 0 WHERE ServerID = ? AND AllianceID = ?'''
    return executeQuery(sql2, (serverId, allianceId))

# Role permissions functions
def saveRolePermissions(serverId, role, memberRole=0, ambassadorRole=0, allyRole=0, adminRole=0, accessAmbassadorChannels=0):
    """Save role permissions."""
    sql = '''
        INSERT OR REPLACE INTO AllianceRolePermissions 
        (ServerID, Role, MemberRole, AmbassadorRole, AllyRole, AdminRole, AccessAmbassadorChannels)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    return executeQuery(sql, (serverId, role, memberRole, ambassadorRole, allyRole, adminRole, accessAmbassadorChannels))

# War-related functions
def incrementMemberKillCount(serverId, allianceId, playerName, killCount):
    """Increment member kill count."""
    sql = '''
        INSERT OR REPLACE INTO AllianceMember (ServerID, AllianceID, PlayerName, KillCount)
        VALUES (?, ?, ?, ?)
    '''
    return executeQuery(sql, (serverId, allianceId, playerName, killCount))

def setWarPointsChannel(serverId, channelName):
    """Set war points channel."""
    sql = '''UPDATE Server SET WarPointsChannel = ? WHERE ServerID = ?'''
    return executeQuery(sql, (channelName, serverId))

# Resource management functions
def saveResource(resource, tier, system, region, reliabilityScore):
    """Save resource information."""
    sql = '''
        INSERT OR REPLACE INTO Resources (Resource, Tier, System, Region, ReliabilityScore)
        VALUES (?, ?, ?, ?, ?)
    '''
    return executeQuery(sql, (resource, tier, system, region, reliabilityScore))

# Intelligence functions
def saveIntellegence(serverId, allianceId, aoa=0, cognap=0, playerKos=0, galacticKos=0, allianceKos=0, nap=0, war=0):
    """Save alliance intelligence."""
    sql = '''
        INSERT OR REPLACE INTO AllianceIntelligence 
        (ServerID, AllianceID, AoA, COGNAP, PlayerKos, GalacticKos, AllianceKos, NAP, War)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    return executeQuery(sql, (serverId, allianceId, aoa, cognap, playerKos, galacticKos, allianceKos, nap, war))

def savePlayerIntelligence(serverId, playerName, playerAlliance, lastUpdate):
    """Save player intelligence."""
    sql = '''
        INSERT OR REPLACE INTO PlayerIntelligence (ServerID, PlayerName, PlayerAlliance, LastUpdate)
        VALUES (?, ?, ?, ?)
    '''
    return executeQuery(sql, (serverId, playerName, playerAlliance, lastUpdate))

def removePlayerIntelligence(serverId, playerName):
    """Remove player intelligence."""
    sql = '''DELETE FROM PlayerIntelligence WHERE ServerID = ? AND PlayerName = ?'''
    return executeQuery(sql, (serverId, playerName))

# ROE (Rules of Engagement) functions
def saveROE(serverId, allianceId, playerName, violations, lastUpdated):
    """Save ROE violation."""
    sql = '''
        INSERT OR REPLACE INTO ROE (ServerID, AllianceID, PlayerName, Violations, LastUpdated)
        VALUES (?, ?, ?, ?, ?)
    '''
    return executeQuery(sql, (serverId, allianceId, playerName, violations, lastUpdated))

def removeROE(serverId, allianceId, playerName):
    """Remove ROE violation."""
    sql = '''DELETE FROM ROE WHERE ServerID = ? AND AllianceID = ? AND PlayerName = ?'''
    return executeQuery(sql, (serverId, allianceId, playerName))

# Utility functions
def deleteServerData(serverId):
    """Delete all data for a server."""
    tables = ['Server', 'Alliance', 'AllianceRolePermissions', 'AllianceMember', 
              'AllianceIntelligence', 'PlayerIntelligence', 'GeneralAllianceInfo', 'ROE']
    
    for table in tables:
        sql = f'DELETE FROM {table} WHERE ServerID = ?'
        executeQuery(sql, (serverId,))
    
    return True