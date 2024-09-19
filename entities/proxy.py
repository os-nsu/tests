from dataclasses import dataclass

# All params that configure proxy
@dataclass(kw_only=True)
class Proxy():
	log_capacity: int
	log_dir_name: str
	log_file_name: str
	log_level: int
	cache_size: int
