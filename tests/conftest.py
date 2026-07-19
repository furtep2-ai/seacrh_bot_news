import pytest
import asyncio
@pytest.fixture(scope="function")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    
    yield loop  # 1. This is where your actual test runs!
    
    # 2. The test finishes, but instead of destroying the loop instantly, we pause:
    try:
        # 3. We keep the loop alive for 0.05 seconds to let SQLAlchemy finish its work
        loop.run_until_complete(asyncio.sleep(0.05))
    finally:
        # 4. NOW it's safe to destroy the loop safely
        loop.close()