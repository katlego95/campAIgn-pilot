from agents.ad_agent import AD_Agent

def test_ad_agent_init():
    agent = AD_Agent()
    assert isinstance(agent, AD_Agent)