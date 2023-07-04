from typing import List, Tuple, Dict, Any, TypedDict
import requests

class Proof(TypedDict):
    nonce: int
    solution: Any
    intermediate_integers: List[Tuple[int, int]]

class APIException(Exception): pass

class API:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url

    def _call(self, query, **kwargs):
        kwargs.update(
            url=f"{self.api_url}/{query}",
            headers={
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
        )
        if 'data' in kwargs or 'json' in kwargs:        
            resp = requests.post(**kwargs)
        else:
            resp = requests.get(**kwargs)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise APIException(resp.text)

    def getEarnings(self):
        return self._call("player/getEarnings")

    def getRecentBenchmarks(self):
        return self._call(f"player/getRecentBenchmarks")

    def getLatestBlock(self):
        return self._call("tig/getLatestBlock")

    def getAlgorithms(self, challenge_id: str):
        return self._call(f"tig/getAlgorithms/{challenge_id}")

    def getFrontiers(self, challenge_id: str):
        return self._call(f"tig/getFrontiers/{challenge_id}")

    def submitBenchmark(
        self, 
        player_id: str,
        block_id: str,
        prev_block_id: str,
        algorithm_id: str,
        challenge_id: str,
        difficulty: Dict[str, int],
        nonces: List[int]
      ):
          return self._call(
            f"player/submitBenchmark", 
            json={
                'player_id': player_id,
                'block_id': block_id,
                'prev_block_id': prev_block_id,
                'algorithm_id': algorithm_id,
                'challenge_id': challenge_id,
                'difficulty': difficulty,
                'nonces': nonces,
            }
          )

    def submitProofs(
        self, 
        benchmark_id: str,
        proofs: List[Proof]
      ):
          return self._call(
            f"player/submitProofs/{benchmark_id}", 
            json={'proofs': proofs}
          )
