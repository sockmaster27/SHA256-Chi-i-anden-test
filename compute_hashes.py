import hashlib
import pickle
import asyncio
import aioconsole
from typing import List

done = False


async def await_stop():
    global done
    await aioconsole.ainput("Press enter to stop and save progress")
    done = True


async def compute_hashes():
    # Hashværdierne kategorises efter værdien er deres første 2 bytes, og der er derfor 2^(2*8) eller 65.536 kategorier i alt.
    category_bytes = 2
    categories = 2 ** (category_bytes * 8)

    try:
        with open(f"frequency_table_{categories}", "rb") as f:
            (frequency_table, end_value) = pickle.load(f)

    except FileNotFoundError:
        frequency_table = [0] * categories
        end_value = [0]

    def increment_value(value: List[int]):
        # Denne funktion går igennem alle bit-kombinationer for alle størrelse på denne måde:
        # 00000000 -> 00000001 -> ... -> 11111111 -> 00000000 00000000 -> 00000000 00000001
        for i in reversed(range(len(value))):
            value[i] = (value[i] + 1) % 256
            if value[i] != 0:
                break
        else:
            # Hvis løkken når til enden uden at blive breaket
            value.insert(0, 0)

    def hash_of_value(value: List[int]) -> bytes:
        # 'value' repræsenterer en liste af bytes i int-form (som hver er imellem 0 og 255).
        return hashlib.sha256(
            bytes(value)
        ).digest()

    def increment_frequency_table(hash_value: bytes):
        nonlocal category_bytes
        first_bytes = hash_value[:category_bytes]
        category = int.from_bytes(
            first_bytes, byteorder="big", signed=False)
        frequency_table[category] += 1

    # Fortsæt hvor vi slap.
    value = end_value

    while not done:
        hash = hash_of_value(value)
        increment_frequency_table(hash)
        increment_value(value)
        # Sov i 0 sekunder for at give await_stop en chance for at køre
        await asyncio.sleep(0)

    with open(f"frequency_table_{categories}", "wb") as f:
        pickle.dump((frequency_table, value), f)
    print(f"Calculated {sum(frequency_table)} hashes")


loop = asyncio.get_event_loop().run_until_complete(asyncio.wait([
    await_stop(),
    compute_hashes()
]))
