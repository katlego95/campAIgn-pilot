from agents.base_model import BaseModel

def test_base_model_init():
    model = BaseModel()
    assert isinstance(model, BaseModel)
```

```python:tests/test_ad_agent.py
from agents.ad_agent import AD_Agent

def test_ad_agent_init():
    agent = AD_Agent()
    assert isinstance(agent, AD_Agent)
```

```python:tests/test_dm_agent.py
from agents.dm_agent import DM_Agent

def test_dm_agent_init():
    agent = DM_Agent()
    assert isinstance(agent, DM_Agent)
```

---

### markdown_guides/

```markdown:markdown_guides/__init__.md
# Markdown guides package
```

```markdown:markdown_guides/base_model.md
# BaseModel

Stub documentation for BaseModel.
```

```markdown:markdown_guides/ad_agent.md
# AD_Agent

Stub documentation for AD_Agent.
```

```markdown:markdown_guides/dm_agent.md
# DM_Agent

Stub documentation for DM_Agent.
```

---

**This gives you a clean, ready-to-extend Python project with the requested structure. Let me know if you want to add or change anything!** 