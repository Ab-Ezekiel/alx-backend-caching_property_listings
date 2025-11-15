# properties/utils.py
import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)

def getallproperties():
    """
    Low-level cache: returns a serializable list of property dicts.
    Looks up key 'all_properties' in cache first, otherwise queries DB,
    stores the result in cache under 'all_properties' for 3600s (1 hour),
    and returns the list.
    """
    queryset = cache.get('all_properties')
    if queryset is not None:
        return queryset

    qs = Property.objects.all().order_by('-created_at').values(
        'id', 'title', 'description', 'price', 'location', 'created_at'
    )
    queryset = list(qs)
    cache.set('all_properties', queryset, 3600)
    return queryset

def get_all_properties():
    """Convenience wrapper used by the view."""
    return getallproperties()


def get_redis_cache_metrics():
    """
    Connect to Redis via django_redis and return cache metrics.

    Returns a dict:
      {
        "keyspace_hits": int,
        "keyspace_misses": int,
        "hit_ratio": float  # 0.0..1.0 or None if no operations yet
      }

    Also logs the metrics at INFO level.
    """
    try:
        # get_redis_connection will use the cache backend named "default"
        # (ensure your CACHES/default is configured to use django_redis)
        conn = get_redis_connection("default")
        info = conn.info()  # returns a dict of INFO sections flattened

        hits = int(info.get("keyspace_hits", 0))
        misses = int(info.get("keyspace_misses", 0))

        total = hits + misses
        hit_ratio = None
        if total > 0:
            hit_ratio = hits / total

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": hit_ratio,
        }

        logger.info(
            "Redis cache metrics - hits: %d, misses: %d, hit_ratio: %s",
            hits,
            misses,
            f"{hit_ratio:.4f}" if hit_ratio is not None else "N/A",
        )

        return metrics

    except Exception as exc:
        # Log exception and return zeros/None so callers can handle gracefully
        logger.exception("Failed to fetch Redis cache metrics: %s", exc)
        return {
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": None,
        }
