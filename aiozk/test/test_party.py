import asyncio
import pytest


@pytest.mark.asyncio
async def test_party_join(zk, path):
    NAME = 'member'
    party = zk.recipes.Party(path, NAME)
    await party.join()
    # Guarantee that member count is updated before returning from .join()
    assert len(party) == 1

    # Should start waiting before party2 join
    task = asyncio.create_task(party.wait_for_change())
    party2 = zk.recipes.Party(path, NAME)
    await party2.join()

    assert len(party2) == 2

    await task
    assert len(party) == 2

    await party.leave()
    await party2.wait_for_change()

    assert len(party2) == 1

    await party2.leave()

    await zk.delete(path)
