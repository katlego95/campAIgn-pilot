from agents.dm_agent import DM_Agent

def test_dm_agent_init():
    agent = DM_Agent()
    assert isinstance(agent, DM_Agent)